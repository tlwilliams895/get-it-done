from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://get-it-done:beproductive@localhost:8889/get-it-done'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Task(db.Model):
    # Anytime a new column is added here, remember to drop_all then create_all
    # in Git Bash to reflect and update changes to database
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    completed = db.Column(db.Boolean)

    def __init__(self, name):
        self.name = name
        self.completed = False

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

# Login Handlers will process requests to database
# Add the request types using inputs from login.html
@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()

        if user and user.password == password:
            # Remember that the user MUST be logged in
            return redirect('/')
        else:
            # Explain why login failed
            return '<h1>Major*User*ERROR!!</h1>'

    return render_template('login.html')


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

            # Remember the user
            return redirect('/')
        else:
            # User better response messaging
            return "Whoa, Duplicate User!"

    return render_template('register.html')


# Global task list is commented out because a
# MySQL database is being used now
# tasks = []


@app.route('/', methods=['POST', 'GET'])
def index():

    if request.method == 'POST':
        task_name = request.form['task']
        new_task = Task(task_name)
        db.session.add(new_task)
        db.session.commit()
        # Removed: Will used an object to create a new object in the db
        # tasks.append(task)

    # Add .filter_by to output the uncompleted tasks by value and pair
    tasks = Task.query.filter_by(completed=False).all()
    # Displays completed tasks
    completed_tasks = Task.query.filter_by(completed=True).all()
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
    # db.session.delete(task)
    db.session.commit()

    return redirect('/')


if __name__ == '__main__':
    app.run()
