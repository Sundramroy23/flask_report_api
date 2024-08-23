from flask import Flask, render_template, redirect, request, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Configuration for SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)

# Define the model for the tasks
class Tasks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    desc = db.Column(db.String(200), nullable=False)
    status = db.Column(db.Boolean, default=False)

    def __init__(self, desc, status):
        self.desc = desc
        self.status = status

# Ensure the database tables are created
with app.app_context():
    db.create_all()

def complete():
    completed_tasks = len(Tasks.query.filter_by(status=True).all())
    total_tasks = Tasks.query.count()
    return completed_tasks, total_tasks

# Define routes
@app.route('/', methods=['GET', 'POST'])
def index():
    tasks = Tasks.query.all()
    completed_tasks, total_tasks = complete()
    return render_template('index.html', tasks=tasks, completed_tasks=completed_tasks, total_tasks=total_tasks)

@app.route('/add_task', methods=['POST'])
def add_task():
    if request.method == 'POST':
        desc = request.form['task']
        complete = False
        new_task = Tasks(desc=desc, status=complete)
        db.session.add(new_task)
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:task_id>', methods=['GET'])
def delete(task_id):
    task_to_delete = Tasks.query.get_or_404(task_id)
    db.session.delete(task_to_delete)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/update/<int:task_id>')
def update(task_id):
    task_to_complete = Tasks.query.get_or_404(task_id)
    task_to_complete.status = not task_to_complete.status
    db.session.commit()
    return redirect(url_for('index'))



if __name__ == '__main__':
    app.run(debug=True)
