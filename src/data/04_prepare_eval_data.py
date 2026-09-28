from pathlib import Path

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


# --------------------------------------------------
# Copy dev and test files
# --------------------------------------------------

splits = ["dev", "test"]

for split in splits:

    english_input = RAW_DIR / f"opus.en-es-{split}.en"
    spanish_input = RAW_DIR / f"opus.en-es-{split}.es"

    english_output = PROCESSED_DIR / f"{split}.en"
    spanish_output = PROCESSED_DIR / f"{split}.es"

    with open(english_input, "r", encoding="utf-8") as f:
        english_sentences = f.readlines()

    with open(spanish_input, "r", encoding="utf-8") as f:
        spanish_sentences = f.readlines()

    # Verify alignment
    if len(english_sentences) != len(spanish_sentences):
        raise ValueError(
            f"{split}: English and Spanish counts do not match."
        )

    # Save unchanged
    with open(english_output, "w", encoding="utf-8") as f:
        f.writelines(english_sentences)

    with open(spanish_output, "w", encoding="utf-8") as f:
        f.writelines(spanish_sentences)

    print(
        f"{split.capitalize()} set prepared:",
        len(english_sentences),
        "pairs"
    )

print("\n✓ Dev and test sets prepared.")