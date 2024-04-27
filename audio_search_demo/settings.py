# coding=utf-8
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(verbose=True)

dotenv_path = Path.cwd().parent / 'env_files' / '.env.work'
if dotenv_path.exists():
    load_dotenv(dotenv_path)
else:
    print("No .env file found in the project root directory")
    exit(1)

MOVIE_NAME = os.environ.get("MOVIE_NAME")
BASE_VIDEO_URL = os.environ.get("BASE_VIDEO_URL")
EMBEDDING_MODEL = os.environ.get("EMBEDDING_MODEL")
QDRANT_URL = os.environ.get("QDRANT_URL")
QDRANT_COLLECTION_NAME = os.environ.get("QDRANT_COLLECTION_NAME")
EMBEDDING_DIM = int(os.environ.get("EMBEDDING_DIM"))