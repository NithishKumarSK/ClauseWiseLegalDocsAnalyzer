# from fastapi import APIRouter
# from pydantic import BaseModel
# from backend.services.granite_llm import get_granite_service
# from backend.core.clause_breakdown import split_into_clauses
# import logging

# logger = logging.getLogger(__name__)

# router = APIRouter()

# class SimplifyRequest(BaseModel):
#     text: str

# @router.post("/")
# def simplify(req: SimplifyRequest):
#     """
#     ClauseWise Clause Simplification using IBM Granite
#     Converts complex legal language into plain, understandable terms
#     """
#     try:
#         # Extract clauses first
#         clauses = split_into_clauses(req.text)
        
#         if not clauses:
#             return {"simplified_clauses": ["No distinct clauses found in the document."]}
        
#         # Get Granite service
#         granite = get_granite_service()
        
#         # Simplify each clause using Granite AI
#         simplified_clauses = []
#         for clause in clauses[:10]:  # Limit to first 10 clauses for performance
#             if len(clause.strip()) > 20:  # Only simplify meaningful clauses
#                 simplified = granite.simplify_clause(clause)
#                 simplified_clauses.append({
#                     "original": clause,
#                     "simplified": simplified
#                 })
        
#         return {"simplified_clauses": simplified_clauses}
        
#     except Exception as e:
#         logger.error(f"Error in clause simplification: {e}")
#         return {"simplified_clauses": [f"Error simplifying clauses: {str(e)}"]}



from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from backend.services.granite_llm import get_granite_service
from backend.core.clause_breakdown import split_into_clauses
import logging
import time
from datetime import datetime
from typing import Optional, List, Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

# Request models to match frontend expectations
class SimplifyRequest(BaseModel):
    clause: str  # Single clause to simplify (from frontend text input)

class SimplifyDocumentRequest(BaseModel):
    text: str  # Full document text for auto-simplification

class SimplifyResponse(BaseModel):
    simplified: str
    success: bool = True
    processing_time: Optional[float] = None
    method_used: Optional[str] = None
    error: Optional[str] = None
    original_length: Optional[int] = None
    simplified_length: Optional[int] = None

class SimplifyDocumentResponse(BaseModel):
    simplified_clauses: List[Dict[str, Any]]
    success: bool = True
    processing_time: Optional[float] = None
    clauses_processed: Optional[int] = None
    method_used: Optional[str] = None
    error: Optional[str] = None

@router.post("/", response_model=SimplifyResponse)
def simplify_clause(request: SimplifyRequest):
    """
    ClauseWise Clause Simplification using IBM Granite
    Converts complex legal language into plain, understandable terms
    
    This endpoint handles single clause simplification from frontend text input
    """
    start_time = time.time()
    
    try:
        # Validate input
        if not request.clause or not request.clause.strip():
            raise HTTPException(
                status_code=400,
                detail="Clause text is required and cannot be empty"
            )
        
        clause_text = request.clause.strip()
        
        if len(clause_text) < 10:
            raise HTTPException(
                status_code=400,
                detail="Clause text is too short. Please provide a more substantial clause to simplify."
            )
        
        if len(clause_text) > 5000:  # Limit to 5KB per clause
            raise HTTPException(
                status_code=413,
                detail="Clause text is too long. Maximum 5000 characters allowed."
            )
        
        logger.info(f"Simplifying clause of length: {len(clause_text)}")
        
        # Try AI-powered simplification with quick timeout
        simplified_text = None
        method_used = "unknown"
        
        try:
            # Get Granite service with timeout
            granite = get_granite_service()
            if granite is None:
                raise Exception("Granite service not available")
            
            # Simplify using Granite AI with quick processing
            simplified_text = granite.simplify_clause(clause_text[:1000])  # Limit text size for speed
            method_used = "granite_ai"
            
            logger.info("Successfully simplified clause using Granite AI")
            
        except Exception as granite_error:
            logger.warning(f"Granite AI simplification failed: {str(granite_error)}")
            
            # Fallback to rule-based simplification
            try:
                simplified_text = simplify_clause_rule_based(clause_text)
                method_used = "rule_based_fallback"
                logger.info("Using rule-based fallback for clause simplification")
            except Exception as fallback_error:
                logger.error(f"Fallback simplification failed: {str(fallback_error)}")
                # Use emergency fallback
                simplified_text = emergency_simplify(clause_text)
                method_used = "emergency_fallback"
                
        if not simplified_text:
            simplified_text = "I couldn't simplify this clause effectively. The original text may already be in plain language, or it contains highly technical terms that require legal expertise to interpret."
        
        processing_time = time.time() - start_time
        
        logger.info(f"Clause simplification completed in {processing_time:.2f}s")
        
        return SimplifyResponse(
            simplified=simplified_text,
            success=True,
            processing_time=round(processing_time, 2),
            method_used=method_used,
            original_length=len(clause_text),
            simplified_length=len(simplified_text)
        )
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
        
    except Exception as e:
        processing_time = time.time() - start_time
        error_message = f"I encountered an error while simplifying this clause: {str(e)}. Please try with a different clause or contact support if the issue persists."
        
        logger.error(f"Error in clause simplification: {str(e)}")
        
        return SimplifyResponse(
            simplified=error_message,
            success=False,
            processing_time=round(processing_time, 2),
            method_used="error_fallback",
            error=str(e),
            original_length=len(request.clause) if request.clause else 0
        )

def emergency_simplify(clause_text: str) -> str:
    """Ultra-fast emergency simplification for demo purposes"""
    word_count = len(clause_text.split())
    sentences = len([s for s in clause_text.split('.') if s.strip()])
    
    return f"This clause contains {word_count} words in {sentences} sentences. It establishes legal obligations and rights between parties. For a detailed interpretation, please consult with a legal professional."

@router.post("/document", response_model=SimplifyDocumentResponse)
def simplify_document_clauses(request: SimplifyDocumentRequest):
    """
    Simplify all clauses in a document (auto-simplification feature)
    """
    start_time = time.time()
    
    try:
        if not request.text or not request.text.strip():
            raise HTTPException(
                status_code=400,
                detail="Document text is required"
            )
        
        logger.info(f"Auto-simplifying document of length: {len(request.text)}")
        
        # Extract clauses first - with error handling
        try:
            clauses = split_into_clauses(request.text)
        except Exception as e:
            logger.error(f"Clause extraction failed: {str(e)}")
            # Create simple clauses by splitting on periods
            sentences = request.text.split('.')
            clauses = [s.strip() + '.' for s in sentences if len(s.strip()) > 50]
        
        if not clauses:
            return SimplifyDocumentResponse(
                simplified_clauses=[{
                    "clause_number": 1,
                    "original": request.text[:500] + "..." if len(request.text) > 500 else request.text,
                    "simplified": f"Document summary: This legal document contains {len(request.text.split())} words and establishes various legal obligations and rights between parties.",
                    "method": "emergency_summary"
                }],
                success=True,
                processing_time=round(time.time() - start_time, 2),
                clauses_processed=1,
                method_used="emergency_summary"
            )
        
        # Get Granite service with timeout protection
        granite = None
        try:
            granite = get_granite_service()
        except:
            pass
            
        method_used = "rule_based_fast"
        
        # Simplify each clause (limit to first 3 for speed)
        simplified_clauses = []
        clauses_to_process = clauses[:3]  # Reduced from 5 to 3 for speed
        
        for i, clause in enumerate(clauses_to_process, 1):
            clause_text = clause if isinstance(clause, str) else str(clause)
            
            # Only simplify substantial clauses
            if len(clause_text.strip()) < 50:
                continue
            
            try:
                # Use fast rule-based method by default for speed
                simplified = simplify_clause_rule_based(clause_text[:500])  # Limit size for speed
                
                simplified_clauses.append({
                    "clause_number": i,
                    "original": clause_text,
                    "simplified": simplified,
                    "original_length": len(clause_text),
                    "simplified_length": len(simplified) if simplified else 0
                })
                
            except Exception as e:
                logger.warning(f"Failed to simplify clause {i}: {str(e)}")
                simplified_clauses.append({
                    "clause_number": i,
                    "original": clause_text,
                    "simplified": emergency_simplify(clause_text),
                    "method": "emergency_fallback"
                })
        
        processing_time = time.time() - start_time
        
        logger.info(f"Document simplification completed: {len(simplified_clauses)} clauses in {processing_time:.2f}s")
        
        return SimplifyDocumentResponse(
            simplified_clauses=simplified_clauses,
            success=True,
            processing_time=round(processing_time, 2),
            clauses_processed=len(simplified_clauses),
            method_used=method_used
        )
        
    except HTTPException:
        raise
        
    except Exception as e:
        processing_time = time.time() - start_time
        
        logger.error(f"Error in document simplification: {str(e)}")
        
        return SimplifyDocumentResponse(
            simplified_clauses=[{
                "clause_number": 1,
                "original": "Error processing document",
                "simplified": f"Unable to process document due to: {str(e)}. This is a demo system for hackathon purposes.",
                "error": str(e)
            }],
            success=False,
            processing_time=round(processing_time, 2),
            clauses_processed=0,
            method_used="error_fallback",
            error=str(e)
        )

def simplify_clause_rule_based(clause_text: str) -> str:
    """Rule-based clause simplification as fallback when AI is unavailable"""
    try:
        # Basic simplification rules
        simplified = clause_text
        
        # Replace common legal terms with simpler alternatives
        replacements = {
            r'\bheretofore\b': 'before this',
            r'\bhereinafter\b': 'from now on',
            r'\bwhereas\b': 'while',
            r'\btherefore\b': 'so',
            r'\bnotwithstanding\b': 'despite',
            r'\bforthwith\b': 'immediately',
            r'\bpursuant to\b': 'according to',
            r'\bin accordance with\b': 'following',
            r'\bshall\b': 'will',
            r'\bparty of the first part\b': 'first party',
            r'\bparty of the second part\b': 'second party',
            r'\baforesaid\b': 'mentioned above',
            r'\bsubject to\b': 'depending on',
            r'\bprovided that\b': 'if',
            r'\bin the event that\b': 'if',
            r'\bfor the purpose of\b': 'to',
            r'\bwith respect to\b': 'about',
            r'\bin consideration of\b': 'because of'
        }
        
        import re
        for pattern, replacement in replacements.items():
            simplified = re.sub(pattern, replacement, simplified, flags=re.IGNORECASE)
        
        # Break down long sentences
        sentences = simplified.split('.')
        simplified_sentences = []
        
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) > 100:  # Long sentence
                # Try to break at conjunctions
                if ' and ' in sentence:
                    parts = sentence.split(' and ')
                    simplified_sentences.extend([part.strip() + '.' for part in parts if part.strip()])
                elif ' or ' in sentence:
                    parts = sentence.split(' or ')
                    simplified_sentences.extend([part.strip() + '.' for part in parts if part.strip()])
                else:
                    simplified_sentences.append(sentence + '.')
            else:
                if sentence:
                    simplified_sentences.append(sentence + '.')
        
        simplified = ' '.join(simplified_sentences)
        
        # Add explanatory note
        simplified += "\n\n[Note: This is a basic simplification for demo purposes. For legal accuracy, consult the original text or a legal professional.]"
        
        return simplified
        
    except Exception as e:
        logger.error(f"Rule-based simplification failed: {str(e)}")
        return emergency_simplify(clause_text)

# Legacy endpoint for backward compatibility
@router.post("/legacy")
def simplify_legacy(request: dict):
    """Legacy simplification endpoint"""
    text = request.get("text", "")
    
    if not text:
        return {"simplified_clauses": ["No text provided for simplification"]}
    
    # Convert to new format and process
    if len(text) > 1000:  # Assume it's a document
        doc_request = SimplifyDocumentRequest(text=text)
        result = simplify_document_clauses(doc_request)
        return {"simplified_clauses": result.simplified_clauses}
    else:  # Assume it's a single clause
        clause_request = SimplifyRequest(clause=text)
        result = simplify_clause(clause_request)
        return {"simplified_clauses": [{"simplified": result.simplified}]}

@router.get("/health")
def simplify_service_health():
    """Health check for simplification service"""
    try:
        # Test Granite service availability
        granite_available = False
        granite_error = None
        
        try:
            granite = get_granite_service()
            granite_available = granite is not None
            if granite and hasattr(granite, 'test_connection'):
                granite_available = granite.test_connection()
        except Exception as e:
            granite_error = str(e)
        
        # Test clause extraction
        clause_extraction_available = False
        try:
            from backend.core.clause_breakdown import split_into_clauses
            test_clauses = split_into_clauses("This is a test clause. This is another test clause.")
            clause_extraction_available = len(test_clauses) > 0
        except Exception:
            pass
        
        return {
            "status": "healthy",
            "service": "simplify",
            "granite_ai_available": granite_available,
            "clause_extraction_available": clause_extraction_available,
            "rule_based_fallback": True,
            "granite_error": granite_error,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return JSONResponse(
            status_code=503,
            content={
                "status": "unhealthy",
                "service": "simplify",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
        )