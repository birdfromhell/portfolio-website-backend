from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship
from typing import List
from pydantic import BaseModel
import enum

# Database Setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./portfolio.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Database Models
class SkillCategory(Base):
    __tablename__ = "skill_categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    skills = relationship("Skill", back_populates="category")

class Skill(Base):
    __tablename__ = "skills"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    category_id = Column(Integer, ForeignKey("skill_categories.id"))
    category = relationship("SkillCategory", back_populates="skills")

class Profile(Base):
    __tablename__ = "profiles"
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    nicknames = Column(String)  # Stored as comma-separated values
    role = Column(String)
    location = Column(String)
    bio = Column(String)
    languages = Column(String)  # Stored as comma-separated values

class Link(Base):
    __tablename__ = "links"
    id = Column(Integer, primary_key=True, index=True)
    platform = Column(String, unique=True, index=True)
    url = Column(String)

# Create tables
Base.metadata.create_all(bind=engine)

# Pydantic Models
class SkillBase(BaseModel):
    name: str

class SkillCreate(SkillBase):
    category_id: int

class SkillResponse(SkillBase):
    id: int
    category_id: int

    class Config:
        orm_mode = True

class CategoryBase(BaseModel):
    name: str

class CategoryCreate(CategoryBase):
    pass

class CategoryResponse(CategoryBase):
    id: int
    skills: List[SkillBase]

    class Config:
        orm_mode = True

class ProfileBase(BaseModel):
    full_name: str
    nicknames: List[str]
    role: str
    location: str
    bio: str
    languages: List[str]

class ProfileCreate(ProfileBase):
    pass

class ProfileResponse(ProfileBase):
    id: int

    class Config:
        orm_mode = True

class LinkBase(BaseModel):
    platform: str
    url: str

class LinkCreate(LinkBase):
    pass

class LinkResponse(LinkBase):
    id: int

    class Config:
        orm_mode = True

# Dependencies
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI(title="Ababil Mustaqim API", description="Personal Portfolio API with SQLite Database")

# Initialize default data
def init_db():
    db = SessionLocal()
    
    # Check if profile exists
    if not db.query(Profile).first():
        default_profile = Profile(
            full_name="Ababil Mustaqim",
            nicknames="ABABIL,MUSTAX",
            role="Backend Developer",
            location="Bandung",
            bio="I am a Backend Web & mobile Developer from Bandung. I have a passion for creating Great Backend App, But i Bad In Frontend. I have experience with various programming languages and specifically web technologies.",
            languages="Indonesian,Sundanese"
        )
        db.add(default_profile)
        
        # Add default categories and skills
        categories = {
            "Programming Languages": ["Python", "Java", "Javascript", "C++", "Kotlin"],
            "Web Frontend": ["HTML", "CSS", "Bootstrap"],
            "Web Backend": ["Django", "Rest Framework"],
            "Mobile": ["Android"],
            "Desktop": ["JavaFx"],
            "Databases": ["Mysql", "Mongodb", "Sqlite"],
            "Library & Framework": ["PyGame", "Pynecone"],
            "Development Tools": ["Visual Studio Code", "Pycharm", "Intellij Idea", "Postman", "Git", "Linux"],
            "Deployment": ["Vercel", "Netlify", "Railway", "Cpanel"],
            "Testing": ["Pytest"]
        }
        
        for cat_name, skills in categories.items():
            category = SkillCategory(name=cat_name)
            db.add(category)
            db.flush()
            
            for skill_name in skills:
                skill = Skill(name=skill_name, category_id=category.id)
                db.add(skill)
        
        # Add default links
        default_links = [
            {"platform": "Email", "url": "mailto:example@email.com"},
            {"platform": "Github", "url": "https://github.com/username"},
            {"platform": "Stackoverflow", "url": "https://stackoverflow.com/users/userid"},
            {"platform": "Instagram", "url": "https://instagram.com/username"},
            {"platform": "Linkedin", "url": "https://linkedin.com/in/username"},
            {"platform": "HackerRank", "url": "https://hackerrank.com/username"}
        ]
        
        for link in default_links:
            db.add(Link(**link))
        
        db.commit()
    db.close()

# Initialize database with default data
init_db()

# API Routes
@app.get("/")
async def read_root():
    return {"message": "Welcome to Ababil Mustaqim's Portfolio API"}

@app.get("/profile", response_model=ProfileResponse)
async def get_profile(db: Session = Depends(get_db)):
    profile = db.query(Profile).first()
    if profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")
    # Convert comma-separated strings to lists
    profile_dict = {
        "id": profile.id,
        "full_name": profile.full_name,
        "nicknames": profile.nicknames.split(","),
        "role": profile.role,
        "location": profile.location,
        "bio": profile.bio,
        "languages": profile.languages.split(",")
    }
    return profile_dict

@app.get("/skills", response_model=List[CategoryResponse])
async def get_skills(db: Session = Depends(get_db)):
    categories = db.query(SkillCategory).all()
    return categories

@app.get("/skills/{category_name}")
async def get_skills_by_category(category_name: str, db: Session = Depends(get_db)):
    category = db.query(SkillCategory).filter(SkillCategory.name == category_name).first()
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@app.get("/links", response_model=List[LinkResponse])
async def get_links(db: Session = Depends(get_db)):
    return db.query(Link).all()

@app.get("/links/{platform}")
async def get_link_by_platform(platform: str, db: Session = Depends(get_db)):
    link = db.query(Link).filter(Link.platform == platform).first()
    if link is None:
        raise HTTPException(status_code=404, detail="Link not found")
    return link

# CRUD operations for skills
@app.post("/skills", response_model=SkillResponse)
async def create_skill(skill: SkillCreate, db: Session = Depends(get_db)):
    db_skill = Skill(**skill.dict())
    db.add(db_skill)
    db.commit()
    db.refresh(db_skill)
    return db_skill

@app.put("/skills/{skill_id}", response_model=SkillResponse)
async def update_skill(skill_id: int, skill: SkillCreate, db: Session = Depends(get_db)):
    db_skill = db.query(Skill).filter(Skill.id == skill_id).first()
    if db_skill is None:
        raise HTTPException(status_code=404, detail="Skill not found")
    
    for key, value in skill.dict().items():
        setattr(db_skill, key, value)
    
    db.commit()
    db.refresh(db_skill)
    return db_skill

@app.delete("/skills/{skill_id}")
async def delete_skill(skill_id: int, db: Session = Depends(get_db)):
    db_skill = db.query(Skill).filter(Skill.id == skill_id).first()
    if db_skill is None:
        raise HTTPException(status_code=404, detail="Skill not found")
    
    db.delete(db_skill)
    db.commit()
    return {"message": "Skill deleted successfully"}
