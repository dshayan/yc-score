CSS = """

* {
    font-family: 'Avenir', sans-serif !important;
}

/* Heading styles */

h1 {
    font-size: 2rem !important;
    font-weight: 700 !important;
}

.app-subtitle {
    font-size: 1rem !important;
    color: #6F6E69 !important;
    margin-bottom: 4rem !important;
}

h2 {
    font-size: 1.6rem !important;
    font-weight: 700 !important;
}

h3 {
    font-size: 1.2rem !important;
    font-weight: 600 !important;
}

/* Paragraph style */

p {
    font-size: 1rem !important;
}

/* Adjust block container width */

.block-container {
    padding-left: 4rem !important;
    padding-right: 4rem !important;
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
    background: linear-gradient(to right, #F25F4C, #FF8E3C) !important;
    border-radius: 8px !important;
    margin-top: 1rem !important;
    margin-bottom: 1rem !important;
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
    background-color: #FF8906 !important;
    color: white !important;
    border-style: none;
    border-radius: 4px !important;
}

.stFormSubmitButton > button:hover {
    background-color: #FF8E3C !important;
}

/* Radar chart container */

.radar-chart-container {
    background-color: #FFFFFF;
    border-radius: 32px;
    padding: 0px;
    margin-top: 0px;
    margin-bottom: 0px;
}

"""