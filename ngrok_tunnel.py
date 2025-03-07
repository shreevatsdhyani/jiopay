import time
from pyngrok import ngrok

# Set your ngrok authentication token
NGROK_AUTH_TOKEN = "2tvpKEi9xNCH0Ppr215W8eOWXHl_4ZxQjwYiEV6xb2y4RSoAD"  # Replace with your token
ngrok.set_auth_token(NGROK_AUTH_TOKEN)

# Define the port where FastAPI is running
FASTAPI_PORT = 8002  # Change if your FastAPI runs on a different port

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
