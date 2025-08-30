# from fastapi import APIRouter
# from pydantic import BaseModel
# from backend.services.granite_llm import get_granite_service
# import logging

# logger = logging.getLogger(__name__)

# router = APIRouter()

# class QueryReq(BaseModel):
#     question: str
#     context: str = ""

# @router.post("/")
# def query(q: QueryReq):
#     """
#     ClauseWise AI Assistant using IBM Granite
#     Answers questions about legal concepts, document analysis, or specific clauses
#     """
#     try:
#         # Get Granite service
#         granite = get_granite_service()
        
#         # Generate answer using Granite AI
#         answer = granite.answer_question(q.question, q.context)
        
#         return {"answer": answer}
        
#     except Exception as e:
#         logger.error(f"Error in document query: {e}")
#         return {"answer": f"I apologize, but I encountered an error while processing your question: {str(e)}. Please try rephrasing your question or contact support if the issue persists."}





from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from backend.services.granite_llm import get_granite_service
import logging
import time
from datetime import datetime
from typing import Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

# Request models to match frontend expectations
class QueryRequest(BaseModel):
    text: str  # Document text (context)
    question: str  # User's question

class LegacyQueryRequest(BaseModel):
    question: str
    context: str = ""

class QueryResponse(BaseModel):
    answer: str
    success: bool = True
    processing_time: Optional[float] = None
    confidence: Optional[float] = None
    method_used: Optional[str] = None
    error: Optional[str] = None

@router.post("/", response_model=QueryResponse)
def query_document(request: QueryRequest):
    """
    ClauseWise AI Assistant using IBM Granite
    Answers questions about legal documents, clauses, and legal concepts
    
    This endpoint matches the frontend expectation: /query/ with {text, question} format
    """
    start_time = time.time()
    
    try:
        # Validate input
        if not request.question or not request.question.strip():
            raise HTTPException(
                status_code=400,
                detail="Question is required and cannot be empty"
            )
        
        if not request.text or not request.text.strip():
            raise HTTPException(
                status_code=400,
                detail="Document text is required for context"
            )
        
        logger.info(f"Processing question: {request.question[:100]}...")
        logger.info(f"Document length: {len(request.text)} characters")
        
        # Try AI-powered answer generation
        answer = None
        method_used = "unknown"
        confidence = 0.0
        
        try:
            # Get Granite service
            granite = get_granite_service()
            if granite is None:
                raise Exception("Granite service not available")
            
            # Generate answer using Granite AI
            answer = granite.answer_question(request.question, request.text)
            method_used = "granite_ai"
            confidence = 0.8  # Assume high confidence for AI responses
            
            logger.info("Successfully generated answer using Granite AI")
            
        except Exception as granite_error:
            logger.warning(f"Granite AI failed: {str(granite_error)}")
            
            # Fallback to rule-based response
            try:
                answer = generate_fallback_answer(request.question, request.text)
                method_used = "rule_based_fallback"
                confidence = 0.4
                logger.info("Using rule-based fallback for answer generation")
            except Exception as fallback_error:
                logger.error(f"Fallback also failed: {str(fallback_error)}")
                raise Exception(f"Both AI and fallback methods failed: {str(fallback_error)}")
        
        processing_time = time.time() - start_time
        
        if not answer:
            answer = "I apologize, but I couldn't generate a response to your question. Please try rephrasing or providing more context."
            confidence = 0.1
        
        logger.info(f"Query completed in {processing_time:.2f}s using {method_used}")
        
        return QueryResponse(
            answer=answer,
            success=True,
            processing_time=round(processing_time, 2),
            confidence=confidence,
            method_used=method_used
        )
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
        
    except Exception as e:
        processing_time = time.time() - start_time
        error_message = f"I apologize, but I encountered an error while processing your question: {str(e)}. Please try rephrasing your question or contact support if the issue persists."
        
        logger.error(f"Error in query processing: {str(e)}")
        
        return QueryResponse(
            answer=error_message,
            success=False,
            processing_time=round(processing_time, 2),
            method_used="error_fallback",
            error=str(e)
        )

# Legacy endpoint for backward compatibility
@router.post("/legacy")
def query_legacy(request: LegacyQueryRequest):
    """Legacy query endpoint for backward compatibility"""
    # Convert to new format
    new_request = QueryRequest(
        text=request.context,
        question=request.question
    )
    
    result = query_document(new_request)
    
    # Return in legacy format
    return {"answer": result.answer}

def generate_fallback_answer(question: str, document_text: str) -> str:
    """Generate a rule-based fallback answer when AI is unavailable"""
    question_lower = question.lower()
    text_lower = document_text.lower()
    
    # Common legal document questions with rule-based responses
    if any(keyword in question_lower for keyword in ['parties', 'who', 'involved']):
        # Extract potential party names
        import re
        party_patterns = [
            r'\b[A-Z][a-z]+ [A-Z][a-z]+\b',  # Person names
            r'\b[A-Z][A-Z\s&]+(?:LLC|Inc|Corp|Company|Ltd|LP|LLP)\b'  # Company names
        ]
        
        parties = []
        for pattern in party_patterns:
            matches = re.findall(pattern, document_text)
            parties.extend(matches[:3])  # Limit to first 3 matches
        
        if parties:
            return f"Based on the document, the parties appear to include: {', '.join(set(parties[:5]))}"
        else:
            return "I found references to parties in the document, but couldn't clearly identify specific names. Please check the document for party information."
    
    elif any(keyword in question_lower for keyword in ['date', 'when', 'deadline', 'term']):
        # Look for dates
        import re
        date_patterns = [
            r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b',
            r'\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}\b'
        ]
        
        dates = []
        for pattern in date_patterns:
            matches = re.findall(pattern, document_text, re.IGNORECASE)
            dates.extend(matches)
        
        if dates:
            return f"The document mentions these dates: {', '.join(set(dates[:5]))}"
        else:
            return "I couldn't find specific dates in the document. Please review the document for date-related information."
    
    elif any(keyword in question_lower for keyword in ['money', 'amount', 'payment', 'fee', 'cost', 'price']):
        # Look for monetary amounts
        import re
        money_patterns = [
            r'\$[\d,]+(?:\.\d{2})?',
            r'\b\d+(?:,\d{3})*(?:\.\d{2})?\s*dollars?\b'
        ]
        
        amounts = []
        for pattern in money_patterns:
            matches = re.findall(pattern, document_text, re.IGNORECASE)
            amounts.extend(matches)
        
        if amounts:
            return f"The document mentions these monetary amounts: {', '.join(set(amounts[:5]))}"
        else:
            return "I couldn't find specific monetary amounts in the document. Please check for payment or fee information."
    
    elif any(keyword in question_lower for keyword in ['purpose', 'about', 'main', 'summary']):
        # Provide a basic summary based on document length and content
        word_count = len(document_text.split())
        
        if 'agreement' in text_lower:
            doc_type = 'agreement'
        elif 'contract' in text_lower:
            doc_type = 'contract'
        elif 'policy' in text_lower:
            doc_type = 'policy'
        else:
            doc_type = 'document'
        
        return f"This appears to be a legal {doc_type} with approximately {word_count} words. For a detailed analysis, I recommend reviewing the specific clauses and sections."
    
    else:
        # Generic response
        return f"I understand you're asking about: '{question}'. While I can't provide a detailed analysis without AI assistance, I recommend reviewing the relevant sections of the document or rephrasing your question to be more specific about parties, dates, amounts, or obligations."

@router.get("/health")
def query_service_health():
    """Health check for query service"""
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
        
        return {
            "status": "healthy",
            "service": "query",
            "granite_ai_available": granite_available,
            "fallback_available": True,
            "granite_error": granite_error,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return JSONResponse(
            status_code=503,
            content={
                "status": "unhealthy",
                "service": "query",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
        )