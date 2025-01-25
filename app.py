import os
from datetime import datetime
import streamlit as st
from anthropic import Anthropic
from core.styles import *
from core.config import *
from core.strings import *

st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_LOGO,
)

def process_ai_feedback(response_text):
    """Parse AI feedback into sections"""
    sections = {
        FOUNDERS_HEADER: "",
        COMPANY_HEADER: "",
        PROGRESS_HEADER: "",
        IDEA_HEADER: "",
        EQUITY_HEADER: "",
        CURIOUS_HEADER: ""
    }
    
    current_section = None
    current_text = []
    
    for line in response_text.split('\n'):
        # More flexible section matching
        matched_section = None
        for section in sections.keys():
            if section.lower() in line.lower():
                matched_section = section
                break
        
        if matched_section:
            if current_section:
                sections[current_section] = '\n'.join(current_text).strip()
            current_section = matched_section
            current_text = []
        elif current_section:
            current_text.append(line)
    
    if current_section:
        sections[current_section] = '\n'.join(current_text).strip()
    
    return sections

def main():
    if not os.path.exists(DATA_DIRECTORY):
        os.makedirs(DATA_DIRECTORY)

    st.title(APP_TITLE)

    # Apply custom CSS
    st.markdown(f'<style>{CSS}</style>', unsafe_allow_html=True)
    
    if 'ai_feedback' not in st.session_state:
        st.session_state.ai_feedback = None
        
    if 'form_data' not in st.session_state:
        st.session_state.form_data = {}

    with st.form(FORM_NAME):
        # 1. Founders Section
        form_col, feedback_col = st.columns(COLUMN_RATIO)
        with form_col:
            st.header(FOUNDERS_HEADER)
            technical_work = st.text_area(TECHNICAL_WORK_LABEL)
            looking_for_cofounder = st.selectbox(COFOUNDER_LABEL, YES_NO_OPTIONS)
            
            # Founder Video as subsection
            st.subheader(FOUNDER_VIDEO_HEADER)
            founder_video = st.file_uploader(FOUNDER_VIDEO_LABEL, type=["mp4", "mov"])
        with feedback_col:
            if st.session_state.ai_feedback:
                st.markdown(AI_REVIEW_HEADER)
                st.markdown(st.session_state.ai_feedback[FOUNDERS_HEADER])
        
        # 2. Company Section
        form_col, feedback_col = st.columns(COLUMN_RATIO)
        with form_col:
            st.header(COMPANY_HEADER)
            company_name = st.text_input(COMPANY_NAME_LABEL)
            company_description = st.text_input(COMPANY_DESCRIPTION_LABEL, max_chars=50)
            company_url = st.text_input(COMPANY_URL_LABEL)
            demo_video = st.file_uploader(DEMO_VIDEO_LABEL, type=["mp4", "mov"])
            product_link = st.text_input(PRODUCT_LINK_LABEL)
            
            login_col1, login_col2 = st.columns(2)
            with login_col1:
                login_username = st.text_input(USERNAME_LABEL)
            with login_col2:
                login_password = st.text_input(PASSWORD_LABEL, type="password")
            
            company_product = st.text_area(COMPANY_PRODUCT_LABEL)
            company_location = st.text_input(COMPANY_LOCATION_LABEL)
            location_explanation = st.text_area(LOCATION_EXPLANATION_LABEL)
        with feedback_col:
            if st.session_state.ai_feedback:
                st.markdown(AI_REVIEW_HEADER)
                st.markdown(st.session_state.ai_feedback[COMPANY_HEADER])
        
        # 3. Progress Section
        form_col, feedback_col = st.columns(COLUMN_RATIO)
        with form_col:
            st.header(PROGRESS_HEADER)
            progress = st.text_area(PROGRESS_LABEL)
            working_time = st.text_area(WORKING_TIME_LABEL)
            tech_stack = st.text_area(TECH_STACK_LABEL)
            product_users = st.selectbox(PRODUCT_USERS_LABEL, YES_NO_OPTIONS)
            revenue = st.selectbox(REVENUE_LABEL, YES_NO_OPTIONS)
            previous_application = st.text_area(PREVIOUS_APPLICATION_LABEL)
            incubator = st.text_area(INCUBATOR_LABEL)
        with feedback_col:
            if st.session_state.ai_feedback:
                st.markdown(AI_REVIEW_HEADER)
                st.markdown(st.session_state.ai_feedback[PROGRESS_HEADER])
        
        # 4. Idea Section
        form_col, feedback_col = st.columns(COLUMN_RATIO)
        with form_col:
            st.header(IDEA_HEADER)
            idea_explanation = st.text_area(IDEA_EXPLANATION_LABEL)
            competitors = st.text_area(COMPETITORS_LABEL)
            business_model = st.text_area(BUSINESS_MODEL_LABEL)
            category = st.selectbox(CATEGORY_LABEL, CATEGORY_OPTIONS)
            other_ideas = st.text_area(OTHER_IDEAS_LABEL)
        with feedback_col:
            if st.session_state.ai_feedback:
                st.markdown(AI_REVIEW_HEADER)
                st.markdown(st.session_state.ai_feedback[IDEA_HEADER])
        
        # 5. Equity Section
        form_col, feedback_col = st.columns(COLUMN_RATIO)
        with form_col:
            st.header(EQUITY_HEADER)
            legal_entity = st.selectbox(LEGAL_ENTITY_LABEL, YES_NO_OPTIONS)
            investment = st.selectbox(INVESTMENT_LABEL, YES_NO_OPTIONS)
            fundraising = st.selectbox(FUNDRAISING_LABEL, YES_NO_OPTIONS)
        with feedback_col:
            if st.session_state.ai_feedback:
                st.markdown(AI_REVIEW_HEADER)
                st.markdown(st.session_state.ai_feedback[EQUITY_HEADER])
        
        # 6. Curious Section
        form_col, feedback_col = st.columns(COLUMN_RATIO)
        with form_col:
            st.header(CURIOUS_HEADER)
            yc_motivation = st.text_area(YC_MOTIVATION_LABEL)
            hear_about_yc = st.text_area(HEAR_ABOUT_YC_LABEL)
        with feedback_col:
            if st.session_state.ai_feedback:
                st.markdown(AI_REVIEW_HEADER)
                st.markdown(st.session_state.ai_feedback[CURIOUS_HEADER])
        
        # Submit button at the bottom of the form
        submitted = st.form_submit_button("Submit Application")

    if submitted:
        # Validate required fields
        if not company_name:
            st.error(COMPANY_NAME_REQUIRED)
        elif not company_description:
            st.error(COMPANY_DESCRIPTION_REQUIRED)
        else:
            # Create a dictionary with all the form data
            application_data = {
                FOUNDERS_HEADER: [
                    {"question": TECHNICAL_WORK_LABEL, "answer": technical_work},
                    {"question": COFOUNDER_LABEL, "answer": looking_for_cofounder}
                ],
                COMPANY_HEADER: [
                    {"question": COMPANY_NAME_LABEL, "answer": company_name},
                    {"question": COMPANY_DESCRIPTION_LABEL, "answer": company_description},
                    {"question": COMPANY_URL_LABEL, "answer": company_url},
                    {"question": PRODUCT_LINK_LABEL, "answer": product_link},
                    {"question": USERNAME_LABEL, "answer": login_username},
                    {"question": PASSWORD_LABEL, "answer": login_password},
                    {"question": COMPANY_PRODUCT_LABEL, "answer": company_product},
                    {"question": COMPANY_LOCATION_LABEL, "answer": company_location},
                    {"question": LOCATION_EXPLANATION_LABEL, "answer": location_explanation}
                ],
                PROGRESS_HEADER: [
                    {"question": PROGRESS_LABEL, "answer": progress},
                    {"question": WORKING_TIME_LABEL, "answer": working_time},
                    {"question": TECH_STACK_LABEL, "answer": tech_stack},
                    {"question": PRODUCT_USERS_LABEL, "answer": product_users},
                    {"question": REVENUE_LABEL, "answer": revenue},
                    {"question": PREVIOUS_APPLICATION_LABEL, "answer": previous_application},
                    {"question": INCUBATOR_LABEL, "answer": incubator}
                ],
                IDEA_HEADER: [
                    {"question": IDEA_EXPLANATION_LABEL, "answer": idea_explanation},
                    {"question": COMPETITORS_LABEL, "answer": competitors},
                    {"question": BUSINESS_MODEL_LABEL, "answer": business_model},
                    {"question": CATEGORY_LABEL, "answer": category},
                    {"question": OTHER_IDEAS_LABEL, "answer": other_ideas}
                ],
                EQUITY_HEADER: [
                    {"question": LEGAL_ENTITY_LABEL, "answer": legal_entity},
                    {"question": INVESTMENT_LABEL, "answer": investment},
                    {"question": FUNDRAISING_LABEL, "answer": fundraising}
                ],
                CURIOUS_HEADER: [
                    {"question": YC_MOTIVATION_LABEL, "answer": yc_motivation},
                    {"question": HEAR_ABOUT_YC_LABEL, "answer": hear_about_yc}
                ]
            }
            
            # Create the content string for file and AI review
            content = FILE_HEADER
            for section, questions in application_data.items():
                content += f"## {section}\n\n"
                for item in questions:
                    content += f"Question: {item['question']}\n"
                    content += f"Answer: {item['answer']}\n\n"
                content += "\n"
            
            # Get AI feedback
            client = Anthropic(api_key=ANTHROPIC_API_KEY)
            response = client.messages.create(
                model=CLAUDE_MODEL,
                max_tokens=MAX_TOKENS,
                temperature=MODEL_TEMPERATURE,
                system=SYSTEM_PROMPT,
                messages=[{"role": "user", "content": content}]
            )
            
            # Process and store AI feedback
            st.session_state.ai_feedback = process_ai_feedback(response.content[0].text)
            
            # Generate timestamp and filename
            timestamp = datetime.now().strftime(FILE_TIMESTAMP_FORMAT)
            filename = f"{DATA_DIRECTORY}/form-{timestamp}.txt"
            
            # Write the data to a file
            with open(filename, 'w') as f:
                f.write(content)
            
            # Show success message
            st.success(SUCCESS_MESSAGE.format(filename))
            st.rerun()  # Rerun to show feedback

if __name__ == "__main__":
    main()