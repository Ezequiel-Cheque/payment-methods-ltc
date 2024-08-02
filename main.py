import os
import uvicorn
from pathlib import Path
from dotenv import load_dotenv

from src.app import *

load_dotenv()

if __name__ == "__main__":
    uvicorn.run(
        f"{Path(__file__).stem}:app",
        host=os.getenv("HOST"),
        port=int(os.getenv("PORT")),
        reload=True,
        log_level="info"
    )