import time
from pyngrok import ngrok
from dotenv import load_dotenv
import os
# Load environment variables from .env file
load_dotenv()

# Set your ngrok authentication token
NGROK_AUTH_TOKEN = os.getenv("NGROK_AUTH_TOKEN")
ngrok.set_auth_token(NGROK_AUTH_TOKEN)

# Define the port where FastAPI is running
FASTAPI_PORT = 8000  # Change if your FastAPI runs on a different port

# Start ngrok tunnel
try:
    tunnel = ngrok.connect(FASTAPI_PORT)
    public_url = tunnel.public_url
    print(f"🚀 FastAPI is now accessible at: {public_url}")
    print(f"🔗 Access the /ask endpoint at: {public_url}/ask")

    # Keep script running
    while True:
        time.sleep(60)
except Exception as e:
    print(f"⚠️ Error starting ngrok: {e}")
