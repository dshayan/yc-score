import os
from datetime import datetime
from anthropic import Anthropic
import streamlit as st
from core.config import *
from core.strings import *
from core.styles import *
from core.pdf_handler import save_pdf_file, get_ai_extraction, parse_ai_response, update_session_state

st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_LOGO,
)

# Apply custom CSS
st.markdown(f'<style>{CSS}</style>', unsafe_allow_html=True)

def process_ai_feedback(response_text):
    """Parse AI feedback into sections while preserving exact content"""
    sections = {
        FOUNDERS_HEADER: "",
        FOUNDER_VIDEO_HEADER: "",
        COMPANY_HEADER: "",
        PROGRESS_HEADER: "",
        IDEA_HEADER: "",
        EQUITY_HEADER: "",
        CURIOUS_HEADER: ""
    }
    
    lines = response_text.split('\n')
    current_section = None
    section_content = []
    
    for i, line in enumerate(lines):
        if line.startswith('##'):
            # Save previous section
            if current_section and section_content:
                sections[current_section] = '\n'.join(section_content)
                section_content = []
            
            # Find the current section
            for section in sections.keys():
                if section.lower() in line.lower():
                    current_section = section
                    break
        elif current_section and i < len(lines):
            section_content.append(line)
    
    # Save the last section
    if current_section and section_content:
        sections[current_section] = '\n'.join(section_content)
    
    return sections

def extract_overall_score(response_text):
    """Extract the overall score from the AI response"""
    for line in response_text.split('\n'):
        if line.startswith('Overall Score'):
            # Extract number between ** **
            score = line.split('**')[1].strip('/')
            return score
    return None

def extract_section_scores(response_text):
    """Extract scores for each section from AI feedback"""
    section_scores = {}
    lines = response_text.split('\n')
    
    # Define section name mappings (normalized to match both formats)
    section_mappings = {
        'founders': FOUNDERS_HEADER,
        'founder video': FOUNDER_VIDEO_HEADER,
        'company': COMPANY_HEADER,
        'progress': PROGRESS_HEADER,
        'idea': IDEA_HEADER,
        'equity': EQUITY_HEADER,
        'curious': CURIOUS_HEADER
    }
    
    current_section = None
    for i, line in enumerate(lines):
        if line.startswith('## '):
            # Find the current section
            section_name = line.strip('# ').strip().lower()
            for key, mapped_name in section_mappings.items():
                if key in section_name:  # Using 'in' for partial matching
                    current_section = mapped_name
                    # Find the score line that follows this section header
                    for next_line in lines[i:i+5]:  # Look at next few lines
                        if next_line.startswith('Score: **'):
                            try:
                                # Extract score between ** ** and handle /100 format
                                score_text = next_line.split('**')[1].strip()
                                score = int(score_text.split('/')[0].strip())
                                section_scores[current_section] = score
                            except (IndexError, ValueError):
                                continue
                    break
    
    """# Debug print to verify scores
    print("Extracted section scores:", section_scores)"""
    
    return section_scores

def create_radar_chart(section_scores):
    """Create a radar chart from section scores"""
    import plotly.graph_objects as go
    
    # Include all sections from the evaluation criteria
    relevant_sections = [
        FOUNDERS_HEADER,
        FOUNDER_VIDEO_HEADER,
        COMPANY_HEADER,
        PROGRESS_HEADER,
        IDEA_HEADER,
        EQUITY_HEADER,
        CURIOUS_HEADER
    ]
    
    # Filter and order the scores
    scores = [section_scores.get(section, 0) for section in relevant_sections]
    
    # Debug print to check scores
    print("Section scores:", dict(zip(relevant_sections, scores)))
    
    fig = go.Figure(data=go.Scatterpolar(
        r=scores,
        theta=relevant_sections,
        fill='toself',
        fillcolor='rgba(255, 137, 6, 0.2)',
        line=dict(color='#ff8906', width=2)
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                showline=False,
                tickfont=dict(
                    size=10,
                    color='#6F6E69'
                ),
                gridcolor='rgba(111, 110, 105, 0.2)'
            ),
            angularaxis=dict(
                tickfont=dict(
                    size=12,
                    color='#6F6E69'
                ),
                gridcolor='rgba(111, 110, 105, 0.2)'
            ),
            bgcolor='rgba(0, 0, 0, 0)'
        ),
        showlegend=False,
        margin=dict(l=32, r=32, t=32, b=32),
        height=320,
        paper_bgcolor='rgba(0, 0, 0, 0)'
    )
    
    return fig

def main():
    if 'overall_score' not in st.session_state:
        st.session_state.overall_score = None    
    
    if not os.path.exists(DATA_DIRECTORY):
        os.makedirs(DATA_DIRECTORY)
    
    st.title(APP_LOGO)
    st.title(APP_TITLE)
    st.markdown(f'<p class="app-subtitle">{APP_SUBTITLE}</p>', unsafe_allow_html=True)

    if 'ai_feedback' not in st.session_state:
        st.session_state.ai_feedback = None
        
    if 'form_data' not in st.session_state:
        st.session_state.form_data = {}

    # Move PDF uploader outside the form but wrap it in columns to match form width
    pdf_col, _ = st.columns(COLUMN_RATIO)
    with pdf_col:
        uploaded_pdf = st.file_uploader(
            PDF_UPLOAD_LABEL,
            type=["pdf"],
            key="pdf_uploader"
        )
    
    # Handle PDF processing
    if 'pdf_processed' not in st.session_state:
        st.session_state.pdf_processed = False
        
    # Process PDF only if it's uploaded and not processed yet
    if uploaded_pdf is not None and not st.session_state.pdf_processed:
        # Check file size
        if uploaded_pdf.size > MAX_PDF_SIZE:
            st.error(PDF_SIZE_ERROR)
        else:
            try:
                with st.spinner(PDF_PROCESSING_MESSAGE):
                    # Save PDF file
                    pdf_path = save_pdf_file(uploaded_pdf)
                    
                    # Extract data using AI
                    ai_response = get_ai_extraction(pdf_path)
                    
                    # Parse AI response
                    parsed_data = parse_ai_response(ai_response)
                    
                    # Update form fields
                    update_session_state(parsed_data)
                    
                    st.success(PDF_UPLOAD_SUCCESS)
            except Exception as e:
                st.error(PDF_EXTRACTION_ERROR.format(str(e)))
                st.session_state.pdf_processed = False
    # Reset processing flag when PDF is cleared
    elif uploaded_pdf is None:
        st.session_state.pdf_processed = False

    # Display overall score after PDF upload
    if st.session_state.overall_score:
        st.markdown(f"""
        <div class="overall-score-container">
            <h2 class="overall-score-text">{OVERALL_SCORE_PREFIX}<span class="score-value">{st.session_state.overall_score}</span>{OVERALL_SCORE_SUFFIX}</h2>
        </div>
        """, unsafe_allow_html=True)

        # Display radar chart if available
        if hasattr(st.session_state, 'radar_chart'):
            st.markdown('<div class="radar-chart-container">', unsafe_allow_html=True)
            st.plotly_chart(st.session_state.radar_chart, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
    
    with st.form(FORM_NAME):
        # Founders Section
        form_col, feedback_col = st.columns(COLUMN_RATIO)
        with form_col:
            st.header(FOUNDERS_HEADER)
            technical_work = st.text_area(
                TECHNICAL_WORK_LABEL,
                value=st.session_state.get('technical_work', '')
            )
            looking_for_cofounder = st.selectbox(
                COFOUNDER_LABEL,
                YES_NO_OPTIONS,
                index=YES_NO_OPTIONS.index(st.session_state.get('looking_for_cofounder', 'No'))
            )
        with feedback_col:
            if st.session_state.ai_feedback:
                st.markdown('<div class="feedback-column">', unsafe_allow_html=True)
                st.markdown(st.session_state.ai_feedback[FOUNDERS_HEADER])
                st.markdown('</div>', unsafe_allow_html=True)

        # Founder Video Section
        form_col, feedback_col = st.columns(COLUMN_RATIO)
        with form_col:
            st.header(FOUNDER_VIDEO_HEADER)
            founder_video = st.file_uploader(FOUNDER_VIDEO_LABEL, type=["mp4", "mov"])
        with feedback_col:
            if st.session_state.ai_feedback:
                st.markdown('<div class="feedback-column">', unsafe_allow_html=True)
                st.markdown(st.session_state.ai_feedback[FOUNDER_VIDEO_HEADER])
                st.markdown('</div>', unsafe_allow_html=True)
        
        # Company Section
        form_col, feedback_col = st.columns(COLUMN_RATIO)
        with form_col:
            st.header(COMPANY_HEADER)
            company_name = st.text_input(
                COMPANY_NAME_LABEL,
                value=st.session_state.get('company_name', '')
            )
            company_description = st.text_input(
                COMPANY_DESCRIPTION_LABEL,
                value=st.session_state.get('company_description', ''),
                max_chars=50
            )
            company_url = st.text_input(
                COMPANY_URL_LABEL,
                value=st.session_state.get('company_url', '')
            )
            demo_video = st.file_uploader(DEMO_VIDEO_LABEL, type=["mp4", "mov"])
            product_link = st.text_input(
                PRODUCT_LINK_LABEL,
                value=st.session_state.get('product_link', '')
            )
                        
            company_product = st.text_area(
                COMPANY_PRODUCT_LABEL,
                value=st.session_state.get('company_product', '')
            )
            company_location = st.text_input(
                COMPANY_LOCATION_LABEL,
                value=st.session_state.get('company_location', '')
            )
            location_explanation = st.text_area(
                LOCATION_EXPLANATION_LABEL,
                value=st.session_state.get('location_explanation', '')
            )
        with feedback_col:
            if st.session_state.ai_feedback:
                st.markdown('<div class="feedback-column">', unsafe_allow_html=True)
                st.markdown(st.session_state.ai_feedback[COMPANY_HEADER])
                st.markdown('</div>', unsafe_allow_html=True)
        
        # Progress Section
        form_col, feedback_col = st.columns(COLUMN_RATIO)
        with form_col:
            st.header(PROGRESS_HEADER)
            progress = st.text_area(
                PROGRESS_LABEL,
                value=st.session_state.get('progress', '')
            )
            working_time = st.text_area(
                WORKING_TIME_LABEL,
                value=st.session_state.get('working_time', '')
            )
            tech_stack = st.text_area(
                TECH_STACK_LABEL,
                value=st.session_state.get('tech_stack', '')
            )
            product_users = st.selectbox(
                PRODUCT_USERS_LABEL,
                YES_NO_OPTIONS,
                index=YES_NO_OPTIONS.index(st.session_state.get('product_users', 'No'))
            )
            revenue = st.selectbox(
                REVENUE_LABEL,
                YES_NO_OPTIONS,
                index=YES_NO_OPTIONS.index(st.session_state.get('revenue', 'No'))
            )
            previous_application = st.text_area(
                PREVIOUS_APPLICATION_LABEL,
                value=st.session_state.get('previous_application', '')
            )
            incubator = st.text_area(
                INCUBATOR_LABEL,
                value=st.session_state.get('incubator', '')
            )
        with feedback_col:
            if st.session_state.ai_feedback:
                st.markdown('<div class="feedback-column">', unsafe_allow_html=True)
                st.markdown(st.session_state.ai_feedback[PROGRESS_HEADER])
                st.markdown('</div>', unsafe_allow_html=True)
        
        # Idea Section
        form_col, feedback_col = st.columns(COLUMN_RATIO)
        with form_col:
            st.header(IDEA_HEADER)
            idea_explanation = st.text_area(
                IDEA_EXPLANATION_LABEL,
                value=st.session_state.get('idea_explanation', '')
            )
            competitors = st.text_area(
                COMPETITORS_LABEL,
                value=st.session_state.get('competitors', '')
            )
            business_model = st.text_area(
                BUSINESS_MODEL_LABEL,
                value=st.session_state.get('business_model', '')
            )
            category = st.selectbox(
                CATEGORY_LABEL,
                CATEGORY_OPTIONS,
                index=CATEGORY_OPTIONS.index(st.session_state.get('category', CATEGORY_OPTIONS[0]))
            )
            other_ideas = st.text_area(
                OTHER_IDEAS_LABEL,
                value=st.session_state.get('other_ideas', '')
            )
        with feedback_col:
            if st.session_state.ai_feedback:
                st.markdown('<div class="feedback-column">', unsafe_allow_html=True)
                st.markdown(st.session_state.ai_feedback[IDEA_HEADER])
                st.markdown('</div>', unsafe_allow_html=True)
        
        # Equity Section
        form_col, feedback_col = st.columns(COLUMN_RATIO)
        with form_col:
            st.header(EQUITY_HEADER)
            legal_entity = st.selectbox(
                LEGAL_ENTITY_LABEL,
                YES_NO_OPTIONS,
                index=YES_NO_OPTIONS.index(st.session_state.get('legal_entity', 'No'))
            )
            investment = st.selectbox(
                INVESTMENT_LABEL,
                YES_NO_OPTIONS,
                index=YES_NO_OPTIONS.index(st.session_state.get('investment', 'No'))
            )
            fundraising = st.selectbox(
                FUNDRAISING_LABEL,
                YES_NO_OPTIONS,
                index=YES_NO_OPTIONS.index(st.session_state.get('fundraising', 'No'))
            )
        with feedback_col:
            if st.session_state.ai_feedback:
                st.markdown('<div class="feedback-column">', unsafe_allow_html=True)
                st.markdown(st.session_state.ai_feedback[EQUITY_HEADER])
                st.markdown('</div>', unsafe_allow_html=True)
        
        # Curious Section
        form_col, feedback_col = st.columns(COLUMN_RATIO)
        with form_col:
            st.header(CURIOUS_HEADER)
            yc_motivation = st.text_area(
                YC_MOTIVATION_LABEL,
                value=st.session_state.get('yc_motivation', '')
            )
            hear_about_yc = st.text_area(
                HEAR_ABOUT_YC_LABEL,
                value=st.session_state.get('hear_about_yc', '')
            )
        with feedback_col:
            if st.session_state.ai_feedback:
                st.markdown('<div class="feedback-column">', unsafe_allow_html=True)
                st.markdown(st.session_state.ai_feedback[CURIOUS_HEADER])
                st.markdown('</div>', unsafe_allow_html=True)
        
        # Submit button at the bottom of the form
        submitted = st.form_submit_button(SUBMIT_BUTTON_LABEL, type="primary")

    if submitted:
        # Collect all validation errors
        error_messages = []
        
        if not company_name:
            error_messages.append(COMPANY_NAME_REQUIRED)
        if not company_description:
            error_messages.append(COMPANY_DESCRIPTION_REQUIRED)
            
        # Show single toast with all errors if any exist
        if error_messages:
            st.toast(" ".join(error_messages), icon="❗️")
        else:
            # Create a dictionary with all the form data
            application_data = {
                FOUNDERS_HEADER: [
                    {"question": TECHNICAL_WORK_LABEL, "answer": technical_work},
                    {"question": COFOUNDER_LABEL, "answer": looking_for_cofounder}
                ],
                FOUNDER_VIDEO_HEADER: [
                    {"question": FOUNDER_VIDEO_LABEL, "answer": founder_video.name if founder_video else ""}
                ],
                COMPANY_HEADER: [
                    {"question": COMPANY_NAME_LABEL, "answer": company_name},
                    {"question": COMPANY_DESCRIPTION_LABEL, "answer": company_description},
                    {"question": COMPANY_URL_LABEL, "answer": company_url},
                    {"question": PRODUCT_LINK_LABEL, "answer": product_link},
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
            
            # Extract and store overall score
            st.session_state.overall_score = extract_overall_score(response.content[0].text)
            
            # Extract section scores and create radar chart
            section_scores = extract_section_scores(response.content[0].text)
            radar_chart = create_radar_chart(section_scores)
            st.session_state.radar_chart = radar_chart

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
            st.rerun()
        
    # Add footnote at the bottom of the page
    st.markdown(f'<p class="footnote">{COPYRIGHT_TEXT}</p>', unsafe_allow_html=True)
                
if __name__ == "__main__":
    main()