import os
import uvicorn

# Use environment variables for host and port if available
host = os.getenv("HOST", "0.0.0.0")
port = int(os.getenv("PORT", 8000))

if __name__ == "__main__":
    uvicorn.run("app.main:app", host=host, port=port, reload=True)
