import pandas as pd
from typing import Optional, List, Dict, Any
import os
import logging
from pymongo import MongoClient
from tqdm import tqdm
from datetime import datetime

class MongoDBBatchDownloader:
    """Class for batch downloading RSS articles from a MongoDB collection"""

    def __init__(self, mongo_url: str, db_name: str, collection_name: str):
        self.logger = logging.getLogger(__name__)
        self.mongo_url = mongo_url
        self.db_name = db_name
        self.collection_name = collection_name
        self.client = MongoClient(self.mongo_url)
        self.collection = self.client[self.db_name][self.collection_name]
        self.logger.info(f"Initialized MongoDBBatchDownloader for collection: {self.collection_name}")

    def download_to_file(self, 
                        output_path: str,
                        file_format: str = 'csv',
                        start_date: Optional[str] = None,
                        end_date: Optional[str] = None) -> str:
        """
        Download articles from MongoDB to a consolidated file
        Args:
            output_path: Path to save the output file.
            file_format: Format to save the file ('csv' or 'json').
            start_date: Optional start date filter (YYYY-MM-DD, expects 'unixTime' field in article).
            end_date: Optional end date filter (YYYY-MM-DD).
        Returns:
            Path to the saved file.
        """
        self.logger.info(f"Starting batch download to {output_path}")
        query = {}
        if start_date or end_date:
            date_query = {}
            if start_date:
                start_ts = int(datetime.strptime(start_date, '%Y-%m-%d').timestamp())
                date_query['$gte'] = start_ts
            if end_date:
                end_ts = int(datetime.strptime(end_date, '%Y-%m-%d').timestamp())
                date_query['$lte'] = end_ts
            query['unixTime'] = date_query
        articles = list(self.collection.find(query))
        self.logger.info(f"Found {len(articles)} articles to process")
        print(f"Found {len(articles)} articles to process")
        # Remove MongoDB _id field for export
        for article in articles:
            article.pop('_id', None)
        # Save to file
        df = pd.DataFrame(articles)
        if file_format == 'csv':
            df.to_csv(output_path, index=False)
        elif file_format == 'json':
            df.to_json(output_path, orient='records', lines=True)
        else:
            raise ValueError(f"Unsupported file format: {file_format}")
        self.logger.info(f"Successfully downloaded {len(articles)} articles to {output_path}")
        return output_path
