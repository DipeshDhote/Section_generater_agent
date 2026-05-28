import os
from typing import Optional, Dict

from dotenv import load_dotenv
from pymongo import MongoClient
from datetime import datetime, timezone
from bson import ObjectId
from typing import Optional

load_dotenv()


class ConfigDocumentService:
    def __init__(self):
        self.mongo_uri = os.getenv("MONGO_URI")
        self.db_name = os.getenv("MONGO_DB_NAME")
        self.collection_name = os.getenv("CONFIG_COLLECTION_NAME")

        if not self.mongo_uri:
            raise ValueError("MONGO_URI is missing in .env")

        if not self.db_name:
            raise ValueError("MONGO_DB_NAME is missing in .env")

        if not self.collection_name:
            raise ValueError("CONFIG_COLLECTION_NAME is missing in .env")

        self.client = MongoClient(self.mongo_uri)
        self.db = self.client[self.db_name]
        self.collection = self.db[self.collection_name]

    def upload_config_document(self,document_type: str,global_constitution: str,specification: str,created_by: str) -> str:
        # deactivate old active config
        self.collection.update_many(
            {"document_type": document_type, "is_active": True},
            {"$set": {"is_active": False}}
        )

        document = {
            "document_type": document_type,
            "global_constitution": global_constitution,
            "specification": specification,
            "created_by": created_by,
            "is_active": True
        }

        result = self.collection.insert_one(document)
        return str(result.inserted_id)

    def get_constitution_and_specification(self,document_type: str = "company_profile") -> Dict[str, Optional[str]]:

        config_doc = self.collection.find_one(
            {
                "document_type": document_type,
                "is_active": True
            },
            {
                "_id": 0,
                "global_constitution": 1,
                "specification": 1
            }
        )

        if not config_doc:
            raise ValueError(
                f"No active constitution/specification found for document_type: {document_type}"
            )

        return {
            "global_constitution": config_doc.get("global_constitution"),
            "specification": config_doc.get("specification")
        }
    

    def save_rewritten_constitution(self,CompanyId: str,constitution: str,user_prompt: str,created_by: str,modified_by: Optional[str] = None) -> str:

        now = datetime.now(timezone.utc)

        self.collection.update_many(
            {
                "document_type": "rewritten_constitution",
                "CompanyId": CompanyId,
                "is_active": True
            },
            {
                "$set": {
                    "is_active": False,
                    "modified_date": now,
                    "modified_by": modified_by or created_by
                }
            }
        )

        document = {
            "_id": ObjectId(),
            "document_type": "rewritten_constitution",
            "CompanyId": CompanyId,
            "constitution": constitution,
            "user_prompt": user_prompt,
            "is_active": True,
            "created_date": now,
            "modified_date": now,
            "created_by": created_by,
            "modified_by": modified_by or created_by,
        }

        result = self.collection.insert_one(document)

        return str(result.inserted_id)
    

