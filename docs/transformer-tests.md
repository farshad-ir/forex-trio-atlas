# Transformer Round-Trip Tests

This document records the validation of the Trio and Variant numbering
and transformation system implemented in `src/transformer.py`.

## Test File

```text
tests/test_round_trip.py
```

The test suite validates the complete numbering space and reverse mappings
for Trios, Weak Relations, and Variants.

## Validated Spaces

| Item                    |  Count |
| ----------------------- | -----: |
| Candle directions       |      8 |
| Strict relation classes |      4 |
| Weak relations          |     13 |
| Trios                   |    512 |
| Variants per direction  |  2,197 |
| Total Variants          | 17,576 |

## Trio Round-Trip

All 512 Trio numbers were converted to their semantic components and
converted back to their original numbers.

Result:

```text
PASS: All 512 Trio numbers round-trip correctly
```

### Trio Boundary Checks

The following boundaries were explicitly validated:

| Trio | Expected                        |
| ---- | ------------------------------- |
| 001  | BBB / Rising / Rising / Rising  |
| 002  | BBB / Rising / Rising / Falling |
| 064  | BBB / Valley / Valley / Valley  |
| 065  | BBS / Rising / Rising / Rising  |
| 128  | BBS / Valley / Valley / Valley  |
| 129  | BSB / Rising / Rising / Rising  |
| 256  | BSS / Valley / Valley / Valley  |
| 257  | SBB / Rising / Rising / Rising  |
| 512  | SSS / Valley / Valley / Valley  |

## Weak Relation Round-Trip

All 13 Weak Relations were tested in both directions:

```text
number → relation
relation → number
```

Result:

```text
PASS: All 13 weak relations round-trip correctly
```

All 13 human-readable Weak Relation names were also validated.

## Variant Round-Trip

The complete Variant space contains:

```text
8 directions × 13 body relations × 13 upper relations × 13 lower relations

= 17,576 Variants
```

All 17,576 Variant numbers were tested through the complete round-trip:

```text
number → semantic components → number
```

Result:

```text
PASS: All 17,576 Variant numbers round-trip correctly
```

All Variant relation-name mappings were also tested.

### Variant Boundary Checks

The following boundaries were explicitly validated:

| Variant | Expected           |
| ------- | ------------------ |
| 00001   | BBB / 1 / 1 / 1    |
| 02197   | BBB / 13 / 13 / 13 |
| 02198   | BBS / 1 / 1 / 1    |
| 04394   | BBS / 13 / 13 / 13 |
| 15380   | SSS / 1 / 1 / 1    |
| 17576   | SSS / 13 / 13 / 13 |

## Final Test Result

```text
======================================================================
RESULT: 27 passed, 0 failed
======================================================================
ALL TESTS PASSED
```

The complete numbering and reverse-mapping system passed all defined
round-trip and boundary validations.

## Validation Status

**Status: PASSED**

The transformer layer is validated for the complete Trio and Variant
numbering spaces.

Validation was performed using:

```bash
python3 tests/test_round_trip.py
```
