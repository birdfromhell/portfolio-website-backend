from flask import Blueprint, render_template, request, redirect, url_for, flash, session # type: ignore
from src.models.models import db, Education, Experience, Project, SkillCategory, Skill
from src.utils.auth import login_required
from datetime import datetime

admin = Blueprint('admin', __name__)

@admin.route('/login', methods=['GET', 'POST'])
def login():
    # Redirect if user is already logged in
    if 'user_id' in session:
        return redirect(url_for('admin.dashboard'))
        
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Simple authentication - replace with proper auth system in production
        if username == "admin" and password == "admin123":
            session['user_id'] = 1
            flash('Welcome back!', 'success')
            return redirect(url_for('admin.dashboard'))
        flash('Invalid username or password', 'error')
    return render_template('admin/login.html')

@admin.route('/dashboard')
@login_required
def dashboard():
    # Get counts for dashboard statistics
    education_count = Education.query.count()
    experience_count = Experience.query.count()
    project_count = Project.query.count()
    skill_count = Skill.query.count()
    
    context = {
        'education_count': education_count,
        'experience_count': experience_count,
        'project_count': project_count,
        'skill_count': skill_count,
        'current_year': datetime.now().year
    }
    
    return render_template('admin/dashboard.html', **context)

@admin.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('admin.login'))

# Education management routes
@admin.route('/education')
@login_required
def manage_education():
    education_list = Education.query.all()
    return render_template('admin/education.html', education=education_list)

@admin.route('/education/add', methods=['GET', 'POST'])
@login_required
def add_education():
    if request.method == 'POST':
        degree = request.form.get('degree')
        institution = request.form.get('institution')
        period = request.form.get('period')
        description = request.form.get('description')
        
        if degree and institution and period:
            new_education = Education(
                degree=degree,
                institution=institution,
                period=period,
                description=description
            )
            
            try:
                db.session.add(new_education)
                db.session.commit()
                flash('Education entry added successfully!', 'success')
            except Exception as e:
                db.session.rollback()
                flash(f'Error adding education: {str(e)}', 'error')
        else:
            flash('Please fill all required fields', 'error')
        
        return redirect(url_for('admin.manage_education'))
    
    # If GET request, redirect to education management page
    return redirect(url_for('admin.manage_education'))

@admin.route('/education/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_education(id):
    education = Education.query.get_or_404(id)
    
    if request.method == 'POST':
        education.degree = request.form.get('degree')
        education.institution = request.form.get('institution')
        education.period = request.form.get('period')
        education.description = request.form.get('description')
        
        try:
            db.session.commit()
            flash('Education entry updated successfully!', 'success')
            return redirect(url_for('admin.manage_education'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating education: {str(e)}', 'error')
    
    return render_template('admin/education_form.html', education=education)

@admin.route('/education/<int:id>/delete', methods=['POST'])
@login_required
def delete_education(id):
    education = Education.query.get_or_404(id)
    
    try:
        db.session.delete(education)
        db.session.commit()
        flash('Education entry deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting education: {str(e)}', 'error')
        
    return redirect(url_for('admin.manage_education'))

# Experience management routes
@admin.route('/experience')
@login_required
def manage_experience():
    experience_list = Experience.query.all()
    return render_template('admin/experience.html', experience=experience_list)

# Project management routes
@admin.route('/projects')
@login_required
def manage_projects():
    projects_list = Project.query.all()
    return render_template('admin/projects.html', projects=projects_list)

# Skills management routes
@admin.route('/skills')
@login_required
def manage_skills():
    categories = SkillCategory.query.all()
    return render_template('admin/skills.html', categories=categories)