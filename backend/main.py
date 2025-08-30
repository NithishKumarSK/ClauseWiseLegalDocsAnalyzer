

# from fastapi import FastAPI
# from backend.api.routers import upload, query, simplify, classify, entities

# app = FastAPI(title="ClauseWise: Legal Document Analyzer", description="AI-powered legal document analysis using IBM Watson & Granite")

# # Add a root endpoint for testing
# @app.get("/")
# def read_root():
#     return {"message": "ClauseWise Legal Document Analyzer API is running!", "powered_by": "IBM Watson & Granite AI"}

# @app.get("/health")
# def health_check():
#     """Health check endpoint with AI model status"""
#     try:
#         from backend.services.granite_llm import get_granite_service
#         granite = get_granite_service()
        
#         return {
#             "status": "healthy",
#             "backend": "online",
#             "ai_model_loaded": granite.model_loaded if granite else False,
#             "device": granite.device if granite else "unknown"
#         }
#     except Exception as e:
#         return {
#             "status": "degraded",
#             "backend": "online",
#             "ai_model_loaded": False,
#             "error": str(e)
#         }

# app.include_router(upload.router, prefix="/upload", tags=["upload"])
# app.include_router(query.router, prefix="/query", tags=["query"])
# app.include_router(simplify.router, prefix="/simplify", tags=["simplify"])
# app.include_router(classify.router, prefix="/classify", tags=["classify"])
# app.include_router(entities.router, prefix="/entities", tags=["entities"])

# # Add new ClauseWise specific endpoints
# @app.post("/extract-clauses/")
# def extract_clauses_endpoint(request: dict):
#     """Extract and breakdown individual clauses from legal documents"""
#     from backend.core.clause_breakdown import split_into_clauses
    
#     text = request.get("text", "")
#     clauses = split_into_clauses(text)
#     return {"clauses": clauses}





# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# import os

# from backend.api.routers import upload, query, simplify, classify, entities

# app = FastAPI(
#     title="ClauseWise: Legal Document Analyzer",
#     description="AI-powered legal document analysis using IBM Watson & Granite"
# )

# # --- CORS setup (added) ---
# origins_env = os.getenv("CORS_ORIGINS", "*")
# if str(origins_env).strip() in ["", "*"]:
#     allow_origins = ["*"]
# else:
#     allow_origins = [o.strip() for o in origins_env.split(",") if o.strip()]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=allow_origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )
# # ---------------------------

# # Add a root endpoint for testing
# @app.get("/")
# def read_root():
#     return {
#         "message": "ClauseWise Legal Document Analyzer API is running!",
#         "powered_by": "IBM Watson & Granite AI"
#     }

# @app.get("/health")
# def health_check():
#     """Health check endpoint with AI model status"""
#     try:
#         from backend.services.granite_llm import get_granite_service
#         granite = get_granite_service()
        
#         return {
#             "status": "healthy",
#             "backend": "online",
#             "ai_model_loaded": granite.model_loaded if granite else False,
#             "device": getattr(granite, "device", "unknown")
#         }
#     except Exception as e:
#         return {
#             "status": "degraded",
#             "backend": "online",
#             "ai_model_loaded": False,
#             "error": str(e)
#         }

# # Routers
# app.include_router(upload.router, prefix="/upload", tags=["upload"])
# app.include_router(query.router, prefix="/query", tags=["query"])
# app.include_router(simplify.router, prefix="/simplify", tags=["simplify"])
# app.include_router(classify.router, prefix="/classify", tags=["classify"])
# app.include_router(entities.router, prefix="/entities", tags=["entities"])

# # Add new ClauseWise specific endpoints
# @app.post("/extract-clauses/")
# def extract_clauses_endpoint(request: dict):
#     """Extract and breakdown individual clauses from legal documents"""
#     from backend.core.clause_breakdown import split_into_clauses
    
#     text = request.get("text", "")
#     clauses = split_into_clauses(text)
#     return {"clauses": clauses}





from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
import sys

# Ensure the backend package can be imported when running directly
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import routers safely
try:
    from backend.api.routers import upload, query, simplify, classify, entities
except ModuleNotFoundError:
    # Fallback if run directly from project root
    import backend.api.routers.upload as upload
    import backend.api.routers.query as query
    import backend.api.routers.simplify as simplify
    import backend.api.routers.classify as classify
    import backend.api.routers.entities as entities

app = FastAPI(
    title="ClauseWise: Legal Document Analyzer",
    description="AI-powered legal document analysis using IBM Watson & Granite",
    version="1.0.0"
)

# --- CORS setup (enhanced) ---
origins_env = os.getenv("CORS_ORIGINS", "*")
if str(origins_env).strip() in ["", "*"]:
    allow_origins = ["*"]
else:
    allow_origins = [o.strip() for o in origins_env.split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add a root endpoint for testing
@app.get("/")
def read_root():
    return {
        "message": "ClauseWise Legal Document Analyzer API is running!",
        "powered_by": "IBM Watson & Granite AI",
        "version": "1.0.0",
        "endpoints": {
            "upload": "/upload/",
            "query": "/query/", 
            "simplify": "/simplify/",
            "classify": "/classify/",
            "entities": "/entities/",
            "extract_clauses": "/extract-clauses/"
        }
    }

@app.get("/health")
def health_check():
    """Enhanced health check endpoint with AI model status"""
    try:
        from backend.services.granite_llm import get_granite_service
        granite = get_granite_service()
        
        ai_status, ai_error = False, None
        try:
            if granite and hasattr(granite, 'test_connection'):
                ai_status = granite.test_connection()
            elif granite:
                ai_status = True
        except Exception as e:
            ai_error = str(e)
        
        return {
            "status": "healthy",
            "backend": "online",
            "ai_model_loaded": ai_status,
            "granite_service": "available" if granite else "unavailable",
            "device": getattr(granite, "device", "unknown"),
            "error": ai_error,
            "api_keys_configured": {
                "pinecone": bool(os.getenv("PINECONE_API_KEY")),
                "granite": bool(os.getenv("GRANITE_API_KEY")),
                "huggingface": bool(os.getenv("HUGGINGFACE_TOKEN"))
            }
        }
    except Exception as e:
        return {
            "status": "degraded",
            "backend": "online",
            "ai_model_loaded": False,
            "error": str(e),
            "api_keys_configured": {
                "pinecone": bool(os.getenv("PINECONE_API_KEY")),
                "granite": bool(os.getenv("GRANITE_API_KEY")),
                "huggingface": bool(os.getenv("HUGGINGFACE_TOKEN"))
            }
        }

# Include routers
app.include_router(upload.router, prefix="/upload", tags=["upload"])
app.include_router(query.router, prefix="/query", tags=["query"])
app.include_router(simplify.router, prefix="/simplify", tags=["simplify"])
app.include_router(classify.router, prefix="/classify", tags=["classify"])
app.include_router(entities.router, prefix="/entities", tags=["entities"])

# Add ClauseWise specific endpoints
@app.post("/extract-clauses/")
def extract_clauses_endpoint(request: dict):
    """Extract and breakdown individual clauses from legal documents"""
    try:
        from backend.core.clause_breakdown import split_into_clauses
        
        text = request.get("text", "")
        if not text:
            return {"clauses": [], "error": "No text provided"}
        
        clauses = split_into_clauses(text)
        return {"clauses": clauses, "success": True, "count": len(clauses)}
        
    except Exception as e:
        return {"clauses": [], "error": str(e), "success": False}

from pydantic import BaseModel
class TextRequest(BaseModel):
    text: str

@app.post("/extract-clauses/")
def extract_clauses_structured(request: TextRequest):
    """Extract clauses with structured request/response"""
    try:
        from backend.core.clause_breakdown import split_into_clauses
        
        if not request.text:
            return {"clauses": [], "error": "No text provided"}
        
        clauses = split_into_clauses(request.text)
        return {"clauses": clauses, "success": True, "count": len(clauses)}
        
    except Exception as e:
        return {"clauses": [], "error": str(e), "success": False}

# Startup event
@app.on_event("startup")
async def startup_event():
    """Verify environment configuration on startup"""
    print("🚀 ClauseWise Backend Starting...")
    
    api_keys = {
        "PINECONE_API_KEY": os.getenv("PINECONE_API_KEY"),
        "GRANITE_API_KEY": os.getenv("GRANITE_API_KEY"), 
        "HUGGINGFACE_TOKEN": os.getenv("HUGGINGFACE_TOKEN")
    }
    
    missing_keys = [key for key, value in api_keys.items() if not value]
    if missing_keys:
        print(f"⚠️ Warning: Missing API keys: {missing_keys}")
    else:
        print("✅ All API keys configured")
    
    try:
        from backend.services.granite_llm import get_granite_service
        granite = get_granite_service()
        if granite:
            print("✅ Granite service initialized")
        else:
            print("⚠️ Granite service initialization failed")
    except Exception as e:
        print(f"❌ Error initializing Granite service: {e}")
    
    print("🎯 ClauseWise Backend Ready!")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
