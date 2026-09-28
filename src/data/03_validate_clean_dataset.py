from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

PROCESSED_DIR = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "en-es"
)

english_file = PROCESSED_DIR / "train.en"
spanish_file = PROCESSED_DIR / "train.es"


# Load cleaned files
with open(english_file, "r", encoding="utf-8") as f:
    english_sentences = f.readlines()

with open(spanish_file, "r", encoding="utf-8") as f:
    spanish_sentences = f.readlines()


print("\n--- Cleaned Dataset Validation ---")

# 1. Check pair counts
print("English pairs:", len(english_sentences))
print("Spanish pairs:", len(spanish_sentences))

if len(english_sentences) != len(spanish_sentences):
    raise ValueError("Alignment error: sentence counts do not match.")

print("✓ Sentence counts match")


# 2. Check empty sentences
empty_english = sum(
    1 for sentence in english_sentences
    if not sentence.strip()
)

empty_spanish = sum(
    1 for sentence in spanish_sentences
    if not sentence.strip()
)

print("Empty English:", empty_english)
print("Empty Spanish:", empty_spanish)


# 3. Check maximum length
english_lengths = [
    len(sentence.strip().split())
    for sentence in english_sentences
]

spanish_lengths = [
    len(sentence.strip().split())
    for sentence in spanish_sentences
]

print("Maximum English length:", max(english_lengths))
print("Maximum Spanish length:", max(spanish_lengths))


# 4. Check extreme ratios
extreme_ratios = 0

for en_len, es_len in zip(
    english_lengths,
    spanish_lengths
):
    ratio = en_len / es_len

    if ratio > 5 or ratio < 0.2:
        extreme_ratios += 1

print("Extreme length-ratio pairs:", extreme_ratios)


# 5. Display sample pairs
print("\n--- Sample Cleaned Pairs ---")

for i in range(5):
    print(f"\nPair {i + 1}")
    print("English:", english_sentences[i].strip())
    print("Spanish:", spanish_sentences[i].strip())


print("\n✓ Cleaned dataset validation completed.")