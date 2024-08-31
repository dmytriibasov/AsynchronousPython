import asyncio
from datetime import datetime

import aiofiles
import aiofiles.os
import json

from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CVERecord


class CveDataProcessor:

    BATCH_SIZE = 1000

    def __init__(self, session: AsyncSession, directory_root: str):
        self.batch_lock = asyncio.Lock()
        self.session = session
        self.directory_root = directory_root

    async def process_file(self, filepath: str):
        async with aiofiles.open(filepath, mode='r') as file:
            content = await file.read()
            data = json.loads(content)

            cna_data = data['containers']['cna']
            # Extracting data to create a CVERecord
            cve_id = data['cveMetadata']['cveId']
            title = cna_data.get('title')
            description = cna_data.get('descriptions', [])[-1].get('value') if cna_data.get('descriptions') else 'n/a'
            updated_at = datetime.strptime(data['cveMetadata']['dateUpdated'].split('.')[0], "%Y-%m-%dT%H:%M:%S")
            published_at = datetime.strptime(data['cveMetadata']['datePublished'].split('.')[0], "%Y-%m-%dT%H:%M:%S")

            return CVERecord(
                cve_id=cve_id,
                title=title,
                description=description,
                updated_at=updated_at,
                published_at=published_at,
            )


    async def insert_records_in_bulk(self, records: list):
        async with self.batch_lock:
            await self.session.execute(
                insert(CVERecord), records
            )
            await self.session.commit()


    async def process_directory(self, directory_path: str, record_batch=None):
        if record_batch is None:
            record_batch = []

        dir_iterator = await aiofiles.os.scandir(directory_path)

        for entry in dir_iterator:
            if entry.is_dir():
                await self.process_directory(entry.path, record_batch)

            elif entry.is_file():
                record = await self.process_file(entry.path)

                async with self.batch_lock:
                    record_batch.append(record)

                # If batch size is reached, insert into the database
                if len(record_batch) >= self.BATCH_SIZE:
                    await self.insert_records_in_bulk(record_batch)
                    record_batch.clear()

    async def run(self):
        record_batch = []

        await self.process_directory(self.directory_root, record_batch)

        # Insert any remaining records in the last batch
        if record_batch:
            await self.insert_records_in_bulk(record_batch)
