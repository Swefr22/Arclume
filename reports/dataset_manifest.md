# Arclume Dataset Manifest

## Dataset

OPUS-100 English-Spanish parallel corpus.

## Language Pair

English ↔ Spanish

## Original Dataset

| Split | Pairs |
|---|---:|
| Train | 1,000,000 |
| Dev | 2,000 |
| Test | 2,000 |

## Training Data Cleaning

The training corpus was analyzed before preprocessing.

### Cleaning rules

1. Remove empty sentence pairs.
2. Remove pairs where either language exceeds 100 whitespace-separated words.
3. Remove pairs with an English/Spanish length ratio greater than 5 or less than 0.2.

### Cleaning results

| Category | Pairs |
|---|---:|
| Original training pairs | 1,000,000 |
| Empty pairs removed | 0 |
| Length-based removals | 1,922 |
| Ratio-based removals | 3,045 |
| Total removed | 4,967 |
| Remaining training pairs | 995,033 |

### Retention

99.5033% of the original training corpus was retained.

## Processed Dataset

| Split | Pairs |
|---|---:|
| Train | 995,033 |
| Dev | 2,000 |
| Test | 2,000 |

## Important

The original OPUS-100 files in `data/raw/` are preserved unchanged.

All preprocessing outputs are stored under:

`data/processed/en-es/`