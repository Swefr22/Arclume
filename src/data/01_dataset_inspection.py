from pathlib import Path
from collections import Counter

# Project root
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Dataset location
DATA_DIR = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "opus-100-corpus"
    / "v1.0"
    / "supervised"
    / "en-es"
)

# Training files
english_file = DATA_DIR / "opus.en-es-train.en"
spanish_file = DATA_DIR / "opus.en-es-train.es"

# Read the files
with open(english_file, "r", encoding="utf-8") as f:
    english_sentences = f.readlines()

with open(spanish_file, "r", encoding="utf-8") as f:
    spanish_sentences = f.readlines()

print("English sentences:", len(english_sentences))
print("Spanish sentences:", len(spanish_sentences))

# Check whether the number of sentences matches
if len(english_sentences) != len(spanish_sentences):
    raise ValueError("English and Spanish files have different numbers of sentences.")

print("Sentence counts match!")

# Display the first 5 sentence pairs
for i in range(5):
    print(f"\nPair {i + 1}")
    print("English :", english_sentences[i].strip())
    print("Spanish :", spanish_sentences[i].strip())

# Dev files
dev_english_file = DATA_DIR / "opus.en-es-dev.en"
dev_spanish_file = DATA_DIR / "opus.en-es-dev.es"

# Test files
test_english_file = DATA_DIR / "opus.en-es-test.en"
test_spanish_file = DATA_DIR / "opus.en-es-test.es"

# Read dev files
with open(dev_english_file, "r", encoding="utf-8") as f:
    dev_english_sentences = f.readlines()

with open(dev_spanish_file, "r", encoding="utf-8") as f:
    dev_spanish_sentences = f.readlines()

# Read test files
with open(test_english_file, "r", encoding="utf-8") as f:
    test_english_sentences = f.readlines()

with open(test_spanish_file, "r", encoding="utf-8") as f:
    test_spanish_sentences = f.readlines()

print("\n--- Dataset Split Sizes ---")
print("Train:", len(english_sentences))
print("Dev  :", len(dev_english_sentences))
print("Test :", len(test_english_sentences))

# Check for empty sentences
def count_empty(sentences):
    return sum(1 for sentence in sentences if not sentence.strip())


print("\n--- Empty Sentence Check ---")

print("Train English empty :", count_empty(english_sentences))
print("Train Spanish empty :", count_empty(spanish_sentences))

print("Dev English empty   :", count_empty(dev_english_sentences))
print("Dev Spanish empty   :", count_empty(dev_spanish_sentences))

print("Test English empty  :", count_empty(test_english_sentences))
print("Test Spanish empty  :", count_empty(test_spanish_sentences))

# Check duplicate English-Spanish sentence pairs
def count_duplicate_pairs(english, spanish):
    pairs = set()
    duplicates = 0

    for en, es in zip(english, spanish):
        pair = (en.strip(), es.strip())

        if pair in pairs:
            duplicates += 1
        else:
            pairs.add(pair)

    return duplicates


print("\n--- Duplicate Pair Check ---")

train_duplicates = count_duplicate_pairs(
    english_sentences,
    spanish_sentences
)

dev_duplicates = count_duplicate_pairs(
    dev_english_sentences,
    dev_spanish_sentences
)

test_duplicates = count_duplicate_pairs(
    test_english_sentences,
    test_spanish_sentences
)

print("Train duplicate pairs:", train_duplicates)
print("Dev duplicate pairs  :", dev_duplicates)
print("Test duplicate pairs :", test_duplicates)

# Find the most frequent training pairs
train_pairs = [
    (en.strip(), es.strip())
    for en, es in zip(english_sentences, spanish_sentences)
]

pair_counts = Counter(train_pairs)

print("\n--- Most Frequent Training Pairs ---")

for pair, count in pair_counts.most_common(10):
    print(f"\nCount: {count}")
    print("English :", pair[0])
    print("Spanish :", pair[1])

def word_lengths(sentences):
    return [len(sentence.strip().split()) for sentence in sentences]
# Calculate sentence lengths
train_english_lengths = word_lengths(english_sentences)
train_spanish_lengths = word_lengths(spanish_sentences)

print("\n--- Training Sentence Lengths ---")

print(
    "English - Average:",
    sum(train_english_lengths) / len(train_english_lengths)
)

print(
    "Spanish - Average:",
    sum(train_spanish_lengths) / len(train_spanish_lengths)
)

print(
    "English - Maximum:",
    max(train_english_lengths)
)

print(
    "Spanish - Maximum:",
    max(train_spanish_lengths)
)

# Find the longest training sentences
longest_english_indices = sorted(
    range(len(train_english_lengths)),
    key=lambda i: train_english_lengths[i],
    reverse=True
)[:5]

longest_spanish_indices = sorted(
    range(len(train_spanish_lengths)),
    key=lambda i: train_spanish_lengths[i],
    reverse=True
)[:5]


print("\n--- Longest English Sentences ---")

for i in longest_english_indices:
    print(f"\nLength: {train_english_lengths[i]} words")
    print(english_sentences[i].strip()[:1000])


print("\n--- Longest Spanish Sentences ---")

for i in longest_spanish_indices:
    print(f"\nLength: {train_spanish_lengths[i]} words")
    print(spanish_sentences[i].strip()[:1000])

# Check how many sentences exceed different lengths
thresholds = [20, 50, 100, 200, 500, 1000]

print("\n--- Sentence Length Distribution ---")

for threshold in thresholds:
    english_count = sum(
        length > threshold for length in train_english_lengths
    )

    spanish_count = sum(
        length > threshold for length in train_spanish_lengths
    )

    print(
        f">{threshold} words | "
        f"English: {english_count} | "
        f"Spanish: {spanish_count}"
    )

# Check alignment between English and Spanish sentence lengths

print("\n--- Sentence Length Ratio Analysis ---")

length_ratios = []

for en_len, es_len in zip(train_english_lengths, train_spanish_lengths):
    if es_len > 0:
        ratio = en_len / es_len
        length_ratios.append(ratio)

print("Average English/Spanish length ratio:",
      sum(length_ratios) / len(length_ratios))

print("Maximum length ratio:",
      max(length_ratios))

print("Minimum length ratio:",
      min(length_ratios))

# Find sentence pairs with unusually large length differences

suspicious_pairs = []

for i, (en_len, es_len) in enumerate(
    zip(train_english_lengths, train_spanish_lengths)
):
    if en_len == 0 or es_len == 0:
        continue

    ratio = en_len / es_len

    if ratio > 5 or ratio < 0.2:
        suspicious_pairs.append((i, en_len, es_len, ratio))

print("\n--- Suspicious Length Ratios ---")
print("Number of suspicious pairs:", len(suspicious_pairs))

for i, en_len, es_len, ratio in suspicious_pairs[:10]:
    print(f"\nPair index: {i}")
    print("English length:", en_len)
    print("Spanish length:", es_len)
    print("Ratio:", ratio)
    print("English:", english_sentences[i].strip()[:500])
    print("Spanish:", spanish_sentences[i].strip()[:500])

print("\n--- Suspicious Pairs by Length ---")

categories = {
    "Both <= 20 words": 0,
    "One side > 20 words": 0,
    "One side > 50 words": 0,
    "One side > 100 words": 0,
}

for i, (en_len, es_len) in enumerate(
    zip(train_english_lengths, train_spanish_lengths)
):
    if en_len == 0 or es_len == 0:
        continue

    ratio = en_len / es_len

    if ratio > 5 or ratio < 0.2:

        if en_len <= 20 and es_len <= 20:
            categories["Both <= 20 words"] += 1

        if en_len > 20 or es_len > 20:
            categories["One side > 20 words"] += 1

        if en_len > 50 or es_len > 50:
            categories["One side > 50 words"] += 1

        if en_len > 100 or es_len > 100:
            categories["One side > 100 words"] += 1

for category, count in categories.items():
    print(f"{category}: {count}")

print("\n--- Most Extreme Length Ratios ---")

extreme_pairs = []

for i, (en_len, es_len) in enumerate(
    zip(train_english_lengths, train_spanish_lengths)
):
    if en_len == 0 or es_len == 0:
        continue

    ratio = en_len / es_len

    extreme_pairs.append((ratio, i, en_len, es_len))

# Sort by ratio
extreme_pairs.sort()

print("\nSmallest ratios:")

for ratio, i, en_len, es_len in extreme_pairs[:5]:
    print(f"\nPair index: {i}")
    print("English length:", en_len)
    print("Spanish length:", es_len)
    print("Ratio:", ratio)
    print("English:", english_sentences[i].strip()[:500])
    print("Spanish:", spanish_sentences[i].strip()[:500])

print("\nLargest ratios:")

for ratio, i, en_len, es_len in extreme_pairs[-5:]:
    print(f"\nPair index: {i}")
    print("English length:", en_len)
    print("Spanish length:", es_len)
    print("Ratio:", ratio)
    print("English:", english_sentences[i].strip()[:500])
    print("Spanish:", spanish_sentences[i].strip()[:500])

print("\n--- Proposed Cleaning Impact ---")

total_pairs = len(english_sentences)

removed_long = 0
removed_ratio = 0
kept_pairs = 0

for en_len, es_len in zip(
    train_english_lengths,
    train_spanish_lengths
):
    # Rule 1: extreme length
    if en_len > 100 or es_len > 100:
        removed_long += 1
        continue

    # Rule 2: extreme ratio
    ratio = en_len / es_len

    if ratio > 5 or ratio < 0.2:
        removed_ratio += 1
        continue

    kept_pairs += 1

print("Total training pairs:", total_pairs)
print("Removed by length:", removed_long)
print("Removed by ratio:", removed_ratio)
print("Remaining pairs:", kept_pairs)

print(
    "Percentage remaining:",
    (kept_pairs / total_pairs) * 100
)

print(
    "Percentage removed:",
    ((total_pairs - kept_pairs) / total_pairs) * 100
)