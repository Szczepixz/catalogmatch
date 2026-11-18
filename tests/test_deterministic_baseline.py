"""Synthetic tests of ranking mechanics, with invented offers and identifiers."""

from fractions import Fraction
import unittest

from deterministic_baseline import compare, evidence_key, normalize, project, rank


def offer(title=None, **fields):
    return normalize(project({"<page title>": title, **fields}))


class RankingTests(unittest.TestCase):
    def test_title_tokens_keep_suffixes_and_qualifiers_and_exclude_transport(self):
        features = offer("ÉCRAN  e\u0301cran X24-T/US.2 24-inch NON-touch Refurbished "
                         "https://host.test/X1 <//host.test/X2> www.host.test/X3 "
                         "mailto:staff@www.host.test")
        self.assertEqual(features["title_tokens"],
                         {"écran", "x24-t/us.2", "24-inch", "non-touch", "refurbished"})
        self.assertEqual(offer("x24-T / US.2")["title_tokens"], {"x24-t", "us.2"})

    def test_identifiers_are_whole_normalized_values_and_preserve_namespaces(self):
        query = offer(brand=" Invented  Display ", **{"product model": "X1-US/2"})
        exact = offer(manufacturer="invented display", **{" Model   Name ": "x1-us/2"})
        self.assertTrue(compare(query, exact)["identifier_agreement"])
        for variant in ("X1", "X1-US", "X1-US/3", "X1 US/2", "X1-US/2 refurbished"):
            reference = offer(brand="Invented Display", **{"product model": variant})
            with self.subTest(variant=variant):
                score = compare(query, reference)
                self.assertFalse(score["identifier_agreement"])
                self.assertEqual(score["identifier_statuses"]["model"], "disagreement")
        same_part = offer(brand="Invented Display", **{"manufacturer part number": "x1-us/2"})
        self.assertFalse(compare(query, same_part)["identifier_agreement"])

    def test_unavailable_and_ambiguous_identifiers_and_comparable_disagreement(self):
        reference = offer(brand="Invented", **{"product model": "X1-US", "manufacturer part number": "P5"})
        for unavailable in ("  ", " N/A ", "https://fixture.test/x", "//fixture.test/x",
                            "www.fixture.test/x", ["invented"], 123, None):
            query = offer(brand=unavailable)
            with self.subTest(unavailable=unavailable):
                self.assertEqual(query["identifiers"]["manufacturer"], ("unavailable", None))
                self.assertFalse(compare(query, reference)["identifier_agreement"])
        ambiguous = offer(brand="Invented", manufacturer="Another", **{"model name": "X1-US"})
        self.assertEqual(compare(ambiguous, reference)["identifier_statuses"]["manufacturer"], "ambiguous")
        self.assertFalse(compare(ambiguous, reference)["identifier_agreement"])
        duplicate = offer(brand="Invented", manufacturer=" invented ",
                          **{"model name": " X1-US ", "product model": "x1-us"})
        self.assertTrue(compare(duplicate, reference)["identifier_agreement"])
        incompatible_part = offer(brand="Invented", **{"model name": "X1-US", "manufacturer part number": "P6"})
        self.assertFalse(compare(incompatible_part, reference)["identifier_agreement"])
        ambiguous_model = offer(brand="Invented", **{"model name": "X1-EU", "product model": "X1-US"})
        self.assertEqual(ambiguous_model["identifiers"]["model"], ("ambiguous", None))
        self.assertFalse(compare(ambiguous_model, reference)["identifier_agreement"])

    def test_full_ranking_uses_exact_jaccard_and_identifier_priority(self):
        query = offer("screen blue blue", brand="Invented", **{"model name": "X1-US"})
        catalog = {"c": offer("blue monitor", brand="Invented", **{"product model": "X1-US"}),
                   "b": offer("screen blue 24-inch"), "a": offer("blue screen 27-inch")}
        rankings = rank(query, catalog)
        self.assertEqual([row["handle"] for row in rankings["T"]], ["a", "b", "c"])
        self.assertEqual([row["handle"] for row in rankings["I+T"]], ["c", "a", "b"])
        self.assertEqual(evidence_key(rankings["T"][0], "T"), (0, Fraction(2, 3)))
        self.assertEqual(evidence_key(rankings["I+T"][0], "I+T"), (1, Fraction(1, 3)))
        self.assertEqual(rank(query, dict(reversed(list(catalog.items())))), rankings)

    def test_missing_and_empty_titles_remain_in_zero_score_ties(self):
        query = offer()
        catalog = {"c": offer("https://fixture.test"), "b": offer("text"), "a": offer(" ")}
        self.assertEqual(query["title_status"], "missing")
        self.assertEqual(catalog["c"]["title_status"], "empty")
        for variant, rows in rank(query, catalog).items():
            self.assertEqual([row["handle"] for row in rows], ["a", "b", "c"])
            self.assertEqual([row["union"] for row in rows], [0, 1, 0])
            self.assertTrue(all(evidence_key(row, variant) == (0, 0) for row in rows))
