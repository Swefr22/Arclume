from pathlib import Path

# --------------------------------------------------
# 1. Project paths
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_DIR = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "opus-100-corpus"
    / "v1.0"
    / "supervised"
    / "en-es"
)

PROCESSED_DIR = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "en-es"
)

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


# --------------------------------------------------
# 2. Load training data
# --------------------------------------------------

english_file = RAW_DIR / "opus.en-es-train.en"
spanish_file = RAW_DIR / "opus.en-es-train.es"

with open(english_file, "r", encoding="utf-8") as f:
    english_sentences = f.readlines()

with open(spanish_file, "r", encoding="utf-8") as f:
    spanish_sentences = f.readlines()


# --------------------------------------------------
# 3. Cleaning rules
# --------------------------------------------------

MAX_WORDS = 100
MAX_RATIO = 5
MIN_RATIO = 0.2

clean_pairs = []

removed_empty = 0
removed_length = 0
removed_ratio = 0


# --------------------------------------------------
# 4. Apply cleaning
# --------------------------------------------------

for en, es in zip(english_sentences, spanish_sentences):

    en = en.strip()
    es = es.strip()

    # Rule 1: remove empty pairs
    if not en or not es:
        removed_empty += 1
        continue

    en_length = len(en.split())
    es_length = len(es.split())

    # Rule 2: remove extremely long pairs
    if en_length > MAX_WORDS or es_length > MAX_WORDS:
        removed_length += 1
        continue

    # Rule 3: remove extreme length-ratio mismatches
    ratio = en_length / es_length

    if ratio > MAX_RATIO or ratio < MIN_RATIO:
        removed_ratio += 1
        continue

    clean_pairs.append((en, es))


# --------------------------------------------------
# 5. Save cleaned corpus
# --------------------------------------------------

clean_english_file = PROCESSED_DIR / "train.en"
clean_spanish_file = PROCESSED_DIR / "train.es"

with open(clean_english_file, "w", encoding="utf-8") as f:
    for en, _ in clean_pairs:
        f.write(en + "\n")

with open(clean_spanish_file, "w", encoding="utf-8") as f:
    for _, es in clean_pairs:
        f.write(es + "\n")


# --------------------------------------------------
# 6. Print cleaning report
# --------------------------------------------------

original_count = len(english_sentences)
clean_count = len(clean_pairs)

removed_total = original_count - clean_count

print("\n--- Arclume Cleaning Report ---")

print("Original pairs :", original_count)
print("Empty removed  :", removed_empty)
print("Length removed :", removed_length)
print("Ratio removed  :", removed_ratio)
print("Total removed  :", removed_total)
print("Remaining pairs:", clean_count)

print(
    "Percentage remaining:",
    round((clean_count / original_count) * 100, 4)
)

print(
    "Percentage removed:",
    round((removed_total / original_count) * 100, 4)
)

print("\nSaved cleaned files:")
print(clean_english_file)
print(clean_spanish_file)