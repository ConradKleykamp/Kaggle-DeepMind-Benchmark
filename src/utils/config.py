import os
from dotenv import load_dotenv

load_dotenv()

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

RESULTS_DIR = os.path.join(PROJECT_ROOT, "results")
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
