import os
from dotenv import load_dotenv
import pathlib
from prompts.evaluation_prompt import SYSTEM_PROMPT

# Load environment variables from .env file
load_dotenv()

# Image assets
ASSETS_DIR = pathlib.Path("assets")
ICON_PATH = ASSETS_DIR / "icon.png"
LOGO_PATH = ASSETS_DIR / "logo.png"

# Get API key from environment variables
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')
if not ANTHROPIC_API_KEY:
    raise ValueError("ANTHROPIC_API_KEY not found in environment variables")

# Form configuration
FORM_NAME = "yc_application_form"
COLUMN_RATIO = [8, 4]  # Form to feedback column ratio

# Model configuration
CLAUDE_MODEL = "claude-3-5-sonnet-latest"
MAX_TOKENS = 4000
MODEL_TEMPERATURE = 0

# File handling
DATA_DIRECTORY = 'data'
FILE_TIMESTAMP_FORMAT = "%Y%m%d_%H%M%S"

# PDF handling
MAX_PDF_SIZE = 10 * 1024 * 1024  # 10MB in bytes
ALLOWED_PDF_TYPES = ["application/pdf"]