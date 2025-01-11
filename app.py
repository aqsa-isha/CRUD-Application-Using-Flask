from flask import Flask, render_template, request, redirect, abort
from models import db, StudentModel

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'GET':
        return render_template('createpage.html')

    if request.method == 'POST':
        hobby = request.form.getlist('hobbies')
        hobbies = ",".join(map(str, hobby))

        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']
        gender = request.form['gender']
        country = request.form['country']
        
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

@app.route('/')
def RetrieveList():
    students = StudentModel.query.all()
    return render_template('datalist.html', students=students)

@app.route('/<int:id>')
def RetrieveStudent(id):
    students = StudentModel.query.filter_by(id=id).first()
    if students:
        return render_template('data.html', students=students)
    return f"Student with id ={id} doesn't exist"

@app.route('/<int:id>/edit', methods=['GET', 'POST'])
def update(id):
    student = StudentModel.query.filter_by(id=id).first()

    if request.method == 'POST':
        if student:
            db.session.delete(student)
            db.session.commit()
        
        hobby = request.form.getlist('hobbies')
        hobbies = ",".join(map(str, hobby))
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']
        gender = request.form['gender']
        country = request.form['country']

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

    return render_template('update.html', student=student)

@app.route('/<int:id>/delete', methods=['GET', 'POST'])
def delete(id):
    student = StudentModel.query.filter_by(id=id).first()
    if request.method == 'POST':
        if student:
            db.session.delete(student)
            db.session.commit()
            return redirect('/')
        abort(404)
    return render_template('delete.html')

if __name__ == '__main__':
    # Create the database tables when the app starts
    with app.app_context():
        db.create_all()
    
    # Run the Flask app
    app.run(host='localhost', port=5000, debug=True)
