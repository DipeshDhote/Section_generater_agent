
from app.services.mongo_service import ConfigDocumentService


service = ConfigDocumentService()

with open("data/constitutions/02_Constitution_File.md", "r", encoding="utf-8") as file:
    constitution = file.read()

with open("data/constitutions/03_Specification_File.md", "r", encoding="utf-8") as file:
    specification = file.read()

inserted_id = service.upload_config_document(
    document_type="company_profile",
    global_constitution=constitution,
    specification=specification,
    created_by="Dipesh"
)

print("Config uploaded:", inserted_id)

config = service.get_constitution_and_specification("company_profile")

print(config["global_constitution"][:500])
print(config["specification"][:500])