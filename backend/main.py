from fastapi import FastAPI
from backend.api import routes_faq
from backend.api import routes_feedback
from backend.db.mongodb import connect_to_mongo, close_mongo_connection

app = FastAPI()

app.include_router(routes_faq.router)
app.include_router(routes_feedback.router)

@app.on_event("startup")
async def startup_db():
    await connect_to_mongo()

@app.on_event("shutdown")
async def shutdown_db():
    await close_mongo_connection()
