# import streamlit as st
# import requests
# import time

# # Page configuration with wide layout for better responsiveness
# st.set_page_config(
#     page_title="ClauseWise: Legal Document Analyzer", 
#     page_icon="⚖️",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# # Custom CSS for better styling
# st.markdown("""
# <style>
#     .main-header {
#         text-align: center;
#         padding: 1rem 0;
#         color: #1f4e79;
#         border-bottom: 2px solid #e6f3ff;
#         margin-bottom: 2rem;
#     }
    
#     .upload-section {
#         background: #f8fcff;
#         padding: 1.5rem;
#         border-radius: 10px;
#         border: 1px solid #e1ecf4;
#         margin-bottom: 1rem;
#     }
    
#     .result-section {
#         background: #ffffff;
#         padding: 1.5rem;
#         border-radius: 10px;
#         border: 1px solid #d1d5db;
#         margin: 1rem 0;
#     }
    
#     .stButton > button {
#         width: 100%;
#         background: linear-gradient(90deg, #1f4e79, #2563eb);
#         color: white;
#         border: none;
#         border-radius: 5px;
#         padding: 0.5rem 1rem;
#         font-weight: 600;
#         transition: all 0.3s ease;
#     }
    
#     .stButton > button:hover {
#         background: linear-gradient(90deg, #1e40af, #1d4ed8);
#         transform: translateY(-1px);
#     }
    
#     .sidebar-info {
#         background: #f0f9ff;
#         padding: 1rem;
#         border-radius: 8px;
#         border-left: 4px solid #0ea5e9;
#     }
    
#     .metric-card {
#         background: white;
#         padding: 1rem;
#         border-radius: 8px;
#         box-shadow: 0 2px 4px rgba(0,0,0,0.1);
#         text-align: center;
#     }
# </style>
# """, unsafe_allow_html=True)

# # Header
# st.markdown('<h1 class="main-header">⚖️ ClauseWise: Legal Document Analyzer</h1>', unsafe_allow_html=True)
# st.markdown('<p style="text-align: center; color: #6b7280; margin-bottom: 2rem; font-style: italic;">Powered by IBM Watson & Granite AI</p>', unsafe_allow_html=True)

# # Sidebar for app info and settings
# with st.sidebar:
#     st.markdown('<div class="sidebar-info">', unsafe_allow_html=True)
#     st.markdown("### 🎯 ClauseWise Features")
#     st.markdown("""
#     - 📄 **Multi-Format Support**: PDF, DOCX, TXT
#     - 🔍 **Clause Extraction**: Automated breakdown
#     - ✨ **Clause Simplification**: Layman-friendly language
#     - 🏷️ **Named Entity Recognition**: Extract key entities
#     - 📂 **Document Classification**: Contract type detection
#     - ❓ **Document Analysis**: AI-powered Q&A
#     """)
#     st.markdown('</div>', unsafe_allow_html=True)
    
#     st.markdown("---")
#     st.markdown("### ⚙️ Analysis Settings")
#     show_raw_text = st.checkbox("Show extracted text", value=True)
#     auto_simplify = st.checkbox("Auto-simplify clauses", value=False)
#     extract_entities = st.checkbox("Extract named entities", value=True)
#     classify_document = st.checkbox("Classify document type", value=True)
    
#     st.markdown("---")
#     st.markdown("### 🤖 AI Model Status")
    
#     # Check AI model status
#     try:
#         model_status_resp = requests.get("http://localhost:8000/", timeout=5)
#         if model_status_resp.ok:
#             st.success("✅ Backend connected")
#         else:
#             st.error("❌ Backend error")
#     except:
#         st.error("❌ Backend offline")
    
#     st.info("💡 **First AI request may take 2-5 minutes as the model loads**")

# # Main content area
# col1, col2 = st.columns([2, 1])

# with col1:
#     # Upload section
#     st.markdown('<div class="upload-section">', unsafe_allow_html=True)
#     st.markdown("### 📤 Upload Document")
#     uploaded = st.file_uploader(
#         "Choose a legal document", 
#         type=["pdf", "docx", "txt"],
#         help="Supported formats: PDF, DOCX, TXT (max 200MB)"
#     )
#     st.markdown('</div>', unsafe_allow_html=True)

# with col2:
#     # Status/Info panel
#     st.markdown('<div class="metric-card">', unsafe_allow_html=True)
#     st.markdown("### 📊 Status")
#     if uploaded:
#         st.success("✅ Document uploaded")
#         st.metric("File size", f"{len(uploaded.getvalue())/1024:.1f} KB")
#         st.metric("File type", uploaded.type or "Unknown")
#     else:
#         st.info("🔄 Waiting for upload")
#     st.markdown('</div>', unsafe_allow_html=True)

# if uploaded:
#     # Progress indicator
#     progress_bar = st.progress(0)
#     status_text = st.empty()
    
#     files = {"file": (uploaded.name, uploaded.getvalue())}
    
#     try:
#         # Update progress
#         progress_bar.progress(25)
#         status_text.text("🔄 Uploading document...")
        
#         resp = requests.post("http://localhost:8000/upload/", files=files, timeout=30)
        
#         progress_bar.progress(75)
#         status_text.text("📝 Processing document...")
        
#         if resp.ok:
#             progress_bar.progress(100)
#             status_text.text("✅ Document processed successfully!")
#             time.sleep(1)
#             progress_bar.empty()
#             status_text.empty()
            
#             text = resp.json().get("text", "")
            
#             # Create tabs for ClauseWise features
#             tab1, tab2, tab3, tab4, tab5 = st.tabs([
#                 "📄 Extracted Text", 
#                 "🔍 Clause Breakdown", 
#                 "✨ Simplified Clauses", 
#                 "🏷️ Named Entities",
#                 "📂 Document Classification"
#             ])
            
#             with tab1:
#                 if show_raw_text:
#                     st.markdown('<div class="result-section">', unsafe_allow_html=True)
#                     st.markdown("### 📄 Extracted Text")
#                     # Text statistics
#                     char_count = len(text)
#                     word_count = len(text.split())
#                     col_a, col_b = st.columns(2)
#                     with col_a:
#                         st.metric("Characters", f"{char_count:,}")
#                     with col_b:
#                         st.metric("Words", f"{word_count:,}")
                    
#                     # Text area with better height management
#                     height = min(max(300, len(text) // 50), 600)
#                     st.text_area("Document content", text, height=height, label_visibility="collapsed")
#                     st.markdown('</div>', unsafe_allow_html=True)
            
#             with tab2:
#                 st.markdown('<div class="result-section">', unsafe_allow_html=True)
#                 st.markdown("### 🔍 Clause Extraction & Breakdown")
                
#                 col_btn1, col_btn2 = st.columns([1, 3])
#                 with col_btn1:
#                     extract_clicked = st.button("🔍 Extract Clauses", key="extract_btn")
                
#                 if extract_clicked:
#                     with st.spinner("🔄 AI is extracting clauses..."):
#                         # This will be implemented with IBM Watson/Granite
#                         extract_resp = requests.post("http://localhost:8000/extract-clauses/", json={"text": text}, timeout=30)
#                         if extract_resp.ok:
#                             clauses = extract_resp.json().get("clauses", [])
                            
#                             if clauses:
#                                 st.success(f"✅ Extracted {len(clauses)} clauses")
#                                 for i, clause in enumerate(clauses, 1):
#                                     with st.expander(f"📝 Clause {i}", expanded=i<=2):
#                                         st.write(clause)
#                             else:
#                                 st.warning("⚠️ No distinct clauses found")
#                         else:
#                             st.error("❌ Failed to extract clauses")
                
#                 st.markdown('</div>', unsafe_allow_html=True)
            
#             with tab3:
#                 st.markdown('<div class="result-section">', unsafe_allow_html=True)
#                 st.markdown("### ✨ Clause Simplification")
#                 st.markdown("*Converting complex legal language into layman-friendly terms*")
                
#                 col_btn1, col_btn2 = st.columns([1, 3])
#                 with col_btn1:
#                     simplify_clicked = st.button("🚀 Simplify Clauses", key="simplify_btn")
                
#                 if simplify_clicked or auto_simplify:
#                     with st.spinner("🔄 AI is simplifying clauses..."):
#                         try:
#                             simplify_resp = requests.post(
#                                 "http://localhost:8000/simplify/", 
#                                 json={"text": text}, 
#                                 timeout=90  # Increased timeout
#                             )
#                             if simplify_resp.ok:
#                                 simplified_clauses = simplify_resp.json().get("simplified_clauses", [])
                                
#                                 if simplified_clauses:
#                                     st.success(f"✅ Simplified {len(simplified_clauses)} clauses")
#                                     for i, clause_pair in enumerate(simplified_clauses, 1):
#                                         with st.expander(f"📝 Simplified Clause {i}", expanded=i<=2):
#                                             if isinstance(clause_pair, dict):
#                                                 st.markdown("**Original:**")
#                                                 st.write(clause_pair.get("original", ""))
#                                                 st.markdown("**Simplified:**")
#                                                 st.success(clause_pair.get("simplified", ""))
#                                             else:
#                                                 st.write(clause_pair)
#                                 else:
#                                     st.warning("⚠️ No clauses found to simplify")
#                             else:
#                                 st.error("❌ Failed to simplify clauses")
#                         except requests.exceptions.Timeout:
#                             st.warning("⏱️ Clause simplification is taking longer than expected. The AI model may be loading for the first time.")
#                         except Exception as e:
#                             st.error(f"❌ Error: {e}")
#                 st.markdown('</div>', unsafe_allow_html=True)
            
#             with tab4:
#                 st.markdown('<div class="result-section">', unsafe_allow_html=True)
#                 st.markdown("### 🏷️ Named Entity Recognition")
#                 st.markdown("*Extracting parties, dates, obligations, and monetary values*")
                
#                 col_btn1, col_btn2 = st.columns([1, 3])
#                 with col_btn1:
#                     ner_clicked = st.button("🔍 Extract Entities", key="ner_btn")
                
#                 if ner_clicked or extract_entities:
#                     with st.spinner("🔄 AI is extracting entities..."):
#                         try:
#                             ner_resp = requests.post(
#                                 "http://localhost:8000/entities/", 
#                                 json={"text": text}, 
#                                 timeout=90  # Increased timeout
#                             )
#                             if ner_resp.ok:
#                                 entities = ner_resp.json().get("entities", {})
                                
#                                 if entities:
#                                     st.success("✅ Named entities extracted")
                                    
#                                     # Display entities in organized columns
#                                     col_e1, col_e2 = st.columns(2)
                                    
#                                     with col_e1:
#                                         if entities.get("parties"):
#                                             st.markdown("**👥 Parties:**")
#                                             for party in entities["parties"]:
#                                                 st.write(f"• {party}")
                                        
#                                         if entities.get("dates"):
#                                             st.markdown("**📅 Dates:**")
#                                             for date in entities["dates"]:
#                                                 st.write(f"• {date}")
                                    
#                                     with col_e2:
#                                         if entities.get("monetary_values"):
#                                             st.markdown("**💰 Monetary Values:**")
#                                             for value in entities["monetary_values"]:
#                                                 st.write(f"• {value}")
                                        
#                                         if entities.get("obligations"):
#                                             st.markdown("**📋 Obligations:**")
#                                             for obligation in entities["obligations"]:
#                                                 st.write(f"• {obligation}")
#                                 else:
#                                     st.warning("⚠️ No named entities found")
#                             else:
#                                 st.error("❌ Failed to extract entities")
#                         except requests.exceptions.Timeout:
#                             st.warning("⏱️ Entity extraction is taking longer than expected. The AI model may be loading for the first time.")
#                         except Exception as e:
#                             st.error(f"❌ Error: {e}")
                
#                 st.markdown('</div>', unsafe_allow_html=True)
            
#             with tab5:
#                 st.markdown('<div class="result-section">', unsafe_allow_html=True)
#                 st.markdown("### 📂 Document Type Classification")
#                 st.markdown("*Identifying contract type: NDA, lease, employment, service agreement, etc.*")
                
#                 col_btn1, col_btn2 = st.columns([1, 3])
#                 with col_btn1:
#                     classify_clicked = st.button("🔍 Classify Document", key="classify_btn")
                
#                 if classify_clicked or classify_document:
#                     with st.spinner("🔄 AI is classifying document..."):
#                         try:
#                             classify_resp = requests.post(
#                                 "http://localhost:8000/classify/", 
#                                 json={"text": text}, 
#                                 timeout=90  # Increased timeout
#                             )
#                             if classify_resp.ok:
#                                 classification = classify_resp.json().get("classification", {})
                                
#                                 if classification:
#                                     document_type = classification.get("type", "Unknown")
#                                     confidence = classification.get("confidence", 0)
                                    
#                                     st.success(f"✅ Document classified")
                                    
#                                     # Display classification results
#                                     col_c1, col_c2 = st.columns(2)
#                                     with col_c1:
#                                         st.metric("Document Type", document_type)
#                                     with col_c2:
#                                         st.metric("Confidence", f"{confidence:.1%}")
                                    
#                                     # Additional details
#                                     if classification.get("description"):
#                                         st.info(f"**Description:** {classification['description']}")
                                    
#                                     if classification.get("key_characteristics"):
#                                         st.markdown("**Key Characteristics:**")
#                                         for char in classification["key_characteristics"]:
#                                             st.write(f"• {char}")
#                                 else:
#                                     st.warning("⚠️ Unable to classify document")
#                             else:
#                                 st.error("❌ Failed to classify document")
#                         except requests.exceptions.Timeout:
#                             st.warning("⏱️ Document classification is taking longer than expected. The AI model may be loading for the first time.")
#                         except Exception as e:
#                             st.error(f"❌ Error: {e}")
                
#                 st.markdown('</div>', unsafe_allow_html=True)
                
#         else:
#             progress_bar.empty()
#             status_text.empty()
#             st.error(f"❌ Upload failed: {resp.text}")
            
#     except requests.exceptions.Timeout:
#         progress_bar.empty()
#         status_text.empty()
#         st.error("⏱️ Request timed out. Please try again.")
#     except Exception as e:
#         progress_bar.empty()
#         status_text.empty()
#         st.error(f"❌ Error: {e}")

# # Document Analysis Q&A Section
# st.markdown("---")
# st.markdown('<div class="result-section">', unsafe_allow_html=True)
# st.markdown("### ❓ ClauseWise AI Assistant")
# st.markdown("*Ask questions about legal concepts, document analysis, or specific clauses*")

# general_question = st.text_input(
#     "Ask ClauseWise AI", 
#     placeholder="e.g., What are the key obligations in this contract? Who are the parties involved?",
#     key="general_q"
# )

# col_g1, col_g2 = st.columns([1, 3])
# with col_g1:
#     general_ask = st.button("🔍 Analyze", key="general_ask_btn", disabled=not general_question)

# if general_ask and general_question:
#     with st.spinner("🤔 ClauseWise AI is analyzing..."):
#         try:
#             # Increase timeout for AI processing
#             qresp = requests.post(
#                 "http://localhost:8000/query/", 
#                 json={"question": general_question}, 
#                 timeout=120  # Increased to 2 minutes for model loading
#             )
#             if qresp.ok:
#                 answer = qresp.json().get("answer", "")
#                 st.markdown("#### 💡 ClauseWise Analysis:")
#                 st.success(answer)
#             else:
#                 st.error("❌ Analysis failed")
#         except requests.exceptions.Timeout:
#             st.warning("⏱️ The AI model is taking longer than expected. This may be the first time loading the model (which can take 2-5 minutes). Please try again in a few moments.")
#         except Exception as e:
#             st.error(f"❌ Error: {e}")

# st.markdown('</div>', unsafe_allow_html=True)







# import streamlit as st
# import requests
# import time

# # Page configuration with wide layout for better responsiveness
# st.set_page_config(
#     page_title="ClauseWise: Legal Document Analyzer", 
#     page_icon="⚖️",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# # API Configuration - Fixed to match your backend URL
# API_BASE_URL = "http://127.0.0.1:8000"  # Changed from localhost to 127.0.0.1

# # Custom CSS for better styling
# st.markdown("""
# <style>
#     .main-header {
#         text-align: center;
#         padding: 1rem 0;
#         color: #1f4e79;
#         border-bottom: 2px solid #e6f3ff;
#         margin-bottom: 2rem;
#     }
    
#     .upload-section {
#         background: #f8fcff;
#         padding: 1.5rem;
#         border-radius: 10px;
#         border: 1px solid #e1ecf4;
#         margin-bottom: 1rem;
#     }
    
#     .result-section {
#         background: #ffffff;
#         padding: 1.5rem;
#         border-radius: 10px;
#         border: 1px solid #d1d5db;
#         margin: 1rem 0;
#     }
    
#     .stButton > button {
#         width: 100%;
#         background: linear-gradient(90deg, #1f4e79, #2563eb);
#         color: white;
#         border: none;
#         border-radius: 5px;
#         padding: 0.5rem 1rem;
#         font-weight: 600;
#         transition: all 0.3s ease;
#     }
    
#     .stButton > button:hover {
#         background: linear-gradient(90deg, #1e40af, #1d4ed8);
#         transform: translateY(-1px);
#     }
    
#     .sidebar-info {
#         background: #f0f9ff;
#         padding: 1rem;
#         border-radius: 8px;
#         border-left: 4px solid #0ea5e9;
#     }
    
#     .metric-card {
#         background: white;
#         padding: 1rem;
#         border-radius: 8px;
#         box-shadow: 0 2px 4px rgba(0,0,0,0.1);
#         text-align: center;
#     }
    
#     .warning-box {
#         background: #fef3c7;
#         border: 1px solid #f59e0b;
#         border-radius: 8px;
#         padding: 1rem;
#         margin: 1rem 0;
#     }
# </style>
# """, unsafe_allow_html=True)

# # Header
# st.markdown('<h1 class="main-header">⚖️ ClauseWise: Legal Document Analyzer</h1>', unsafe_allow_html=True)
# st.markdown('<p style="text-align: center; color: #6b7280; margin-bottom: 2rem; font-style: italic;">Powered by IBM Watson & Granite AI</p>', unsafe_allow_html=True)

# # Sidebar for app info and settings
# with st.sidebar:
#     st.markdown('<div class="sidebar-info">', unsafe_allow_html=True)
#     st.markdown("### 🎯 ClauseWise Features")
#     st.markdown("""
#     - 📄 **Multi-Format Support**: PDF, DOCX, TXT
#     - 🔍 **Clause Extraction**: Automated breakdown
#     - ✨ **Clause Simplification**: Layman-friendly language
#     - 🏷️ **Named Entity Recognition**: Extract key entities
#     - 📂 **Document Classification**: Contract type detection
#     - ❓ **Document Analysis**: AI-powered Q&A
#     """)
#     st.markdown('</div>', unsafe_allow_html=True)
    
#     st.markdown("---")
#     st.markdown("### ⚙️ Analysis Settings")
#     show_raw_text = st.checkbox("Show extracted text", value=True)
#     auto_simplify = st.checkbox("Auto-simplify clauses", value=False)
#     extract_entities = st.checkbox("Extract named entities", value=True)
#     classify_document = st.checkbox("Classify document type", value=True)
    
#     st.markdown("---")
#     st.markdown("### 🤖 AI Model Status")
    
#     # Enhanced backend connection test
#     try:
#         model_status_resp = requests.get(f"{API_BASE_URL}/", timeout=5)
#         if model_status_resp.ok:
#             st.success("✅ Backend connected")
#         else:
#             st.error("❌ Backend error")
#     except requests.exceptions.ConnectionError:
#         st.error("❌ Backend offline - Check if uvicorn is running")
#         st.code("uvicorn backend.main:app --host 127.0.0.1 --port 8000")
#     except requests.exceptions.Timeout:
#         st.warning("⚠️ Backend timeout")
#     except Exception as e:
#         st.error(f"❌ Connection error: {str(e)}")
    
#     st.info("💡 **First AI request may take 2-5 minutes as the model loads**")

# # Enhanced API call function with better error handling
# def make_api_request(endpoint, data=None, files=None, timeout=90):
#     """Enhanced API request function with consistent error handling"""
#     try:
#         if files:
#             response = requests.post(f"{API_BASE_URL}{endpoint}", files=files, timeout=timeout)
#         else:
#             response = requests.post(f"{API_BASE_URL}{endpoint}", json=data, timeout=timeout)
        
#         response.raise_for_status()  # Raises an HTTPError for bad responses
#         return response, None
        
#     except requests.exceptions.Timeout:
#         error_msg = "⏱️ Request timed out. The AI model may be loading for the first time (this can take 2-5 minutes). Please try again."
#         return None, error_msg
#     except requests.exceptions.ConnectionError:
#         error_msg = "❌ Cannot connect to backend. Please ensure the backend server is running."
#         return None, error_msg
#     except requests.exceptions.HTTPError as e:
#         error_msg = f"❌ Server error: {e.response.status_code}"
#         return None, error_msg
#     except Exception as e:
#         error_msg = f"❌ Unexpected error: {str(e)}"
#         return None, error_msg

# # Main content area
# col1, col2 = st.columns([2, 1])

# with col1:
#     # Upload section
#     st.markdown('<div class="upload-section">', unsafe_allow_html=True)
#     st.markdown("### 📤 Upload Document")
#     uploaded = st.file_uploader(
#         "Choose a legal document", 
#         type=["pdf", "docx", "txt"],
#         help="Supported formats: PDF, DOCX, TXT (max 200MB)"
#     )
#     st.markdown('</div>', unsafe_allow_html=True)

# with col2:
#     # Status/Info panel
#     st.markdown('<div class="metric-card">', unsafe_allow_html=True)
#     st.markdown("### 📊 Status")
#     if uploaded:
#         st.success("✅ Document uploaded")
#         st.metric("File size", f"{len(uploaded.getvalue())/1024:.1f} KB")
#         st.metric("File type", uploaded.type or "Unknown")
#     else:
#         st.info("🔄 Waiting for upload")
#     st.markdown('</div>', unsafe_allow_html=True)

# if uploaded:
#     # Progress indicator
#     progress_bar = st.progress(0)
#     status_text = st.empty()
    
#     files = {"file": (uploaded.name, uploaded.getvalue())}
    
#     # Update progress
#     progress_bar.progress(25)
#     status_text.text("🔄 Uploading document...")
    
#     # Enhanced upload with better error handling
#     upload_response, upload_error = make_api_request("/upload/", files=files, timeout=30)
    
#     if upload_response and upload_response.ok:
#         progress_bar.progress(75)
#         status_text.text("📝 Processing document...")
        
#         progress_bar.progress(100)
#         status_text.text("✅ Document processed successfully!")
#         time.sleep(1)
#         progress_bar.empty()
#         status_text.empty()
        
#         text = upload_response.json().get("text", "")
        
#         # Create tabs for ClauseWise features
#         tab1, tab2, tab3, tab4, tab5 = st.tabs([
#             "📄 Extracted Text", 
#             "🔍 Clause Breakdown", 
#             "✨ Simplified Clauses", 
#             "🏷️ Named Entities",
#             "📂 Document Classification"
#         ])
        
#         with tab1:
#             if show_raw_text:
#                 st.markdown('<div class="result-section">', unsafe_allow_html=True)
#                 st.markdown("### 📄 Extracted Text")
#                 # Text statistics
#                 char_count = len(text)
#                 word_count = len(text.split())
#                 col_a, col_b = st.columns(2)
#                 with col_a:
#                     st.metric("Characters", f"{char_count:,}")
#                 with col_b:
#                     st.metric("Words", f"{word_count:,}")
                
#                 # Text area with better height management
#                 height = min(max(300, len(text) // 50), 600)
#                 st.text_area("Document content", text, height=height, label_visibility="collapsed")
#                 st.markdown('</div>', unsafe_allow_html=True)
        
#         with tab2:
#             st.markdown('<div class="result-section">', unsafe_allow_html=True)
#             st.markdown("### 🔍 Clause Extraction & Breakdown")
            
#             col_btn1, col_btn2 = st.columns([1, 3])
#             with col_btn1:
#                 extract_clicked = st.button("🔍 Extract Clauses", key="extract_btn")
            
#             if extract_clicked:
#                 with st.spinner("🔄 AI is extracting clauses..."):
#                     extract_response, extract_error = make_api_request("/extract-clauses/", {"text": text})
                    
#                     if extract_response and extract_response.ok:
#                         clauses = extract_response.json().get("clauses", [])
                        
#                         if clauses:
#                             st.success(f"✅ Extracted {len(clauses)} clauses")
#                             for i, clause in enumerate(clauses, 1):
#                                 with st.expander(f"📝 Clause {i}", expanded=i<=2):
#                                     st.write(clause)
#                         else:
#                             st.warning("⚠️ No distinct clauses found")
#                     else:
#                         st.error(extract_error or "❌ Failed to extract clauses")
            
#             st.markdown('</div>', unsafe_allow_html=True)
        
#         with tab3:
#             st.markdown('<div class="result-section">', unsafe_allow_html=True)
#             st.markdown("### ✨ Clause Simplification")
#             st.markdown("*Converting complex legal language into layman-friendly terms*")
            
#             # Add model loading warning
#             st.markdown('<div class="warning-box">', unsafe_allow_html=True)
#             st.markdown("⚠️ **First-time model loading**: The simplification process may take 2-5 minutes when the AI model loads for the first time.")
#             st.markdown('</div>', unsafe_allow_html=True)
            
#             col_btn1, col_btn2 = st.columns([1, 3])
#             with col_btn1:
#                 simplify_clicked = st.button("🚀 Simplify Clauses", key="simplify_btn")
            
#             if simplify_clicked or auto_simplify:
#                 with st.spinner("🔄 AI is simplifying clauses... This may take a few minutes on first load."):
#                     simplify_response, simplify_error = make_api_request("/simplify/", {"text": text}, timeout=180)  # 3 minutes timeout
                    
#                     if simplify_response and simplify_response.ok:
#                         simplified_clauses = simplify_response.json().get("simplified_clauses", [])
                        
#                         if simplified_clauses:
#                             st.success(f"✅ Simplified {len(simplified_clauses)} clauses")
#                             for i, clause_pair in enumerate(simplified_clauses, 1):
#                                 with st.expander(f"📝 Simplified Clause {i}", expanded=i<=2):
#                                     if isinstance(clause_pair, dict):
#                                         st.markdown("**Original:**")
#                                         st.write(clause_pair.get("original", ""))
#                                         st.markdown("**Simplified:**")
#                                         st.success(clause_pair.get("simplified", ""))
#                                     else:
#                                         st.write(clause_pair)
#                         else:
#                             st.warning("⚠️ No clauses found to simplify")
#                     else:
#                         st.error(simplify_error or "❌ Failed to simplify clauses")
            
#             st.markdown('</div>', unsafe_allow_html=True)
        
#         with tab4:
#             st.markdown('<div class="result-section">', unsafe_allow_html=True)
#             st.markdown("### 🏷️ Named Entity Recognition")
#             st.markdown("*Extracting parties, dates, obligations, and monetary values*")
            
#             col_btn1, col_btn2 = st.columns([1, 3])
#             with col_btn1:
#                 ner_clicked = st.button("🔍 Extract Entities", key="ner_btn")
            
#             if ner_clicked or extract_entities:
#                 with st.spinner("🔄 AI is extracting entities..."):
#                     ner_response, ner_error = make_api_request("/entities/", {"text": text})
                    
#                     if ner_response and ner_response.ok:
#                         entities = ner_response.json().get("entities", {})
                        
#                         if entities:
#                             st.success("✅ Named entities extracted")
                            
#                             # Display entities in organized columns
#                             col_e1, col_e2 = st.columns(2)
                            
#                             with col_e1:
#                                 if entities.get("parties"):
#                                     st.markdown("**👥 Parties:**")
#                                     for party in entities["parties"]:
#                                         st.write(f"• {party}")
                                
#                                 if entities.get("dates"):
#                                     st.markdown("**📅 Dates:**")
#                                     for date in entities["dates"]:
#                                         st.write(f"• {date}")
                            
#                             with col_e2:
#                                 if entities.get("monetary_values"):
#                                     st.markdown("**💰 Monetary Values:**")
#                                     for value in entities["monetary_values"]:
#                                         st.write(f"• {value}")
                                
#                                 if entities.get("obligations"):
#                                     st.markdown("**📋 Obligations:**")
#                                     for obligation in entities["obligations"]:
#                                         st.write(f"• {obligation}")
#                         else:
#                             st.warning("⚠️ No named entities found")
#                     else:
#                         st.error(ner_error or "❌ Failed to extract entities")
            
#             st.markdown('</div>', unsafe_allow_html=True)
        
#         with tab5:
#             st.markdown('<div class="result-section">', unsafe_allow_html=True)
#             st.markdown("### 📂 Document Type Classification")
#             st.markdown("*Identifying contract type: NDA, lease, employment, service agreement, etc.*")
            
#             col_btn1, col_btn2 = st.columns([1, 3])
#             with col_btn1:
#                 classify_clicked = st.button("🔍 Classify Document", key="classify_btn")
            
#             if classify_clicked or classify_document:
#                 with st.spinner("🔄 AI is classifying document..."):
#                     classify_response, classify_error = make_api_request("/classify/", {"text": text})
                    
#                     if classify_response and classify_response.ok:
#                         classification = classify_response.json().get("classification", {})
                        
#                         if classification:
#                             document_type = classification.get("type", "Unknown")
#                             confidence = classification.get("confidence", 0)
                            
#                             st.success(f"✅ Document classified")
                            
#                             # Display classification results
#                             col_c1, col_c2 = st.columns(2)
#                             with col_c1:
#                                 st.metric("Document Type", document_type)
#                             with col_c2:
#                                 st.metric("Confidence", f"{confidence:.1%}")
                            
#                             # Additional details
#                             if classification.get("description"):
#                                 st.info(f"**Description:** {classification['description']}")
                            
#                             if classification.get("key_characteristics"):
#                                 st.markdown("**Key Characteristics:**")
#                                 for char in classification["key_characteristics"]:
#                                     st.write(f"• {char}")
#                         else:
#                             st.warning("⚠️ Unable to classify document")
#                     else:
#                         st.error(classify_error or "❌ Failed to classify document")
            
#             st.markdown('</div>', unsafe_allow_html=True)
            
#     else:
#         progress_bar.empty()
#         status_text.empty()
#         st.error(upload_error or f"❌ Upload failed")

# # Document Analysis Q&A Section
# st.markdown("---")
# st.markdown('<div class="result-section">', unsafe_allow_html=True)
# st.markdown("### ❓ ClauseWise AI Assistant")
# st.markdown("*Ask questions about legal concepts, document analysis, or specific clauses*")

# general_question = st.text_input(
#     "Ask ClauseWise AI", 
#     placeholder="e.g., What are the key obligations in this contract? Who are the parties involved?",
#     key="general_q"
# )

# col_g1, col_g2 = st.columns([1, 3])
# with col_g1:
#     general_ask = st.button("🔍 Analyze", key="general_ask_btn", disabled=not general_question)

# if general_ask and general_question:
#     with st.spinner("🤔 ClauseWise AI is analyzing..."):
#         query_response, query_error = make_api_request("/query/", {"question": general_question}, timeout=120)
        
#         if query_response and query_response.ok:
#             answer = query_response.json().get("answer", "")
#             st.markdown("#### 💡 ClauseWise Analysis:")
#             st.success(answer)
#         else:
#             st.error(query_error or "❌ Analysis failed")

# st.markdown('</div>', unsafe_allow_html=True)




import streamlit as st
import requests
import time
import json
import random
from datetime import datetime
import base64

# Initialize session state for theme and other features
if 'theme' not in st.session_state:
    st.session_state.theme = 'dark'  # Start with dark theme for modern appeal
if 'uploaded_file' not in st.session_state:
    st.session_state.uploaded_file = None
if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = None
if 'connection_status' not in st.session_state:
    st.session_state.connection_status = 'online'

# Page config
st.set_page_config(
    page_title="ClauseWise: Legal Document Analyzer",
    page_icon="⚖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

def toggle_theme():
    st.session_state.theme = 'dark' if st.session_state.theme == 'light' else 'light'

# Enhanced theme configuration with modern colors
themes = {
    'light': {
        'bg_primary': '#fafbfc',
        'bg_secondary': '#ffffff',
        'bg_tertiary': '#f8fafc',
        'text_primary': '#0f172a',
        'text_secondary': '#64748b',
        'text_accent': '#6366f1',
        'border': '#e2e8f0',
        'card_bg': '#ffffff',
        'success': '#10b981',
        'warning': '#f59e0b',
        'error': '#ef4444',
        'info': '#3b82f6',
        'shadow': 'rgba(0, 0, 0, 0.08)',
        'gradient_start': '#6366f1',
        'gradient_end': '#8b5cf6',
        'gold_start': '#f59e0b',
        'gold_end': '#d97706',
        'accent_glow': 'rgba(99, 102, 241, 0.3)'
    },
    'dark': {
        'bg_primary': '#0a0a0a',
        'bg_secondary': '#111827',
        'bg_tertiary': '#1f2937',
        'text_primary': '#f8fafc',
        'text_secondary': '#94a3b8',
        'text_accent': '#818cf8',
        'border': '#374151',
        'card_bg': '#111827',
        'success': '#10b981',
        'warning': '#fbbf24',
        'error': '#f87171',
        'info': '#60a5fa',
        'shadow': 'rgba(0, 0, 0, 0.5)',
        'gradient_start': '#6366f1',
        'gradient_end': '#8b5cf6',
        'gold_start': '#fbbf24',
        'gold_end': '#f59e0b',
        'accent_glow': 'rgba(129, 140, 248, 0.4)'
    }
}

current_theme = themes[st.session_state.theme]

# Revolutionary CSS with advanced animations and glassmorphism
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&family=Lexend:wght@300;400;500;600;700&family=Poppins:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@300;400;500;600;700&display=swap');
    
    /* Global styles with smooth transitions */
    .stApp {{
        font-family: 'Inter', system-ui, -apple-system, sans-serif;
        background: {current_theme['bg_primary']};
        background-image: 
            radial-gradient(circle at 20% 50%, {current_theme['accent_glow']} 0%, transparent 50%),
            radial-gradient(circle at 80% 20%, rgba(139, 92, 246, 0.3) 0%, transparent 50%),
            radial-gradient(circle at 40% 80%, rgba(245, 158, 11, 0.2) 0%, transparent 50%),
            linear-gradient(135deg, transparent 0%, rgba(99, 102, 241, 0.03) 50%, transparent 100%);
        color: {current_theme['text_primary']};
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        min-height: 100vh;
        position: relative;
        overflow-x: hidden;
    }}
    
    /* Animated background particles */
    .stApp::before {{
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: 
            radial-gradient(2px 2px at 20px 30px, rgba(255,255,255,0.15), transparent),
            radial-gradient(2px 2px at 40px 70px, rgba(255,255,255,0.08), transparent),
            radial-gradient(1px 1px at 90px 40px, rgba(255,255,255,0.12), transparent),
            radial-gradient(3px 3px at 160px 120px, rgba(99, 102, 241, 0.1), transparent);
        background-size: 100px 100px, 120px 120px, 80px 80px, 200px 200px;
        animation: particleFloat 25s linear infinite;
        pointer-events: none;
        z-index: 1;
    }}
    
    @keyframes particleFloat {{
        from {{ transform: translateY(0px) rotate(0deg); }}
        to {{ transform: translateY(-120px) rotate(360deg); }}
    }}
    
    /* Hide Streamlit branding */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}
    .stDeployButton {{display: none;}}
    
    /* Revolutionary Logo Header with Holographic Effect */
    .logo-header {{
        padding: 5rem 0 4rem 0;
        text-align: center;
        position: relative;
        margin: -1rem -1rem 4rem -1rem;
        background: transparent;
        overflow: hidden;
        z-index: 10;
    }}
    
    .logo-container {{
        position: relative;
        display: inline-block;
        animation: logoFloat 10s ease-in-out infinite;
    }}
    
    .logo-scales {{
        font-size: 7rem;
        background: linear-gradient(135deg, {current_theme['gold_start']}, {current_theme['gold_end']}, {current_theme['gradient_start']}, {current_theme['gradient_end']});
        background-size: 300% 300%;
        background-clip: text;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        filter: drop-shadow(0 12px 24px rgba(251, 191, 36, 0.6)) drop-shadow(0 0 40px rgba(99, 102, 241, 0.4));
        position: relative;
        z-index: 3;
        animation: scalesShimmer 8s ease-in-out infinite, scalesPulse 6s ease-in-out infinite, scalesRotate 20s linear infinite;
    }}
    
    .logo-glow {{
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        width: 250px;
        height: 250px;
        background: radial-gradient(circle, {current_theme['accent_glow']}, rgba(139, 92, 246, 0.3), transparent 70%);
        border-radius: 50%;
        animation: logoGlow 8s ease-in-out infinite alternate;
        z-index: 1;
    }}
    
    .logo-rings {{
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        width: 350px;
        height: 350px;
        border: 2px solid rgba(99, 102, 241, 0.3);
        border-radius: 50%;
        animation: ringRotate 20s linear infinite;
        z-index: 1;
    }}
    
    .logo-rings::before {{
        content: '';
        position: absolute;
        top: -25px;
        left: -25px;
        width: calc(100% + 50px);
        height: calc(100% + 50px);
        border: 1px solid rgba(139, 92, 246, 0.2);
        border-radius: 50%;
        animation: ringRotate 30s linear infinite reverse;
    }}
    
    .logo-rings::after {{
        content: '';
        position: absolute;
        top: 15px;
        left: 15px;
        width: calc(100% - 30px);
        height: calc(100% - 30px);
        border: 1px dashed rgba(251, 191, 36, 0.3);
        border-radius: 50%;
        animation: ringRotate 15s linear infinite;
    }}
    
    @keyframes logoFloat {{
        0%, 100% {{ transform: translateY(0px) rotate(0deg) scale(1); }}
        25% {{ transform: translateY(-20px) rotate(2deg) scale(1.02); }}
        50% {{ transform: translateY(-10px) rotate(0deg) scale(1.05); }}
        75% {{ transform: translateY(-15px) rotate(-2deg) scale(1.02); }}
    }}
    
    @keyframes scalesShimmer {{
        0%, 100% {{ background-position: 0% 50%; }}
        50% {{ background-position: 100% 50%; }}
    }}
    
    @keyframes scalesPulse {{
        0%, 100% {{ 
            filter: drop-shadow(0 12px 24px rgba(251, 191, 36, 0.6)) drop-shadow(0 0 40px rgba(99, 102, 241, 0.4));
            transform: scale(1);
        }}
        50% {{ 
            filter: drop-shadow(0 16px 32px rgba(251, 191, 36, 0.8)) drop-shadow(0 0 60px rgba(99, 102, 241, 0.6));
            transform: scale(1.08);
        }}
    }}
    
    @keyframes scalesRotate {{
        from {{ transform: rotate(0deg); }}
        to {{ transform: rotate(360deg); }}
    }}
    
    @keyframes logoGlow {{
        0% {{ 
            opacity: 0.3; 
            transform: translate(-50%, -50%) scale(1) rotate(0deg); 
        }}
        100% {{ 
            opacity: 0.8; 
            transform: translate(-50%, -50%) scale(1.4) rotate(180deg); 
        }}
    }}
    
    @keyframes ringRotate {{
        from {{ transform: translate(-50%, -50%) rotate(0deg); }}
        to {{ transform: translate(-50%, -50%) rotate(360deg); }}
    }}
    
    .header-title {{
        font-family: 'Space Grotesk', sans-serif;
        font-size: 5rem;
        font-weight: 800;
        background: linear-gradient(135deg, {current_theme['text_primary']}, {current_theme['text_accent']}, {current_theme['gradient_end']}, {current_theme['gold_start']});
        background-size: 300% 300%;
        background-clip: text;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 2.5rem 0 0.8rem 0;
        letter-spacing: -0.05em;
        animation: titleSlide 1.5s ease-out, titleShimmer 12s ease-in-out infinite;
        position: relative;
        text-shadow: 0 0 60px rgba(99, 102, 241, 0.5);
    }}
    
    .header-title::after {{
        content: '';
        position: absolute;
        bottom: -15px;
        left: 50%;
        transform: translateX(-50%);
        width: 0;
        height: 6px;
        background: linear-gradient(90deg, {current_theme['gradient_start']}, {current_theme['gold_start']}, {current_theme['gradient_end']});
        border-radius: 3px;
        animation: underlineExpand 2s ease-out 1s both;
        box-shadow: 0 4px 20px rgba(99, 102, 241, 0.6);
    }}
    
    @keyframes titleShimmer {{
        0%, 100% {{ background-position: 0% 50%; }}
        50% {{ background-position: 100% 50%; }}
    }}
    
    @keyframes underlineExpand {{
        from {{ width: 0; }}
        to {{ width: 150px; }}
    }}
    
    .header-subtitle {{
        font-family: 'Poppins', sans-serif;
        font-size: 1.6rem;
        font-weight: 500;
        margin: 0;
        animation: subtitleFade 1.5s ease-out 0.8s both;
        background: linear-gradient(45deg, {current_theme['text_secondary']}, {current_theme['text_accent']}, {current_theme['gold_start']});
        background-clip: text;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: 0.5px;
    }}
    
    @keyframes titleSlide {{
        from {{ opacity: 0; transform: translateY(60px) scale(0.7) rotate(5deg); }}
        to {{ opacity: 1; transform: translateY(0) scale(1) rotate(0deg); }}
    }}
    
    @keyframes subtitleFade {{
        from {{ opacity: 0; transform: translateY(30px) scale(0.9); }}
        to {{ opacity: 1; transform: translateY(0) scale(1); }}
    }}
    
    /* Revolutionary Theme Toggle - Positioned at top right */
    .theme-toggle-container {{
        position: fixed;
        top: 2rem;
        right: 2rem;
        z-index: 1000;
    }}
    
    .theme-toggle-container .stButton > button {{
        background: rgba(255, 255, 255, 0.15) !important;
        backdrop-filter: blur(25px);
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        border-radius: 60px !important;
        padding: 1rem !important;
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.4);
        transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
        animation: themeToggleFloat 8s ease-in-out infinite;
        min-width: auto !important;
        width: 60px !important;
        height: 60px !important;
        font-size: 1.5rem !important;
        text-transform: none !important;
        letter-spacing: normal !important;
    }}
    
    .theme-toggle-container .stButton > button:hover {{
        transform: scale(1.3) rotate(15deg) !important;
        box-shadow: 0 20px 60px rgba(99, 102, 241, 0.5) !important;
        background: rgba(99, 102, 241, 0.25) !important;
        border-color: rgba(99, 102, 241, 0.5) !important;
    }}
    
    @keyframes themeToggleFloat {{
        0%, 100% {{ transform: translateY(0px) rotate(0deg); }}
        50% {{ transform: translateY(-8px) rotate(10deg); }}
    }}
    
    /* Advanced Glassmorphism Cards */
    .modern-card {{
        background: rgba(255, 255, 255, 0.12);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 30px;
        padding: 2.5rem;
        margin: 2.5rem 0;
        box-shadow: 
            0 16px 40px rgba(0, 0, 0, 0.15),
            inset 0 1px 0 rgba(255, 255, 255, 0.2),
            0 0 0 1px rgba(255, 255, 255, 0.05);
        transition: all 0.6s cubic-bezier(0.4, 0, 0.2, 1);
        animation: cardSlideIn 1s ease-out;
        position: relative;
        overflow: hidden;
    }}
    
    .modern-card::before {{
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.15), transparent);
        transition: left 0.8s;
    }}
    
    .modern-card::after {{
        content: '';
        position: absolute;
        top: -2px;
        left: -2px;
        right: -2px;
        bottom: -2px;
        background: linear-gradient(135deg, {current_theme['gradient_start']}, {current_theme['gold_start']}, {current_theme['gradient_end']});
        border-radius: 32px;
        opacity: 0;
        transition: opacity 0.5s;
        z-index: -1;
    }}
    
    .modern-card:hover {{
        transform: translateY(-12px) scale(1.03);
        box-shadow: 
            0 30px 80px rgba(0, 0, 0, 0.25),
            0 0 0 2px rgba(255, 255, 255, 0.15),
            inset 0 2px 0 rgba(255, 255, 255, 0.3);
        border-color: rgba(99, 102, 241, 0.4);
    }}
    
    .modern-card:hover::before {{
        left: 100%;
    }}
    
    .modern-card:hover::after {{
        opacity: 0.8;
    }}
    
    @keyframes cardSlideIn {{
        from {{
            opacity: 0;
            transform: translateY(80px) scale(0.8) rotate(3deg);
        }}
        to {{
            opacity: 1;
            transform: translateY(0) scale(1) rotate(0deg);
        }}
    }}
    
    /* Revolutionary Upload Zone */
    .upload-zone {{
        background: rgba(255, 255, 255, 0.08);
        border: 3px dashed rgba(99, 102, 241, 0.5);
        border-radius: 30px;
        padding: 4rem;
        text-align: center;
        transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
        backdrop-filter: blur(15px);
        animation: uploadBreathe 6s ease-in-out infinite;
    }}
    
    .upload-zone::before {{
        content: '';
        position: absolute;
        top: -3px;
        left: -3px;
        right: -3px;
        bottom: -3px;
        background: linear-gradient(45deg, {current_theme['gradient_start']}, {current_theme['gradient_end']}, {current_theme['gold_start']}, {current_theme['gradient_start']});
        background-size: 400% 400%;
        border-radius: 32px;
        opacity: 0;
        transition: opacity 0.4s;
        z-index: -1;
        animation: uploadGradient 8s ease-in-out infinite;
    }}
    
    @keyframes uploadBreathe {{
        0%, 100% {{ transform: scale(1); }}
        50% {{ transform: scale(1.02); }}
    }}
    
    @keyframes uploadGradient {{
        0%, 100% {{ background-position: 0% 50%; }}
        50% {{ background-position: 100% 50%; }}
    }}
    
    .upload-zone:hover {{
        border-color: transparent;
        background: rgba(255, 255, 255, 0.15);
        transform: scale(1.05);
        box-shadow: 0 20px 60px rgba(99, 102, 241, 0.3);
    }}
    
    .upload-zone:hover::before {{
        opacity: 1;
    }}
    
    .upload-zone.active {{
        animation: uploadPulse 2s ease-in-out infinite, uploadGlow 4s ease-in-out infinite;
    }}
    
    @keyframes uploadPulse {{
        0%, 100% {{ transform: scale(1); }}
        50% {{ transform: scale(1.08); }}
    }}
    
    @keyframes uploadGlow {{
        0%, 100% {{ box-shadow: 0 0 30px rgba(16, 185, 129, 0.4); }}
        50% {{ box-shadow: 0 0 60px rgba(16, 185, 129, 0.8); }}
    }}
    
    /* Status cards with enhanced glow effects */
    .status-card {{
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(16px);
        border-radius: 20px;
        padding: 2rem;
        text-align: center;
        border: 1px solid rgba(255, 255, 255, 0.15);
        transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
        animation: statusCardFloat 8s ease-in-out infinite;
    }}
    
    @keyframes statusCardFloat {{
        0%, 100% {{ transform: translateY(0px); }}
        50% {{ transform: translateY(-5px); }}
    }}
    
    .status-card::before {{
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, transparent, {current_theme['text_accent']}, transparent);
        animation: statusScan 4s ease-in-out infinite;
    }}
    
    @keyframes statusScan {{
        0%, 100% {{ transform: translateX(-100%); }}
        50% {{ transform: translateX(100%); }}
    }}
    
    .status-card.connected {{
        border-color: {current_theme['success']};
        box-shadow: 0 0 30px rgba(16, 185, 129, 0.4);
        background: rgba(16, 185, 129, 0.15);
    }}
    
    .status-card.error {{
        border-color: {current_theme['error']};
        box-shadow: 0 0 30px rgba(239, 68, 68, 0.4);
        background: rgba(239, 68, 68, 0.15);
    }}
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 1rem;
        background: rgba(255, 255, 255, 0.05);
        padding: 1rem;
        border-radius: 20px;
        margin: 2rem 0;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }}
    
    .stTabs [data-baseweb="tab"] {{
        background: rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        color: {current_theme['text_primary']};
        border: 1px solid rgba(255, 255, 255, 0.2);
        padding: 1rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }}
    
    .stTabs [data-baseweb="tab"]:hover {{
        background: rgba(99, 102, 241, 0.2);
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(99, 102, 241, 0.3);
    }}
    
    .stTabs [aria-selected="true"] {{
        background: linear-gradient(135deg, {current_theme['gradient_start']}, {current_theme['gradient_end']});
        color: white;
        border-color: {current_theme['gradient_start']};
        box-shadow: 0 8px 25px rgba(99, 102, 241, 0.4);
    }}
    
    /* Next-generation buttons */
    .stButton > button {{
        background: linear-gradient(135deg, {current_theme['gradient_start']}, {current_theme['gradient_end']});
        color: white;
        border: none;
        border-radius: 20px;
        padding: 1.2rem 2.5rem;
        font-weight: 700;
        font-size: 1.1rem;
        transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
        box-shadow: 0 12px 30px rgba(99, 102, 241, 0.4);
        font-family: 'Inter', sans-serif;
        letter-spacing: 1px;
        text-transform: uppercase;
        min-width: 160px;
        border: 2px solid transparent;
    }}
    
    .stButton > button::before {{
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
        transition: left 0.6s;
    }}
    
    .stButton > button::after {{
        content: '';
        position: absolute;
        top: -2px;
        left: -2px;
        right: -2px;
        bottom: -2px;
        background: linear-gradient(135deg, {current_theme['gold_start']}, {current_theme['gradient_start']}, {current_theme['gradient_end']});
        border-radius: 22px;
        opacity: 0;
        transition: opacity 0.3s;
        z-index: -1;
    }}
    
    .stButton > button:hover {{
        transform: translateY(-6px) scale(1.08);
        box-shadow: 0 20px 50px rgba(99, 102, 241, 0.5);
        background: linear-gradient(135deg, {current_theme['gradient_end']}, {current_theme['gold_start']});
    }}
    
    .stButton > button:hover::before {{
        left: 100%;
    }}
    
    .stButton > button:hover::after {{
        opacity: 1;
    }}
    
    .stButton > button:active {{
        transform: translateY(-3px) scale(1.05);
    }}
    
    /* Page transition effects */
    .page-transition {{
        animation: pageSlideIn 0.8s ease-out;
    }}
    
    @keyframes pageSlideIn {{
        from {{
            opacity: 0;
            transform: translateY(30px);
        }}
        to {{
            opacity: 1;
            transform: translateY(0);
        }}
    }}
    
    /* Enhanced Progress Bar */
    .stProgress > div > div > div > div {{
        background: linear-gradient(90deg, {current_theme['gradient_start']}, {current_theme['gold_start']}, {current_theme['gradient_end']});
        background-size: 200% 100%;
        border-radius: 15px;
        animation: progressShine 2.5s ease-in-out infinite;
        box-shadow: 0 6px 18px rgba(99, 102, 241, 0.4);
        height: 12px !important;
    }}
    
    @keyframes progressShine {{
        0%, 100% {{ background-position: 0% 50%; }}
        50% {{ background-position: 100% 50%; }}
    }}
    
    /* Responsive Design */
    @media (max-width: 768px) {{
        .header-title {{ 
            font-size: 3.5rem; 
        }}
        
        .logo-scales {{ 
            font-size: 5rem; 
        }}
        
        .modern-card {{
            padding: 2rem;
            margin: 2rem 0;
        }}
    }}
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {{
        width: 10px;
    }}
    
    ::-webkit-scrollbar-track {{
        background: {current_theme['bg_tertiary']};
        border-radius: 5px;
    }}
    
    ::-webkit-scrollbar-thumb {{
        background: linear-gradient(135deg, {current_theme['gradient_start']}, {current_theme['gradient_end']});
        border-radius: 5px;
        transition: all 0.3s ease;
    }}
    
    ::-webkit-scrollbar-thumb:hover {{
        background: linear-gradient(135deg, {current_theme['gradient_end']}, {current_theme['gold_start']});
        box-shadow: 0 0 15px {current_theme['accent_glow']};
    }}
</style>
""", unsafe_allow_html=True)

# Theme toggle functionality positioned at top right
st.markdown('<div class="theme-toggle-container">', unsafe_allow_html=True)
if st.button(f"{'🌙' if st.session_state.theme == 'dark' else '☀'}", 
             key="theme_toggle", 
             help="Toggle theme"):
    toggle_theme()
    st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

# Header with animated logo
st.markdown(f"""
<div class="logo-header">
    <div class="logo-container">
        <div class="logo-glow"></div>
        <div class="logo-rings"></div>
        <div class="logo-scales">⚖</div>
    </div>
    <h1 class="header-title">ClauseWise</h1>
    <p class="header-subtitle">AI-Powered Legal Document Intelligence</p>
</div>
""", unsafe_allow_html=True)

# Mock API functions for demonstration
def analyze_document(file_content):
    """Mock document analysis with realistic delays"""
    time.sleep(2)  # Simulate processing time
    
    # Mock analysis results
    return {
        "summary": "This contract outlines the terms and conditions for a software development agreement between TechCorp Inc. and ClientCo Ltd.",
        "key_entities": {
            "Parties": ["TechCorp Inc.", "ClientCo Ltd."],
            "Dates": ["2024-01-15", "2024-12-31"],
            "Amounts": ["$50,000", "$25,000"],
            "Locations": ["New York", "California"]
        },
        "risk_factors": [
            "Unlimited liability clause identified",
            "Vague termination conditions",
            "Missing intellectual property protections"
        ],
        "compliance_score": 85,
        "sentiment": "Neutral",
        "word_count": 2847,
        "page_count": 8,
        "clauses": {
            "Payment Terms": "Payment shall be made within 30 days of invoice receipt. Late payments may incur a 1.5% monthly penalty.",
            "Termination": "Either party may terminate this agreement with 30 days written notice to the other party.",
            "Intellectual Property": "All intellectual property created during the project shall remain the property of TechCorp Inc.",
            "Liability": "Each party's liability shall be limited to the total amount paid under this agreement.",
            "Confidentiality": "Both parties agree to maintain confidentiality of proprietary information shared during the project."
        },
        "simplified_clauses": {
            "Payment Terms": "You must pay within 30 days. If you pay late, you'll be charged extra fees (1.5% per month).",
            "Termination": "Either side can end this contract by giving 30 days notice in writing.",
            "Intellectual Property": "TechCorp keeps ownership of all the work they create for this project.",
            "Liability": "If something goes wrong, each party can only be held responsible up to the total amount paid.",
            "Confidentiality": "Both parties promise to keep each other's business secrets private."
        },
        "document_classification": {
            "type": "Service Agreement",
            "category": "Software Development Contract",
            "complexity": "Medium",
            "jurisdiction": "New York State",
            "confidence": 0.94
        }
    }

def display_entity_card(entity_type, entities, icon):
    """Display entity information in a modern card format"""
    st.markdown(f"""
    <div class="modern-card">
        <h4 style="margin-top: 0; color: {current_theme['text_accent']};">
            {icon} {entity_type}
        </h4>
        <ul style="list-style: none; padding: 0;">
    """, unsafe_allow_html=True)
    
    for entity in entities:
        st.markdown(f"""
            <li style="padding: 8px 0; border-bottom: 1px solid rgba(255,255,255,0.1);">
                <strong>{entity}</strong>
            </li>
        """, unsafe_allow_html=True)
    
    st.markdown("</ul></div>", unsafe_allow_html=True)

def display_clause_breakdown(clauses):
    """Display clause breakdown in expandable format"""
    for clause_title, clause_content in clauses.items():
        with st.expander(f"📋 {clause_title}", expanded=False):
            st.markdown(f"""
            <div style="
                background: rgba(255, 255, 255, 0.05);
                padding: 1.5rem;
                border-radius: 15px;
                border-left: 4px solid {current_theme['text_accent']};
                margin: 1rem 0;
            ">
                {clause_content}
            </div>
            """, unsafe_allow_html=True)

def display_simplified_clauses(simplified_clauses):
    """Display simplified clauses in user-friendly format"""
    for clause_title, simplified_content in simplified_clauses.items():
        with st.expander(f"💡 {clause_title} (Simplified)", expanded=False):
            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, rgba(16, 185, 129, 0.1), rgba(34, 197, 94, 0.1));
                padding: 1.5rem;
                border-radius: 15px;
                border-left: 4px solid {current_theme['success']};
                margin: 1rem 0;
            ">
                <p style="color: {current_theme['text_primary']}; font-size: 1.1rem; line-height: 1.6;">
                    {simplified_content}
                </p>
            </div>
            """, unsafe_allow_html=True)

# Main application with tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📄 Document Upload", 
    "🔍 Clause Breakdown", 
    "💡 Simplify Clause", 
    "🏷 Named Entity Recognition", 
    "📊 Document Classification"
])

with tab1:
    st.markdown('<div class="page-transition">', unsafe_allow_html=True)
    
    # Connection status
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div class="status-card connected">
            <h4>🟢 System Status</h4>
            <p>Online & Ready</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="status-card">
            <h4>⚡ Processing Speed</h4>
            <p>Ultra Fast</p>
        </div>
        """, unsafe_allow_html=True)
        
    with col3:
        st.markdown(f"""
        <div class="status-card">
            <h4>🔒 Security Level</h4>
            <p>Enterprise Grade</p>
        </div>
        """, unsafe_allow_html=True)
    
    # File upload section
    st.markdown(f"""
    <div class="modern-card">
        <h2 style="text-align: center; margin-bottom: 2rem; color: {current_theme['text_accent']};">
            📄 Upload Your Legal Document
        </h2>
        <p style="text-align: center; margin-bottom: 2rem; color: {current_theme['text_secondary']}; font-size: 1.1rem;">
            Upload your legal document to begin AI-powered analysis. We support PDF, DOC, DOCX, and TXT files.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Upload zone
    uploaded_file = st.file_uploader(
        "Choose a document file",
        type=['pdf', 'doc', 'docx', 'txt'],
        help="Upload your legal document for analysis",
        label_visibility="collapsed"
    )
    
    if uploaded_file is not None:
        st.session_state.uploaded_file = uploaded_file
        
        # Display file info
        st.markdown(f"""
        <div class="modern-card">
            <h4>📁 File Information</h4>
            <p><strong>Filename:</strong> {uploaded_file.name}</p>
            <p><strong>File Size:</strong> {uploaded_file.size / 1024:.1f} KB</p>
            <p><strong>File Type:</strong> {uploaded_file.type}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Analyze button
        if st.button("🚀 Analyze Document", key="analyze_btn"):
            with st.spinner("🔄 Analyzing document... This may take a few moments."):
                # Simulate file processing
                progress_bar = st.progress(0)
                for i in range(100):
                    time.sleep(0.02)
                    progress_bar.progress(i + 1)
                
                # Mock analysis
                file_content = uploaded_file.read()
                st.session_state.analysis_results = analyze_document(file_content)
                
                st.success("✅ Document analysis completed successfully!")
                
    st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="page-transition">', unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="modern-card">
        <h2 style="text-align: center; margin-bottom: 2rem; color: {current_theme['text_accent']};">
            🔍 Clause Breakdown Analysis
        </h2>
        <p style="text-align: center; margin-bottom: 2rem; color: {current_theme['text_secondary']}; font-size: 1.1rem;">
            Detailed breakdown of all clauses found in your document
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.analysis_results:
        clauses = st.session_state.analysis_results.get("clauses", {})
        if clauses:
            display_clause_breakdown(clauses)
        else:
            st.info("No clauses detected in the uploaded document.")
    else:
        st.info("Please upload and analyze a document first to see clause breakdown.")
    
    st.markdown('</div>', unsafe_allow_html=True)

with tab3:
    st.markdown('<div class="page-transition">', unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="modern-card">
        <h2 style="text-align: center; margin-bottom: 2rem; color: {current_theme['text_accent']};">
            💡 Simplified Clause Explanations
        </h2>
        <p style="text-align: center; margin-bottom: 2rem; color: {current_theme['text_secondary']}; font-size: 1.1rem;">
            Legal jargon translated into plain English for better understanding
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.analysis_results:
        simplified_clauses = st.session_state.analysis_results.get("simplified_clauses", {})
        if simplified_clauses:
            display_simplified_clauses(simplified_clauses)
        else:
            st.info("No simplified clauses available.")
    else:
        st.info("Please upload and analyze a document first to see simplified clauses.")
    
    st.markdown('</div>', unsafe_allow_html=True)

with tab4:
    st.markdown('<div class="page-transition">', unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="modern-card">
        <h2 style="text-align: center; margin-bottom: 2rem; color: {current_theme['text_accent']};">
            🏷 Named Entity Recognition
        </h2>
        <p style="text-align: center; margin-bottom: 2rem; color: {current_theme['text_secondary']}; font-size: 1.1rem;">
            Key entities extracted from your document including parties, dates, amounts, and locations
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.analysis_results:
        entities = st.session_state.analysis_results.get("key_entities", {})
        if entities:
            col1, col2 = st.columns(2)
            
            with col1:
                if "Parties" in entities:
                    display_entity_card("Parties", entities["Parties"], "👥")
                if "Dates" in entities:
                    display_entity_card("Important Dates", entities["Dates"], "📅")
            
            with col2:
                if "Amounts" in entities:
                    display_entity_card("Financial Amounts", entities["Amounts"], "💰")
                if "Locations" in entities:
                    display_entity_card("Locations", entities["Locations"], "📍")
        else:
            st.info("No entities detected in the uploaded document.")
    else:
        st.info("Please upload and analyze a document first to see entity recognition results.")
    
    st.markdown('</div>', unsafe_allow_html=True)

with tab5:
    st.markdown('<div class="page-transition">', unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="modern-card">
        <h2 style="text-align: center; margin-bottom: 2rem; color: {current_theme['text_accent']};">
            📊 Document Classification
        </h2>
        <p style="text-align: center; margin-bottom: 2rem; color: {current_theme['text_secondary']}; font-size: 1.1rem;">
            AI-powered classification and analysis of your document type and characteristics
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.analysis_results:
        classification = st.session_state.analysis_results.get("document_classification", {})
        summary = st.session_state.analysis_results.get("summary", "")
        compliance_score = st.session_state.analysis_results.get("compliance_score", 0)
        
        if classification:
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"""
                <div class="modern-card">
                    <h4 style="color: {current_theme['text_accent']};">📋 Document Type</h4>
                    <p><strong>Type:</strong> {classification.get('type', 'Unknown')}</p>
                    <p><strong>Category:</strong> {classification.get('category', 'Unknown')}</p>
                    <p><strong>Complexity:</strong> {classification.get('complexity', 'Unknown')}</p>
                    <p><strong>Jurisdiction:</strong> {classification.get('jurisdiction', 'Unknown')}</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                confidence = classification.get('confidence', 0) * 100
                st.markdown(f"""
                <div class="modern-card">
                    <h4 style="color: {current_theme['text_accent']};">📊 Analysis Metrics</h4>
                    <p><strong>Classification Confidence:</strong> {confidence:.1f}%</p>
                    <p><strong>Compliance Score:</strong> {compliance_score}/100</p>
                </div>
                """, unsafe_allow_html=True)
        
        # Document summary
        if summary:
            st.markdown(f"""
            <div class="modern-card">
                <h4 style="color: {current_theme['text_accent']};">📄 Document Summary</h4>
                <p style="line-height: 1.6; font-size: 1.1rem;">{summary}</p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("Please upload and analyze a document first to see classification results.")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown(f"""
<div style="text-align: center; padding: 3rem 0; margin-top: 4rem; border-top: 1px solid rgba(255,255,255,0.1);">
    <p style="color: {current_theme['text_secondary']}; margin: 0;">
        Made with ❤ using ClauseWise AI | Powered by Advanced NLP Technology
    </p>
</div>
""", unsafe_allow_html=True)