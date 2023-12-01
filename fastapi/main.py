import uvicorn
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

if(__name__ == "__main__"):
    uvicorn.run('app.app:app', port=int(os.getenv("PORT", 5000)), reload=os.getenv("DEBUG"))