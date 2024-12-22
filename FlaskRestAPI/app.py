from flask import Flask, render_template, request, redirect, abort
from models import db, StudentModel

app = Flask(__name__)

# Configure the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Function to create tables
def create_tables():
    with app.app_context():  # Ensure the app context is active
        db.create_all()

@app.route('/', methods=['GET'])
def home():
    # Display a list of students on the home page
    students = StudentModel.query.all()
    return render_template('index.html', students=students)

@app.route('/<int:id>/edit', methods=['GET', 'POST'])
def update(id):
    student = StudentModel.query.filter_by(id=id).first()
    if not student:
        abort(404)  # Student not found

    if request.method == 'POST':
        try:
            # Update student details
            hobby = request.form.getlist('hobbies')
            hobbies = ",".join(map(str, hobby))
            student.first_name = request.form.get('first_name', student.first_name)
            student.last_name = request.form.get('last_name', student.last_name)
            student.email = request.form.get('email', student.email)
            student.password = request.form.get('password', student.password)
            student.gender = request.form.get('gender', student.gender)
            student.country = request.form.get('country', student.country)
            student.hobbies = hobbies

            db.session.commit()
            return redirect('/')
        except Exception as e:
            db.session.rollback()  # Roll back in case of error
            return f"An error occurred while updating: {e}"

    return render_template('update.html', student=student)

@app.route('/<int:id>/delete', methods=['GET', 'POST'])
def delete(id):
    # Fetch the student by ID
    student = StudentModel.query.filter_by(id=id).first()
    if not student:
        abort(404)  # Student not found

    if request.method == 'POST':
        try:
            db.session.delete(student)
            db.session.commit()
            return redirect('/')
        except Exception as e:
            db.session.rollback()  # Roll back in case of error
            return f"An error occurred while deleting: {e}"

    # Render the delete confirmation page
    return render_template('delete.html', student=student)

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'GET':
        return render_template('create.html')

    if request.method == 'POST':
        try:
            # Handle POST request for adding a new student
            hobby = request.form.getlist('hobbies')
            hobbies = ",".join(map(str, hobby))
            first_name = request.form.get('first_name')
            last_name = request.form.get('last_name')
            email = request.form.get('email')
            password = request.form.get('password')
            gender = request.form.get('gender')
            country = request.form.get('country')

            # Create a new student record
            student = StudentModel(
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password,
                gender=gender,
                hobbies=hobbies,
                country=country
            )
            db.session.add(student)
            db.session.commit()
            return redirect('/')
        except Exception as e:
            db.session.rollback()  # Roll back in case of error
            return f"An error occurred while creating: {e}"

if __name__ == '__main__':
    create_tables()  # Create tables before starting the app
    app.run(host='localhost', port=5000)
