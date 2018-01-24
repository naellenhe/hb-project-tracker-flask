"""A web application for tracking projects, students, and student grades."""

from flask import Flask, request, render_template

import hackbright

app = Flask(__name__)


@app.route("/student")
def get_student():
    """Show information about a student."""

    github = request.args.get('github')

    first, last, github = hackbright.get_student_by_github(github)

    grades = hackbright.get_grades_by_github(github)

    return render_template('student_info.html',
        github=github, first=first, last=last, grades=grades)


@app.route("/student-search")
def get_student_form():
    """Show form for searching for a student."""

    return render_template('search.html')


@app.route("/create-student")
def create_student_form():
    """Show form for adding a student."""

    return render_template('create-student.html')


@app.route("/create-student",methods=['POST'])
def show_new_student():
    """Show form for searching for a student."""

    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    github = request.form.get('github')

    hackbright.make_new_student(first_name, last_name, github)

    return render_template('show-student.html',
        first_name=first_name, last_name=last_name,github=github)


@app.route('/project/<title>')
def show_project(title):
    """Show the information about specific projects"""

    project_info = hackbright.get_project_by_title(title)

    return render_template('project-info.html', project_info=project_info)



if __name__ == "__main__":
    hackbright.connect_to_db(app)
    app.run(debug=True)
