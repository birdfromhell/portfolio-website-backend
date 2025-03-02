from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Education(db.Model):
    __tablename__ = 'education'
    id = db.Column(db.Integer, primary_key=True)
    degree = db.Column(db.String(100), nullable=False)
    institution = db.Column(db.String(100), nullable=False)
    period = db.Column(db.String(100), nullable=False)  # e.g. "2019 - 2023"
    description = db.Column(db.Text)

class Experience(db.Model):
    __tablename__ = 'experiences'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    company = db.Column(db.String(100), nullable=False) 
    period = db.Column(db.String(100), nullable=False)  # e.g. "August 2019 - June 2022"
    description = db.Column(db.Text)
    
class Project(db.Model):
    __tablename__ = 'projects'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    image_url = db.Column(db.String(255))
    project_url = db.Column(db.String(255))
    github_url = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class SkillCategory(db.Model):
    __tablename__ = 'skill_categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(db.Text)
    skills = db.relationship('Skill', backref='category_ref', lazy=True)

class Skill(db.Model):
    __tablename__ = 'skills'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('skill_categories.id'), nullable=False)
