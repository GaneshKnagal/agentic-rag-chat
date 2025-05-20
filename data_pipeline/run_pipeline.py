import asyncio
from data_pipeline.downloader import download_federal_data
from data_pipeline.processor import process_raw_data
from db.insert_documents import insert_documents



if __name__ == "__main__":
    asyncio.run(download_federal_data())
    process_raw_data()
    asyncio.run(insert_documents())


