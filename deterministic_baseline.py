"""Inference-only features for the fixed F2-D1 title and identifier rankings."""

from fractions import Fraction
import re
import unicodedata


TITLE = "<page title>"
IDENTIFIER_FIELDS = {
    "manufacturer": ("brand", "brand name", "manufacturer"),
    "model": ("model name", "product model"),
    "part_number": ("manufacturer part number",),
}
PLACEHOLDERS = ("-", "--", "n/a", "na", "none", "null", "unknown",
                "not available", "not applicable", "unspecified")
TOKEN = re.compile(r"[^\W_]+(?:[./-][^\W_]+)*")
URL = re.compile(r"(?<![\w./-])(?:[a-z][a-z0-9+.-]*://|//|www\.)[^\s<>()\[\]{}\"',;]+")
EMAIL = re.compile(r"(?:mailto:)?[\w.!#$%&'*+/=?^\x60{|}~-]+@(?:[\w-]+\.)+[\w-]+")
TRANSPORT = re.compile(f"{EMAIL.pattern}|{URL.pattern}")
HANDLE_VERSION = "f2-d1-projected-offer-v1"
VARIANTS = ("T", "I+T")


def configuration():
    return {
        "version": "f2-d1-ranking-v1",
        "title_field": TITLE,
        "identifier_fields": IDENTIFIER_FIELDS,
        "identifier_namespaces": "separate manufacturer, model and part number",
        "field_and_value_normalization": "NFC, casefold, collapse whitespace",
        "unicode_data_version": unicodedata.unidata_version,
        "identifier_values": "nonempty scalar strings; reject literal placeholders and URL prefixes",
        "identifier_placeholders": PLACEHOLDERS,
        "identifier_agreement": "equal unambiguous manufacturer and model or part number; "
                                "veto any comparable model or part-number disagreement",
        "title_url_pattern": URL.pattern,
        "title_email_pattern": EMAIL.pattern,
        "title_transport_removal": "one pass, leftmost match, email before URL at the same position",
        "title_token_pattern": TOKEN.pattern,
        "title_score": "exact token-set Jaccard; empty union scores zero",
        "variants": {
            "T": ["title_score descending", "handle ascending"],
            "I+T": ["identifier_agreement descending", "title_score descending", "handle ascending"],
        },
        "handle": {"version": HANDLE_VERSION, "hash": "SHA-256 of [version, projected offer, occurrence]",
                   "occurrence": "zero-based within identical projections in locator order"},
        "candidate_pool": "all original development references",
        "seed": None,
    }


def canonical_text(value):
    return " ".join(unicodedata.normalize("NFC", value).casefold().split())


def project(record):
    """Copy only original title and allowlisted scalar identifier fields."""
    title = record.get(TITLE)
    fields = [(canonical_text(name), value) for name, value in record.items()
              if isinstance(value, str)]
    return {
        "title": title if isinstance(title, str) else None,
        **{namespace: sorted(value for name, value in fields if name in allowed)
           for namespace, allowed in IDENTIFIER_FIELDS.items()},
    }


def identifier(values):
    normalized = {canonical_text(value) for value in values}
    usable = {value for value in normalized if value and value not in PLACEHOLDERS
              and not URL.match(value)}
    if len(usable) == 1:
        return "available", usable.pop()
    return ("ambiguous" if usable else "unavailable"), None


def normalize(offer):
    title = offer["title"]
    text = TRANSPORT.sub(" ", canonical_text(title or ""))
    tokens = frozenset(TOKEN.findall(text))
    return {
        "title_tokens": tokens,
        "title_status": "missing" if title is None else ("available" if tokens else "empty"),
        "identifiers": {namespace: identifier(offer[namespace]) for namespace in IDENTIFIER_FIELDS},
    }


def compare_identifier(left, right):
    left_status, left_value = left
    right_status, right_value = right
    if "ambiguous" in (left_status, right_status):
        return "ambiguous"
    if "unavailable" in (left_status, right_status):
        return "unavailable"
    return "equal" if left_value == right_value else "disagreement"


def compare(query, reference):
    query_tokens, reference_tokens = query["title_tokens"], reference["title_tokens"]
    statuses = {name: compare_identifier(query["identifiers"][name], reference["identifiers"][name])
                for name in IDENTIFIER_FIELDS}
    product_codes = (statuses["model"], statuses["part_number"])
    return {
        "intersection": len(query_tokens & reference_tokens),
        "union": len(query_tokens | reference_tokens),
        "identifier_statuses": statuses,
        "identifier_agreement": (statuses["manufacturer"] == "equal" and "equal" in product_codes
                                 and "disagreement" not in product_codes),
    }


def evidence_key(candidate, variant):
    """Sort by evidence only so the evaluator can also identify exact ties."""
    return (int(variant == "I+T" and candidate["identifier_agreement"]),
            Fraction(candidate["intersection"], candidate["union"] or 1))


def rank(query, catalog):
    """Score the full catalog once and order the same comparisons for both variants."""
    scores = [{"handle": handle, **compare(query, reference)} for handle, reference in catalog.items()]

    def sort_key(candidate, variant):
        agreement, title_score = evidence_key(candidate, variant)
        return -agreement, -title_score, candidate["handle"]

    return {variant: sorted(scores, key=lambda score: sort_key(score, variant)) for variant in VARIANTS}
