import os

MONGODB_URI = os.environ.get("MONGODB_URI")
DATABASE_NAME = os.environ.get("DATABASE_NAME", "3davatar")

if not MONGODB_URI:
    raise RuntimeError(
        "MONGODB_URI is not set. Configure it via environment variables or .env file."
    )
