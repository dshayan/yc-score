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
    color: #666666 !important;
    margin-bottom: 2rem !important;
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
    background: linear-gradient(to right, #f25f4c, #f9bc60) !important;  /* Change from left orange to right red */
    border-radius: 8px !important;
    margin-right: -1rem;
    margin-left: -1rem;
    margin-top: 1rem !important;
    margin-bottom: 1rem !important;
}

.overall-score-text {
    margin: 0;
    color: #ffffff !important;
}

.score-value {
    text-decoration: underline;
    text-underline-offset: 4px;
    text-decoration-thickness: 4px;

}

/* Button styles */

.stFormSubmitButton > button {
    background-color: #ff8e3c !important;
    border-style: none;
    color: white !important;
}

.stFormSubmitButton > button:hover {
    background-color: #f9bc60 !important;
}

"""