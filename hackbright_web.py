"""A web application for tracking projects, students, and student grades."""

from flask import Flask, request, render_template, redirect

import hackbright

app = Flask(__name__)

@app.route("/")
def show_homepage():
    """Show homepage."""

    students = hackbright.get_all_students()

    projects = hackbright.get_all_projects()


    return render_template('homepage.html', students=students, projects=projects)



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


@app.route("/create-project", methods=['GET'])
def create_project_form():
    """Show form for adding a project."""

    return render_template('create-project.html')


@app.route("/create-project", methods=['POST'])
def show_new_project():
    """Show form for searching for a project."""

    title = request.form.get('title')
    description = request.form.get('description')
    max_grade = request.form.get('max_grade')

    hackbright.make_new_project(title, description, max_grade)

    return redirect('/project/' + title)


@app.route("/assign-grades", methods=['GET'])
def show_grades_form():
    """Show form for adding a grade to a project."""

    students = hackbright.get_all_students()

    projects = hackbright.get_all_projects()

    return render_template('assign-grades.html', students=students,
        projects=projects)


@app.route("/assign-grades", methods=['POST'])
def post_grades():
    """Assign new grades to the hackbright db"""

    grade = request.form.get('grade')
    title = request.form.get('title')
    github = request.form.get('github')

    hackbright.assign_grade(github, title, grade)

    return redirect('/project/' + title)


@app.route('/project/<title>')
def show_project(title):
    """Show the information about specific projects"""

    project_info = hackbright.get_project_by_title(title)

    #a list of tuples contains all student grades for a project by its title
    student_grades = hackbright.get_grades_by_title(title)

    return render_template('project-info.html',
                            project_info=project_info,
                            student_grades=student_grades)




if __name__ == "__main__":
    hackbright.connect_to_db(app)
    app.run(debug=True)
