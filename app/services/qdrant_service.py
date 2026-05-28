import os
from typing import List, Dict, Any

from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.models import Filter, FieldCondition, MatchValue


load_dotenv()


class QdrantService:

    def __init__(self):

        self.client = QdrantClient(url=os.getenv("QDRANT_URL"))

        self.collection_name = os.getenv("QDRANT_COLLECTION_NAME")

    def get_unique_section_names_by_company_id(self,CompanyId: str) -> List[str]:

        section_names = set()
        offset = None

        while True:

            points, offset = self.client.scroll(
                collection_name=self.collection_name,

                scroll_filter=Filter(
                    must=[
                        FieldCondition(
                            key="CompanyId",
                            match=MatchValue(value=CompanyId)
                        )
                    ]
                ),

                limit=100,
                with_payload=True,
                with_vectors=False,
                offset=offset
            )

            for point in points:

                payload = point.payload or {}

                related_section = payload.get(
                    "RelatedSection",
                    ""
                )

                if related_section:

                    sections = [
                        section.strip()
                        for section in str(
                            related_section
                        ).split(",")
                        if section.strip()
                    ]

                    section_names.update(sections)

            if offset is None:
                break

        return sorted(section_names)

    def get_chunks_by_company_id_and_section_name(self,CompanyId: str,RelatedSection: str) -> List[Dict[str, Any]]:

        chunks = []
        offset = None

        while True:

            points, offset = self.client.scroll(
                collection_name=self.collection_name,

                scroll_filter=Filter(
                    must=[
                        FieldCondition(
                            key="CompanyId",
                            match=MatchValue(value=CompanyId)
                        )
                    ]
                ),

                limit=100,
                with_payload=True,
                with_vectors=False,
                offset=offset
            )

            for point in points:

                payload = point.payload or {}  

                related_section = payload.get(
                    "RelatedSection",
                    ""
                )

                related_sections = [
                    section.strip()
                    for section in str(
                        related_section
                    ).split(",")
                    if section.strip()
                ]

                if RelatedSection in related_sections:
                    chunks.append(payload)

            if offset is None:
                break

        return chunks