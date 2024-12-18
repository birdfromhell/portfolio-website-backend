from datetime import datetime
from typing import Optional, List
from fastapi import FastAPI, HTTPException,Request, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from supabase import create_client, Client
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import requests


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
# app.mount("/static", StaticFiles(directory="static"), name="static")

# Setup templates
templates = Jinja2Templates(directory="templates")
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

class Skill(BaseModel):
    id: Optional[int] = None
    category: str
    name: str

class Contact(BaseModel):
        name: str
        email: str
        message: str

@app.get("/admin", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/")
async def read_root():
    return {"message": "Welcome to my portfolio API"}
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

@app.post("/upload_image/")
async def upload_image(file: UploadFile = File(...)):
    try:
        api_key = "977a4cec831e8db5c11f8e3d93efcab4"
        response = requests.post(
            "https://api.imgbb.com/1/upload",
            params={"key": api_key},
            files={"image": file.file}
        )
        response_data = response.json()
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Failed to upload image")
        return {"image_url": response_data['data']['url']}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/projects/{project_id}")
async def get_project(project_id: int):
    response = supabase.table("projects").select("*").eq("id", project_id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Project not found")
    return response.data[0]

# Endpoint untuk membuat proyek dengan URL gambar yang diunggah
@app.post("/projects")
async def create_project(project: Project, image: UploadFile = File(...)):
    try:
        image_response = await upload_image(image)
        project.image = image_response["image_url"]
        response = supabase.table("projects").insert(project.model_dump(exclude={'id'})).execute()
        return response.data[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint untuk memperbarui proyek dengan URL gambar yang diunggah
@app.put("/projects/{project_id}")
async def update_project(project_id: int, project: Project, image: UploadFile = File(...)):
    try:
        image_response = await upload_image(image)
        project.image = image_response["image_url"]
        response = supabase.table("projects").update(project.model_dump(exclude={'id'})).eq("id", project_id).execute()
        if not response.data:
            raise HTTPException(status_code=404, detail="Project not found")
        return response.data[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
@app.delete("/projects/{project_id}")
async def delete_project(project_id: int):
    response = supabase.table("projects").delete().eq("id", project_id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Project not found")
    return {"message": "Project deleted successfully"}

# Skill endpoints
@app.get("/skills")
async def get_all_skills():
    """Get all skills grouped by category"""
    response = supabase.table("skills").select("*").execute()
    
    if not response.data:
        return {}
    
    # Group skills by category
    grouped_skills: Dict[str, List[str]] = {}
    for skill in response.data:
        category = skill['category']
        if category not in grouped_skills:
            grouped_skills[category] = []
        grouped_skills[category].append(skill['name'])
    
    return grouped_skills

@app.get("/skills/raw")
async def get_raw_skills():
    """Get all skills without grouping"""
    response = supabase.table("skills").select("*").execute()
    return response.data

@app.get("/skills/{category}")
async def get_skills_by_category(category: str):
    """Get skills for a specific category"""
    response = supabase.table("skills").select("*").eq("category", category).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail=f"No skills found for category: {category}")
    return [skill['name'] for skill in response.data]

@app.post("/skills")
async def create_skill(skill: Skill):
    try:
        response = supabase.table("skills").insert(skill.model_dump(exclude={'id'})).execute()
        return response.data[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/skills/{skill_id}")
async def delete_skill(skill_id: int):
    response = supabase.table("skills").delete().eq("id", skill_id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Skill not found")
    return {"message": "Skill deleted successfully"}

@app.get("/message")
async def get_all_message():
    response = supabase.table("contacts").select("*").execute()
    return response.data

@app.post("/webhook/contact")
async def webhook_contact(contact: Contact):
        try:
            response = supabase.table("contacts").insert({
                "name": contact.name,
                "email": contact.email, 
                "message": contact.message,
                "created_at": datetime.now().isoformat()
            }).execute()
            return response.data[0]
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
    