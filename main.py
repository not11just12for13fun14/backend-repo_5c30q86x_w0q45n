import os
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from bson import ObjectId

from database import db, create_document, get_documents
from schemas import PortfolioProject, ContactMessage

app = FastAPI(title="Digital Marketing Portfolio API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Helpers

def serialize_doc(doc: dict) -> dict:
    if not doc:
        return doc
    d = dict(doc)
    _id = d.pop("_id", None)
    if isinstance(_id, ObjectId):
        d["id"] = str(_id)
    elif _id is not None:
        d["id"] = _id
    return d

# Seed sample portfolio projects if empty
@app.on_event("startup")
def seed_projects():
    if db is None:
        return
    try:
        count = db["portfolioproject"].count_documents({})
        if count == 0:
            samples = [
                {
                    "title": "E-commerce Launch Campaign",
                    "client": "NovaWear",
                    "summary": "Full-funnel launch across paid social, search, and email. 2.4x ROAS in first 30 days.",
                    "services": ["Paid Social", "SEO/SEM", "Email Drip", "Creative"],
                    "cover_url": "https://images.unsplash.com/photo-1516542076529-1ea3854896e1?q=80&w=1600&auto=format&fit=crop",
                    "metrics": {"roas": 2.4, "impressions": 1200000, "ctr": 3.8},
                },
                {
                    "title": "B2B Lead Engine",
                    "client": "Acme Cloud",
                    "summary": "Content + LinkedIn ABM program driving SQLs with a 32% MQL→SQL rate.",
                    "services": ["Content", "LinkedIn Ads", "ABM", "Landing Pages"],
                    "cover_url": "https://images.unsplash.com/photo-1522071820081-009f0129c71c?q=80&w=1600&auto=format&fit=crop",
                    "metrics": {"cpl": 42, "mql_to_sql": 32, "pipeline_usd": 240000},
                },
                {
                    "title": "App Growth Sprint",
                    "client": "FlowNote",
                    "summary": "Creative iteration loop on TikTok & UAC, +86% installs at steady CAC.",
                    "services": ["ASO", "UAC", "TikTok Ads", "Creative"],
                    "cover_url": "https://images.unsplash.com/photo-1550525811-e5869dd03032?q=80&w=1600&auto=format&fit=crop",
                    "metrics": {"installs": 56000, "cac_delta_pct": -12},
                },
            ]
            for s in samples:
                create_document("portfolioproject", s)
    except Exception:
        # Safe fail on seed
        pass

@app.get("/")
def read_root():
    return {"message": "Digital Marketing Portfolio API is running"}

@app.get("/api/hello")
def hello():
    return {"message": "Hello from the backend API!"}

@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }
    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
            response["database_name"] = db.name
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️ Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️ Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"
    return response

# Portfolio Endpoints

@app.get("/api/projects")
def list_projects(limit: Optional[int] = 12):
    try:
        docs = get_documents("portfolioproject", {}, limit)
        return [serialize_doc(d) for d in docs]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Contact form endpoint
class ContactResponse(BaseModel):
    id: str
    status: str

@app.post("/api/contact", response_model=ContactResponse)
def create_contact(message: ContactMessage):
    try:
        _id = create_document("contactmessage", message)
        return {"id": _id, "status": "received"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
