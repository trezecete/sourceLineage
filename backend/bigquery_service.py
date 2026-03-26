from google.cloud import bigquery_datatransfer
from google.oauth2 import service_account
from typing import List, Dict, Any
import json

class BigQueryDataTransferService:
    def __init__(self, service_account_info: Dict[str, Any]):
        self.credentials = service_account.Credentials.from_service_account_info(service_account_info)
        self.client = bigquery_datatransfer.DataTransferServiceClient(credentials=self.credentials)
        self.project_id = service_account_info.get("project_id")

    def list_scheduled_queries(self, location: str = "us") -> List[Dict[str, Any]]:
        """
        Lists all scheduled queries in the given project and location.
        """
        parent = f"projects/{self.project_id}/locations/{location}"
        configs = self.client.list_transfer_configs(parent=parent)
        
        scheduled_queries = []
        for config in configs:
            # Check if it's a scheduled query (standard SQL query)
            # DataSourceId for scheduled queries is usually 'scheduled_query'
            if config.data_source_id == "scheduled_query":
                params = config.params
                query = params.get("query")
                dest_dataset = params.get("destination_dataset_id")
                
                scheduled_queries.append({
                    "name": config.display_name,
                    "id": config.name,
                    "query": query,
                    "destination_dataset": dest_dataset,
                    "schedule": config.schedule,
                    "disabled": config.disabled
                })
        
        return scheduled_queries

    def get_project_id(self) -> str:
        return self.project_id
