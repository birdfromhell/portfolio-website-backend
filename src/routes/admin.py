from flask import Blueprint, render_template, request, redirect, url_for, flash, session # type: ignore
from src.models.models import db, Education, Experience, Project, SkillCategory, Skill
from src.utils.auth import login_required
from datetime import datetime
import cloudinary.uploader
from werkzeug.utils import secure_filename
import os


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

@admin.route('/experience')
@login_required
def manage_experience():
    experience_list = Experience.query.all()
    return render_template('admin/experience.html', experience=experience_list)

@admin.route('/experience/add', methods=['GET', 'POST'])
@login_required
def add_experience():
    if request.method == 'POST':
        title = request.form.get('title')
        company = request.form.get('company')
        period = request.form.get('period')
        description = request.form.get('description')

        if title and company and period:
            new_experience = Experience(
                title=title,
                company=company,
                period=period,
                description=description
            )

            try:
                db.session.add(new_experience)
                db.session.commit()
                flash('Experience entry added successfully!', 'success')
            except Exception as e:
                db.session.rollback()
                flash(f'Error adding experience: {str(e)}', 'error')
        else:
            flash('Please fill all required fields', 'error')

        return redirect(url_for('admin.manage_experience'))

    return redirect(url_for('admin.manage_experience'))

@admin.route('/experience/<int:id>/edit', methods=['POST'])
@login_required
def edit_experience(id):
    experience = Experience.query.get_or_404(id)

    if request.method == 'POST':
        experience.title = request.form.get('title')
        experience.company = request.form.get('company')
        experience.period = request.form.get('period')
        experience.description = request.form.get('description')

        try:
            db.session.commit()
            flash('Experience entry updated successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating experience: {str(e)}', 'error')

    return redirect(url_for('admin.manage_experience'))

@admin.route('/experience/<int:id>/delete', methods=['POST'])
@login_required
def delete_experience(id):
    experience = Experience.query.get_or_404(id)

    try:
        db.session.delete(experience)
        db.session.commit()
        flash('Experience entry deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting experience: {str(e)}', 'error')

    return redirect(url_for('admin.manage_experience'))


@admin.route('/projects')
@login_required
def manage_projects():
    projects_list = Project.query.all()
    return render_template('admin/projects.html', projects=projects_list)

@admin.route('/projects/add', methods=['GET', 'POST'])
@login_required
def add_project():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        project_url = request.form.get('project_url')
        github_url = request.form.get('github_url')

        image_url = None
        if 'image' in request.files:
            image_file = request.files['image']
            if image_file and image_file.filename:
                try:
                    # Debug Cloudinary configuration
                    print("Cloudinary config:", {
                        "cloud_name": cloudinary.config().cloud_name,
                        "api_key": bool(cloudinary.config().api_key),  # Print True/False for security
                        "api_secret": bool(cloudinary.config().api_secret)  # Print True/False for security
                    })
                    
                    # Upload to Cloudinary
                    upload_result = cloudinary.uploader.upload(image_file)
                    image_url = upload_result.get('secure_url')
                    print(f"Image uploaded successfully: {image_url}")
                except Exception as e:
                    print(f"Cloudinary upload error: {str(e)}")
                    flash(f'Error uploading image: {str(e)}', 'error')

        if title:
            new_project = Project(
                title=title,
                description=description,
                image_url=image_url,
                project_url=project_url,
                github_url=github_url
            )

            try:
                db.session.add(new_project)
                db.session.commit()
                flash('Project added successfully!', 'success')
            except Exception as e:
                db.session.rollback()
                flash(f'Error adding project: {str(e)}', 'error')
        else:
            flash('Please provide a project title', 'error')

        return redirect(url_for('admin.manage_projects'))

    return redirect(url_for('admin.manage_projects'))


@admin.route('/projects/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_project(id):
    project = Project.query.get_or_404(id)

    if request.method == 'POST':
        project.title = request.form.get('title')
        project.description = request.form.get('description')
        project.project_url = request.form.get('project_url')
        project.github_url = request.form.get('github_url')

        if 'image' in request.files:
            image_file = request.files['image']
            if image_file and image_file.filename:
                try:
                    # Upload to Cloudinary
                    upload_result = cloudinary.uploader.upload(image_file)
                    project.image_url = upload_result.get('secure_url')
                except Exception as e:
                    flash(f'Error uploading image: {str(e)}', 'error')

        try:
            db.session.commit()
            flash('Project updated successfully!', 'success')
            return redirect(url_for('admin.manage_projects'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating project: {str(e)}', 'error')

    return render_template('admin/project_form.html', project=project)


@admin.route('/projects/<int:id>/delete', methods=['POST'])
@login_required
def delete_project(id):
    project = Project.query.get_or_404(id)

    try:
        # Optionally: Delete image from Cloudinary if needed
        # if project.image_url:
        #     # Extract public_id from URL
        #     # cloudinary.uploader.destroy(public_id)

        db.session.delete(project)
        db.session.commit()
        flash('Project deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting project: {str(e)}', 'error')

    return redirect(url_for('admin.manage_projects'))

# Skills management routes
@admin.route('/skills')
@login_required
def manage_skills():
    categories = SkillCategory.query.all()
    return render_template('admin/skills.html', categories=categories)