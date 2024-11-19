from datetime import datetime
from typing import Optional, List
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from supabase import create_client, Client

# Initialize FastAPI app
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Supabase configuration
SUPABASE_URL = "https://zvoagczrhwvanijcbgef.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inp2b2FnY3pyaHd2YW5pamNiZ2VmIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzIwMzc3MjgsImV4cCI6MjA0NzYxMzcyOH0.MdMH9NAKhBuOJcyMtKkPYV67qYBsr4MwbJNI0vbDV9Q"

# Initialize Supabase client
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

class Education(BaseModel):
    id: Optional[int] = None
    degree: str
    field: str
    institution: str
    period: str

class Experience(BaseModel):
    id: Optional[int] = None
    title: str
    company: str
    period: str
    description: str

class Project(BaseModel):
    id: Optional[int] = None
    title: str
    desc: str
    preview: Optional[str]
    github: Optional[str]
    image: Optional[str]

# Education endpoints
@app.get("/education")
async def get_all_education():
    response = supabase.table("education").select("*").execute()
    return response.data

@app.get("/education/{edu_id}")
async def get_education(edu_id: int):
    response = supabase.table("education").select("*").eq("id", edu_id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Education not found")
    return response.data[0]

@app.post("/education")
async def create_education(education: Education):
    try:
        response = supabase.table("education").insert(education.model_dump(exclude={'id'})).execute()
        return response.data[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/education/{edu_id}")
async def update_education(edu_id: int, education: Education):
    response = supabase.table("education").update(education.model_dump(exclude={'id'})).eq("id", edu_id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Education not found")
    return response.data[0]

@app.delete("/education/{edu_id}")
async def delete_education(edu_id: int):
    response = supabase.table("education").delete().eq("id", edu_id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Education not found")
    return {"message": "Education deleted successfully"}

# Experience endpoints
@app.get("/experiences")
async def get_all_experiences():
    response = supabase.table("experiences").select("*").execute()
    return response.data

@app.get("/experiences/{exp_id}")
async def get_experience(exp_id: int):
    response = supabase.table("experiences").select("*").eq("id", exp_id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Experience not found")
    return response.data[0]

@app.post("/experiences")
async def create_experience(experience: Experience):
    try:
        response = supabase.table("experiences").insert(experience.model_dump(exclude={'id'})).execute()
        return response.data[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/experiences/{exp_id}")
async def update_experience(exp_id: int, experience: Experience):
    response = supabase.table("experiences").update(experience.model_dump(exclude={'id'})).eq("id", exp_id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Experience not found")
    return response.data[0]

@app.delete("/experiences/{exp_id}")
async def delete_experience(exp_id: int):
    response = supabase.table("experiences").delete().eq("id", exp_id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Experience not found")
    return {"message": "Experience deleted successfully"}

# Project endpoints
@app.get("/projects")
async def get_all_projects():
    response = supabase.table("projects").select("*").execute()
    return response.data

@app.get("/projects/{project_id}")
async def get_project(project_id: int):
    response = supabase.table("projects").select("*").eq("id", project_id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Project not found")
    return response.data[0]

@app.post("/projects")
async def create_project(project: Project):
    try:
        response = supabase.table("projects").insert(project.model_dump(exclude={'id'})).execute()
        return response.data[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/projects/{project_id}")
async def update_project(project_id: int, project: Project):
    response = supabase.table("projects").update(project.model_dump(exclude={'id'})).eq("id", project_id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Project not found")
    return response.data[0]

@app.delete("/projects/{project_id}")
async def delete_project(project_id: int):
    response = supabase.table("projects").delete().eq("id", project_id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Project not found")
    return {"message": "Project deleted successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)