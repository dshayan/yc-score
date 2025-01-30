# YC Score

YC Score provides instant feedback on Y Combinator application drafts using AI, based on publicly available YC application criteria.

## Features

- Interactive form matching YC's application
- PDF upload for auto-filling application
- Real-time AI evaluation using Claude Sonnet 3.5
- Section-by-section feedback and scoring
- Overall application score with radar chart visualization

## Setup

1. Install dependencies:

```
pip install -r requirements.txt
```

2. Set environment variables in `.env`:

```
ANTHROPIC_API_KEY=your_api_key
```

3. Run the app:

```
streamlit run app.py
```
