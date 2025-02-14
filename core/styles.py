CSS = """
/* CSS Variables */
* {
    font-family: 'Avenir', sans-serif !important;
    --primary-color: #FF6D00;
    --secondary-color: #EF6C00;
    --text-gray: #6F6E69;
    --gradient-start: #FF5722;
    --gradient-end: #FF9100;
}

/* Page layout */
.block-container {
    min-height: 100vh !important;
    padding-bottom: 0 !important;
    max-width: 64rem !important;    
}

/* Main content area */
.main {
    flex: 1 0 auto !important;
    padding-bottom: 1rem !important;
}

/* Form container */
div[data-testid="stForm"] {
    flex: 1 !important;
    border: none !important;
    padding: 0 !important;
    border-radius: 0 !important;
    background-color: transparent !important;
    box-shadow: none !important;
    margin-bottom: 2rem !important;
}

/* Add smooth scrolling to html and body */
html {
    scroll-behavior: smooth !important;
}

body {
    scroll-behavior: smooth !important;
}

/* Heading styles */
h1, h2, h3 {
    font-weight: 700 !important;
    line-height: 1.2 !important;
}

h1 {
    font-size: 2rem !important;
}

h2 {
    font-size: 1.6rem !important;
}

h3 {
    font-size: 1.2rem !important;
}

/* Paragraph style */
p {
    font-size: 1rem !important;
}

.app-subtitle {
    font-size: 1rem !important;
    color: var(--text-gray) !important;
    margin-bottom: 4rem !important;
}

/* Input field spacing */
div.stTextInput, 
div.stSelectbox, 
div.stTextArea, 
div.stFileUploader {
    margin-bottom: 1.6rem !important;
}

/* AI Feedback column spacing */
.feedback-column {
    margin-top: 1rem !important;
}

/* Button styles */
.stFormSubmitButton > button {
    background-color: var(--primary-color) !important;
    color: white !important;
    border: none !important;
    border-radius: 4px !important;
    transition: background-color 0.2s ease !important;
}

.stFormSubmitButton > button:hover {
    background-color: var(--secondary-color) !important;
}

.stFormSubmitButton > button:focus {
    outline: none !important;
}

[data-testid="stFileUploader"] button[kind="secondary"] {
    background-color: none !important;
    color: var(--primary-color) !important;
    border: 1px solid var(--primary-color) !important;
    border-radius: 4px !important;
    transition: all 0.2s ease !important;
}

[data-testid="stFileUploader"] button[kind="secondary"]:hover {
    background-color: var(--primary-color) !important;
    color: white !important;
}

[data-testid="stFileUploader"] button[kind="secondary"]:focus {
    outline: none !important;
}

/* Add spinner styling */
div[data-testid="stSpinner"] i[class*="st-emotion-cache-"] {
    border-color: var(--secondary-color) !important;
    border-bottom-color: transparent !important;
    height: 1rem;
    width: 1rem;
}

/* Overall score container */
.overall-score-container {
    padding: 1rem;
    background: linear-gradient(to right, var(--gradient-start), var(--gradient-end)) !important;
    border-radius: 8px !important;
    margin-block: 1rem !important;
}

.overall-score-text {
    margin: 0;
    color: #FFFFFF !important;
}

.score-value {
    text-decoration: underline;
    text-underline-offset: 4px;
    text-decoration-thickness: 4px;
}

/* Radar chart container */
.radar-chart-container {
    padding: 0;
    margin-block: 0;
}

/* Footer styling */
.footnote {
    flex-shrink: 0 !important;
    font-size: 0.8rem !important;
    color: var(--text-gray) !important;
    text-align: left !important;
    padding: 1rem 0 1rem 0 !important;
    margin-top: 4rem !important;
}

.footnote a {
    color: var(--text-gray) !important;
    text-decoration: underline !important;
    text-underline-offset: 4px;
    text-decoration-thickness: 4px;
}
"""