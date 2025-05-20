import json
import datetime
from pathlib import Path

RAW_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed")
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

def clean_record(doc):
    # Use abstract or excerpts if abstract is missing
    summary = doc.get("abstract") or doc.get("excerpts") or ""

    return {
        "document_number": doc.get("document_number"),
        "title": doc.get("title", "").strip(),
        "summary": summary.strip() if isinstance(summary, str) else "",
        "publication_date": doc.get("publication_date"),
        "agency_names": ", ".join([a.get("name", "") for a in doc.get("agencies", [])]),
        "html_url": doc.get("html_url", ""),
        "pdf_url": doc.get("pdf_url", "")
    }

def process_raw_data():
    today = datetime.date.today().isoformat()
    raw_file = RAW_DIR / f"{today}.json"
    processed_file = PROCESSED_DIR / f"{today}_processed.json"

    if not raw_file.exists():
        print(f"❌ Raw file not found: {raw_file}")
        return

    with open(raw_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    documents = data.get("results", [])
    print(f"🧹 Cleaning {len(documents)} documents...")

    cleaned = [clean_record(doc) for doc in documents]

    # Optional: print first record for inspection
    if cleaned:
        print("🔎 Sample cleaned record:")
        print(json.dumps(cleaned[0], indent=2))

    with open(processed_file, "w", encoding="utf-8") as f:
        json.dump(cleaned, f, indent=2)

    print(f"✅ Processed {len(cleaned)} records and saved to: {processed_file}")
