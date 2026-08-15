"""
Vercel Serverless Function Entry Point for AdAIPS.

This file exports the FastAPI ASGI application instance (`app`)
so Vercel's Python runtime routes HTTP requests directly into FastAPI.
"""

import os
import sys
from pathlib import Path

# Add project root to sys.path to enable backend.* imports
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from backend.api.main import app
