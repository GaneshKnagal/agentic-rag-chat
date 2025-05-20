import aiohttp
import os
import datetime
from pathlib import Path

DATA_DIR = Path("data/raw")
DATA_DIR.mkdir(parents=True, exist_ok=True)

async def download_federal_data():
    today = datetime.date.today().isoformat()
    url = (
        "https://www.federalregister.gov/api/v1/documents.json"
        "?per_page=100&order=newest&conditions[publication_date][gte]=2025-01-01"
    )
    save_path = DATA_DIR / f"{today}.json"

    print(f"🌐 Fetching data from URL:\n{url}")

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            print(f"📶 Response status: {response.status}")
            if response.status != 200:
                print("❌ Failed to fetch data.")
                return

            data = await response.json()
            print(f"📄 Total documents received: {len(data.get('results', []))}")

            with open(save_path, "w", encoding="utf-8") as f:
                import json
                json.dump(data, f, indent=2)

            print(f"✅ Downloaded and saved raw data to: {save_path}")
