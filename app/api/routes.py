from pathlib import Path

from fastapi import APIRouter, HTTPException, logger
from app.api.schemas import SectionGenerateRequest, SectionGenerateResponse
from app.services.section_generator_service import SectionGeneratorService
from app.services.mongo_service import ConfigDocumentService

import json
import time
import socket
import threading
import traceback
from uuid import uuid4
from pathlib import Path
from datetime import datetime, timezone
from fastapi import HTTPException
 


router = APIRouter()

section_service = SectionGeneratorService()

service = ConfigDocumentService()



# @router.post("/generate-sections",response_model=SectionGenerateResponse)
# def generate_sections(request: SectionGenerateRequest):

#     try:

#         # -----------------------------------
#         # Read Constitution File
#         # -----------------------------------
#         constitution_text = Path(
#             "data/constitutions/02_Constitution_File.md"
#         ).read_text(encoding="utf-8")

#         # -----------------------------------
#         # Read Specification File
#         # -----------------------------------
#         specification_text = Path(
#             "data/constitutions/03_Specification_File.md"
#         ).read_text(encoding="utf-8")


#         # -----------------------------------
#         # Run Workflow
#         # -----------------------------------
#         result = section_service.generate_sections(
#             CompanyId=request.CompanyId,
#             user_id=request.user_id,
#             user_name=request.user_name,

#             global_constitution=constitution_text,
#             specification=specification_text,

#             max_retries=request.max_retries
#         )

#         return {
#             "status": "success",
#             "company_id": request.CompanyId,
#             "total_sections": len(
#                 result.get("generated_sections", [])
#             ),
#             "generated_sections": result.get(
#                 "generated_sections",
#                 []
#             ),
#             "error": None
#         }

#     except Exception as e:

#         raise HTTPException(
#             status_code=500,
#             detail=str(e)
#         )
    
# Initialize Custom Logging
LOGGER_API = "https://vibeappop.saa.ai/EnterpriseLogging/api/Logs"

def safe_logger(**kwargs):
    try:
        return logger(**kwargs)
    except Exception as exc:
        print(f"\nLogger API failed: {exc}")
        return None

@router.post("/generate-sections",response_model=SectionGenerateResponse)
def generate_sections(request: SectionGenerateRequest):
    start_time = time.time()
    session_id = str(uuid4())
    correlation_id = str(uuid4())
    request_id = str(uuid4())
    log_id = str(uuid4())
    try:
        # -----------------------------------
        # Request Received Log
        # -----------------------------------
        safe_logger(
            api_url=LOGGER_API,
            logId=log_id,
            timestampUtc=datetime.now(timezone.utc).isoformat(),
            logLevel=2,
            message="Generate sections request received",
            eventType="GenerateSectionsStarted",
            sourceApplication="Section-Generator-AI",
            sourceModule="API.Routes",
            environment="Development",
            userId=str(request.user_id),
            sessionId=session_id,
            correlationId=correlation_id,
            requestId=request_id,
            machineName=socket.gethostname(),
            threadId=str(threading.get_ident()),
            exceptionMessage=None,
            stackTrace=None,
            metadata={
                "endpoint": "/generate-sections",
                "company_id": request.CompanyId
            },
            durationMs=0,
            isSuccess=True,
            payloadJson=json.dumps({
                "company_id": request.CompanyId,
                "user_name": request.user_name
            })
        )
        # -----------------------------------
        # Read Constitution File
        # -----------------------------------
        constitution_text = Path(
            "data/constitutions/02_Constitution_File.md"
        ).read_text(encoding="utf-8")
        # -----------------------------------
        # Read Specification File
        # -----------------------------------
        specification_text = Path(
            "data/constitutions/03_Specification_File.md"
        ).read_text(encoding="utf-8")
        # -----------------------------------
        # Run Workflow
        # -----------------------------------
        result = section_service.generate_sections(
            CompanyId=request.CompanyId,
            user_id=request.user_id,
            user_name=request.user_name,
            global_constitution=constitution_text,
            specification=specification_text,
            max_retries=request.max_retries
        )
        duration_ms = int(
            (time.time() - start_time) * 1000
        )
        # -----------------------------------
        # Success Log
        # -----------------------------------
        safe_logger(
            api_url=LOGGER_API,
            logId=log_id,
            timestampUtc=datetime.now(
                timezone.utc
            ).isoformat(),
            logLevel=2,
            message="Sections generated successfully",
            eventType="GenerateSectionsCompleted",
            sourceApplication="Section-Generator-AI",
            sourceModule="API.Routes",
            environment="Development",
            userId=str(request.user_id),
            sessionId=session_id,
            correlationId=correlation_id,
            requestId=request_id,
            machineName=socket.gethostname(),
            threadId=str(threading.get_ident()),
            exceptionMessage=None,
            stackTrace=None,
            metadata={
                "endpoint": "/generate-sections",
                "company_id": request.CompanyId,
                "total_sections": len(
                    result.get("generated_sections", [])
                )
            },
            durationMs=duration_ms,
            isSuccess=True,
            payloadJson=json.dumps(result)
        )
        return {
            "status": "success",
            "company_id": request.CompanyId,
            "total_sections": len(
                result.get("generated_sections", [])
            ),
            "generated_sections": result.get(
                "generated_sections",
                []
            ),
            "error": None
        }
    except Exception as e:
        duration_ms = int(
            (time.time() - start_time) * 1000)
        # -----------------------------------
        # Error Log
        # -----------------------------------
        safe_logger(
            api_url=LOGGER_API,
            logId=log_id,
            timestampUtc=datetime.now(timezone.utc).isoformat(),
            logLevel=4,
            message="Generate sections failed",
            eventType="GenerateSectionsError",
            sourceApplication="Section-Generator-AI",
            sourceModule="API.Routes",
            environment="Development",
            userId=str(request.user_id),
            sessionId=session_id,
            correlationId=correlation_id,
            requestId=request_id,
            machineName=socket.gethostname(),
            threadId=str(threading.get_ident()),
            exceptionMessage=str(e),
            stackTrace=traceback.format_exc(),
            metadata={
                "endpoint": "/generate-sections",
                "company_id": request.CompanyId
            },
            durationMs=duration_ms,
            isSuccess=False,
            payloadJson=json.dumps({
                "company_id": request.CompanyId,
                "user_name": request.user_name
            })
        )
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
 