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


@app.rout('/login')
def login():
    return render_template('login.html')


@app.rout('/register')
def register():
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
    return render_template(
        'todos.html',
        title="Megan, Get It Done!",
        tasks=tasks,
        completed_tasks=completed_tasks
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
