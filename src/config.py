import os
from pathlib import Path

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[1]

load_dotenv(PROJECT_ROOT / ".env")

DATA_RAW = PROJECT_ROOT / "data" / "raw"
DATA_INTERIM = PROJECT_ROOT / "data" / "interim"
DATA_PROCESSED = PROJECT_ROOT / "data" / "processed"
DATA_DICTIONARY = PROJECT_ROOT / "data" / "dictionary"

# Hugging Face Hub - dataset compartilhado do time (público, leitura sem token)
HF_REPO_ID = "pbf-feijao-mecai-usp/bf-feijao-dados"
HF_TOKEN = os.getenv("huggingface_token")
