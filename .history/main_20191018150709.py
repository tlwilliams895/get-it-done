from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://get-it-done:beproductive@localhost:8889/get-it-done'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = "someSecretCodeword"


class Task(db.Model):
    # Anytime a new column is added here, remember to drop_all then create_all
    # in Git Bash to reflect and update changes to database
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    completed = db.Column(db.Boolean)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, name):
        self.name = name
        self.completed = False
        self.owner = owner


# User object to enter is email address and password in MyPHPadmin
class User(db.Model):
    # Create fields/columns for db; add more later
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))

    # Initializer/Constructor
    def __init__(self, email, password):
        self.email = email
        self.password = password


# .before_request - Create required login to check if user has logged-in website
@app.before_request
def require_login():
    allowed_routes = ['login', 'register']
    if request.endpoint not in allowed_routes and 'email' not in session:
        return redirect('/login')
# The code about prevents access to other web pages until user login or register


# Login Handlers will process requests to database
# Add the request types using inputs from login.html
@app.route('/login', methods=['POST', 'GET'])
def login():
    # This request will login the user with proper credentials
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        # Verifies email/user and password together as a result set
        user = User.query.filter_by(email=email).first()

        # Checks if user/email exists
        if user and user.password == password:
            # Enter user/email session data to store here
            session['email'] = email
            flash("Login Successful")
            # Remember that the user MUST be logged in
            return redirect('/')
        else:
            # Create flash message category
            flash()
            # Explain why login failed
            return '<h2>*USER*ERROR*</h2>'

    return render_template('login.html', message="*Please Log In*")


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        verify = request.form['verify']

        # Always validate user's data means good user found
        # Enter code here

        existing_user = User.query.filter_by(email=email).first()
        if not existing_user:
            new_user = User(email, password)
            db.session.add(new_user)
            db.session.commit()
            # User/email session data will remember that the user logged-in
            session['email'] = email

            # Remember the user
            return redirect('/')
        else:
            # User better response messaging
            return '<h2>*Whoa, Duplicate User!*</h2>'

    return render_template('register.html')


# Log-out user here/remove user email and redirect to main page
@app.route('/logout')  # or ('/logout', methods=['GET'])
def logout():
    del session['email']
    return redirect('/')


# Global task list is commented out because the MySQL database is being used now
# tasks = []


@app.route('/', methods=['POST', 'GET'])
def index():

    # Specify that a user has many tasks and you want SQLAlchemy to look for matches between the two
    # Get the owner of the task so that you can pass that into the Task constructor
    owner = User.query.filter_by(email=session['email']).first()

    if request.method == 'POST':
        task_name = request.form['task']
        # Add owner
        new_task = Task(task_name, owner)
        db.session.add(new_task)
        db.session.commit()

        # Removed: Will used an object to create a new object in the db
        # tasks.append(task)

    # Add .filter_by to output the uncompleted tasks by value and pair
    tasks = Task.query.filter_by(completed=False, owner=owner).all()
    # Displays completed tasks
    completed_tasks = Task.query.filter_by(completed=True, owner=owner).all()
    # Watch Part 4 Video:
    # remove_tasks = Task.query.filter_by(remove_tasks=True).all()
    return render_template(
        'todos.html',
        title="Megan, Get It Done!",
        tasks=tasks,
        completed_tasks=completed_tasks,
        # remove_tasks=remove_tasks
    )


@app.route('/delete-task', methods=['POST'])
def delete_task():

    task_id = int(request.form['task-id'])
    task = Task.query.get(task_id)
    task.completed = True
    db.session.add(task)

    # Removed to update delete functions
    # completed_tasks = False
    # db.session.delete(completed_tasks)
    # How can I delete the completed tasks to disappear in todos.html?
    db.session.commit()

    return redirect('/')


if __name__ == '__main__':
    app.run()
