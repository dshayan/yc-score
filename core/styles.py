CSS = """
/* CSS Variables */
* {
    font-family: 'Avenir', sans-serif !important;
    --primary-color: #FF6D00;
    --primary-hover: #EF6C00;
    --text-gray: #6F6E69;
    --gradient-start: #FF5722;
    --gradient-end: #FF9100;
    box-sizing: border-box !important;
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

.app-subtitle {
    font-size: 1rem !important;
    color: var(--text-gray) !important;
    margin-bottom: 4rem !important;
}

/* Paragraph style */
p {
    font-size: 1rem !important;
}

/* Adjust block container width */
.block-container {
    padding-inline: 4rem !important;
    max-width: 72rem !important;
    margin-top: -2rem;
}

/* Remove form borders and padding */
div[data-testid="stForm"] {
    border: none !important;
    padding: 0 !important;
    border-radius: 0 !important;
    background-color: transparent !important;
    box-shadow: none !important;
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

/* Button styles */
.stFormSubmitButton > button {
    background-color: var(--primary-color) !important;
    color: white !important;
    border: none !important;
    border-radius: 4px !important;
    transition: background-color 0.2s ease !important;
}

.stFormSubmitButton > button:hover {
    background-color: var(--primary-hover) !important;
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

/* Radar chart container */
.radar-chart-container {
    padding: 0;
    margin-block: 0;
}

/* Footnote style */
.footnote {
    font-size: 0.8rem !important;
    color: var(--text-gray) !important;
    text-align: left !important;
    padding: 2rem 0 1rem 0 !important;
    margin-top: 4rem !important;
    margin-bottom: -8rem;
    position: relative !important;
}

.footnote a {
    color: var(--text-gray) !important;
    text-decoration: underline !important;
    text-underline-offset: 4px;
    text-decoration-thickness: 4px;
}

"""