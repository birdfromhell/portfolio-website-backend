from flask import Blueprint, jsonify
from src.models.models import Education, Experience, Project, SkillCategory, Skill

api = Blueprint('api', __name__)

@api.route('/education', methods=['GET'])
def get_education():
    education = Education.query.all()
    return jsonify([{
        'id': edu.id,
        'degree': edu.degree,
        'institution': edu.institution,
        'period': edu.period,
        'field': edu.description
    } for edu in education])

@api.route('/experiences', methods=['GET'])
def get_experience():
    experiences = Experience.query.all()
    return jsonify([{
        'id': exp.id,
        'title': exp.title,
        'company': exp.company,
        'period': exp.period,
        'description': exp.description
    } for exp in experiences])

@api.route('/projects', methods=['GET'])
def get_projects():
    projects = Project.query.all()
    return jsonify([{
        'id': proj.id,
        'title': proj.title,
        'description': proj.description,
        'image': proj.image_url,
        'preview': proj.project_url,
        'github': proj.github_url,
        'created_at': proj.created_at.isoformat()
    } for proj in projects])

@api.route('/skills', methods=['GET'])
def get_skills():
    categories = SkillCategory.query.all()
    return jsonify([{
        'id': cat.id,
        'name': cat.name,
        'description': cat.description,
        'skills': [{
            'id': skill.id,
            'name': skill.name
        } for skill in cat.skills]
    } for cat in categories])

@api.route('/skills/<int:category_id>', methods=['GET'])
def get_skills_by_category(category_id):
    category = SkillCategory.query.get_or_404(category_id)
    return jsonify({
        'category': category.name,
        'description': category.description,
        'skills': [{
            'id': skill.id,
            'name': skill.name
        } for skill in category.skills]
    })