# F0: WDC Products data audit

Date: 2026-10-29; updated 2026-10-30. Task: F0 accepted at revision 2; bounded semantic follow-ups recorded in [feasibility plan](plans/000-feasibility.md), revision 7. Recommendation: `needs_targeted_followup`.

## Outcome and evidence boundary

The documentation-only F0 branch remains accepted and done. On 2026-10-30 the user authorized bounded local inspection despite unresolved rights, retaining WDC and the exact-variant project. Both examples were acquired and structurally inspected; model-assisted semantic review of all 50 PW rows is now complete. Dataset-wide variant correctness and category suitability remain unverified. Rights remain `unresolved`, not prohibited or newly licensed. F1 remains draft. Historical no-acquisition statements below describe the earlier documentation-only tasks.

For the original F0 task, the user authorized source/terms research and conditional inspection of the two publisher examples within the plan limits. That authorization does not resolve source rights. No archives, model weights, dependencies, paid calls, provider uploads, infrastructure, external messages or Git mutations were used. Personal notes were not read. The report is AI-assisted analysis and author self-check, not independent or human review.

## Bounded local inspection (2026-10-30)

Status: structural inspection, the ten-pair semantic follow-up and the separately authorized remaining 40-pair review complete. The user approved proceeding after discussion of the unresolved-rights gate. This is a limited project decision, not a publisher grant. No raw text is reproduced in public documentation. Structural scripts produced metadata and aggregates; the semantic follow-ups processed all 50 PW pairs in this chat with explicit authorization, without an additional model or external service. F0's accepted review is unchanged. No archives, additional datasets, separate model API calls, installations, Git mutations or F1 execution.

### Acquisition evidence

Publisher documentation hrefs were rechecked before acquisition and matched the exact URLs in the reproduction section. Both responses were HTTP 200, `application/json`, no Content-Encoding, no redirect; UTF-8 JSONL parsed completely. Transfer and decoded totals were both **89,095 bytes**. Original bytes are retained locally outside versioned artifacts. Dates below are UTC on 2026-10-30.

| File | Start / completion | Bytes (also Content-Length) | SHA-256 |
| --- | --- | --- | --- |
| `sample_pairwise.json` | 18:55:52.138484 / 18:55:52.460134 | 55,960 | `8c023e0f5571a95a833c431cb94d0f909db3c4bc6e0993d01c5b7488e356d90b` |
| `sample_multi.json` | 18:55:52.462136 / 18:55:52.606345 | 33,135 | `b3a148084b89054e2f193c75eefb628c370b57384bde5c3cb7563af2b40ed00e` |

An initial sandbox attempt failed at DNS resolution before receiving bytes. The approved outside-sandbox execution used a fresh output directory and succeeded; no dataset bytes were consumed by the failed attempt. The downloader enforces 1 MiB per body and 2 MiB combined, rejects redirects/encoded bodies, uses a 10-second socket timeout and a 60-second deadline checked between reads. Identity decoding makes the combined decoded size equal to transfer size and below 5 MiB. At an exact cap it requires established completion without an extra byte. No downloader boundary/fault-injection tests were run; successful small transfers do not validate all failure paths.

### Observed structure and coverage

All 50/50 PW rows and 50/50 MC rows were inspected in source order for structure; no row truncation. Every row contained every expected key for its format. There were no empty strings in these fields. Counts below use occurrences, not deduplicated offers.

| Property | PW (50 pairs / 100 offer occurrences) | MC (50 offer occurrences) |
| --- | --- | --- |
| Unique offer IDs / clusters | 97 / 89 | 50 / 50 |
| Repeated offer IDs / conflicting payloads | 3 / 0 | 0 / 0 |
| Labels | 46 negative, 4 positive | 50 distinct integer labels, each equal to cluster_id |
| Hard-negative flag | 39 true, 11 false | Not present |
| Unseen flag | Not present | 50 false |
| Null brand | 30 left + 30 right / 100 | 31 / 50 |
| Null description | 17 left + 15 right / 100 | 16 / 50 |
| Null price | 1 left + 3 right / 100 | 5 / 50 |
| Null priceCurrency | 1 left + 3 right / 100 | 6 / 50 |
| Null title / ID / cluster ID | 0 | 0 |

Observed keys: PW has `id`, `cluster_id`, `brand`, `title`, `description`, `price`, `priceCurrency` each with `_left`/`_right`, plus `pair_id`, `label`, `is_hard_negative`. MC has the seven unsuffixed offer fields plus `label`, `unseen`. IDs, cluster IDs and labels are integers; pair_id and titles are strings; flags are booleans. Brand/description/price/currency are strings **or null**, a material addition to the documented schema. Category, merchant/source URL and explicit split name are absent from both examples.

Reconciliation: six IDs overlap between PW and MC. Across 150 occurrences there are **141 unique offers and 127 unique clusters**; no same-ID payload conflicts after removing pair/MC supervision fields. All 50 pair IDs are unique and equal the left/right IDs joined by `#`. All pair labels agree with cluster equality; this verifies internal consistency only, not variant correctness. MC `unseen=false` does not establish train membership. Treat all inspected identities as schema discovery only and exclude their identity groups from any future custom frozen test; do not tune prompts or thresholds on them. The exclusion set can be regenerated from the hash-identified files' IDs and cluster IDs; a definitive grouping remains an F1 prerequisite.

### Ten bounded diagnostic probes (historical mechanical pass)

Only PW rows 1-10 were probed for identity evidence, using local deterministic comparisons of brand availability, descriptions and numeric-unit tokens from title/description. These are mechanical diagnostics, not semantic judgments or human-reviewed labels. Source labels are all 0; hard-negative is true for rows 1-9 and false for row 10. No label was corrected.

| PW row locator (1-based, file hash above) | Descriptions present (out of 2) | Numeric-unit token counts left/right | Shared tokens |
| --- | --- | --- | --- |
| 1 | 1 | 1 / 1 | 0 |
| 2 | 1 | 0 / 0 | 0 |
| 3 | 2 | 1 / 0 | 0 |
| 4 | 2 | 0 / 0 | 0 |
| 5 | 2 | 0 / 0 | 0 |
| 6 | 2 | 1 / 1 | 0 |
| 7 | 1 | 1 / 0 | 0 |
| 8 | 1 | 1 / 1 | 1 |
| 9 | 0 | 0 / 0 | 0 |
| 10 | 1 | 0 / 2 | 0 |

No probed pair has both brands present or identical titles. Unit detection used case-insensitive numeric values followed by GB/TB/MB/ml/kg/mm/cm/inch/pack; token sets were lowercased and spaces removed. Different units may describe unrelated attributes, and equal units do not establish identity. This pass did not assess semantics; the follow-up below supersedes that limitation for these ten rows only.

### Model-assisted semantic review (2026-10-30)

Scope: exactly physical JSONL lines 1-10, in source order, from `sample_pairwise.json`. Locator prefix **H** means SHA-256 `8c023e0f5571a95a833c431cb94d0f909db3c4bc6e0993d01c5b7488e356d90b`; every table locator combines H, a 1-based line and the original `pair_id`. Recomputed SHA-256 and 55,960-byte length match both saved metadata and the acquisition table. No raw titles or descriptions are reproduced below.

Method: first read only brand, title, description, price and currency for each side, masking `label`, `cluster_id` and `is_hard_negative`; fix attribute judgments before reading row-level supervision and pair IDs. This was **not fully blinded**: the required pre-read audit already disclosed that all ten labels were 0 and the flag distribution. Judgments rely on offer evidence, not these fields. Prices/currencies do not establish identity. This is **model-assisted semantic review**, not human-reviewed annotation, independent validation or gold ground truth. Source labels and payloads were not changed. The authorized local data was read into this chat only; no additional model, external service, merchant page, download or installation was used. The optional HTML worksheet was not needed or read.

| Locator: hash / line / pair_id | Attribute judgment | Rationale and decisive or missing attributes | Comparison after judgment |
| --- | --- | --- | --- |
| H / 1 / `75937316#38128607` | `different_variant` | USB drives differ in named model family and explicit capacity: 16 versus 64 GB. Capacity alone rules out the same exact variant; incomplete interface evidence does not affect this conflict. | Consistent with source 0 (different). |
| H / 2 / `81858107#44726488` | `different_variant` | Both are printers, but their explicit manufacturer model numbers differ. Shared brand/product type does not override that distinction; condition and regional configuration are not established. | Consistent with source 0. |
| H / 3 / `91942249#86779035` | `different_variant` | A camera mounting bracket versus photographic film. The left description lists compatible camera models; these are not the sold product. Product type is decisive even without pack/condition evidence. | Consistent with source 0. |
| H / 4 / `48329606#25011125` | `different_variant` | Surveillance recorders have different explicit model identifiers and channel counts (8 versus 16). The left title/description also differ in codec wording, but resolving that internal inconsistency is unnecessary for this mismatch. | Consistent with source 0. |
| H / 5 / `67017951#5303451` | `insufficient_evidence` | Left text describes a security-platform family and points to a review; it identifies no sellable model, bundle or included contents. Right identifies an infrared-extension accessory and its own model code; its compatible camera is not the sold item. Missing left identity prevents an exact-variant comparison. | Potential evidential divergence from source 0: a negative label may be plausible, but is not established from a defined left variant. This is not a demonstrated label error. |
| H / 6 / `16691545#86650421` | `different_variant` | Micro camera versus bullet camera: distinct named camera variants. Right explicitly sells three units; left unit count is not explicit and is not assumed to be one. Model difference is sufficient without resolving quantity. | Consistent with source 0. |
| H / 7 / `43900336#13950014` | `different_variant` | Computer-memory kit versus photographic tripod kit. The sold product types differ; shared kit/color wording is not identity evidence. | Consistent with source 0. |
| H / 8 / `37708089#70265673` | `different_variant` | Equal brand, 4 GB, memory generation and speed do not establish identity. Left explicitly identifies a laptop SO-DIMM; right identifies desktop RAM with a model code. These denote different module types/use; no unstated pin count is inferred. | Consistent with source 0. |
| H / 9 / `41364196#29165749` | `different_variant` | Caps carry different named team designs and style lines. Those explicit design differences establish distinct sellable products despite missing descriptions, size, color and condition. No size/color values are inferred. | Consistent with source 0. |
| H / 10 / `21293905#77791574` | `different_variant` | Wristwatch with a reference identifier versus internal SSD. Product type suffices. The SSD title and description disagree on flash-cell type; that unresolved internal conflict does not affect this pair decision. | Consistent with source 0. |

After judgments, all ten source labels were confirmed as 0 with unequal source clusters; hard-negative flags were true for lines 1-9 and false for line 10. These fields supplied no semantic evidence. Descriptively, this pass contains nine `different_variant`, one `insufficient_evidence` and no `same_variant` judgments. This is not an agreement/accuracy estimate. In particular, some flagged hard negatives are different product types; the flag cannot define our exact-variant difficulty slices.

Feasibility implications: explicit model/capacity/form-factor evidence supports useful deterministic conflict checks, but no baseline or normalization rule was implemented or evaluated. Compatibility lists must be separated from sold-item identity, family/editorial records require an eligibility decision, and contradictory attributes must remain visible. Missing condition, size, color or pack evidence must not be imputed; decisive observed differences can still establish a negative pair. None of these ten cases requires inventing a new identity policy to claim a positive match. The records span several product types and do not justify selecting one category or demonstrate enough category coverage. WDC remains a candidate, with recommendation `needs_targeted_followup`.

Limitations: ten consecutive examples are not representative; all source labels are negative, so positive exact-variant evidence has not been assessed. No human judgments, quality metrics, dataset-wide label-noise estimate, retrieval/candidate evaluation or offer-to-catalog result follow. Split membership remains unknown: do not use these identities for prompt, threshold or model tuning, and keep their identity groups excluded from a future custom frozen test. No F1 work, source-label correction or final identity/eligibility policy was performed.

### Accepted eligibility decision (2026-10-30)

The owner authorized adoption of the recommended rule: [D15](DECISIONS.md), policy v1, as specified in the [evaluation contract](EVALUATION.md#offer-eligibility). Exclude confirmed editorial/family records without a sellable item; retain incomplete offers and uncertain eligibility. This resolves the preceding semantic review's open eligibility question without changing category-specific identity rules.

Application: H / line 5 / pair `67017951#5303451`, left offer `67017951`, is excluded from future eligible offer inputs. Reason: `editorial_without_sellable_item`; evidence is a platform/family overview pointing to a review, with no defined sold model or bundle. Assessment origin: AI-assisted analysis under an owner-approved policy, not human annotation. Preserve the raw record, source label 0 and historical pair judgment `insufficient_evidence`; the original ten-pair summary remains nine different and one unresolved. No new sample-wide eligibility measurement is claimed. Future custom evaluation must report exclusions separately and preserve the full-input denominator.

### Verification and conclusion

Saved bytes were reparsed offline with a separate line-by-line pass. Both hashes, byte counts, 50-row counts, pair-ID composition/uniqueness and combined unique offer/cluster counts were checked. No performance evaluation was run. The examples are usable for schema discovery, but do not establish one category with 100-150 diagnostic cases or an offer-to-catalog benchmark. Recommendation remains `needs_targeted_followup`; retain WDC, with F1-F4 draft.


## Remaining-pair semantic analysis (2026-10-30, revision 7 execution)

The owner explicitly authorized the proposed extension to PW physical lines 11-50 in this chat despite the recorded unresolved rights. The saved payload and metadata match H and 55,960 bytes; all 50 physical lines are present. No new download, MC inspection, merchant lookup, extra service, paid call or installation was used. Existing proposal changes were preserved.

Method: four batches of ten in source order; brand/title/description/price/currency were read and judgments recorded before revealing each batch's row-level labels, clusters and hard-negative flags. Aggregate label counts and the prior report were already known, so this is not fully blinded. Assessments are AI-assisted diagnostic judgments, not gold labels or a measured model baseline. No category-specific identity policy was invented to force a positive. Matching model names without enough configuration or bundle evidence remain unresolved; unobserved condition is never assumed new.

### Forty additional judgments

H is the same SHA-256 defined above. Each locator is H / physical line / original pair ID; its left and right offer IDs are the components of that pair ID. E/E means both sides are eligible under D15 v1; U/E means left eligibility is uncertain and retained in the eligible denominator. Every E assessment has evidence of a named sellable item in the input; it does not imply complete variant evidence. The category describes both sides unless marked cross-type, where the rationale names the left and right types. No new exclusion was made.

| Locator: H / line / pair_id | Product type / slice | Eligibility L/R | Judgment | Evidence and unresolved attributes | Source label |
| --- | --- | --- | --- | --- | --- |
| H / 11 / `49744056#66087579` | Label tapes | E/E | `different_variant` | Tape widths differ: 19 versus 12 mm; model codes also differ. | 0 |
| H / 12 / `33473348#16164619` | Computer cases | E/E | `different_variant` | Distinct case model families and explicit colors; both are mid-tower cases. | 0 |
| H / 13 / `78194247#19072250` | Headsets | E/E | `different_variant` | Different headset families and duo versus mono configuration. | 0 |
| H / 14 / `1331887#46707617` | Cross-type | E/E | `different_variant` | Camera lens versus uninterruptible power supply. | 0 |
| H / 15 / `14954745#7309472` | Bicycle chains | E/E | `insufficient_evidence` | Same chain family and speed, but right specifies 116 links and left does not establish length; weights differ without resolving configuration. | 1 |
| H / 16 / `24300732#50979472` | Wireless access points | E/E | `different_variant` | In-wall versus Pro model identifiers; both explicitly five-unit packs. | 0 |
| H / 17 / `4402971#13802221` | Cross-type | E/E | `different_variant` | Monitor versus hex-wrench set. | 0 |
| H / 18 / `36616040#52341668` | Cross-type | E/E | `different_variant` | Headset versus notebook paper refill. | 0 |
| H / 19 / `63505292#40438621` | Bicycle brake pads | E/E | `different_variant` | Sintered versus organic compound despite matching backing material and compatible brakes. | 0 |
| H / 20 / `63587638#52588862` | External SSDs | E/E | `different_variant` | Touch versus standard model and black versus blue; equal 2 TB capacity is insufficient. | 0 |
| H / 21 / `25138178#45664586` | Cross-type | E/E | `different_variant` | Memory card versus internal SSD; equal capacity is not identity. | 0 |
| H / 22 / `14636186#625440` | Cross-type | E/E | `different_variant` | Mouse versus ink cartridge; compatible printers are not the sold item. | 0 |
| H / 23 / `70272012#11565762` | Cross-type | E/E | `different_variant` | Bicycle chain versus internal SSD. | 0 |
| H / 24 / `56902092#5578260` | Headsets | E/E | `different_variant` | Distinct headset model families, 2400 II versus 2300. | 0 |
| H / 25 / `25607937#45641488` | UPS units | E/E | `different_variant` | Different UPS model designations, 1000 LCD versus SRT 3000. | 0 |
| H / 26 / `28769706#78600248` | Cross-type | E/E | `different_variant` | Wireless earbuds with charging case versus USB drive. | 0 |
| H / 27 / `25831104#57162953` | Bicycle cassettes | E/E | `different_variant` | Different cassette models and 11 versus seven speeds. | 0 |
| H / 28 / `11556800#87112730` | Tablets | E/E | `insufficient_evidence` | Matching family, screen size, capacity and silver color; right omits Wi-Fi-only versus cellular configuration. | 1 |
| H / 29 / `20791179#51278033` | Computer cases | E/E | `different_variant` | Different case models, H500M versus 110R; compatible components are not sold contents. | 0 |
| H / 30 / `28403450#47959304` | Ink cartridges | E/E | `different_variant` | Distinct cartridge codes, color and size designations: yellow XL versus mono XXL. | 0 |
| H / 31 / `62062623#16111692` | UPS units | E/E | `different_variant` | Different explicit UPS codes: SMT1000RMI2UC versus SMT1000I; equal VA rating does not establish identity. | 0 |
| H / 32 / `21390817#18996777` | Cross-type | E/E | `different_variant` | Graphics card versus surveillance recorder. | 0 |
| H / 33 / `6563464#89906566` | Cross-type | E/E | `different_variant` | Wristwatch versus camera bracket; bracket title and description conflict on color, without affecting this pair decision. | 0 |
| H / 34 / `78660792#84859691` | Toner cartridges | E/E | `different_variant` | Different cartridge identifiers and compatible versus original product claims; no assumption that the compatibility brand is the manufacturer. | 0 |
| H / 35 / `37083729#28769706` | Wireless earbuds | E/E | `different_variant` | Pro versus second-generation earbuds; shared charging-case feature does not establish identity. | 0 |
| H / 36 / `45833973#96299407` | Notebook accessories | U/E | `insufficient_evidence` | Left names only notebook accessories, with price but no subtype; right specifies a slip case and dimensions. Left may be an incomplete offer or a category listing, so eligibility remains uncertain rather than excluded. | 0 |
| H / 37 / `70728429#60131715` | Internal SSDs | E/E | `different_variant` | Same SSD family but 250 versus 500 GB capacity. | 0 |
| H / 38 / `45366053#34146981` | Sports watches | E/E | `different_variant` | 5S Sapphire versus 5S Plus and different case finishes; generic multi-model description does not override the sold-item title. | 0 |
| H / 39 / `54164067#3553691` | Cross-type | E/E | `different_variant` | Photo paper versus wristwatch. | 0 |
| H / 40 / `33520763#47121877` | Headphones | E/E | `different_variant` | Distinct headphone model codes, M50XWH versus PRO7x. | 0 |
| H / 41 / `6562952#14979345` | Bicycle pedals | E/E | `insufficient_evidence` | Same pedal model and interface, but left explicitly includes cleats while right does not establish included contents or unit count. Do not assume a standard bundle. | 1 |
| H / 42 / `34868774#23678296` | Wristwatches | E/E | `different_variant` | Different model lines and 42 versus 41 mm case size; right is explicitly pre-owned and customized, while left condition is unstated. | 0 |
| H / 43 / `68792553#22150807` | Cross-type | E/E | `different_variant` | Complete UPS versus replacement battery cartridge; battery compatibility is not complete-device identity. | 0 |
| H / 44 / `34920376#40438621` | Bicycle brake pads | E/E | `different_variant` | Sintered versus organic compound and different named compatible brake families. | 0 |
| H / 45 / `31517280#43227294` | Cross-type | E/E | `different_variant` | System memory module versus graphics card; graphics memory is not the sold standalone RAM. | 0 |
| H / 46 / `88973966#13546282` | Drum heads | E/E | `different_variant` | Different model families and 14 versus 20 inch diameter. | 0 |
| H / 47 / `25445188#14737778` | Cross-type | E/E | `different_variant` | Memory card with adapter versus mechanical mounting base; RAM is a mounting brand here, not computer memory. | 0 |
| H / 48 / `87238244#84550965` | Cross-type | E/E | `different_variant` | Mouse versus printer ribbon; ribbon minimum purchase of three is not silently converted into a three-unit pack. | 0 |
| H / 49 / `63396450#65942456` | Privacy filters | E/E | `insufficient_evidence` | Same brand and nominal diagonal, but left Flex wording does not establish model, dimensions or mounting; right explicitly framed. Do not infer an incompatible construction from an unexplained shorthand. | 1 |
| H / 50 / `3553691#8032910` | Wristwatches | E/E | `different_variant` | Different watch reference identifiers and model lines. | 0 |

The four source-positive rows are 15, 28, 41 and 49; all remain `insufficient_evidence`. Missing chain length, tablet connectivity, pedal bundle contents and filter construction/model evidence respectively prevent confirmation. Row 36 is a source-negative with unresolved identity and uncertain left eligibility. These are evidential disagreements, not proven source errors. The other 35 new rows have decisive differences consistent with source negatives. Labels agree with source cluster equality throughout; source labels and payloads were not changed.

### Coverage and denominators

Historical lines 1-10: 9 different, 1 insufficient. New lines 11-50: 35 different, 5 insufficient. Combined: **50 pairs, 44 different, 6 insufficient, 0 supported same-variant judgments**. Original supervision remains 46 negative / 4 positive. These counts are not accuracy, label-noise estimates or evidence that the source has no valid positive matches.

The 100 offer occurrences contain 97 unique IDs: 95 eligible, one eligibility-uncertain and one excluded. Counting uncertainty in the eligible denominator gives 96/97 retained unique records; on an occurrence basis, 99/100 are retained (98 eligible, one uncertain, one excluded). These are input-accounting denominators, not automation metrics. The sole exclusion is historical line 5 left offer `67017951`, reason `editorial_without_sellable_item`. The uncertainty is line 36 left offer `45833973`: a generic accessory title and a price do not establish either a concrete subtype or an editorial/category page. Retain it for review.

Repeated offer IDs are `28769706` (lines 26/35), `40438621` (19/44) and `3553691` (39/50), each with unchanged payloads. Pair IDs and unordered offer-ID pairs are unique. Source clusters also correlate records across pairs; neither different offer IDs nor source clusters prove independent exact identities. No new identity groups were established.

The following table groups original pairs, not all possible combinations. Source counts are negative/positive; judgment counts are same/different/insufficient. Excluded/uncertain columns count unique offers within each slice; unique-offer totals across slices overlap. Confusing negatives share observed product type or family and a decisive conflict; this descriptive selection is not a difficulty benchmark. Historical types are taken from the existing ten-row audit, without rereading those attributes. The unresolved-type slice is line 5; cross-type pairs are not credited to a candidate category.

| Observed pair slice | Pairs | Unique offers | Source -/+ | Judgments S/D/I | Excluded/uncertain | Confusing negatives |
| --- | --- | --- | --- | --- | --- | --- |
| USB drives | 1 | 2 | 1/0 | 0/1/0 | 0/0 | 1 |
| Printers | 1 | 2 | 1/0 | 0/1/0 | 0/0 | 1 |
| Cross-type | 17 | 34 | 17/0 | 0/17/0 | 0/0 | 0 |
| Surveillance recorders | 1 | 2 | 1/0 | 0/1/0 | 0/0 | 1 |
| Unresolved product type | 1 | 2 | 1/0 | 0/0/1 | 1/0 | 0 |
| Surveillance cameras | 1 | 2 | 1/0 | 0/1/0 | 0/0 | 1 |
| Memory modules | 1 | 2 | 1/0 | 0/1/0 | 0/0 | 1 |
| Caps | 1 | 2 | 1/0 | 0/1/0 | 0/0 | 1 |
| Label tapes | 1 | 2 | 1/0 | 0/1/0 | 0/0 | 1 |
| Computer cases | 2 | 4 | 2/0 | 0/2/0 | 0/0 | 2 |
| Headsets | 2 | 4 | 2/0 | 0/2/0 | 0/0 | 2 |
| Bicycle chains | 1 | 2 | 0/1 | 0/0/1 | 0/0 | 0 |
| Wireless access points | 1 | 2 | 1/0 | 0/1/0 | 0/0 | 1 |
| Bicycle brake pads | 2 | 3 | 2/0 | 0/2/0 | 0/0 | 2 |
| External SSDs | 1 | 2 | 1/0 | 0/1/0 | 0/0 | 1 |
| UPS units | 2 | 4 | 2/0 | 0/2/0 | 0/0 | 2 |
| Bicycle cassettes | 1 | 2 | 1/0 | 0/1/0 | 0/0 | 1 |
| Tablets | 1 | 2 | 0/1 | 0/0/1 | 0/0 | 0 |
| Ink cartridges | 1 | 2 | 1/0 | 0/1/0 | 0/0 | 1 |
| Toner cartridges | 1 | 2 | 1/0 | 0/1/0 | 0/0 | 1 |
| Wireless earbuds | 1 | 2 | 1/0 | 0/1/0 | 0/0 | 1 |
| Notebook accessories | 1 | 2 | 1/0 | 0/0/1 | 0/1 | 0 |
| Internal SSDs | 1 | 2 | 1/0 | 0/1/0 | 0/0 | 1 |
| Sports watches | 1 | 2 | 1/0 | 0/1/0 | 0/0 | 1 |
| Headphones | 1 | 2 | 1/0 | 0/1/0 | 0/0 | 1 |
| Bicycle pedals | 1 | 2 | 0/1 | 0/0/1 | 0/0 | 0 |
| Wristwatches | 2 | 4 | 2/0 | 0/2/0 | 0/0 | 2 |
| Drum heads | 1 | 2 | 1/0 | 0/1/0 | 0/0 | 1 |
| Privacy filters | 1 | 2 | 0/1 | 0/0/1 | 0/0 | 0 |

### Outcome and next action

**No category meets the predeclared discovery threshold of two supported positive pairs and two confusing negatives.** None has a supported positive pair in this review; the four source positives also lie in four separate types. Changing the threshold or combining unrelated bicycle/electronic products would not supply the missing evidence. Recommendation remains `needs_targeted_followup`; no category is selected and F1-F4 remain draft.

The precise missing slice is multiple independently checked same-variant pairs with explicit identity-bearing configuration and bundle evidence in one category, alongside confusing negatives in that category. Further work also needs category-specific rules for sufficient positive evidence, including treatment of unspecified condition and standard included accessories; this pass does not assume those rules. No larger acquisition is justified solely by these 50 examples.

Next action: prepare a documentation-only comparison of a bounded WDC continuation versus one alternative source, focusing on explicit permitted use, category-specific positive/negative coverage and variant-level evidence, before proposing any new acquisition. No publisher contact, data download or provider upload is authorized by this recommendation. Keep all inspected identity groups excluded from future custom frozen tests; do not tune models, prompts or thresholds on this unknown-split sample. Source rights and offer-to-catalog construction remain unresolved.

## Dated primary-source evidence

All sources below were inspected on 2026-10-29. Web pages and repository `main` are mutable; no immutable dataset revision or payload hash was established. The source is WDC Products, initially released 2022-12-22 according to its publisher page; no particular benchmark variant was selected.

| ID | Primary source and locator | Evidence and classification |
| --- | --- | --- |
| S1 | [WDC Products](https://webdatacommons.org/largescaleproductcorpus/wdc-products/), sections 2, 3, 5 and footer | Publisher claims: identifier-derived clusters; two expert annotators estimated 4.00% and 4.17% noise on 600 sampled pairs. Offer-disjoint splits include seen/unseen products. Examples are linked publicly. Footer discourages inclusion in training corpora. No data-specific permission grant was found. |
| S2 | [Publisher repository README](https://github.com/wbsg-uni-mannheim/wdcproducts), README and root inventory | Observed documentation: repository describes code and external data download links. It gives environment and pipeline execution instructions; none were executed. No explicit grant covering the externally hosted examples was found in the README. |
| S3 | [Repository LICENSE](https://github.com/wbsg-uni-mannheim/wdcproducts/blob/main/LICENSE) | Observed license text: BSD-style source/binary redistribution conditions, attribution and non-endorsement obligations, and software warranty disclaimer. Inference: this software wording does not establish rights to third-party product text hosted outside the repository. |
| S4 | [WDC home page](https://webdatacommons.org/index.html), License and Available Software | Observed scope: Apache licensing is expressly attached to the extraction framework. Inference: it cannot be transferred to benchmark data merely because both belong to WDC. |
| S5 | [Earlier WDC corpus page](https://webdatacommons.org/largescaleproductcorpus/), source-family documentation | Read as a provenance/terms lead, not an alternative dataset audit. Public download descriptions do not establish terms for the WDC Products examples. No payload or merchant page was opened. |

Search scope was the publisher page, repository README/root license, WDC home licensing section and the earlier corpus documentation. No directly linked data-use agreement was identified there. This is not an exhaustive search of all upstream rights or a legal opinion. No alternative was investigated: unresolved rights do not establish a concrete semantic/access failure, and the smallest useful next step concerns this source's terms.

## Targeted rights follow-up (2026-10-29)

Scope: public documentation and terms for the two exact PW/MC URLs in the reproduction section only. The user expressly prohibited requesting either payload even if permission was found. No other data, archives, author contact, terms acceptance action, installations, paid calls, Git mutations, delegation or F1 work were authorized or performed. This follow-up supplements the accepted F0 audit; it does not reopen its historical review.

### Additional primary evidence and applicability

All entries were inspected on 2026-10-29. Locators identify headings or distinctive passages rather than unstable browser line numbers. These are documentation observations, not payload observations.

| ID | Source and precise locator | Source content | Applicability assessment |
| --- | --- | --- | --- |
| S6 | [WDC Products](https://webdatacommons.org/largescaleproductcorpus/wdc-products/), section 2 first two paragraphs; section 5 opening, processing paragraph and Example (PW)/(MC) columns | Publisher offers the benchmark for download, describes local JSON processing and traces it to PDC2020-C/Common Crawl. HTML links match both requested URLs. | Positive evidence of intended research use, beyond mere server accessibility. However, neither these passages nor the example links identify the rights conveyed in underlying merchant content. The training-corpus footer concerns a different activity; it is not a ban on local inspection. |
| S7 | [PDC2020](https://webdatacommons.org/largescaleproductcorpus/v2020/index.html), opening paragraph and section 1; [2020 subsets](https://webdatacommons.org/structureddata/2020-12/stats/schema_org_subsets.html), release title; [structured-data documentation](https://webdatacommons.org/structureddata/), section 1 final paragraph and section 9 | PDC2020 identifies its source as the December 2020 WDC Product subsets. The structured-data page states: "We publish the corpora for research purposes only." Section 9 licenses the extraction framework. | Documented upstream chain makes this research-purpose statement relevant. It concerns the extracted corpora; no explicit extension to these derived JSON examples or explanation of third-party permissions was found. Research-only scope is compatible with the proposed inspection, but does not by itself settle the rights gate. No commercial-use permission inferred. |
| S8 | [Common Crawl Terms of Use](https://commoncrawl.org/terms-of-use), last updated March 7, 2024; introduction, sections 1, 2, 3, 9 and 13 | CC grants limited access/use of its Service, without transfer or sublicensing. Crawled Content may have separate owner terms; users must respect third-party rights. Use is described as acceptance; section 9 includes indemnification obligations. | Applies expressly to CC's Service/Crawled Content, not expressly to WDC's two hosted examples. Provenance establishes relevance, not automatic downstream licensing. It supplies no blanket merchant-content clearance. Which terms/version govern the derived 2020 content remains unresolved; no agreement was accepted on the user's behalf. |
| S9 | [Common Crawl FAQ](https://commoncrawl.org/faq), General Questions: "What is Common Crawl?" and "Under what terms is Common Crawl data released?" | Research/analysis access is intended for researchers, companies and individuals; the release-terms answer refers to the ToU. | Supports the intended use context, but does not remove S8's conditions or license WDC's derived examples separately. |
| S10 | [Authors' release announcement](https://groups.google.com/g/web-data-commons/c/SYGS9oAIky4), January 26, 2023, Download paragraph and Peeters/Bizer signature; [paper v2](https://arxiv.org/html/2301.09521v2), end of section 1 and sections 3.1-3.2 | Authors invite benchmark download and explain its origin and research purpose. No data-license statement was identified in those passages; a text search for `licen` in the paper found none. | Stronger evidence of publisher intent than third-party dataset listings, but not an express clarification of content rights or conditions for local inspection. A publication license would not automatically license externally hosted data. |
| S11 | [Website repository](https://github.com/wbsg-uni-mannheim/wdc-page), README and root inventory; [benchmark LICENSE](https://raw.githubusercontent.com/wbsg-uni-mannheim/wdcproducts/main/LICENSE), copyright line, grant, three conditions and disclaimer | Website README describes support for researchers/companies through public downloads. Benchmark license names Ralph Peeters and permits source/binary use subject to notice, disclaimer and non-endorsement conditions. | No statement found extending that software license to the two external examples or granting rights on behalf of merchants. Website root inventory/README supplied no additional applicable data terms. |

### Finding and search limits

**Local acquisition and inspection: `unresolved` for both `sample_pairwise.json` and `sample_multi.json`.** The publisher's invitations and research-only statement are positive evidence of intended use. Our interpretation is that they do not yet establish the applicable content-rights basis required by this plan. Common Crawl's limited license preserves separate owner rights rather than resolving them. This is not evidence of a prohibition, and `restricted` is not assigned to the proposed local activity merely because upstream conditions exist.

The missing evidence is a publisher/rightsholder clarification applying to these two examples: whether local storage and offline inspection for product-matching research are permitted, what conditions apply, and whether underlying merchant content requires additional permission or another stated basis. It need not authorize public statistics, raw redistribution or model-provider transmission. Those future activities are not prerequisites for this narrow decision.

Concrete leads checked beyond F0: the documented PDC2020/structured-data/Common Crawl chain, CC FAQ/ToU, authors' announcement and paper, website repository README/root, and benchmark issue listing. Targeted web searches combined WDC Products/Web Data Commons with license, terms and permission, including the official group/repository. Third-party license labels and unrelated dataset results were not used as grants or pursued as alternative audits. No merchant terms were guessed without identifying a relevant source record.

Coverage limits: the GitHub issue view returned a loading error and an empty open-issue result, so no comprehensive issue-history claim is made. Google Groups' license-search URL was inaccessible; the public group listing and exact release announcement were readable. Its announcement link initially resolved to a duplicated `/g/g/` path; the canonical `/g/` URL succeeded. A raw website-source URL returned a cache miss; the published page and repository README/root were readable. No evidence is inferred from these failures. Research stopped early after the concrete leads were checked, within the 60-minute maximum; it was not an exhaustive legal or historical-terms investigation.

The follow-up rechecked the two hrefs using documentation-only curl output. The sandbox request failed with DNS exit 6; the same command outside the sandbox succeeded with exit 0. Neither sample endpoint was requested, including for headers. Dataset bytes and inspected records remain zero. The existing conditional recipe remains unexecuted.

## Rights assessment

Statuses describe the evidence available for this task, not universal legal conclusions. All rows use the inspection date above.

| Activity | Status | Evidence, scope and consequence |
| --- | --- | --- |
| Access to public documentation/download links | supported | S1/S2/S4 expose public documentation and links. Both exact example endpoints returned HTTP 200 during the bounded acquisition; accessibility does not establish data-use rights. |
| Local acquisition and inspection of examples | unresolved | S6-S11 establish intended research/download use and upstream conditions, but not a sufficient applicable content-rights basis for either exact example. The 2026-10-30 owner decision permits bounded local inspection despite this uncertainty; it does not change the rights status. |
| Publication of derived dataset statistics | unresolved | No applicable data terms identified. This audit includes bounded structural aggregates and original semantic summaries under the owner's requested reporting scope; this does not establish broader publication or redistribution rights. |
| Raw dataset redistribution | unresolved | S3/S4 cover software; applicability to external product records is unestablished. Publish no raw product text. |
| Future transmission to a model provider | unresolved | Neither inference processing, retention nor provider training rights are established. S1's training-corpus notice adds a constraint to resolve; it is not permission for inference uploads. The owner separately authorized analysis of ten local pairs in this chat; no additional provider/service upload was performed or authorized. |

The missing evidence is a publisher/rightsholder statement or applicable data license explicitly covering these hosted examples and their underlying product content, with scope for local research inspection. A software license, download button or repository visibility alone is insufficient under this plan. Broader publication and provider processing rights need separate evidence before those activities.

## Historical documentation-only schema assessment

Documented only (S1, section 5): JSON rows represent pairs or single offers. Offer fields are `id` and `cluster_id` (integers), and `brand`, `title`, `description`, `price`, `priceCurrency` (strings). Pair offer fields use `_left`/`_right`; `label` is 0/1, `pair_id` joins offer IDs, and `is_hard_negative` is boolean. Multi-class `label` corresponds to `cluster_id`; `unseen` is boolean. `url` is documented for the corpus only. Category is not listed in the benchmark schema.

These are publisher declarations, not observed field names, types or domains. Sample serialization, completeness and agreement with that description remain unknown.

The following table records the original documentation-only F0 result, superseded for acquisition/structure by the 2026-10-30 section above.

| Inspection | Original F0 result |
| --- | --- |
| Dataset requests, acquired payloads and dataset bytes | 0, 0 and 0; documentation requests are separate |
| Available PW/MC rows | Unknown; no endpoint request |
| Inspected PW rows / single-offer rows / diagnostic cases | 0 / 0 / 0 |
| Payload acquisition times, byte sizes and SHA-256 | Not applicable: no acquisition; no invented hashes |
| Decoding, full parsing, offline re-parse and row counts | Not run: rights gate unresolved |
| Missing keys versus null versus empty values | Not run; rates and denominators unknown |
| Unique offers/clusters, duplicate IDs and payload conflicts | Not run; unknown |
| PW/MC overlap reconciliation | Not run; no combined record count asserted |
| Identity evidence, label conflicts and case locators | Not run; no record-level judgments or corrections |
| Category coverage and sample split membership | Unknown; no category recommendation |

## Identity and evaluation implications

AI-assisted assessment: identifier-derived supervision needs checking against exact sellable variants. It cannot establish that capacity, model, pack size or condition differences were preserved. The publisher's noise estimates are neither a CatalogMatch error estimate nor local human verification. Keep benchmark labels separate from future `same_variant`, `different_variant` and `insufficient_evidence` judgments. No identity policy changed.

The documented pair/class tasks do not supply a validated offer-to-catalog protocol. Future work must establish:

- How reference records are chosen without using answer labels as inference features.
- Reliable exact-variant identity groups before creating product-disjoint partitions; distinct offers alone are insufficient.
- Complete identity removal for absent-product cases. A negative pair or missing retrieval candidate does not prove catalog absence.
- Supplier provenance and sufficient supplier coverage before any unseen-supplier claim.
- Separate candidate recall and decision evaluation, preserving original benchmark protocols when using their name.

Category suitability and enough examples for F1's 100-150 diagnostics remain unproven. Historical benchmark contamination cannot be excluded. If later examples have unknown/test membership, use them only for schema discovery, exclude inspected identities from a custom frozen test, and do not tune prompts or thresholds on them. Source cluster IDs and labels must stay outside proposed inference features. No retrieval, annotation, splits or benchmark were implemented.

## Reproduction and conditional inspection recipe

Documentation review used browser-tool reads of S1-S5 and the following PowerShell command to resolve example links from S1's HTML without requesting the linked payloads:

```powershell
curl.exe --fail --silent --show-error --max-time 30 https://webdatacommons.org/largescaleproductcorpus/wdc-products/ | Select-String -Pattern 'href=.*(example|Example)|license|terms|TRAINING'
```

The first sandbox attempt failed with curl exit 6 (DNS resolution); the same command succeeded outside the sandbox with exit 0. The command retrieves documentation only and does not enforce dataset byte limits. It must not be repurposed as the sample downloader.

Exact example targets observed in the page HTML, not fetched:

- PW: [sample_pairwise.json](https://data.dws.informatik.uni-mannheim.de/largescaleproductcorpus/data/wdc-products/sample_pairwise.json)
- MC: [sample_multi.json](https://data.dws.informatik.uni-mannheim.de/largescaleproductcorpus/data/wdc-products/sample_multi.json)

The following is the original conditional recipe. Revision 4 authorized a bounded exception to its rights gate. Acquisition and structural checks ran as recorded above; revision 5 completed the ten-pair model-assisted semantic follow-up. The recipe requires only Python's standard library and an arbitrary user-selected work directory; no personal notes are required inputs. The successful acquisition script is reproduced below; its boundary/failure paths have not been tested.

1. Recheck S1 and the applicable permission statement. Verify the two exact targets still correspond to Example (PW)/(MC). Record permission URL, scope, date and source version. Stop if unresolved.
2. Save into the selected work directory with exclusive creation; preserve original bytes. Use a bounded streaming HTTP reader with a 30-second request timeout and an overall transfer deadline. Reject redirects outside publisher hosting before following them; rejecting all redirects is also acceptable. Reject authentication/access restrictions, archives, unexpected content encodings and non-success responses. Do not fetch corpus/category examples or archives.
3. Enforce a maximum of 1,048,576 response-body bytes per request and 2,097,152 combined, counting failed attempts too. Do not rely on Content-Length. At the cap, accept only if response completion can be established without consuming more bytes; otherwise stop as indeterminate/oversize. Do not retry beyond the combined allowance. Bound decoded data to 5,242,880 bytes combined. If decoding/decompression would exceed it, stop. A file extension is not evidence of format.
4. Require a complete JSON document or complete JSON-lines records according to the actual representation; reject truncated or unexpected representations. Record UTC acquisition timestamp, exact/final URL, response metadata, received and decoded byte counts, format, completeness and SHA-256 for every acquired payload, including rejected partial payloads kept for diagnosis. Never publish raw values while redistribution remains unresolved.
5. Count available rows offline, then inspect the first at most 50 PW and 50 MC rows in original order. Record the inspected/available counts and truncation. Preserve raw values; enumerate observed keys/types and label domains. Count absent keys, nulls and empty values separately. Compare repeated IDs using their full offer payloads; repeated offers across pairs are expected unless payloads conflict. Reconcile PW/MC overlap before any combined unique count.
6. Examine at most 10 cases for variant evidence, ambiguity and label conflict; record file hash plus row/side/ID locators and only permitted evidence. Separate AI-assisted judgments from original labels. Repeat parsing/counting from saved bytes offline and reconcile results. Apply the split restrictions above. Return for review; do not promote a tiny example to representative data.

## Validation and proposed F1 input contract

F0 validation: required repository inputs were read; the working tree was initially clean at `1a4292e`; Python 3.12.4 was observed. Documentation links, consistency, public-content boundary and Git diff/status were checked as recorded in the active plan. Payload checks are explicitly not run in the table above. No application test result is claimed.

Proposed inputs, not a frozen schema or acquisition authorization:

| Input concern | Required evidence for subsequent work |
| --- | --- |
| Rights/provenance | Applicable terms, source/version and exact URL, acquisition time, hashes, byte counts and transformation history |
| Raw records | Stable source offer ID, original attributes/values and missingness; supplier/source provenance when available, explicitly unavailable otherwise |
| Supervision | Original pair/class labels and cluster IDs stored separately from review judgment, rationale, reviewer type and provenance |
| Grouping | Evidence that groups represent exact variants; unresolved identity conflicts retained, no silent label correction |
| Evaluation | Original split membership, schema-inspected identity exclusion list, proposed reference selection and absent-product construction for later review |
| Category | Observed category evidence and sufficient permitted diagnostic coverage; no selected category yet |
| Acquisition envelope | Both examples were already acquired under the owner's bounded unresolved-rights exception (2 MiB transfer / 5 MiB decoded limits). The ten-pair chat review adds no acquisition permission. Any larger diagnostic acquisition requires an explicitly sized proposal and approval; none is authorized here. |

**One next action:** prepare the documentation-only source comparison specified in the remaining-pair analysis above. The authorized 40-pair extension is complete; no category passed the discovery threshold. No new acquisition or F1 execution is authorized.

## Executed acquisition script

Save the following as `acquire_examples.py` and run `py -3.12 acquire_examples.py <new-output-directory>` only with equivalent authorization. Python 3.12 standard library only; no personal notes required. This is the script used for the successful acquisition. Preserve output metadata alongside bytes. It is a one-run tool, not a retrying downloader; failed transfers count against the total allowance across any manually approved retries.

```python
import hashlib, json, sys, time, urllib.request
from datetime import datetime, timezone
from pathlib import Path

class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        raise RuntimeError("Redirect rejected")

out = Path(sys.argv[1])
out.mkdir(parents=True, exist_ok=True)
limit = 1048576
total = 0
opener = urllib.request.build_opener(NoRedirect())
for name in ("sample_pairwise.json", "sample_multi.json"):
    url = "https://data.dws.informatik.uni-mannheim.de/largescaleproductcorpus/data/wdc-products/" + name
    body = bytearray()
    meta = {"url": url, "started_utc": datetime.now(timezone.utc).isoformat()}
    target = out / name
    if target.exists():
        raise RuntimeError("Refusing overwrite")
    try:
        deadline = time.monotonic() + 60
        req = urllib.request.Request(url, headers={"Accept-Encoding": "identity"})
        with opener.open(req, timeout=10) as response:
            meta.update(status=response.status, final_url=response.url,
                        content_type=response.headers.get("Content-Type"),
                        content_length=response.headers.get("Content-Length"),
                        content_encoding=response.headers.get("Content-Encoding"))
            if response.status != 200 or response.headers.get("Content-Encoding", "identity") != "identity":
                raise RuntimeError("Unexpected status/encoding")
            if response.headers.get("Content-Length") and int(response.headers["Content-Length"]) > limit:
                raise RuntimeError("Declared size exceeds cap")
            while True:
                if time.monotonic() >= deadline:
                    raise RuntimeError("Transfer deadline")
                remaining = min(limit - len(body), 2 * limit - total)
                if remaining == 0:
                    if response.length == 0 or response.isclosed():
                        break
                    raise RuntimeError("Cap reached without established completion")
                chunk = response.read1(min(16384, remaining))
                if not chunk:
                    if response.length not in (None, 0):
                        raise RuntimeError("Incomplete response")
                    break
                body.extend(chunk)
                total += len(chunk)
        if body[:2] in (b"PK", b"\x1f\x8b"):
            raise RuntimeError("Archive/compression rejected")
        text = body.decode("utf-8")
        if len(text.encode("utf-8")) > 5242880:
            raise RuntimeError("Decoded cap exceeded")
        try:
            parsed = json.loads(text)
            meta["format"] = "JSON"
        except json.JSONDecodeError:
            parsed = [json.loads(line) for line in text.splitlines() if line.strip()]
            meta["format"] = "JSONL"
        meta["complete"] = True
    except Exception as exc:
        meta.update(complete=False, error=type(exc).__name__ + ": " + str(exc))
    finally:
        if body:
            with target.open("xb") as f:
                f.write(body)
        meta.update(bytes=len(body), sha256=hashlib.sha256(body).hexdigest() if body else None,
                    finished_utc=datetime.now(timezone.utc).isoformat())
        with (out / (name + ".metadata.json")).open("x", encoding="utf-8") as f:
            json.dump(meta, f, indent=2)
        print(json.dumps(meta))
    if not meta["complete"]:
        sys.exit(1)
```
