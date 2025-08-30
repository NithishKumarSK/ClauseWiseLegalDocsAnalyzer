# # """
# # Granite LLM Service for ClauseWise
# # Uses IBM Granite 3.3-2B Instruct model from Hugging Face
# # """

# # import os
# # from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
# # import torch
# # from typing import List, Dict, Any
# # import re
# # import logging
# # from huggingface_hub import login

# # # Set up logging
# # logging.basicConfig(level=logging.INFO)
# # logger = logging.getLogger(__name__)

# # class GraniteLLMService:
# #     def __init__(self):
# #         # self.model_name = "ibm-granite/granite-3.3-2b-instruct"
# #         self.model_name = "ibm-ai-platform/micro-g3.3-8b-instruct-1b"
# #         self.device = "cuda" if torch.cuda.is_available() else "cpu"
# #         self.model = None
# #         self.tokenizer = None
# #         self.pipeline = None
# #         self.model_loaded = False
# #         self._setup_huggingface_auth()
# #         # Don't initialize model immediately - do it lazily
    
# #     def _setup_huggingface_auth(self):
# #         """Setup Hugging Face authentication"""
# #         try:
# #             # Try to get token from environment
# #             hf_token = os.getenv('HUGGINGFACE_TOKEN')
# #             if hf_token and hf_token != 'your_huggingface_token_here':
# #                 logger.info("Using Hugging Face token for authentication")
# #                 login(token=hf_token)
# #             else:
# #                 logger.info("No Hugging Face token provided, using public access")
# #         except Exception as e:
# #             logger.warning(f"Hugging Face authentication failed: {e}")
# #             logger.info("Continuing without authentication (public models only)")
    
# #     def _ensure_model_loaded(self):
# #         """Lazy loading of the model when first needed"""
# #         if not self.model_loaded:
# #             self._initialize_model()
    
# #     def _initialize_model(self):
# #         """Initialize the Granite model and tokenizer"""
# #         try:
# #             logger.info(f"Loading Granite model: {self.model_name}")
# #             logger.info(f"Using device: {self.device}")
            
# #             # Load tokenizer
# #             self.tokenizer = AutoTokenizer.from_pretrained(
# #                 self.model_name,
# #                 trust_remote_code=True
# #             )
            
# #             # Load model with appropriate settings
# #             self.model = AutoModelForCausalLM.from_pretrained(
# #                 self.model_name,
# #                 torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
# #                 device_map="auto" if self.device == "cuda" else None,
# #                 trust_remote_code=True,
# #                 low_cpu_mem_usage=True
# #             )
            
# #             # Create text generation pipeline
# #             self.pipeline = pipeline(
# #                 "text-generation",
# #                 model=self.model,
# #                 tokenizer=self.tokenizer,
# #                 device=0 if self.device == "cuda" else -1,
# #                 torch_dtype=torch.float16 if self.device == "cuda" else torch.float32
# #             )
            
# #             logger.info("Granite model loaded successfully!")
# #             self.model_loaded = True
            
# #         except Exception as e:
# #             logger.error(f"Error loading Granite model: {e}")
# #             self.model_loaded = False
# #             # Don't raise the error - allow graceful fallback
    
# #     def generate_response(self, prompt: str, max_length: int = 512, temperature: float = 0.7) -> str:
# #         """Generate response using Granite model"""
# #         try:
# #             self._ensure_model_loaded()
            
# #             if not self.model_loaded or not self.pipeline:
# #                 return "Model not available. Please check system requirements and try again."
            
# #             # Format prompt for Granite instruction format
# #             formatted_prompt = f"<|user|>\n{prompt}\n<|assistant|>\n"
            
# #             # Generate response with optimized parameters for speed
# #             try:
# #                 outputs = self.pipeline(
# #                     formatted_prompt,
# #                     max_new_tokens=min(max_length, 100),  # Reduce max tokens for speed
# #                     temperature=0.3,  # Lower temperature for faster, more focused responses
# #                     do_sample=True,
# #                     top_p=0.8,
# #                     repetition_penalty=1.05,
# #                     pad_token_id=self.tokenizer.eos_token_id,
# #                     num_return_sequences=1
# #                 )
                
# #                 # Extract generated text
# #                 full_response = outputs[0]['generated_text']
# #                 # Remove the prompt part and extract only the assistant's response
# #                 response = full_response.split("<|assistant|>\n")[-1].strip()
                
# #                 # If response is empty or too short, provide a basic response
# #                 if not response or len(response) < 10:
# #                     return "I understand your question. Due to current processing constraints, please try a more specific question or check back shortly."
                
# #                 return response
                
# #             except Exception as gen_error:
# #                 logger.error(f"Generation error: {gen_error}")
# #                 return "I'm experiencing some technical difficulties with text generation. Please try again with a simpler question."
            
# #         except Exception as e:
# #             logger.error(f"Error generating response: {e}")
# #             return f"I apologize, but I'm experiencing technical difficulties. Please try again later."
    
# #     def simplify_clause(self, clause_text: str) -> str:
# #         """Simplify legal clause using Granite"""
# #         try:
# #             self._ensure_model_loaded()
            
# #             if not self.model_loaded:
# #                 # Fallback to simple text processing
# #                 return f"Simplified: {clause_text[:200]}... (AI model not available)"
            
# #             prompt = f"""Please simplify the following legal clause into plain, everyday language that a non-lawyer can easily understand. Keep the essential meaning but make it clear and simple:

# # Legal Clause: {clause_text}

# # Simplified Version:"""
            
# #             return self.generate_response(prompt, max_length=300)
# #         except Exception as e:
# #             logger.error(f"Error in clause simplification: {e}")
# #             return f"Error simplifying clause: {str(e)}"
    
# #     def extract_entities_with_ai(self, text: str) -> Dict[str, List[str]]:
# #         """Extract named entities using Granite AI"""
# #         try:
# #             self._ensure_model_loaded()
            
# #             if not self.model_loaded:
# #                 # Fallback to empty entities
# #                 return {
# #                     "parties": [],
# #                     "dates": [],
# #                     "monetary_values": [],
# #                     "obligations": [],
# #                     "legal_terms": []
# #                 }
            
# #             prompt = f"""Analyze the following legal document and extract key information. Return the results in this exact format:

# # PARTIES: [list the individuals, companies, or organizations involved]
# # DATES: [list all dates mentioned]
# # MONETARY VALUES: [list all money amounts, fees, or financial terms]
# # OBLIGATIONS: [list key duties, responsibilities, or requirements]
# # LEGAL TERMS: [list important legal concepts or technical terms]

# # Document: {text[:2000]}...

# # Analysis:"""
            
# #             response = self.generate_response(prompt, max_length=400)
            
# #             # Parse the response into structured data
# #             entities = {
# #                 "parties": [],
# #                 "dates": [],
# #                 "monetary_values": [],
# #                 "obligations": [],
# #                 "legal_terms": []
# #             }
            
# #             try:
# #                 lines = response.split('\n')
# #                 current_category = None
                
# #                 for line in lines:
# #                     line = line.strip()
# #                     if line.startswith('PARTIES:'):
# #                         current_category = "parties"
# #                         # Extract items from the same line
# #                         items = line.replace('PARTIES:', '').strip()
# #                         if items and items != '[list the individuals, companies, or organizations involved]':
# #                             entities[current_category].extend([item.strip() for item in items.split(',') if item.strip()])
# #                     elif line.startswith('DATES:'):
# #                         current_category = "dates"
# #                         items = line.replace('DATES:', '').strip()
# #                         if items and items != '[list all dates mentioned]':
# #                             entities[current_category].extend([item.strip() for item in items.split(',') if item.strip()])
# #                     elif line.startswith('MONETARY VALUES:'):
# #                         current_category = "monetary_values"
# #                         items = line.replace('MONETARY VALUES:', '').strip()
# #                         if items and items != '[list all money amounts, fees, or financial terms]':
# #                             entities[current_category].extend([item.strip() for item in items.split(',') if item.strip()])
# #                     elif line.startswith('OBLIGATIONS:'):
# #                         current_category = "obligations"
# #                         items = line.replace('OBLIGATIONS:', '').strip()
# #                         if items and items != '[list key duties, responsibilities, or requirements]':
# #                             entities[current_category].extend([item.strip() for item in items.split(',') if item.strip()])
# #                     elif line.startswith('LEGAL TERMS:'):
# #                         current_category = "legal_terms"
# #                         items = line.replace('LEGAL TERMS:', '').strip()
# #                         if items and items != '[list important legal concepts or technical terms]':
# #                             entities[current_category].extend([item.strip() for item in items.split(',') if item.strip()])
# #                     elif current_category and line.startswith('-') or line.startswith('•'):
# #                         # Handle bullet points
# #                         item = line.lstrip('-•').strip()
# #                         if item:
# #                             entities[current_category].append(item)
            
# #             except Exception as e:
# #                 logger.error(f"Error parsing entities: {e}")
            
# #             return entities
            
# #         except Exception as e:
# #             logger.error(f"Error in AI entity extraction: {e}")
# #             return {
# #                 "parties": [],
# #                 "dates": [],
# #                 "monetary_values": [],
# #                 "obligations": [],
# #                 "legal_terms": []
# #             }
    
# #     def classify_document_with_ai(self, text: str) -> Dict[str, Any]:
# #         """Classify document type using Granite AI"""
# #         try:
# #             self._ensure_model_loaded()
            
# #             if not self.model_loaded:
# #                 # Fallback classification
# #                 return {
# #                     "type": "General Legal Document",
# #                     "confidence": 0.3,
# #                     "description": "AI model not available for detailed classification",
# #                     "key_characteristics": ["Document contains legal terminology"]
# #                 }
            
# #             prompt = f"""Analyze the following legal document and classify its type. Choose from these categories:
# # - Non-Disclosure Agreement (NDA)
# # - Employment Contract
# # - Service Agreement
# # - Lease Agreement
# # - Purchase Agreement
# # - Partnership Agreement
# # - License Agreement
# # - General Legal Document

# # Also provide confidence level (0.0 to 1.0) and key characteristics.

# # Document excerpt: {text[:1500]}...

# # Classification:
# # Type:
# # Confidence:
# # Description:
# # Key Characteristics:"""
        
# #             response = self.generate_response(prompt, max_length=300)
            
# #             # Parse response
# #             result = {
# #                 "type": "General Legal Document",
# #                 "confidence": 0.5,
# #                 "description": "Legal document analysis",
# #                 "key_characteristics": []
# #             }
            
# #             try:
# #                 lines = response.split('\n')
# #                 for line in lines:
# #                     line = line.strip()
# #                     if line.startswith('Type:'):
# #                         doc_type = line.replace('Type:', '').strip()
# #                         if doc_type:
# #                             result["type"] = doc_type
# #                     elif line.startswith('Confidence:'):
# #                         conf_str = line.replace('Confidence:', '').strip()
# #                         try:
# #                             # Extract numeric value
# #                             conf_match = re.search(r'(\d+\.?\d*)', conf_str)
# #                             if conf_match:
# #                                 conf_val = float(conf_match.group(1))
# #                                 if conf_val > 1.0:  # If it's a percentage
# #                                     conf_val = conf_val / 100.0
# #                                 result["confidence"] = conf_val
# #                         except:
# #                             pass
# #                     elif line.startswith('Description:'):
# #                         desc = line.replace('Description:', '').strip()
# #                         if desc:
# #                             result["description"] = desc
# #                     elif line.startswith('Key Characteristics:'):
# #                         continue
# #                     elif line.startswith('-') or line.startswith('•'):
# #                         char = line.lstrip('-•').strip()
# #                         if char:
# #                             result["key_characteristics"].append(char)
            
# #             except Exception as e:
# #                 logger.error(f"Error parsing classification: {e}")
            
# #             return result
            
# #         except Exception as e:
# #             logger.error(f"Error in AI document classification: {e}")
# #             return {
# #                 "type": "General Legal Document",
# #                 "confidence": 0.3,
# #                 "description": f"Classification error: {str(e)}",
# #                 "key_characteristics": ["Document analysis failed"]
# #             }
    
# #     def answer_question(self, question: str, context: str = "") -> str:
# #         """Answer questions about legal documents using Granite"""
# #         try:
# #             # Quick check for simple questions that can be answered without AI
# #             simple_answers = self._try_simple_answer(question, context)
# #             if simple_answers:
# #                 return simple_answers
            
# #             self._ensure_model_loaded()
            
# #             if not self.model_loaded:
# #                 return self._fallback_answer(question, context)
            
# #             prompt = f"""You are ClauseWise AI, a legal document analysis assistant. Answer the following question about legal concepts or document analysis.

# # Context: {context[:1000] if context else "General legal knowledge"}

# # Question: {question}

# # Answer:"""
            
# #             return self.generate_response(prompt, max_length=200)  # Reduced for faster response
            
# #         except Exception as e:
# #             logger.error(f"Error in AI question answering: {e}")
# #             return self._fallback_answer(question, context)
    
# #     def _try_simple_answer(self, question: str, context: str = "") -> str:
# #         """Try to answer simple questions without AI model"""
# #         question_lower = question.lower()
        
# #         # Simple question patterns
# #         if "what is" in question_lower or "define" in question_lower:
# #             if "nda" in question_lower or "non-disclosure" in question_lower:
# #                 return "An NDA (Non-Disclosure Agreement) is a legal contract that prevents parties from sharing confidential information with third parties."
# #             elif "contract" in question_lower:
# #                 return "A contract is a legally binding agreement between two or more parties that creates mutual obligations enforceable by law."
# #             elif "clause" in question_lower:
# #                 return "A clause is a specific provision or section within a legal document that addresses a particular aspect of the agreement."
        
# #         elif "how to" in question_lower:
# #             if "simplify" in question_lower:
# #                 return "To simplify legal language: 1) Replace complex terms with everyday words, 2) Break long sentences into shorter ones, 3) Use active voice, 4) Define technical terms."
        
# #         elif "summarize" in question_lower:
# #             if context:
# #                 # Simple context-based summary
# #                 sentences = context.split('.')[:3]  # First 3 sentences
# #                 return f"Summary: {'. '.join(sentences)}... (This is a basic summary. Upload a document for detailed AI analysis.)"
# #             else:
# #                 return "Please upload a document first, then I can provide a detailed summary using AI analysis."
        
# #         return ""  # No simple answer found
    
# #     def _fallback_answer(self, question: str, context: str = "") -> str:
# #         """Provide fallback answers when AI model is not available"""
# #         question_lower = question.lower()
        
# #         if "summarize" in question_lower or "summary" in question_lower:
# #             return "I can help summarize documents, but the AI model is currently loading. Please try again in a few moments, or upload a document for rule-based analysis."
        
# #         elif "parties" in question_lower or "who" in question_lower:
# #             return "To identify parties in a legal document, look for names of individuals, companies, or organizations mentioned in the beginning sections or signature areas."
        
# #         elif "obligation" in question_lower or "responsibility" in question_lower:
# #             return "Legal obligations are typically found in sections containing words like 'shall', 'must', 'agrees to', or 'responsible for'."
        
# #         elif "date" in question_lower or "when" in question_lower:
# #             return "Important dates in legal documents include effective dates, expiration dates, and deadlines. Look for date formats like MM/DD/YYYY or spelled-out dates."
        
# #         else:
# #             return "I'm still loading the AI model for detailed analysis. For immediate help, try uploading a document to use our rule-based analysis features."

# # # Global instance
# # granite_service = None

# # def get_granite_service() -> GraniteLLMService:
# #     """Get or create Granite service instance"""
# #     global granite_service
# #     if granite_service is None:
# #         granite_service = GraniteLLMService()
# #     return granite_service



# # """
# # Granite LLM Service for ClauseWise
# # Uses IBM Granite 3.3-2B Instruct model from Hugging Face
# # """

# # import os
# # from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
# # import torch
# # from typing import List, Dict, Any
# # import re
# # import logging
# # from huggingface_hub import login

# # # Set up logging
# # logging.basicConfig(level=logging.INFO)
# # logger = logging.getLogger(__name__)

# # class GraniteLLMService:
# #     def __init__(self):
# #         self.model_name = "ibm-granite/granite-3.3-2b-instruct"
# #         self.device = "cuda" if torch.cuda.is_available() else "cpu"
# #         self.model = None
# #         self.tokenizer = None
# #         self.pipeline = None
# #         self.model_loaded = False
# #         self._setup_huggingface_auth()
# #         # Don't initialize model immediately - do it lazily
# #         logger.info("GraniteLLMService initialized successfully")
    
# #     def _setup_huggingface_auth(self):
# #         """Setup Hugging Face authentication"""
# #         try:
# #             # Try to get token from environment
# #             hf_token = os.getenv('HUGGINGFACE_TOKEN')
# #             if hf_token and hf_token != 'your_huggingface_token_here':
# #                 logger.info("Using Hugging Face token for authentication")
# #                 login(token=hf_token)
# #             else:
# #                 logger.info("No Hugging Face token provided, using public access")
# #         except Exception as e:
# #             logger.warning(f"Hugging Face authentication failed: {e}")
# #             logger.info("Continuing without authentication (public models only)")
    
# #     def _ensure_model_loaded(self):
# #         """Lazy loading of the model when first needed"""
# #         if not self.model_loaded:
# #             self._initialize_model()
    
# #     def _initialize_model(self):
# #         """Initialize the Granite model and tokenizer"""
# #         try:
# #             logger.info(f"Loading Granite model: {self.model_name}")
# #             logger.info(f"Using device: {self.device}")
            
# #             # Load tokenizer
# #             self.tokenizer = AutoTokenizer.from_pretrained(
# #                 self.model_name,
# #                 trust_remote_code=True
# #             )
            
# #             # Load model with appropriate settings
# #             self.model = AutoModelForCausalLM.from_pretrained(
# #                 self.model_name,
# #                 torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
# #                 device_map="auto" if self.device == "cuda" else None,
# #                 trust_remote_code=True,
# #                 low_cpu_mem_usage=True
# #             )
            
# #             # Create text generation pipeline
# #             self.pipeline = pipeline(
# #                 "text-generation",
# #                 model=self.model,
# #                 tokenizer=self.tokenizer,
# #                 device=0 if self.device == "cuda" else -1,
# #                 torch_dtype=torch.float16 if self.device == "cuda" else torch.float32
# #             )
            
# #             logger.info("Granite model loaded successfully!")
# #             self.model_loaded = True
            
# #         except Exception as e:
# #             logger.error(f"Error loading Granite model: {e}")
# #             self.model_loaded = False
# #             # Don't raise the error - allow graceful fallback
    
# #     def generate_response(self, prompt: str, max_length: int = 512, temperature: float = 0.7) -> str:
# #         """Generate response using Granite model"""
# #         try:
# #             self._ensure_model_loaded()
            
# #             if not self.model_loaded or not self.pipeline:
# #                 return "Model not available. Please check system requirements and try again."
            
# #             # Format prompt for Granite instruction format
# #             formatted_prompt = f"<|user|>\n{prompt}\n<|assistant|>\n"
            
# #             # Generate response with optimized parameters for speed
# #             try:
# #                 outputs = self.pipeline(
# #                     formatted_prompt,
# #                     max_new_tokens=min(max_length, 100),  # Reduce max tokens for speed
# #                     temperature=0.3,  # Lower temperature for faster, more focused responses
# #                     do_sample=True,
# #                     top_p=0.8,
# #                     repetition_penalty=1.05,
# #                     pad_token_id=self.tokenizer.eos_token_id,
# #                     num_return_sequences=1
# #                 )
                
# #                 # Extract generated text
# #                 full_response = outputs[0]['generated_text']
# #                 # Remove the prompt part and extract only the assistant's response
# #                 response = full_response.split("<|assistant|>\n")[-1].strip()
                
# #                 # If response is empty or too short, provide a basic response
# #                 if not response or len(response) < 10:
# #                     return "I understand your question. Due to current processing constraints, please try a more specific question or check back shortly."
                
# #                 return response
                
# #             except Exception as gen_error:
# #                 logger.error(f"Generation error: {gen_error}")
# #                 return "I'm experiencing some technical difficulties with text generation. Please try again with a simpler question."
            
# #         except Exception as e:
# #             logger.error(f"Error generating response: {e}")
# #             return f"I apologize, but I'm experiencing technical difficulties. Please try again later."
    
# #     def simplify_clause(self, clause_text: str) -> str:
# #         """Simplify legal clause using Granite"""
# #         try:
# #             logger.info("Starting clause simplification")
# #             self._ensure_model_loaded()
            
# #             if not self.model_loaded:
# #                 # Fallback to simple text processing
# #                 logger.warning("Model not loaded, using fallback for clause simplification")
# #                 return f"Simplified: {clause_text[:200]}... (AI model not available)"
            
# #             prompt = f"""Please simplify the following legal clause into plain, everyday language that a non-lawyer can easily understand. Keep the essential meaning but make it clear and simple:

# # Legal Clause: {clause_text}

# # Simplified Version:"""
            
# #             result = self.generate_response(prompt, max_length=300)
# #             logger.info("Clause simplification completed")
# #             return result
            
# #         except Exception as e:
# #             logger.error(f"Error in clause simplification: {e}")
# #             return f"Error simplifying clause: {str(e)}"
    
# #     def extract_entities_with_ai(self, text: str) -> Dict[str, List[str]]:
# #         """Extract named entities using Granite AI"""
# #         try:
# #             logger.info("Starting AI entity extraction")
# #             self._ensure_model_loaded()
            
# #             if not self.model_loaded:
# #                 # Fallback to empty entities
# #                 logger.warning("Model not loaded, returning empty entities")
# #                 return {
# #                     "parties": [],
# #                     "dates": [],
# #                     "monetary_values": [],
# #                     "obligations": [],
# #                     "legal_terms": []
# #                 }
            
# #             prompt = f"""Analyze the following legal document and extract key information. Return the results in this exact format:

# # PARTIES: [list the individuals, companies, or organizations involved]
# # DATES: [list all dates mentioned]
# # MONETARY VALUES: [list all money amounts, fees, or financial terms]
# # OBLIGATIONS: [list key duties, responsibilities, or requirements]
# # LEGAL TERMS: [list important legal concepts or technical terms]

# # Document: {text[:2000]}...

# # Analysis:"""
            
# #             response = self.generate_response(prompt, max_length=400)
            
# #             # Parse the response into structured data
# #             entities = {
# #                 "parties": [],
# #                 "dates": [],
# #                 "monetary_values": [],
# #                 "obligations": [],
# #                 "legal_terms": []
# #             }
            
# #             try:
# #                 lines = response.split('\n')
# #                 current_category = None
                
# #                 for line in lines:
# #                     line = line.strip()
# #                     if line.startswith('PARTIES:'):
# #                         current_category = "parties"
# #                         # Extract items from the same line
# #                         items = line.replace('PARTIES:', '').strip()
# #                         if items and items != '[list the individuals, companies, or organizations involved]':
# #                             entities[current_category].extend([item.strip() for item in items.split(',') if item.strip()])
# #                     elif line.startswith('DATES:'):
# #                         current_category = "dates"
# #                         items = line.replace('DATES:', '').strip()
# #                         if items and items != '[list all dates mentioned]':
# #                             entities[current_category].extend([item.strip() for item in items.split(',') if item.strip()])
# #                     elif line.startswith('MONETARY VALUES:'):
# #                         current_category = "monetary_values"
# #                         items = line.replace('MONETARY VALUES:', '').strip()
# #                         if items and items != '[list all money amounts, fees, or financial terms]':
# #                             entities[current_category].extend([item.strip() for item in items.split(',') if item.strip()])
# #                     elif line.startswith('OBLIGATIONS:'):
# #                         current_category = "obligations"
# #                         items = line.replace('OBLIGATIONS:', '').strip()
# #                         if items and items != '[list key duties, responsibilities, or requirements]':
# #                             entities[current_category].extend([item.strip() for item in items.split(',') if item.strip()])
# #                     elif line.startswith('LEGAL TERMS:'):
# #                         current_category = "legal_terms"
# #                         items = line.replace('LEGAL TERMS:', '').strip()
# #                         if items and items != '[list important legal concepts or technical terms]':
# #                             entities[current_category].extend([item.strip() for item in items.split(',') if item.strip()])
# #                     elif current_category and (line.startswith('-') or line.startswith('•')):
# #                         # Handle bullet points
# #                         item = line.lstrip('-•').strip()
# #                         if item:
# #                             entities[current_category].append(item)
            
# #             except Exception as e:
# #                 logger.error(f"Error parsing entities: {e}")
            
# #             logger.info("AI entity extraction completed")
# #             return entities
            
# #         except Exception as e:
# #             logger.error(f"Error in AI entity extraction: {e}")
# #             return {
# #                 "parties": [],
# #                 "dates": [],
# #                 "monetary_values": [],
# #                 "obligations": [],
# #                 "legal_terms": []
# #             }
    
# #     def classify_document_with_ai(self, text: str) -> Dict[str, Any]:
# #         """Classify document type using Granite AI"""
# #         try:
# #             logger.info("Starting AI document classification")
# #             self._ensure_model_loaded()
            
# #             if not self.model_loaded:
# #                 # Fallback classification
# #                 logger.warning("Model not loaded, using fallback classification")
# #                 return {
# #                     "type": "General Legal Document",
# #                     "confidence": 0.3,
# #                     "description": "AI model not available for detailed classification",
# #                     "key_characteristics": ["Document contains legal terminology"]
# #                 }
            
# #             prompt = f"""Analyze the following legal document and classify its type. Choose from these categories:
# # - Non-Disclosure Agreement (NDA)
# # - Employment Contract
# # - Service Agreement
# # - Lease Agreement
# # - Purchase Agreement
# # - Partnership Agreement
# # - License Agreement
# # - General Legal Document

# # Also provide confidence level (0.0 to 1.0) and key characteristics.

# # Document excerpt: {text[:1500]}...

# # Classification:
# # Type:
# # Confidence:
# # Description:
# # Key Characteristics:"""
        
# #             response = self.generate_response(prompt, max_length=300)
            
# #             # Parse response
# #             result = {
# #                 "type": "General Legal Document",
# #                 "confidence": 0.5,
# #                 "description": "Legal document analysis",
# #                 "key_characteristics": []
# #             }
            
# #             try:
# #                 lines = response.split('\n')
# #                 for line in lines:
# #                     line = line.strip()
# #                     if line.startswith('Type:'):
# #                         doc_type = line.replace('Type:', '').strip()
# #                         if doc_type:
# #                             result["type"] = doc_type
# #                     elif line.startswith('Confidence:'):
# #                         conf_str = line.replace('Confidence:', '').strip()
# #                         try:
# #                             # Extract numeric value
# #                             conf_match = re.search(r'(\d+\.?\d*)', conf_str)
# #                             if conf_match:
# #                                 conf_val = float(conf_match.group(1))
# #                                 if conf_val > 1.0:  # If it's a percentage
# #                                     conf_val = conf_val / 100.0
# #                                 result["confidence"] = conf_val
# #                         except:
# #                             pass
# #                     elif line.startswith('Description:'):
# #                         desc = line.replace('Description:', '').strip()
# #                         if desc:
# #                             result["description"] = desc
# #                     elif line.startswith('Key Characteristics:'):
# #                         continue
# #                     elif line.startswith('-') or line.startswith('•'):
# #                         char = line.lstrip('-•').strip()
# #                         if char:
# #                             result["key_characteristics"].append(char)
            
# #             except Exception as e:
# #                 logger.error(f"Error parsing classification: {e}")
            
# #             logger.info("AI document classification completed")
# #             return result
            
# #         except Exception as e:
# #             logger.error(f"Error in AI document classification: {e}")
# #             return {
# #                 "type": "General Legal Document",
# #                 "confidence": 0.3,
# #                 "description": f"Classification error: {str(e)}",
# #                 "key_characteristics": ["Document analysis failed"]
# #             }
    
# #     def answer_question(self, question: str, context: str = "") -> str:
# #         """Answer questions about legal documents using Granite"""
# #         try:
# #             # Quick check for simple questions that can be answered without AI
# #             simple_answers = self._try_simple_answer(question, context)
# #             if simple_answers:
# #                 return simple_answers
            
# #             self._ensure_model_loaded()
            
# #             if not self.model_loaded:
# #                 return self._fallback_answer(question, context)
            
# #             prompt = f"""You are ClauseWise AI, a legal document analysis assistant. Answer the following question about legal concepts or document analysis.

# # Context: {context[:1000] if context else "General legal knowledge"}

# # Question: {question}

# # Answer:"""
            
# #             return self.generate_response(prompt, max_length=200)  # Reduced for faster response
            
# #         except Exception as e:
# #             logger.error(f"Error in AI question answering: {e}")
# #             return self._fallback_answer(question, context)
    
# #     def _try_simple_answer(self, question: str, context: str = "") -> str:
# #         """Try to answer simple questions without AI model"""
# #         question_lower = question.lower()
        
# #         # Simple question patterns
# #         if "what is" in question_lower or "define" in question_lower:
# #             if "nda" in question_lower or "non-disclosure" in question_lower:
# #                 return "An NDA (Non-Disclosure Agreement) is a legal contract that prevents parties from sharing confidential information with third parties."
# #             elif "contract" in question_lower:
# #                 return "A contract is a legally binding agreement between two or more parties that creates mutual obligations enforceable by law."
# #             elif "clause" in question_lower:
# #                 return "A clause is a specific provision or section within a legal document that addresses a particular aspect of the agreement."
        
# #         elif "how to" in question_lower:
# #             if "simplify" in question_lower:
# #                 return "To simplify legal language: 1) Replace complex terms with everyday words, 2) Break long sentences into shorter ones, 3) Use active voice, 4) Define technical terms."
        
# #         elif "summarize" in question_lower:
# #             if context:
# #                 # Simple context-based summary
# #                 sentences = context.split('.')[:3]  # First 3 sentences
# #                 return f"Summary: {'. '.join(sentences)}... (This is a basic summary. Upload a document for detailed AI analysis.)"
# #             else:
# #                 return "Please upload a document first, then I can provide a detailed summary using AI analysis."
        
# #         return ""  # No simple answer found
    
# #     def _fallback_answer(self, question: str, context: str = "") -> str:
# #         """Provide fallback answers when AI model is not available"""
# #         question_lower = question.lower()
        
# #         if "summarize" in question_lower or "summary" in question_lower:
# #             return "I can help summarize documents, but the AI model is currently loading. Please try again in a few moments, or upload a document for rule-based analysis."
        
# #         elif "parties" in question_lower or "who" in question_lower:
# #             return "To identify parties in a legal document, look for names of individuals, companies, or organizations mentioned in the beginning sections or signature areas."
        
# #         elif "obligation" in question_lower or "responsibility" in question_lower:
# #             return "Legal obligations are typically found in sections containing words like 'shall', 'must', 'agrees to', or 'responsible for'."
        
# #         elif "date" in question_lower or "when" in question_lower:
# #             return "Important dates in legal documents include effective dates, expiration dates, and deadlines. Look for date formats like MM/DD/YYYY or spelled-out dates."
        
# #         else:
# #             return "I'm still loading the AI model for detailed analysis. For immediate help, try uploading a document to use our rule-based analysis features."

# # # Global instance - Fixed singleton pattern
# # _granite_service = None

# # def get_granite_service() -> GraniteLLMService:
# #     """Get or create Granite service instance"""
# #     global _granite_service
# #     if _granite_service is None:
# #         logger.info("Creating new GraniteLLMService instance")
# #         _granite_service = GraniteLLMService()
# #     return _granite_service

# # # For backwards compatibility
# # granite_service = get_granite_service()





# """
# Granite LLM Service for ClauseWise
# Uses IBM Micro Granite model from Hugging Face
# """

# import os
# from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
# import torch
# from typing import List, Dict, Any
# import re
# import logging
# from huggingface_hub import login

# # Set up logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# class GraniteLLMService:
#     def __init__(self):
#         # Switched from Granite 2B → Micro Granite model
#         self.model_name = "ibm-ai-platform/micro-g3.3-8b-instruct-1b"
#         self.device = "cuda" if torch.cuda.is_available() else "cpu"
#         self.model = None
#         self.tokenizer = None
#         self.pipeline = None
#         self.model_loaded = False
#         self._setup_huggingface_auth()
#         # Lazy loading: don’t load immediately

#     def _setup_huggingface_auth(self):
#         """Setup Hugging Face authentication"""
#         try:
#             hf_token = os.getenv('HUGGINGFACE_TOKEN')
#             if hf_token and hf_token != 'your_huggingface_token_here':
#                 logger.info("Using Hugging Face token for authentication")
#                 login(token=hf_token)
#             else:
#                 logger.info("No Hugging Face token provided, using public access")
#         except Exception as e:
#             logger.warning(f"Hugging Face authentication failed: {e}")
#             logger.info("Continuing without authentication (public models only)")

#     def _ensure_model_loaded(self):
#         """Lazy loading of the model when first needed"""
#         if not self.model_loaded:
#             self._initialize_model()

#     def _initialize_model(self):
#         """Initialize the Micro Granite model and tokenizer"""
#         try:
#             logger.info(f"Loading IBM Micro Granite model: {self.model_name}")
#             logger.info(f"Using device: {self.device}")

#             # Load tokenizer
#             self.tokenizer = AutoTokenizer.from_pretrained(
#                 self.model_name,
#                 trust_remote_code=True
#             )

#             # Load model directly to CPU/GPU (⚡ fixes meta tensor issue)
#             self.model = AutoModelForCausalLM.from_pretrained(
#                 self.model_name,
#                 torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
#                 trust_remote_code=True,
#                 low_cpu_mem_usage=True
#             ).to(self.device)

#             # Create text generation pipeline
#             self.pipeline = pipeline(
#                 "text-generation",
#                 model=self.model,
#                 tokenizer=self.tokenizer,
#                 device=0 if self.device == "cuda" else -1,
#                 torch_dtype=torch.float16 if self.device == "cuda" else torch.float32
#             )

#             logger.info("IBM Micro Granite model loaded successfully!")
#             self.model_loaded = True

#         except Exception as e:
#             logger.error(f"Error loading IBM Micro Granite model: {e}")
#             self.model_loaded = False

#     def generate_response(self, prompt: str, max_length: int = 512, temperature: float = 0.7) -> str:
#         """Generate response using IBM Micro Granite"""
#         try:
#             self._ensure_model_loaded()
#             if not self.model_loaded or not self.pipeline:
#                 return "Model not available. Please check system requirements and try again."

#             formatted_prompt = f"<|user|>\n{prompt}\n<|assistant|>\n"

#             try:
#                 outputs = self.pipeline(
#                     formatted_prompt,
#                     max_new_tokens=min(max_length, 100),
#                     temperature=temperature,
#                     do_sample=True,
#                     top_p=0.8,
#                     repetition_penalty=1.05,
#                     pad_token_id=self.tokenizer.eos_token_id,
#                     num_return_sequences=1
#                 )
#                 full_response = outputs[0]['generated_text']
#                 response = full_response.split("<|assistant|>\n")[-1].strip()
#                 if not response or len(response) < 10:
#                     return "I understand your question. Due to current processing constraints, please try a more specific question or check back shortly."
#                 return response

#             except Exception as gen_error:
#                 logger.error(f"Generation error: {gen_error}")
#                 return "I'm experiencing some technical difficulties with text generation. Please try again with a simpler question."

#         except Exception as e:
#             logger.error(f"Error generating response: {e}")
#             return "I apologize, but I'm experiencing technical difficulties. Please try again later."
    
#     def simplify_clause(self, clause: str) -> str:
#         """Simplify a legal clause into plain English"""
#         prompt = (
#             "Simplify the following legal clause into plain English so it is easy to understand:\n\n"
#             f"{clause}\n\nSimplified clause:"
#         )
#         return self.generate_response(prompt, max_length=200)

#     def extract_entities_with_ai(self, text: str) -> str:
#         """Extract key legal entities (names, dates, amounts, organizations, etc.) from text"""
#         prompt = (
#             "Extract all the important legal entities (names, organizations, dates, amounts, etc.) "
#             "from the following text:\n\n"
#             f"{text}\n\nEntities:"
#         )
#         return self.generate_response(prompt, max_length=300)

#     def classify_document_with_ai(self, text: str) -> str:
#         """Classify the document into a type (e.g., Contract, NDA, Agreement, Lease, Policy, etc.)"""
#         prompt = (
#             "Classify the type of this legal document. "
#             "Choose from categories such as: Contract, NDA, Lease, Employment Agreement, Policy, Other.\n\n"
#             f"Document:\n{text}\n\nClassification:"
#         )
#         return self.generate_response(prompt, max_length=100)

#     def answer_question(self, text: str, question: str) -> str:
#         """Answer a legal question based on the document text"""
#         prompt = (
#             f"Document:\n{text}\n\n"
#             f"Question: {question}\n\n"
#             "Answer in clear, simple language:"
#         )
#         return self.generate_response(prompt, max_length=300)

#     # --- All your other methods (simplify_clause, extract_entities_with_ai, classify_document_with_ai, answer_question, etc.)
#     # remain unchanged because they all call `generate_response()` internally.
#     # No changes needed there.
#     # ------------------------------------------------------------------------

# # Global instance
# granite_service = None

# def get_granite_service() -> GraniteLLMService:
#     """Get or create Granite service instance"""
#     global granite_service
#     if granite_service is None:
#         granite_service = GraniteLLMService()
#     return granite_service


# import os
# from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
# import torch
# import logging
# from huggingface_hub import login

# # Set up logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# class GraniteLLMService:
#     def __init__(self):
#         # Switched from Granite 2B → Micro Granite model
#         self.model_name = "ibm-ai-platform/micro-g3.3-8b-instruct-1b"
#         self.device = "cuda" if torch.cuda.is_available() else "cpu"
#         self.model = None
#         self.tokenizer = None
#         self.pipeline = None
#         self.model_loaded = False
#         self._setup_huggingface_auth()
#         # Lazy loading

#     def _setup_huggingface_auth(self):
#         """Setup Hugging Face authentication"""
#         try:
#             hf_token = os.getenv('HUGGINGFACE_TOKEN')
#             if hf_token and hf_token != 'your_huggingface_token_here':
#                 logger.info("Using Hugging Face token for authentication")
#                 login(token=hf_token)
#             else:
#                 logger.info("No Hugging Face token provided, using public access")
#         except Exception as e:
#             logger.warning(f"Hugging Face authentication failed: {e}")
#             logger.info("Continuing without authentication (public models only)")

#     def _ensure_model_loaded(self):
#         """Lazy loading of the model when first needed"""
#         if not self.model_loaded:
#             self._initialize_model()

#     def _initialize_model(self):
#         """Initialize the Micro Granite model and tokenizer"""
#         try:
#             logger.info(f"Loading IBM Micro Granite model: {self.model_name}")
#             logger.info(f"Using device: {self.device}")

#             # Load tokenizer
#             self.tokenizer = AutoTokenizer.from_pretrained(
#                 self.model_name,
#                 trust_remote_code=True
#             )

#             # Load model directly to CPU/GPU
#             self.model = AutoModelForCausalLM.from_pretrained(
#                 self.model_name,
#                 torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
#                 trust_remote_code=True,
#                 low_cpu_mem_usage=True
#             ).to(self.device)

#             # Create text generation pipeline
#             self.pipeline = pipeline(
#                 "text-generation",
#                 model=self.model,
#                 tokenizer=self.tokenizer,
#                 device=0 if self.device == "cuda" else -1,
#                 torch_dtype=torch.float16 if self.device == "cuda" else torch.float32
#             )

#             logger.info("IBM Micro Granite model loaded successfully!")
#             self.model_loaded = True

#         except Exception as e:
#             logger.error(f"Error loading IBM Micro Granite model: {e}")
#             self.model_loaded = False

#     def generate_response(self, prompt: str, max_length: int = 512, temperature: float = 0.7) -> str:
#         """Generate response using IBM Micro Granite"""
#         try:
#             self._ensure_model_loaded()
#             if not self.model_loaded or not self.pipeline:
#                 return "Model not available. Please check system requirements and try again."

#             formatted_prompt = f"<|user|>\n{prompt}\n<|assistant|>\n"

#             try:
#                 outputs = self.pipeline(
#                     formatted_prompt,
#                     max_new_tokens=min(max_length, 100),
#                     temperature=temperature,
#                     do_sample=True,
#                     top_p=0.8,
#                     repetition_penalty=1.05,
#                     pad_token_id=self.tokenizer.eos_token_id,
#                     num_return_sequences=1
#                 )
#                 full_response = outputs[0]['generated_text']
#                 response = full_response.split("<|assistant|>\n")[-1].strip()
#                 if not response or len(response) < 10:
#                     return "I understand your question. Due to current processing constraints, please try again with a more specific question or check back shortly."
#                 return response

#             except Exception as gen_error:
#                 logger.error(f"Generation error: {gen_error}")
#                 return "I'm experiencing some technical difficulties with text generation. Please try again with a simpler question."

#         except Exception as e:
#             logger.error(f"Error generating response: {e}")
#             return "I apologize, but I'm experiencing technical difficulties. Please try again later."
    
#     def simplify_clause(self, clause: str) -> dict:
#         """Simplify a legal clause into plain English"""
#         prompt = (
#             "Simplify the following legal clause into plain English so it is easy to understand:\n\n"
#             f"{clause}\n\nSimplified clause:"
#         )
#         response = self.generate_response(prompt, max_length=200)
#         return {"simplified_clause": response}

#     def extract_entities_with_ai(self, text: str) -> dict:
#         """Extract key legal entities (names, dates, amounts, organizations, etc.) from text"""
#         prompt = (
#             "Extract all the important legal entities (names, organizations, dates, amounts, etc.) "
#             "from the following text. Return them in JSON-like format.\n\n"
#             f"{text}\n\nEntities:"
#         )
#         response = self.generate_response(prompt, max_length=300)
#         return {"entities": response}

#     def classify_document_with_ai(self, text: str) -> dict:
#         """Classify the document into a type (e.g., Contract, NDA, Agreement, Lease, Policy, etc.)"""
#         prompt = (
#             "Classify the type of this legal document. "
#             "Choose from categories such as: Contract, NDA, Lease, Employment Agreement, Policy, Other.\n\n"
#             f"Document:\n{text}\n\nClassification:"
#         )
#         response = self.generate_response(prompt, max_length=100)
#         return {"classification": response}

#     def answer_question(self, text: str, question: str) -> dict:
#         """Answer a legal question based on the document text"""
#         prompt = (
#             f"Document:\n{text}\n\n"
#             f"Question: {question}\n\n"
#             "Answer in clear, simple language:"
#         )
#         response = self.generate_response(prompt, max_length=300)
#         return {"answer": response}

# # Global instance
# granite_service = None

# def get_granite_service() -> GraniteLLMService:
#     """Get or create Granite service instance"""
#     global granite_service
#     if granite_service is None:
#         granite_service = GraniteLLMService()
#     return granite_service










# import logging
# import os
# import torch
# from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

# # Set up logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# class GraniteLLMService:
#     """
#     CPU-friendly replacement for the previous IBM Micro Granite model.
#     Uses TinyLlama (1.1B) so it runs on laptops without a GPU.
#     Keeps all public methods and return shapes identical to avoid breaking the app.
#     """
#     def __init__(self, model_name: str | None = None):
#         # Lightweight local model for CPU
#         self.model_name = model_name or "TinyLlama/TinyLlama-1.1B-Chat-v1.0"

#         # Force CPU on laptops without CUDA to prevent half-precision issues
#         self.device = "cpu"

#         self.model = None
#         self.tokenizer = None
#         self.pipeline = None
#         self.model_loaded = False

#         # No HF login required for a public model; keeping placeholder for future use
#         self._setup_huggingface_auth()

#     def _setup_huggingface_auth(self):
#         """Optional: use HF token if you set HUGGINGFACE_TOKEN, otherwise skip."""
#         try:
#             from huggingface_hub import login
#             hf_token = os.getenv("HUGGINGFACE_TOKEN")
#             if hf_token and hf_token.strip():
#                 logger.info("Using Hugging Face token for authentication")
#                 login(token=hf_token)
#             else:
#                 logger.info("No Hugging Face token provided (public model access)")
#         except Exception as e:
#             logger.warning(f"Hugging Face authentication skipped/failed: {e}")

#     def _ensure_model_loaded(self):
#         if not self.model_loaded:
#             self._initialize_model()

#     def _initialize_model(self):
#         """Load TinyLlama on CPU with minimal RAM footprint."""
#         try:
#             logger.info(f"Loading local CPU model: {self.model_name}")

#             # Tokenizer
#             self.tokenizer = AutoTokenizer.from_pretrained(
#                 self.model_name,
#                 use_fast=True
#             )

#             # Model (float32 on CPU; low_cpu_mem_usage to reduce peak RAM)
#             self.model = AutoModelForCausalLM.from_pretrained(
#                 self.model_name,
#                 torch_dtype=torch.float32,
#                 low_cpu_mem_usage=True
#             )

#             # Text-generation pipeline (device = -1 means CPU)
#             self.pipeline = pipeline(
#                 "text-generation",
#                 model=self.model,
#                 tokenizer=self.tokenizer,
#                 device=-1
#             )

#             # Ensure a pad token to avoid generation warnings
#             if self.pipeline.tokenizer.pad_token_id is None:
#                 self.pipeline.tokenizer.pad_token = self.pipeline.tokenizer.eos_token

#             logger.info("TinyLlama model loaded successfully on CPU.")
#             self.model_loaded = True

#         except Exception as e:
#             logger.exception(f"Error loading model: {e}")
#             self.model_loaded = False

#     def generate_response(self, prompt: str, max_length: int = 512, temperature: float = 0.7) -> str:
#         """Generate response using the CPU model (keeps original signature)."""
#         try:
#             self._ensure_model_loaded()
#             if not self.model_loaded or not self.pipeline:
#                 return "Model not available. Please check system requirements and try again."

#             # Keep your original wrapper format so other parts of the code remain untouched.
#             formatted_prompt = f"<|user|>\n{prompt}\n<|assistant|>\n"

#             try:
#                 outputs = self.pipeline(
#                     formatted_prompt,
#                     max_new_tokens=min(max_length, 120),
#                     temperature=temperature,
#                     do_sample=True,
#                     top_p=0.9,
#                     repetition_penalty=1.05,
#                     pad_token_id=self.tokenizer.eos_token_id,
#                     num_return_sequences=1
#                 )
#                 full = outputs[0]["generated_text"]
#                 # Split on your existing delimiter to keep behavior stable
#                 response = full.split("<|assistant|>\n")[-1].strip()
#                 if not response or len(response) < 5:
#                     return "I’m ready, but the request is too short to respond meaningfully. Please provide a bit more detail."
#                 return response

#             except Exception as gen_error:
#                 logger.error(f"Generation error: {gen_error}")
#                 return "I'm experiencing some technical difficulties with text generation. Please try again with a simpler question."

#         except Exception as e:
#             logger.error(f"Error generating response: {e}")
#             return "I apologize, but I'm experiencing technical difficulties. Please try again later."

#     # ---- Public methods kept identical so the rest of your app still works ----

#     def simplify_clause(self, clause: str) -> dict:
#         prompt = (
#             "Simplify the following legal clause into plain English so it is easy to understand:\n\n"
#             f"{clause}\n\nSimplified clause:"
#         )
#         return {"simplified_clause": self.generate_response(prompt, max_length=200)}

#     def extract_entities_with_ai(self, text: str) -> dict:
#         prompt = (
#             "Extract all the important legal entities (names, organizations, dates, amounts, etc.) "
#             "from the following text. Return them in JSON-like format.\n\n"
#             f"{text}\n\nEntities:"
#         )
#         return {"entities": self.generate_response(prompt, max_length=300)}

#     def classify_document_with_ai(self, text: str) -> dict:
#         prompt = (
#             "Classify the type of this legal document. "
#             "Choose from: Contract, NDA, Lease, Employment Agreement, Policy, Other.\n\n"
#             f"Document:\n{text}\n\nClassification:"
#         )
#         return {"classification": self.generate_response(prompt, max_length=100)}

#     def answer_question(self, text: str, question: str) -> dict:
#         prompt = (
#             f"Document:\n{text}\n\n"
#             f"Question: {question}\n\n"
#             "Answer in clear, simple language:"
#         )
#         return {"answer": self.generate_response(prompt, max_length=300)}

# # Global instance (kept for compatibility)
# granite_service = None

# def get_granite_service() -> "GraniteLLMService":
#     global granite_service
#     if granite_service is None:
#         granite_service = GraniteLLMService()
#     return granite_service




# import logging
# import os
# import torch
# from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

# # Set up logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# class GraniteLLMService:
#     """
#     CPU-friendly replacement using TinyLlama (1.1B).
#     Runs on laptops without GPU while keeping public methods identical.
#     """
#     def __init__(self, model_name: str | None = None):
#         # Use TinyLlama by default
#         self.model_name = model_name or "TinyLlama/TinyLlama-1.1B-Chat-v1.0"

#         # Force CPU on laptops without CUDA
#         self.device = "cpu"

#         self.model = None
#         self.tokenizer = None
#         self.pipeline = None
#         self.model_loaded = False

#         # HuggingFace login (optional)
#         self._setup_huggingface_auth()

#     def _setup_huggingface_auth(self):
#         """Optional: use HF token if set, otherwise skip."""
#         try:
#             from huggingface_hub import login
#             hf_token = os.getenv("HUGGINGFACE_TOKEN")
#             if hf_token and hf_token.strip():
#                 logger.info("Using Hugging Face token for authentication")
#                 login(token=hf_token)
#             else:
#                 logger.info("No Hugging Face token provided (public model access)")
#         except Exception as e:
#             logger.warning(f"Hugging Face authentication skipped/failed: {e}")

#     def _ensure_model_loaded(self):
#         if not self.model_loaded:
#             self._initialize_model()

#     def _initialize_model(self):
#         """Load TinyLlama on CPU with minimal RAM footprint."""
#         try:
#             logger.info(f"Loading local CPU model: {self.model_name}")

#             # Tokenizer
#             self.tokenizer = AutoTokenizer.from_pretrained(
#                 self.model_name,
#                 use_fast=True
#             )

#             # Model
#             self.model = AutoModelForCausalLM.from_pretrained(
#                 self.model_name,
#                 torch_dtype=torch.float32,
#                 low_cpu_mem_usage=True
#             )

#             # Text-generation pipeline
#             self.pipeline = pipeline(
#                 "text-generation",
#                 model=self.model,
#                 tokenizer=self.tokenizer,
#                 device=-1  # CPU
#             )

#             # Ensure pad token
#             if self.pipeline.tokenizer.pad_token_id is None:
#                 self.pipeline.tokenizer.pad_token = self.pipeline.tokenizer.eos_token

#             logger.info("TinyLlama model loaded successfully on CPU.")
#             self.model_loaded = True

#         except Exception as e:
#             logger.exception(f"Error loading model: {e}")
#             self.model_loaded = False

#     def generate_response(self, prompt: str, max_length: int = 512, temperature: float = 0.7) -> str:
#         """
#         General-purpose chat-like response generator.
#         Works for questions, summaries, explanations, etc.
#         """
#         try:
#             self._ensure_model_loaded()
#             if not self.model_loaded or not self.pipeline:
#                 return "Model not available. Please check system requirements and try again."

#             # Chat-style formatted prompt
#             formatted_prompt = f"<|user|>\n{prompt}\n<|assistant|>\n"

#             outputs = self.pipeline(
#                 formatted_prompt,
#                 max_new_tokens=min(max_length, 200),
#                 temperature=temperature,
#                 do_sample=True,
#                 top_p=0.9,
#                 repetition_penalty=1.05,
#                 pad_token_id=self.tokenizer.eos_token_id,
#                 num_return_sequences=1
#             )

#             full = outputs[0]["generated_text"]
#             response = full.split("<|assistant|>\n")[-1].strip()

#             if not response or len(response) < 5:
#                 return "I'm ready to help! Could you please provide more detail in your question?"

#             return response

#         except Exception as e:
#             logger.error(f"Error generating response: {e}")
#             return "I’m having some trouble generating a reply. Please try again later."

#     # ---- Public methods (unchanged) ----

#     def simplify_clause(self, clause: str) -> dict:
#         prompt = (
#             "Simplify the following legal clause into plain English:\n\n"
#             f"{clause}\n\nSimplified clause:"
#         )
#         return {"simplified_clause": self.generate_response(prompt, max_length=200)}

#     def extract_entities_with_ai(self, text: str) -> dict:
#         prompt = (
#             "Extract important legal entities (names, organizations, dates, amounts, etc.) "
#             "from the following text. Return them in JSON-like format.\n\n"
#             f"{text}\n\nEntities:"
#         )
#         return {"entities": self.generate_response(prompt, max_length=300)}

#     def classify_document_with_ai(self, text: str) -> dict:
#         prompt = (
#             "Classify this legal document. Choose from: Contract, NDA, Lease, "
#             "Employment Agreement, Policy, Other.\n\n"
#             f"Document:\n{text}\n\nClassification:"
#         )
#         return {"classification": self.generate_response(prompt, max_length=100)}

#     def answer_question(self, text: str, question: str) -> dict:
#         prompt = (
#             f"Document:\n{text}\n\n"
#             f"Question: {question}\n\n"
#             "Answer in clear, simple language:"
#         )
#         return {"answer": self.generate_response(prompt, max_length=300)}

# # Global instance
# granite_service = None

# def get_granite_service() -> "GraniteLLMService":
#     global granite_service
#     if granite_service is None:
#         granite_service = GraniteLLMService()
#     return granite_service





# import logging
# import os
# import torch
# from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

# # Set up logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# class GraniteLLMService:
#     """
#     CPU-friendly replacement using TinyLlama (1.1B).
#     Runs on laptops without GPU while keeping public methods identical.
#     Now includes safe fallbacks if model fails to load.
#     """
#     def __init__(self, model_name: str | None = None):
#         # Use TinyLlama by default
#         self.model_name = model_name or "TinyLlama/TinyLlama-1.1B-Chat-v1.0"

#         # Force CPU on laptops without CUDA
#         self.device = "cpu"

#         self.model = None
#         self.tokenizer = None
#         self.pipeline = None
#         self.model_loaded = False

#         # HuggingFace login (optional)
#         self._setup_huggingface_auth()

#     def _setup_huggingface_auth(self):
#         """Optional: use HF token if set, otherwise skip."""
#         try:
#             from huggingface_hub import login
#             hf_token = os.getenv("HUGGINGFACE_TOKEN")
#             if hf_token and hf_token.strip():
#                 logger.info("Using Hugging Face token for authentication")
#                 login(token=hf_token)
#             else:
#                 logger.info("No Hugging Face token provided (public model access)")
#         except Exception as e:
#             logger.warning(f"Hugging Face authentication skipped/failed: {e}")

#     def _ensure_model_loaded(self):
#         if not self.model_loaded:
#             self._initialize_model()

#     def _initialize_model(self):
#         """Load TinyLlama on CPU with minimal RAM footprint."""
#         try:
#             logger.info(f"Loading local CPU model: {self.model_name}")

#             # Tokenizer
#             self.tokenizer = AutoTokenizer.from_pretrained(
#                 self.model_name,
#                 use_fast=True
#             )

#             # Model
#             self.model = AutoModelForCausalLM.from_pretrained(
#                 self.model_name,
#                 torch_dtype=torch.float32,
#                 low_cpu_mem_usage=True
#             )

#             # Text-generation pipeline
#             self.pipeline = pipeline(
#                 "text-generation",
#                 model=self.model,
#                 tokenizer=self.tokenizer,
#                 device=-1  # CPU
#             )

#             # Ensure pad token
#             if self.pipeline.tokenizer.pad_token_id is None:
#                 self.pipeline.tokenizer.pad_token = self.pipeline.tokenizer.eos_token

#             logger.info("TinyLlama model loaded successfully on CPU.")
#             self.model_loaded = True

#         except Exception as e:
#             logger.exception(f"Error loading model: {e}")
#             self.model_loaded = False

#     def generate_response(self, prompt: str, max_length: int = 512, temperature: float = 0.7) -> str:
#         """
#         General-purpose chat-like response generator.
#         Works for questions, summaries, explanations, etc.
#         Falls back to stub text if model not available.
#         """
#         try:
#             self._ensure_model_loaded()
#             if not self.model_loaded or not self.pipeline:
#                 logger.warning("Granite LLM not available — using fallback.")
#                 return f"[Stub response] {prompt[:120]}..."

#             # Chat-style formatted prompt
#             formatted_prompt = f"<|user|>\n{prompt}\n<|assistant|>\n"

#             outputs = self.pipeline(
#                 formatted_prompt,
#                 max_new_tokens=min(max_length, 200),
#                 temperature=temperature,
#                 do_sample=True,
#                 top_p=0.9,
#                 repetition_penalty=1.05,
#                 pad_token_id=self.tokenizer.eos_token_id,
#                 num_return_sequences=1
#             )

#             full = outputs[0]["generated_text"]
#             response = full.split("<|assistant|>\n")[-1].strip()

#             if not response or len(response) < 5:
#                 return "I'm ready to help! Could you please provide more detail in your question?"

#             return response

#         except Exception as e:
#             logger.error(f"Error generating response: {e}")
#             return "I’m having some trouble generating a reply. Please try again later."

#     # ---- Public methods (unchanged interface) ----

#     def simplify_clause(self, clause: str) -> dict:
#         prompt = (
#             "Simplify the following legal clause into plain English:\n\n"
#             f"{clause}\n\nSimplified clause:"
#         )
#         return {"simplified_clause": self.generate_response(prompt, max_length=200)}

#     def extract_entities_with_ai(self, text: str) -> dict:
#         prompt = (
#             "Extract important legal entities (names, organizations, dates, amounts, etc.) "
#             "from the following text. Return them in JSON-like format.\n\n"
#             f"{text}\n\nEntities:"
#         )
#         return {"entities": self.generate_response(prompt, max_length=300)}

#     def classify_document_with_ai(self, text: str) -> dict:
#         prompt = (
#             "Classify this legal document. Choose from: Contract, NDA, Lease, "
#             "Employment Agreement, Policy, Other.\n\n"
#             f"Document:\n{text}\n\nClassification:"
#         )
#         return {"classification": self.generate_response(prompt, max_length=100)}

#     def answer_question(self, text: str, question: str) -> dict:
#         prompt = (
#             f"Document:\n{text}\n\n"
#             f"Question: {question}\n\n"
#             "Answer in clear, simple language:"
#         )
#         return {"answer": self.generate_response(prompt, max_length=300)}

# # Global instance
# granite_service = None

# def get_granite_service() -> "GraniteLLMService":
#     global granite_service
#     if granite_service is None:
#         granite_service = GraniteLLMService()
#     return granite_service



import logging
import os
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import re
import json
from typing import Dict, List, Any, Optional

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GraniteLLMService:
    """
    Enhanced ClauseWise Granite LLM Service
    CPU-friendly replacement using TinyLlama (1.1B) with all features intact.
    Runs on laptops without GPU while keeping public methods identical.
    Now includes safe fallbacks if model fails to load.
    """
    def __init__(self, model_name: str | None = None):
        # Use TinyLlama by default
        self.model_name = model_name or "TinyLlama/TinyLlama-1.1B-Chat-v1.0"

        # Force CPU on laptops without CUDA
        self.device = "cpu"

        self.model = None
        self.tokenizer = None
        self.pipeline = None
        self.model_loaded = False

        # HuggingFace login (optional)
        self._setup_huggingface_auth()

    def _setup_huggingface_auth(self):
        """Optional: use HF token if set, otherwise skip."""
        try:
            from huggingface_hub import login
            hf_token = os.getenv("HUGGINGFACE_TOKEN")
            if hf_token and hf_token.strip():
                logger.info("Using Hugging Face token for authentication")
                login(token=hf_token)
            else:
                logger.info("No Hugging Face token provided (public model access)")
        except Exception as e:
            logger.warning(f"Hugging Face authentication skipped/failed: {e}")

    def _ensure_model_loaded(self):
        if not self.model_loaded:
            self._initialize_model()

    def _initialize_model(self):
        """Load TinyLlama on CPU with minimal RAM footprint."""
        try:
            logger.info(f"Loading local CPU model: {self.model_name}")

            # Tokenizer
            self.tokenizer = AutoTokenizer.from_pretrained(
                self.model_name,
                use_fast=True
            )

            # Model
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_name,
                torch_dtype=torch.float32,
                low_cpu_mem_usage=True
            )

            # Text-generation pipeline
            self.pipeline = pipeline(
                "text-generation",
                model=self.model,
                tokenizer=self.tokenizer,
                device=-1  # CPU
            )

            # Ensure pad token
            if self.pipeline.tokenizer.pad_token_id is None:
                self.pipeline.tokenizer.pad_token = self.pipeline.tokenizer.eos_token

            logger.info("TinyLlama model loaded successfully on CPU.")
            self.model_loaded = True

        except Exception as e:
            logger.exception(f"Error loading model: {e}")
            self.model_loaded = False

    def test_connection(self) -> bool:
        """Test if the model is loaded and working"""
        try:
            self._ensure_model_loaded()
            if self.model_loaded and self.pipeline:
                # Quick test generation
                test_result = self.generate_response("Hello", max_length=10)
                return len(test_result) > 0
            return False
        except Exception as e:
            logger.error(f"Connection test failed: {e}")
            return False

    def generate_response(self, prompt: str, max_length: int = 512, temperature: float = 0.7) -> str:
        """
        General-purpose chat-like response generator.
        Works for questions, summaries, explanations, etc.
        Falls back to stub text if model not available.
        """
        try:
            self._ensure_model_loaded()
            if not self.model_loaded or not self.pipeline:
                logger.warning("Granite LLM not available — using fallback.")
                return self._generate_fallback_response(prompt)

            # Chat-style formatted prompt
            formatted_prompt = f"<|user|>\n{prompt}\n<|assistant|>\n"

            outputs = self.pipeline(
                formatted_prompt,
                max_new_tokens=min(max_length, 200),
                temperature=temperature,
                do_sample=True,
                top_p=0.9,
                repetition_penalty=1.05,
                pad_token_id=self.tokenizer.eos_token_id,
                num_return_sequences=1
            )

            full = outputs[0]["generated_text"]
            response = full.split("<|assistant|>\n")[-1].strip()

            if not response or len(response) < 5:
                return "I'm ready to help! Could you please provide more detail in your question?"

            return response

        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return self._generate_fallback_response(prompt)

    def _generate_fallback_response(self, prompt: str) -> str:
        """Generate rule-based fallback response when AI is unavailable"""
        prompt_lower = prompt.lower()
        
        if "simplify" in prompt_lower:
            return "This clause discusses legal terms and conditions. For precise legal interpretation, please consult a legal professional."
        elif "classify" in prompt_lower:
            return "This appears to be a legal document. Please review the content for specific classification."
        elif "entities" in prompt_lower:
            return "Legal entities and important information can be found throughout the document. Please review carefully."
        elif "question" in prompt_lower or "?" in prompt:
            return "Based on the document content provided, please review the relevant sections for detailed information."
        else:
            return "I'm ready to help with legal document analysis. Please provide more specific details about what you need."

    # ---- Enhanced Public Methods for Frontend Integration ----

    def simplify_clause(self, clause: str) -> str:
        """
        Simplify a legal clause into plain English
        Returns string directly (not dict) to match frontend expectations
        """
        prompt = (
            "Simplify the following legal clause into plain English that anyone can understand. "
            "Make it clear and concise:\n\n"
            f"Legal clause: {clause}\n\n"
            "Simplified explanation:"
        )
        
        try:
            result = self.generate_response(prompt, max_length=300)
            # Clean up the result
            if result.startswith("Simplified explanation:"):
                result = result.replace("Simplified explanation:", "").strip()
            return result
        except Exception as e:
            logger.error(f"Error in simplify_clause: {e}")
            return f"This clause contains legal terminology that requires interpretation. Original text: {clause[:200]}..."

    def extract_entities_with_ai(self, text: str) -> dict:
        """
        Extract legal entities using AI
        Returns dict with categorized entities to match frontend expectations
        """
        prompt = (
            "Extract important legal entities from the following text and categorize them. "
            "Focus on: parties (people/companies), dates, monetary amounts, obligations, and legal terms.\n\n"
            f"Text: {text}\n\n"
            "Extracted entities (categorized):"
        )
        
        try:
            result = self.generate_response(prompt, max_length=400)
            
            # Try to parse structured response or create basic structure
            entities = {
                "parties": [],
                "dates": [], 
                "monetary_values": [],
                "obligations": [],
                "legal_terms": []
            }
            
            # Basic parsing of the AI response
            lines = result.split('\n')
            current_category = None
            
            for line in lines:
                line = line.strip()
                if any(cat in line.lower() for cat in entities.keys()):
                    for cat in entities.keys():
                        if cat.replace('_', ' ') in line.lower() or cat in line.lower():
                            current_category = cat
                            break
                elif line and current_category and not line.startswith('*'):
                    # Clean the line and add to current category
                    clean_line = re.sub(r'^[-*•]\s*', '', line).strip()
                    if clean_line and len(clean_line) > 2:
                        entities[current_category].append(clean_line)
            
            # Fallback: extract some basic patterns if AI parsing failed
            if all(len(v) == 0 for v in entities.values()):
                entities = self._extract_entities_fallback(text)
            
            return entities
            
        except Exception as e:
            logger.error(f"Error in extract_entities_with_ai: {e}")
            return self._extract_entities_fallback(text)

    def _extract_entities_fallback(self, text: str) -> dict:
        """Fallback entity extraction using regex patterns"""
        entities = {
            "parties": [],
            "dates": [],
            "monetary_values": [],
            "obligations": [],
            "legal_terms": []
        }
        
        try:
            # Extract parties (names and companies)
            party_patterns = [
                r'\b[A-Z][a-z]+ [A-Z][a-z]+\b',  # Person names
                r'\b[A-Z][A-Z\s&]+(?:LLC|Inc|Corp|Company|Ltd)\b'  # Company names
            ]
            
            for pattern in party_patterns:
                matches = re.findall(pattern, text)
                entities["parties"].extend(matches[:3])
            
            # Extract dates
            date_patterns = [
                r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b',
                r'\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}\b'
            ]
            
            for pattern in date_patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                entities["dates"].extend(matches[:3])
            
            # Extract monetary values
            money_patterns = [
                r'\$[\d,]+(?:\.\d{2})?',
                r'\b\d+(?:,\d{3})*(?:\.\d{2})?\s*dollars?\b'
            ]
            
            for pattern in money_patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                entities["monetary_values"].extend(matches[:3])
            
            # Extract basic legal terms
            legal_terms = ['confidential', 'liability', 'breach', 'termination', 'agreement', 'contract']
            for term in legal_terms:
                if re.search(r'\b' + term + r'\b', text, re.IGNORECASE):
                    entities["legal_terms"].append(term.title())
            
        except Exception as e:
            logger.error(f"Fallback entity extraction failed: {e}")
        
        return entities

    def classify_document_with_ai(self, text: str) -> dict:
        """
        Classify document type using AI
        Returns dict with classification details to match frontend expectations  
        """
        prompt = (
            "Classify this legal document. Determine the document type, confidence level, "
            "and key characteristics. Choose from: NDA, Employment Contract, Service Agreement, "
            "Lease Agreement, Purchase Agreement, Partnership Agreement, License Agreement, "
            "Terms of Service, Privacy Policy, or General Legal Document.\n\n"
            f"Document text: {text}\n\n"
            "Classification:"
        )
        
        try:
            result = self.generate_response(prompt, max_length=300)
            
            # Parse the AI response to extract classification details
            classification = {
                "type": "General Legal Document",
                "confidence": 0.5,
                "description": "AI-classified legal document",
                "key_characteristics": []
            }
            
            # Extract document type from result
            doc_types = ["NDA", "Employment Contract", "Service Agreement", "Lease Agreement", 
                        "Purchase Agreement", "Partnership Agreement", "License Agreement",
                        "Terms of Service", "Privacy Policy"]
            
            result_lower = result.lower()
            for doc_type in doc_types:
                if doc_type.lower() in result_lower:
                    classification["type"] = doc_type
                    classification["confidence"] = 0.7
                    break
            
            # Extract characteristics from the result
            characteristics = []
            if "confidential" in result_lower:
                characteristics.append("Contains confidentiality clauses")
            if "employment" in result_lower:
                characteristics.append("Employment-related terms")
            if "service" in result_lower:
                characteristics.append("Service delivery terms")
            if "payment" in result_lower or "fee" in result_lower:
                characteristics.append("Financial obligations")
            
            classification["key_characteristics"] = characteristics[:4]
            
            return classification
            
        except Exception as e:
            logger.error(f"Error in classify_document_with_ai: {e}")
            return {
                "type": "General Legal Document", 
                "confidence": 0.3,
                "description": "Document classification unavailable",
                "key_characteristics": ["Contains legal content"]
            }

    def answer_question(self, question: str, context: str) -> str:
        """
        Answer questions about legal documents
        Returns string directly to match frontend expectations
        """
        prompt = (
            f"Based on the following legal document, answer this question clearly and concisely:\n\n"
            f"Document: {context}\n\n"
            f"Question: {question}\n\n"
            f"Answer:"
        )
        
        try:
            result = self.generate_response(prompt, max_length=400)
            
            # Clean up the result
            if result.startswith("Answer:"):
                result = result.replace("Answer:", "").strip()
            
            if not result or len(result) < 10:
                return "I need more context to provide a specific answer to your question. Please review the document sections relevant to your inquiry."
            
            return result
            
        except Exception as e:
            logger.error(f"Error in answer_question: {e}")
            return "I encountered an issue while analyzing your question. Please try rephrasing your question or provide more specific details."

# Global instance
granite_service = None

def get_granite_service() -> "GraniteLLMService":
    """Get the global Granite service instance"""
    global granite_service
    if granite_service is None:
        granite_service = GraniteLLMService()
    return granite_service