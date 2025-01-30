import os
from anthropic import Anthropic
from datetime import datetime
import streamlit as st
import PyPDF2
from core.config import *
from core.strings import *
from prompts.read_pdf_prompt import SYSTEM_PROMPT

def save_pdf_file(pdf_file):
    """Save uploaded PDF to data directory and return the file path"""
    if not os.path.exists(DATA_DIRECTORY):
        os.makedirs(DATA_DIRECTORY)
        
    timestamp = datetime.now().strftime(FILE_TIMESTAMP_FORMAT)
    filename = f"{DATA_DIRECTORY}/uploaded-{timestamp}.pdf"
    
    with open(filename, "wb") as f:
        f.write(pdf_file.getvalue())
    
    return filename

def get_ai_extraction(pdf_path):
    """Send PDF to Anthropic AI for data extraction"""
    
    # Extract text from PDF
    pdf_text = ""
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        for page in pdf_reader.pages:
            pdf_text += page.extract_text()
    
    client = Anthropic(api_key=ANTHROPIC_API_KEY)
    
    response = client.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=MAX_TOKENS,
        temperature=MODEL_TEMPERATURE,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": pdf_text}]
    )
    
    return response.content[0].text

def parse_ai_response(response_text):
    """Parse AI response into question-answer pairs"""
    parsed_data = {}
    lines = response_text.split('\n')
    
    current_question = None
    current_answer = []
    
    for line in lines:
        if line.startswith('Question: '):
            if current_question:
                parsed_data[current_question] = '\n'.join(current_answer).strip()
                current_answer = []
            current_question = line[len('Question: '):].strip()
        elif line.startswith('Answer:'): # Changed this line to match both formats
            answer_content = line[len('Answer:'):].strip()
            if answer_content:  # Only append if there's actual content
                current_answer.append(answer_content)
        elif current_question and line.strip():
            current_answer.append(line.strip())
    
    if current_question:
        parsed_data[current_question] = '\n'.join(current_answer).strip()
    
    return parsed_data

def update_session_state(parsed_data):
    """Update session state with parsed data"""
    # Skip if already processed
    if 'pdf_processed' not in st.session_state:
        st.session_state.pdf_processed = False
    
    if st.session_state.pdf_processed:
        return
        
    # Initialize session state variables if they don't exist
    default_fields = {
        'technical_work': '',
        'looking_for_cofounder': 'No',
        'company_name': '',
        'company_description': '',
        'company_url': '',
        'company_product': '',
        'company_location': '',
        'progress': '',
        'working_time': '',
        'tech_stack': '',
        'product_users': 'No',
        'revenue': 'No',
        'idea_explanation': '',
        'competitors': '',
        'business_model': '',
        'legal_entity': 'No',
        'investment': 'No',
        'fundraising': 'No',
        'yc_motivation': '',
        'hear_about_yc': ''
    }
    
    # Initialize session state for each field if not already present
    for field, default_value in default_fields.items():
        if field not in st.session_state:
            st.session_state[field] = default_value

    # Map questions to form field keys
    field_mapping = {
        TECHNICAL_WORK_LABEL: 'technical_work',
        COFOUNDER_LABEL: 'looking_for_cofounder',
        COMPANY_NAME_LABEL: 'company_name',
        COMPANY_DESCRIPTION_LABEL: 'company_description',
        COMPANY_URL_LABEL: 'company_url',
        COMPANY_PRODUCT_LABEL: 'company_product',
        COMPANY_LOCATION_LABEL: 'company_location',
        PROGRESS_LABEL: 'progress',
        WORKING_TIME_LABEL: 'working_time',
        TECH_STACK_LABEL: 'tech_stack',
        PRODUCT_USERS_LABEL: 'product_users',
        REVENUE_LABEL: 'revenue',
        IDEA_EXPLANATION_LABEL: 'idea_explanation',
        COMPETITORS_LABEL: 'competitors',
        BUSINESS_MODEL_LABEL: 'business_model',
        LEGAL_ENTITY_LABEL: 'legal_entity',
        INVESTMENT_LABEL: 'investment',
        FUNDRAISING_LABEL: 'fundraising',
        YC_MOTIVATION_LABEL: 'yc_motivation',
        HEAR_ABOUT_YC_LABEL: 'hear_about_yc'
    }
    
    # Update session state with parsed data
    for question, answer in parsed_data.items():
        if question in field_mapping:
            field_key = field_mapping[question]
            if field_key in ['looking_for_cofounder', 'product_users', 'revenue', 
                           'legal_entity', 'investment', 'fundraising']:
                answer = 'Yes' if any(pos in answer.lower() for pos in ['yes', 'true', 'y']) else 'No'
            st.session_state[field_key] = answer
            
    # Set the processed flag
    st.session_state.pdf_processed = True
    
    # Force Streamlit to rerun to update the form
    st.rerun()