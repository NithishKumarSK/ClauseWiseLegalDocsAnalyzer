# from fastapi import APIRouter
# from pydantic import BaseModel
# from backend.services.granite_llm import get_granite_service
# import re
# import logging
# from datetime import datetime

# logger = logging.getLogger(__name__)

# router = APIRouter()

# class EntityRequest(BaseModel):
#     text: str

# @router.post("/")
# def extract_entities(request: EntityRequest):
#     """
#     ClauseWise Named Entity Recognition using IBM Granite
#     Extracts parties, dates, monetary values, obligations, and legal terms from legal documents
#     """
#     try:
#         # Get Granite service
#         granite = get_granite_service()
        
#         # Use Granite AI for advanced entity extraction
#         ai_entities = granite.extract_entities_with_ai(request.text)
        
#         # Also use rule-based extraction as backup/enhancement
#         rule_entities = extract_entities_rule_based(request.text)
        
#         # Combine AI and rule-based results
#         combined_entities = merge_entity_results(ai_entities, rule_entities)
        
#         return {"entities": combined_entities}
        
#     except Exception as e:
#         logger.error(f"Error in entity extraction: {e}")
#         # Fallback to rule-based only if AI fails
#         rule_entities = extract_entities_rule_based(request.text)
#         return {"entities": rule_entities}

# def extract_entities_rule_based(text: str) -> dict:
#     """Rule-based entity extraction as backup"""
#     entities = {
#         "parties": extract_parties(text),
#         "dates": extract_dates(text),
#         "monetary_values": extract_monetary_values(text),
#         "obligations": extract_obligations(text),
#         "legal_terms": extract_legal_terms(text)
#     }
#     return entities

# def merge_entity_results(ai_entities: dict, rule_entities: dict) -> dict:
#     """Merge AI and rule-based entity extraction results"""
#     merged = {}
    
#     for category in ["parties", "dates", "monetary_values", "obligations", "legal_terms"]:
#         ai_items = ai_entities.get(category, [])
#         rule_items = rule_entities.get(category, [])
        
#         # Combine and deduplicate
#         combined = list(set(ai_items + rule_items))
#         # Remove empty items
#         combined = [item for item in combined if item and item.strip()]
        
#         merged[category] = combined[:10]  # Limit to top 10 items per category
    
#     return merged

# def extract_parties(text: str) -> list[str]:
#     """Extract party names and organizations"""
#     party_patterns = [
#         r'\b[A-Z][a-z]+ [A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b',  # Person names
#         r'\b[A-Z][A-Z\s&]+(?:LLC|Inc|Corp|Company|Ltd|LP|LLP)\b',  # Company names
#         r'(?:Company|Corporation|LLC|Inc|Ltd|LP|LLP)(?:\s+[A-Z][a-z]+)*',  # Company entities
#         r'(?:Party|Parties|Client|Contractor|Employee|Employer|Lessor|Lessee)(?:\s+[A-Z][a-z]+)*'  # Legal party terms
#     ]
    
#     parties = []
#     for pattern in party_patterns:
#         matches = re.findall(pattern, text, re.IGNORECASE)
#         parties.extend(matches)
    
#     # Remove duplicates and clean
#     return list(set([p.strip() for p in parties if len(p.strip()) > 3]))[:5]

# def extract_dates(text: str) -> list[str]:
#     """Extract dates and time periods"""
#     date_patterns = [
#         r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b',  # MM/DD/YYYY or MM-DD-YYYY
#         r'\b\d{4}[/-]\d{1,2}[/-]\d{1,2}\b',  # YYYY/MM/DD or YYYY-MM-DD
#         r'\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}\b',  # Month DD, YYYY
#         r'\b\d{1,2}\s+(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4}\b',  # DD Month YYYY
#         r'\b(?:within|after|before|during)\s+\d+\s+(?:days|months|years)\b',  # Time periods
#     ]
    
#     dates = []
#     for pattern in date_patterns:
#         matches = re.findall(pattern, text, re.IGNORECASE)
#         dates.extend(matches)
    
#     return list(set(dates))[:5]

# def extract_monetary_values(text: str) -> list[str]:
#     """Extract monetary amounts and financial terms"""
#     monetary_patterns = [
#         r'\$[\d,]+(?:\.\d{2})?',  # $1,000.00
#         r'\b\d+(?:,\d{3})*(?:\.\d{2})?\s*dollars?\b',  # 1,000 dollars
#         r'\b(?:USD|EUR|GBP)\s*[\d,]+(?:\.\d{2})?\b',  # USD 1,000.00
#         r'\b(?:salary|wage|fee|payment|compensation|amount)\s*:?\s*\$?[\d,]+(?:\.\d{2})?\b',  # salary: $1,000
#         r'\b(?:per|each|every)\s+(?:hour|month|year|week)\s*:?\s*\$?[\d,]+(?:\.\d{2})?\b',  # per hour: $25
#     ]
    
#     amounts = []
#     for pattern in monetary_patterns:
#         matches = re.findall(pattern, text, re.IGNORECASE)
#         amounts.extend(matches)
    
#     return list(set(amounts))[:5]

# def extract_obligations(text: str) -> list[str]:
#     """Extract obligations and responsibilities"""
#     obligation_patterns = [
#         r'(?:shall|must|will|agrees? to|required to|responsible for)\s+[^.]+[.]',  # Modal verbs indicating obligations
#         r'(?:obligation|duty|responsibility|requirement)\s+[^.]+[.]',  # Direct obligation terms
#         r'(?:Party|Employee|Contractor|Company)\s+(?:shall|must|will|agrees?)\s+[^.]+[.]',  # Party-specific obligations
#     ]
    
#     obligations = []
#     for pattern in obligation_patterns:
#         matches = re.findall(pattern, text, re.IGNORECASE | re.DOTALL)
#         obligations.extend([match.strip() for match in matches])
    
#     # Clean and limit
#     cleaned_obligations = [obs for obs in obligations if len(obs) > 20 and len(obs) < 200]
#     return cleaned_obligations[:5]

# def extract_legal_terms(text: str) -> list[str]:
#     """Extract key legal terms and concepts"""
#     legal_terms = [
#         'confidentiality', 'non-disclosure', 'liability', 'indemnification', 'breach',
#         'termination', 'jurisdiction', 'governing law', 'force majeure', 'arbitration',
#         'intellectual property', 'copyright', 'trademark', 'patent', 'trade secret',
#         'warranty', 'guarantee', 'representation', 'covenant', 'consideration'
#     ]
    
#     found_terms = []
#     for term in legal_terms:
#         if re.search(r'\b' + re.escape(term) + r'\b', text, re.IGNORECASE):
#             found_terms.append(term.title())
    
#     return found_terms[:8]




from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from backend.services.granite_llm import get_granite_service
import re
import logging
import asyncio
import time
import traceback
from typing import Dict, Any, List, Optional
from functools import wraps
from datetime import datetime

# Configure enhanced logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

router = APIRouter()

class EntityRequest(BaseModel):
    text: str

class EntityResponse(BaseModel):
    entities: Dict[str, List[str]]
    success: bool = True
    processing_time: Optional[float] = None
    method_used: Optional[str] = None
    error: Optional[str] = None

# Custom exceptions
class GraniteServiceError(Exception):
    """Custom exception for Granite service issues"""
    pass

class EntityExtractionError(Exception):
    """Custom exception for entity extraction issues"""
    pass

# Error handling decorators
def handle_timeout(timeout_seconds: int = 30):
    """Decorator for handling timeouts"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                elapsed_time = time.time() - start_time
                if elapsed_time > timeout_seconds:
                    logger.warning(f"Function {func.__name__} took {elapsed_time:.2f}s (timeout: {timeout_seconds}s)")
                return result
            except Exception as e:
                elapsed_time = time.time() - start_time
                logger.error(f"Function {func.__name__} failed after {elapsed_time:.2f}s: {str(e)}")
                raise
        return wrapper
    return decorator

def retry_on_failure(max_retries: int = 2, delay: float = 1.0):
    """Decorator for retrying failed operations"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            
            for attempt in range(max_retries + 1):
                try:
                    if attempt > 0:
                        logger.info(f"Retry attempt {attempt}/{max_retries} for {func.__name__}")
                        time.sleep(delay * attempt)  # Exponential backoff
                    
                    return func(*args, **kwargs)
                
                except Exception as e:
                    last_exception = e
                    logger.warning(f"Attempt {attempt + 1} failed for {func.__name__}: {str(e)}")
                    
                    if attempt == max_retries:
                        logger.error(f"All {max_retries + 1} attempts failed for {func.__name__}")
                        break
            
            raise last_exception
        return wrapper
    return decorator

def log_performance(func):
    """Decorator for logging performance metrics"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            elapsed_time = time.time() - start_time
            logger.info(f"{func.__name__} completed successfully in {elapsed_time:.2f}s")
            return result
        except Exception as e:
            elapsed_time = time.time() - start_time
            logger.error(f"{func.__name__} failed after {elapsed_time:.2f}s: {str(e)}")
            raise
    return wrapper

@router.post("/", response_model=EntityResponse)
@handle_timeout(timeout_seconds=300)  # 5 minute timeout
@log_performance
def extract_entities(request: EntityRequest):
    """
    ClauseWise Named Entity Recognition using IBM Granite
    Extracts parties, dates, monetary values, obligations, and legal terms from legal documents
    """
    start_time = time.time()
    method_used = "unknown"
    
    try:
        # Validate input
        if not request.text or not request.text.strip():
            raise HTTPException(
                status_code=400, 
                detail="Text content is required and cannot be empty"
            )
        
        if len(request.text) > 100000:  # 100KB limit
            raise HTTPException(
                status_code=413, 
                detail="Text content is too large. Maximum 100KB allowed"
            )
        
        logger.info(f"Starting entity extraction for text of length: {len(request.text)}")
        
        # Try AI-powered extraction first
        ai_entities = None
        granite_error = None
        
        try:
            ai_entities = extract_with_granite_ai(request.text)
            method_used = "ai_primary"
            logger.info("Successfully extracted entities using Granite AI")
        except Exception as e:
            granite_error = str(e)
            logger.warning(f"Granite AI extraction failed: {granite_error}")
        
        # Always use rule-based extraction as backup/enhancement
        try:
            rule_entities = extract_entities_rule_based(request.text)
            logger.info("Successfully extracted entities using rule-based method")
        except Exception as e:
            logger.error(f"Rule-based extraction failed: {str(e)}")
            raise EntityExtractionError(f"Both AI and rule-based extraction failed: {str(e)}")
        
        # Combine results if both methods worked
        if ai_entities:
            combined_entities = merge_entity_results(ai_entities, rule_entities)
            method_used = "ai_and_rules"
        else:
            combined_entities = rule_entities
            method_used = "rules_only"
        
        processing_time = time.time() - start_time
        
        logger.info(f"Entity extraction completed successfully in {processing_time:.2f}s using {method_used}")
        
        return EntityResponse(
            entities=combined_entities,
            success=True,
            processing_time=round(processing_time, 2),
            method_used=method_used
        )
        
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    
    except EntityExtractionError as e:
        logger.error(f"Entity extraction error: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": "extraction_failed",
                "message": str(e),
                "entities": {},
                "processing_time": round(time.time() - start_time, 2)
            }
        )
    
    except Exception as e:
        logger.error(f"Unexpected error in entity extraction: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        
        # Try to provide fallback response
        try:
            rule_entities = extract_entities_rule_based(request.text)
            processing_time = time.time() - start_time
            
            return EntityResponse(
                entities=rule_entities,
                success=True,
                processing_time=round(processing_time, 2),
                method_used="rules_fallback",
                error=f"AI extraction failed: {str(e)}"
            )
        except:
            # Complete failure
            return JSONResponse(
                status_code=500,
                content={
                    "success": False,
                    "error": "complete_failure",
                    "message": "All extraction methods failed",
                    "entities": {},
                    "processing_time": round(time.time() - start_time, 2)
                }
            )

@retry_on_failure(max_retries=2, delay=1.0)
@handle_timeout(timeout_seconds=180)  # 3 minute timeout for AI
def extract_with_granite_ai(text: str) -> dict:
    """Extract entities using Granite AI with error handling"""
    try:
        # Get Granite service with error handling
        granite = get_granite_service()
        if granite is None:
            raise GraniteServiceError("Granite service is not available")
        
        # Use Granite AI for advanced entity extraction
        ai_entities = granite.extract_entities_with_ai(text)
        
        if not ai_entities:
            raise GraniteServiceError("Granite AI returned empty results")
        
        return ai_entities
        
    except AttributeError as e:
        raise GraniteServiceError(f"Granite service method not available: {str(e)}")
    except Exception as e:
        raise GraniteServiceError(f"Granite AI extraction failed: {str(e)}")

@handle_timeout(timeout_seconds=30)
def extract_entities_rule_based(text: str) -> dict:
    """Rule-based entity extraction as backup with enhanced error handling"""
    try:
        if not text or not text.strip():
            return {
                "parties": [],
                "dates": [],
                "monetary_values": [],
                "obligations": [],
                "legal_terms": []
            }
        
        entities = {
            "parties": extract_parties(text),
            "dates": extract_dates(text),
            "monetary_values": extract_monetary_values(text),
            "obligations": extract_obligations(text),
            "legal_terms": extract_legal_terms(text)
        }
        
        # Validate extraction results
        for category, items in entities.items():
            if not isinstance(items, list):
                logger.warning(f"Invalid result type for {category}: {type(items)}")
                entities[category] = []
        
        return entities
        
    except Exception as e:
        logger.error(f"Rule-based extraction failed: {str(e)}")
        # Return empty structure on failure
        return {
            "parties": [],
            "dates": [],
            "monetary_values": [],
            "obligations": [],
            "legal_terms": []
        }

def merge_entity_results(ai_entities: dict, rule_entities: dict) -> dict:
    """Merge AI and rule-based entity extraction results with error handling"""
    try:
        merged = {}
        
        for category in ["parties", "dates", "monetary_values", "obligations", "legal_terms"]:
            ai_items = ai_entities.get(category, []) if ai_entities else []
            rule_items = rule_entities.get(category, []) if rule_entities else []
            
            # Ensure items are lists
            if not isinstance(ai_items, list):
                ai_items = []
            if not isinstance(rule_items, list):
                rule_items = []
            
            # Combine and deduplicate
            combined = []
            seen = set()
            
            # Add AI items first (higher priority)
            for item in ai_items:
                if item and item.strip() and item.lower() not in seen:
                    combined.append(item)
                    seen.add(item.lower())
            
            # Add rule-based items
            for item in rule_items:
                if item and item.strip() and item.lower() not in seen:
                    combined.append(item)
                    seen.add(item.lower())
            
            # Limit to top 10 items per category
            merged[category] = combined[:10]
        
        return merged
        
    except Exception as e:
        logger.error(f"Error merging entity results: {str(e)}")
        # Return rule-based results as fallback
        return rule_entities if rule_entities else {}

def extract_parties(text: str) -> list[str]:
    """Extract party names and organizations with enhanced error handling"""
    try:
        party_patterns = [
            r'\b[A-Z][a-z]+ [A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b',  # Person names
            r'\b[A-Z][A-Z\s&]+(?:LLC|Inc|Corp|Company|Ltd|LP|LLP)\b',  # Company names
            r'(?:Company|Corporation|LLC|Inc|Ltd|LP|LLP)(?:\s+[A-Z][a-z]+)*',  # Company entities
            r'(?:Party|Parties|Client|Contractor|Employee|Employer|Lessor|Lessee)(?:\s+[A-Z][a-z]+)*'  # Legal party terms
        ]
        
        parties = []
        for pattern in party_patterns:
            try:
                matches = re.findall(pattern, text, re.IGNORECASE)
                parties.extend(matches)
            except re.error as e:
                logger.warning(f"Regex error in party extraction: {str(e)}")
                continue
        
        # Remove duplicates and clean
        cleaned_parties = []
        seen = set()
        for p in parties:
            if p and len(p.strip()) > 3:
                clean_party = p.strip()
                if clean_party.lower() not in seen:
                    cleaned_parties.append(clean_party)
                    seen.add(clean_party.lower())
        
        return cleaned_parties[:5]
        
    except Exception as e:
        logger.error(f"Error extracting parties: {str(e)}")
        return []

def extract_dates(text: str) -> list[str]:
    """Extract dates and time periods with enhanced error handling"""
    try:
        date_patterns = [
            r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b',  # MM/DD/YYYY or MM-DD-YYYY
            r'\b\d{4}[/-]\d{1,2}[/-]\d{1,2}\b',  # YYYY/MM/DD or YYYY-MM-DD
            r'\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}\b',  # Month DD, YYYY
            r'\b\d{1,2}\s+(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4}\b',  # DD Month YYYY
            r'\b(?:within|after|before|during)\s+\d+\s+(?:days|months|years)\b',  # Time periods
        ]
        
        dates = []
        for pattern in date_patterns:
            try:
                matches = re.findall(pattern, text, re.IGNORECASE)
                dates.extend(matches)
            except re.error as e:
                logger.warning(f"Regex error in date extraction: {str(e)}")
                continue
        
        return list(set(dates))[:5]
        
    except Exception as e:
        logger.error(f"Error extracting dates: {str(e)}")
        return []

def extract_monetary_values(text: str) -> list[str]:
    """Extract monetary amounts and financial terms with enhanced error handling"""
    try:
        monetary_patterns = [
            r'\$[\d,]+(?:\.\d{2})?',  # $1,000.00
            r'\b\d+(?:,\d{3})*(?:\.\d{2})?\s*dollars?\b',  # 1,000 dollars
            r'\b(?:USD|EUR|GBP)\s*[\d,]+(?:\.\d{2})?\b',  # USD 1,000.00
            r'\b(?:salary|wage|fee|payment|compensation|amount)\s*:?\s*\$?[\d,]+(?:\.\d{2})?\b',  # salary: $1,000
            r'\b(?:per|each|every)\s+(?:hour|month|year|week)\s*:?\s*\$?[\d,]+(?:\.\d{2})?\b',  # per hour: $25
        ]
        
        amounts = []
        for pattern in monetary_patterns:
            try:
                matches = re.findall(pattern, text, re.IGNORECASE)
                amounts.extend(matches)
            except re.error as e:
                logger.warning(f"Regex error in monetary extraction: {str(e)}")
                continue
        
        return list(set(amounts))[:5]
        
    except Exception as e:
        logger.error(f"Error extracting monetary values: {str(e)}")
        return []

def extract_obligations(text: str) -> list[str]:
    """Extract obligations and responsibilities with enhanced error handling"""
    try:
        obligation_patterns = [
            r'(?:shall|must|will|agrees? to|required to|responsible for)\s+[^.]+[.]',  # Modal verbs indicating obligations
            r'(?:obligation|duty|responsibility|requirement)\s+[^.]+[.]',  # Direct obligation terms
            r'(?:Party|Employee|Contractor|Company)\s+(?:shall|must|will|agrees?)\s+[^.]+[.]',  # Party-specific obligations
        ]
        
        obligations = []
        for pattern in obligation_patterns:
            try:
                matches = re.findall(pattern, text, re.IGNORECASE | re.DOTALL)
                obligations.extend([match.strip() for match in matches])
            except re.error as e:
                logger.warning(f"Regex error in obligation extraction: {str(e)}")
                continue
        
        # Clean and limit
        cleaned_obligations = []
        for obs in obligations:
            if obs and 20 <= len(obs) <= 200:
                cleaned_obligations.append(obs)
        
        return cleaned_obligations[:5]
        
    except Exception as e:
        logger.error(f"Error extracting obligations: {str(e)}")
        return []

def extract_legal_terms(text: str) -> list[str]:
    """Extract key legal terms and concepts with enhanced error handling"""
    try:
        legal_terms = [
            'confidentiality', 'non-disclosure', 'liability', 'indemnification', 'breach',
            'termination', 'jurisdiction', 'governing law', 'force majeure', 'arbitration',
            'intellectual property', 'copyright', 'trademark', 'patent', 'trade secret',
            'warranty', 'guarantee', 'representation', 'covenant', 'consideration'
        ]
        
        found_terms = []
        for term in legal_terms:
            try:
                if re.search(r'\b' + re.escape(term) + r'\b', text, re.IGNORECASE):
                    found_terms.append(term.title())
            except re.error as e:
                logger.warning(f"Regex error searching for term '{term}': {str(e)}")
                continue
        
        return found_terms[:8]
        
    except Exception as e:
        logger.error(f"Error extracting legal terms: {str(e)}")
        return []

# Health check endpoint for monitoring
@router.get("/health")
def health_check():
    """Health check endpoint for the entity extraction service"""
    try:
        # Test rule-based extraction
        test_text = "This is a test contract between John Doe and ABC Company Inc."
        test_result = extract_entities_rule_based(test_text)
        
        # Test Granite service availability
        granite_available = False
        try:
            granite = get_granite_service()
            granite_available = granite is not None
        except Exception:
            pass
        
        return {
            "status": "healthy",
            "rule_based_extraction": "working",
            "granite_ai_available": granite_available,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return JSONResponse(
            status_code=503,
            content={
                "status": "unhealthy",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
        )