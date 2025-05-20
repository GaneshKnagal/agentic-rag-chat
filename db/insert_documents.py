import aiomysql
import json
import datetime
from pathlib import Path
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

PROCESSED_DIR = Path("data/processed")

async def insert_documents():
    today = datetime.date.today().isoformat()
    file_path = PROCESSED_DIR / f"{today}_processed.json"

    if not file_path.exists():
        print(f"❌ No processed file found for today: {file_path}")
        return

    with open(file_path, "r", encoding="utf-8") as f:
        records = json.load(f)

    print(f"📦 Loaded {len(records)} records from {file_path}")

    # Connect to MySQL
    conn = await aiomysql.connect(
        host="localhost",
        port=3306,
        user="root",
        password="Ganesh55@",  
        db="rag_demo"
    )

    successful_inserts = 0
    skipped_duplicates = 0

    async with conn.cursor() as cur:
        for i, rec in enumerate(records):
            try:
                await cur.execute("""
                    INSERT IGNORE INTO federal_documents
                    (document_number, title, summary, publication_date, agency_names, html_url, pdf_url)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (
                    rec["document_number"],
                    rec["title"],
                    rec["summary"],
                    rec["publication_date"],
                    rec["agency_names"],
                    rec["html_url"],
                    rec["pdf_url"]
                ))

                if cur.rowcount == 1:
                    successful_inserts += 1
                    print(f"✅ [{i+1}] Inserted: {rec['title'][:80]}...")
                else:
                    skipped_duplicates += 1
                    print(f"⚠️ [{i+1}] Skipped duplicate: {rec['document_number']}")

            except Exception as e:
                print(f"❌ Error inserting record [{i+1}]: {e}")

        await conn.commit()
        print(f"\n✅ Summary:")
        print(f"   - Successfully inserted: {successful_inserts}")
        print(f"   - Duplicates skipped:    {skipped_duplicates}")
        print(f"   - Total processed:       {len(records)}")

    await conn.ensure_closed()
    print("🔒 MySQL connection closed.")
