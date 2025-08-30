# from fastapi import APIRouter
# from pydantic import BaseModel
# from backend.services.granite_llm import get_granite_service
# import re
# import logging

# logger = logging.getLogger(__name__)

# router = APIRouter()

# class ClassifyRequest(BaseModel):
#     text: str

# @router.post("/")
# def classify_document(request: ClassifyRequest):
#     """
#     ClauseWise Document Type Classification using IBM Granite
#     Accurately classifies uploaded legal documents into categories like NDA, lease, employment contract, or service agreement.
#     """
#     try:
#         # Get Granite service
#         granite = get_granite_service()
        
#         # Use Granite AI for document classification
#         ai_classification = granite.classify_document_with_ai(request.text)
        
#         # Also use rule-based classification as backup/enhancement
#         rule_classification = classify_document_rule_based(request.text)
        
#         # Combine AI and rule-based results
#         final_classification = merge_classification_results(ai_classification, rule_classification)
        
#         return {"classification": final_classification}
        
#     except Exception as e:
#         logger.error(f"Error in document classification: {e}")
#         # Fallback to rule-based only if AI fails
#         rule_classification = classify_document_rule_based(request.text)
#         return {"classification": rule_classification}

# def classify_document_rule_based(text: str) -> dict:
#     """Rule-based document classification as backup"""
#     text_lower = text.lower()
    
#     # Document classification patterns
#     document_types = {
#         "Non-Disclosure Agreement (NDA)": {
#             "keywords": ["confidential", "non-disclosure", "proprietary", "trade secret", "confidentiality"],
#             "phrases": ["confidential information", "proprietary information", "trade secrets", "non-disclosure agreement"],
#             "description": "A legal contract that establishes confidential relationships between parties"
#         },
#         "Employment Contract": {
#             "keywords": ["employment", "employee", "employer", "salary", "wages", "benefits", "termination"],
#             "phrases": ["employment agreement", "terms of employment", "job duties", "compensation package"],
#             "description": "A contract between an employer and employee outlining terms of employment"
#         },
#         "Service Agreement": {
#             "keywords": ["services", "provider", "client", "deliverables", "scope of work", "statement of work"],
#             "phrases": ["service agreement", "professional services", "scope of services", "service provider"],
#             "description": "A contract for the provision of services between a service provider and client"
#         },
#         "Lease Agreement": {
#             "keywords": ["lease", "rent", "tenant", "landlord", "premises", "property", "rental"],
#             "phrases": ["lease agreement", "rental agreement", "leased premises", "monthly rent"],
#             "description": "A contract between a landlord and tenant for the rental of property"
#         },
#         "Purchase Agreement": {
#             "keywords": ["purchase", "sale", "buyer", "seller", "goods", "merchandise", "payment"],
#             "phrases": ["purchase agreement", "sale agreement", "purchase price", "delivery terms"],
#             "description": "A contract for the sale and purchase of goods or services"
#         },
#         "Partnership Agreement": {
#             "keywords": ["partnership", "partner", "profit", "loss", "business", "venture"],
#             "phrases": ["partnership agreement", "business partnership", "profit sharing", "joint venture"],
#             "description": "A contract establishing terms of a business partnership"
#         },
#         "License Agreement": {
#             "keywords": ["license", "licensor", "licensee", "intellectual property", "patent", "copyright"],
#             "phrases": ["license agreement", "licensing terms", "intellectual property rights", "license fee"],
#             "description": "A contract granting permission to use intellectual property or other assets"
#         }
#     }
    
#     scores = {}
    
#     # Calculate scores for each document type
#     for doc_type, patterns in document_types.items():
#         score = 0
        
#         # Check keywords
#         for keyword in patterns["keywords"]:
#             if keyword in text_lower:
#                 score += 2
        
#         # Check phrases (higher weight)
#         for phrase in patterns["phrases"]:
#             if phrase in text_lower:
#                 score += 5
        
#         scores[doc_type] = score
    
#     # Find the best match
#     if not scores or max(scores.values()) == 0:
#         return {
#             "type": "General Legal Document",
#             "confidence": 0.3,
#             "description": "Unable to classify into a specific category",
#             "key_characteristics": ["Contains legal terminology", "Formal document structure"]
#         }
    
#     best_match = max(scores, key=scores.get)
#     max_score = scores[best_match]
#     confidence = min(max_score / 15.0, 1.0)  # Normalize to 0-1 range
    
#     # Generate key characteristics
#     characteristics = []
#     doc_info = document_types[best_match]
    
#     for keyword in doc_info["keywords"]:
#         if keyword in text_lower:
#             characteristics.append(f"Contains '{keyword}' terminology")
    
#     for phrase in doc_info["phrases"]:
#         if phrase in text_lower:
#             characteristics.append(f"Includes '{phrase}' language")
    
#     return {
#         "type": best_match,
#         "confidence": confidence,
#         "description": doc_info["description"],
#         "key_characteristics": characteristics[:4]  # Limit to top 4 characteristics
#     }

# def merge_classification_results(ai_result: dict, rule_result: dict) -> dict:
#     """Merge AI and rule-based classification results"""
#     # Prefer AI result if confidence is reasonable, otherwise use rule-based
#     if ai_result.get("confidence", 0) > 0.3:
#         # Use AI result but enhance with rule-based characteristics
#         merged = ai_result.copy()
#         rule_chars = rule_result.get("key_characteristics", [])
#         ai_chars = merged.get("key_characteristics", [])
        
#         # Combine characteristics without duplicates
#         all_chars = list(set(ai_chars + rule_chars))
#         merged["key_characteristics"] = all_chars[:5]
        
#         return merged
#     else:
#         # Use rule-based result as primary
#         return rule_result












from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from backend.services.granite_llm import get_granite_service
import re
import logging
import time
from datetime import datetime
from typing import Optional, Dict, List, Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

class ClassifyRequest(BaseModel):
    text: str

class ClassifyResponse(BaseModel):
    classification: Dict[str, Any]
    success: bool = True
    processing_time: Optional[float] = None
    confidence: Optional[float] = None
    method_used: Optional[str] = None
    error: Optional[str] = None

@router.post("/", response_model=ClassifyResponse)
def classify_document(request: ClassifyRequest):
    """
    ClauseWise Document Type Classification using IBM Granite
    Accurately classifies uploaded legal documents into categories like NDA, lease, employment contract, or service agreement.
    """
    start_time = time.time()
    
    try:
        # Validate input
        if not request.text or not request.text.strip():
            raise HTTPException(
                status_code=400,
                detail="Document text is required and cannot be empty"
            )
        
        if len(request.text) > 50000:  # 50KB limit
            raise HTTPException(
                status_code=413,
                detail="Document text is too large. Maximum 50KB allowed"
            )
        
        logger.info(f"Classifying document of length: {len(request.text)}")
        
        # Try AI-powered classification first
        ai_classification = None
        method_used = "unknown"
        
        try:
            # Get Granite service
            granite = get_granite_service()
            if granite is None:
                raise Exception("Granite service not available")
            
            # Use Granite AI for document classification
            ai_classification = granite.classify_document_with_ai(request.text)
            method_used = "granite_ai"
            
            logger.info("Successfully classified document using Granite AI")
            
        except Exception as granite_error:
            logger.warning(f"Granite AI classification failed: {str(granite_error)}")
        
        # Always use rule-based classification as backup/enhancement
        try:
            rule_classification = classify_document_rule_based(request.text)
            logger.info("Successfully classified document using rule-based method")
        except Exception as e:
            logger.error(f"Rule-based classification failed: {str(e)}")
            raise Exception(f"Both AI and rule-based classification failed: {str(e)}")
        
        # Combine AI and rule-based results
        if ai_classification:
            final_classification = merge_classification_results(ai_classification, rule_classification)
            method_used = "ai_and_rules"
        else:
            final_classification = rule_classification
            method_used = "rules_only"
        
        processing_time = time.time() - start_time
        confidence = final_classification.get("confidence", 0.0)
        
        logger.info(f"Document classification completed in {processing_time:.2f}s using {method_used}")
        
        return ClassifyResponse(
            classification=final_classification,
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
        
        logger.error(f"Error in document classification: {str(e)}")
        
        # Try to provide fallback classification
        try:
            fallback_classification = classify_document_rule_based(request.text)
            return ClassifyResponse(
                classification=fallback_classification,
                success=True,
                processing_time=round(processing_time, 2),
                confidence=fallback_classification.get("confidence", 0.0),
                method_used="rules_fallback",
                error=f"AI classification failed: {str(e)}"
            )
        except:
            # Complete failure
            return ClassifyResponse(
                classification={
                    "type": "Unknown Document Type",
                    "confidence": 0.0,
                    "description": "Unable to classify document",
                    "key_characteristics": ["Classification failed"]
                },
                success=False,
                processing_time=round(processing_time, 2),
                method_used="error",
                error=str(e)
            )

def classify_document_rule_based(text: str) -> dict:
    """Rule-based document classification as backup"""
    text_lower = text.lower()
    
    # Document classification patterns
    document_types = {
        "Non-Disclosure Agreement (NDA)": {
            "keywords": ["confidential", "non-disclosure", "proprietary", "trade secret", "confidentiality"],
            "phrases": ["confidential information", "proprietary information", "trade secrets", "non-disclosure agreement"],
            "description": "A legal contract that establishes confidential relationships between parties"
        },
        "Employment Contract": {
            "keywords": ["employment", "employee", "employer", "salary", "wages", "benefits", "termination"],
            "phrases": ["employment agreement", "terms of employment", "job duties", "compensation package"],
            "description": "A contract between an employer and employee outlining terms of employment"
        },
        "Service Agreement": {
            "keywords": ["services", "provider", "client", "deliverables", "scope of work", "statement of work"],
            "phrases": ["service agreement", "professional services", "scope of services", "service provider"],
            "description": "A contract for the provision of services between a service provider and client"
        },
        "Lease Agreement": {
            "keywords": ["lease", "rent", "tenant", "landlord", "premises", "property", "rental"],
            "phrases": ["lease agreement", "rental agreement", "leased premises", "monthly rent"],
            "description": "A contract between a landlord and tenant for the rental of property"
        },
        "Purchase Agreement": {
            "keywords": ["purchase", "sale", "buyer", "seller", "goods", "merchandise", "payment"],
            "phrases": ["purchase agreement", "sale agreement", "purchase price", "delivery terms"],
            "description": "A contract for the sale and purchase of goods or services"
        },
        "Partnership Agreement": {
            "keywords": ["partnership", "partner", "profit", "loss", "business", "venture"],
            "phrases": ["partnership agreement", "business partnership", "profit sharing", "joint venture"],
            "description": "A contract establishing terms of a business partnership"
        },
        "License Agreement": {
            "keywords": ["license", "licensor", "licensee", "intellectual property", "patent", "copyright"],
            "phrases": ["license agreement", "licensing terms", "intellectual property rights", "license fee"],
            "description": "A contract granting permission to use intellectual property or other assets"
        },
        "Terms of Service": {
            "keywords": ["terms", "service", "user", "website", "platform", "account"],
            "phrases": ["terms of service", "user agreement", "terms and conditions", "acceptable use"],
            "description": "Agreement governing the use of a website or online service"
        },
        "Privacy Policy": {
            "keywords": ["privacy", "data", "information", "collect", "personal", "cookies"],
            "phrases": ["privacy policy", "data collection", "personal information", "data processing"],
            "description": "Document explaining how personal data is collected and used"
        }
    }
    
    scores = {}
    
    # Calculate scores for each document type
    for doc_type, patterns in document_types.items():
        score = 0
        
        # Check keywords
        for keyword in patterns["keywords"]:
            if keyword in text_lower:
                score += 2
        
        # Check phrases (higher weight)
        for phrase in patterns["phrases"]:
            if phrase in text_lower:
                score += 5
        
        scores[doc_type] = score
    
    # Find the best match
    if not scores or max(scores.values()) == 0:
        return {
            "type": "General Legal Document",
            "confidence": 0.3,
            "description": "Unable to classify into a specific category",
            "key_characteristics": ["Contains legal terminology", "Formal document structure"],
            "category": "Legal Document",
            "complexity": "Unknown",
            "jurisdiction": "Unknown"
        }
    
    best_match = max(scores, key=scores.get)
    max_score = scores[best_match]
    confidence = min(max_score / 15.0, 1.0)  # Normalize to 0-1 range
    
    # Generate key characteristics
    characteristics = []
    doc_info = document_types[best_match]
    
    for keyword in doc_info["keywords"]:
        if keyword in text_lower:
            characteristics.append(f"Contains '{keyword}' terminology")
    
    for phrase in doc_info["phrases"]:
        if phrase in text_lower:
            characteristics.append(f"Includes '{phrase}' language")
    
    # Determine complexity based on document length and structure
    word_count = len(text.split())
    if word_count > 2000:
        complexity = "High"
    elif word_count > 800:
        complexity = "Medium"
    else:
        complexity = "Low"
    
    # Try to determine jurisdiction
    jurisdiction = "Unknown"
    jurisdiction_patterns = {
        "United States": ["united states", "usa", "u.s.", "american", "federal", "state of"],
        "United Kingdom": ["united kingdom", "uk", "england", "british", "wales", "scotland"],
        "Canada": ["canada", "canadian", "province of"],
        "Australia": ["australia", "australian"]
    }
    
    for country, patterns in jurisdiction_patterns.items():
        if any(pattern in text_lower for pattern in patterns):
            jurisdiction = country
            break
    
    # Determine category
    category_mapping = {
        "Non-Disclosure Agreement (NDA)": "Confidentiality",
        "Employment Contract": "Employment", 
        "Service Agreement": "Commercial",
        "Lease Agreement": "Real Estate",
        "Purchase Agreement": "Commercial",
        "Partnership Agreement": "Business",
        "License Agreement": "Intellectual Property",
        "Terms of Service": "Digital/Online",
        "Privacy Policy": "Data Protection"
    }
    
    category = category_mapping.get(best_match, "Legal Document")
    
    return {
        "type": best_match,
        "confidence": round(confidence, 2),
        "description": doc_info["description"],
        "key_characteristics": characteristics[:4],  # Limit to top 4 characteristics
        "category": category,
        "complexity": complexity,
        "jurisdiction": jurisdiction,
        "word_count": word_count,
        "analysis_method": "rule_based"
    }

def merge_classification_results(ai_result: dict, rule_result: dict) -> dict:
    """Merge AI and rule-based classification results"""
    try:
        # Prefer AI result if confidence is reasonable, otherwise use rule-based
        if ai_result.get("confidence", 0) > 0.4:
            # Use AI result but enhance with rule-based characteristics
            merged = ai_result.copy()
            rule_chars = rule_result.get("key_characteristics", [])
            ai_chars = merged.get("key_characteristics", [])
            
            # Combine characteristics without duplicates
            all_chars = []
            seen_chars = set()
            
            # Add AI characteristics first
            for char in ai_chars:
                if char.lower() not in seen_chars:
                    all_chars.append(char)
                    seen_chars.add(char.lower())
            
            # Add rule-based characteristics
            for char in rule_chars:
                if char.lower() not in seen_chars:
                    all_chars.append(char)
                    seen_chars.add(char.lower())
            
            merged["key_characteristics"] = all_chars[:5]
            
            # Add rule-based metadata if missing
            if "category" not in merged:
                merged["category"] = rule_result.get("category", "Legal Document")
            if "complexity" not in merged:
                merged["complexity"] = rule_result.get("complexity", "Unknown")
            if "jurisdiction" not in merged:
                merged["jurisdiction"] = rule_result.get("jurisdiction", "Unknown")
            
            merged["analysis_method"] = "ai_enhanced"
            
            return merged
        else:
            # Use rule-based result as primary
            rule_result["analysis_method"] = "rule_based_primary"
            return rule_result
            
    except Exception as e:
        logger.error(f"Error merging classification results: {str(e)}")
        # Return rule-based result as fallback
        rule_result["analysis_method"] = "rule_based_fallback"
        return rule_result

@router.get("/health")
def classify_service_health():
    """Health check for classification service"""
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
        
        # Test rule-based classification
        test_text = "This is a test employment agreement between Company Inc and John Doe."
        test_result = classify_document_rule_based(test_text)
        rule_based_working = test_result.get("type") == "Employment Contract"
        
        return {
            "status": "healthy",
            "service": "classify",
            "granite_ai_available": granite_available,
            "rule_based_working": rule_based_working,
            "supported_types": [
                "NDA", "Employment Contract", "Service Agreement", 
                "Lease Agreement", "Purchase Agreement", "Partnership Agreement",
                "License Agreement", "Terms of Service", "Privacy Policy"
            ],
            "granite_error": granite_error,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return JSONResponse(
            status_code=503,
            content={
                "status": "unhealthy",
                "service": "classify",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
        )