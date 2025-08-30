# from fastapi import APIRouter, UploadFile, File, HTTPException
# from backend.services.parser_service import parse_document

# router = APIRouter()

# @router.post("/")
# async def upload_document(file: UploadFile = File(...)):
#     """
#     Upload and extract text from PDF, DOCX, or TXT documents.
#     """

#     # Allowed formats
#     allowed_extensions = [".pdf", ".docx", ".txt"]
#     allowed_mime_types = [
#         "application/pdf",
#         "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
#         "text/plain",
#     ]

#     # Detect extension + mime type
#     file_extension = (
#         "." + file.filename.lower().split(".")[-1] if "." in file.filename else ""
#     )

#     if (
#         file.content_type not in allowed_mime_types
#         and file_extension not in allowed_extensions
#     ):
#         raise HTTPException(status_code=400, detail="Unsupported file type")

#     try:
#         # Read raw file content
#         content = await file.read()

#         # Use parser service to handle different formats
#         text = parse_document(file.filename, content)

#         if not text or text.strip() == "":
#             raise HTTPException(
#                 status_code=500, detail="No readable text found in the document"
#             )

#         return {
#             "filename": file.filename,
#             "size": len(content),
#             "type": file.content_type,
#             "text": text,
#         }

#     except HTTPException:
#         raise
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Parsing failed: {str(e)}")


import io
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from backend.services.parser_service import parse_document
import logging
import time
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/")
async def upload_document(file: UploadFile = File(...)):
    """
    Upload and extract text from PDF, DOCX, or TXT documents.
    Enhanced with better error handling and response formatting for ClauseWise frontend.
    """
    start_time = time.time()
    
    try:
        # Validate file
        if not file or not file.filename:
            raise HTTPException(status_code=400, detail="No file provided")
        
        # Allowed formats
        allowed_extensions = [".pdf", ".docx", ".txt", ".doc"]
        allowed_mime_types = [
            "application/pdf",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            "application/msword",
            "text/plain",
        ]

        # Detect extension + mime type
        file_extension = (
            "." + file.filename.lower().split(".")[-1] if "." in file.filename else ""
        )

        logger.info(f"Processing file: {file.filename}, type: {file.content_type}, extension: {file_extension}")

        if (
            file.content_type not in allowed_mime_types
            and file_extension not in allowed_extensions
        ):
            raise HTTPException(
                status_code=400, 
                detail=f"Unsupported file type. Allowed: {', '.join(allowed_extensions)}"
            )

        # Check file size (limit to 10MB)
        MAX_SIZE = 10 * 1024 * 1024  # 10MB
        content = await file.read()
        
        if len(content) > MAX_SIZE:
            raise HTTPException(
                status_code=413,
                detail=f"File too large. Maximum size: {MAX_SIZE // (1024*1024)}MB"
            )

        if len(content) == 0:
            raise HTTPException(status_code=400, detail="Empty file provided")

        logger.info(f"File size: {len(content)} bytes")

        # Use parser service to handle different formats
        try:
            parsed_result = parse_document(file.filename, content)
            
            # Handle different return types from parse_document
            if isinstance(parsed_result, dict):
                # If parse_document returns a dict, extract text
                text = parsed_result.get('text', '') or parsed_result.get('content', '') or str(parsed_result)
            elif isinstance(parsed_result, str):
                # If parse_document returns a string
                text = parsed_result
            else:
                # Convert to string as fallback
                text = str(parsed_result)
                
        except Exception as parse_error:
            logger.error(f"Parsing error for {file.filename}: {str(parse_error)}")
            raise HTTPException(
                status_code=500, 
                detail=f"Failed to parse document: {str(parse_error)}"
            )

        # Ensure text is a string before calling strip
        if not isinstance(text, str):
            text = str(text)

        if not text or text.strip() == "":
            raise HTTPException(
                status_code=500, 
                detail="No readable text found in the document"
            )

        # Clean up text
        cleaned_text = text.strip()
        word_count = len(cleaned_text.split())
        char_count = len(cleaned_text)
        
        processing_time = time.time() - start_time

        logger.info(f"Successfully processed {file.filename} in {processing_time:.2f}s")
        logger.info(f"Extracted {word_count} words, {char_count} characters")

        # Return response in format expected by frontend
        return {
            "success": True,
            "filename": file.filename,
            "size": len(content),
            "type": file.content_type,
            "text": cleaned_text,
            "metadata": {
                "word_count": word_count,
                "char_count": char_count,
                "processing_time": round(processing_time, 2),
                "file_extension": file_extension,
                "timestamp": datetime.now().isoformat()
            }
        }

    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        processing_time = time.time() - start_time
        logger.error(f"Unexpected error processing {file.filename if file else 'unknown'}: {str(e)}")
        
        # Return error response in consistent format
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": "upload_failed",
                "message": f"Document processing failed: {str(e)}",
                "filename": file.filename if file else "unknown",
                "processing_time": round(processing_time, 2),
                "timestamp": datetime.now().isoformat()
            }
        )

@router.get("/health")
def upload_service_health():
    """Health check for upload service"""
    try:
        from backend.services.parser_service import test_parser_availability
        parser_status = test_parser_availability() if hasattr(parse_document, 'test_parser_availability') else True
        
        return {
            "status": "healthy",
            "service": "upload",
            "parser_available": parser_status,
            "supported_formats": [".pdf", ".docx", ".txt", ".doc"],
            "max_file_size": "10MB",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return JSONResponse(
            status_code=503,
            content={
                "status": "unhealthy",
                "service": "upload", 
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
        )