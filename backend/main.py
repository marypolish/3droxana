from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
from backend.api import routes_faq
from backend.api import routes_feedback
from backend.api import routes_links
from backend.api import routes_sessions
from backend.api import routes_users
from backend.db.mongodb import connect_to_mongo, close_mongo_connection
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # або ["*"] для всіх
    allow_credentials=True,
    allow_methods=["*"],  # або ['POST', 'GET'] тощо
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="frontend"), name="static")

@app.get("/", response_class=FileResponse)
async def serve_frontend():
    print("Serving index.html...")
    return FileResponse(os.path.join("frontend", "pages", "index.html"))

@app.get("/auth", response_class=FileResponse)
async def serve_auth():
    return FileResponse(os.path.join("frontend", "pages", "auth.html"))

@app.get("/chat", response_class=FileResponse)
async def serve_faq():
    return FileResponse(os.path.join("frontend", "pages", "chat.html"))

@app.get("/history", response_class=FileResponse)
async def serve_faq():
    return FileResponse(os.path.join("frontend", "pages", "history.html"))

app.include_router(routes_faq.router)
app.include_router(routes_feedback.router)
app.include_router(routes_links.router)
app.include_router(routes_sessions.router)
app.include_router(routes_users.router)
@app.on_event("startup")
async def startup_db():
    await connect_to_mongo()

@app.on_event("shutdown")
async def shutdown_db():
    await close_mongo_connection()
