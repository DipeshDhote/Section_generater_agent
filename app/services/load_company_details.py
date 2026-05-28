from qdrant_client import QdrantClient
from qdrant_client.models import Filter, FieldCondition, MatchValue
from dotenv import load_dotenv
import os


class QdrantChunkStore:
    def __init__(
        self,
        url: str = os.getenv("MONGO_URI"),
        collection_name: str = "CPDocuments",
    ):
        self.client = QdrantClient(url=url)
        self.collection_name = collection_name

    def get_chunks_by_company_id(
        self,
        CompanyId: str,
        with_vectors: bool = False,
        limit: int = 100,
    ):
        all_chunks = []
        offset = None

        while True:
            points, offset = self.client.scroll(
                collection_name=self.collection_name,
                scroll_filter=Filter(
                    must=[
                        FieldCondition(
                            key="CompanyId",
                            match=MatchValue(value=CompanyId),
                        )
                    ]
                ),
                limit=limit,
                offset=offset,
                with_payload=True,
                with_vectors=with_vectors,
            )

            for point in points:
                all_chunks.append({
                    "point_id": point.id,
                    "payload": point.payload,
                    "vector": point.vector if with_vectors else None,
                })

            if offset is None:
                break

        return all_chunks




# # Test Class
# obj = QdrantChunkStore()

# company_id = "6a0d60f0801ca563ed46b914"

# chunks = obj.get_chunks_by_company_id(company_id)

# print("Total chunks found:", len(chunks))
# summary = ""
# for chunk in chunks:
#     print("=" * 50)
#     print("Point ID : ",chunk["point_id"])
#     print("\n")
#     if chunk["payload"]:
#         print("CompanyProfileId : ", chunk["payload"].get("CompanyProfileId"))
#         print("Title : ", chunk["payload"].get("Title"))
#         print("Context : ", chunk["payload"].get("Context"))
        
#         context = chunk["payload"].get("Context", "")

#         if context:
#             summary += context + "\n"
    
# print(summary)

