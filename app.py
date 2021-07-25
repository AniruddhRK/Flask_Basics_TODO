from flask import Flask, request, render_template,redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc,asc
from datetime import datetime
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
db = SQLAlchemy(app)
tasks = []
#create DataBase Model
class Task(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    task = db.Column(db.String(100),nullable=False)
    date_created = db.Column(db.DateTime,default=datetime.utcnow)
    completed = db.Column(db.Boolean,default=False)
    
    # def __repr__(self):
        # return '<Name%r> %self.id'
@app.route('/',methods=['GET','POST'])
def index():
    title = "TODO"
    if request.method == 'POST':
        task = request.form['task']
        tasks.append(task)
        return render_template('index.html',title=title,tasks = tasks)
    else:    
        return render_template('index.html',title=title)

@app.route('/Add',methods=['POST','GET'])
def Add():
    title = 'TODO'
    if request.method == 'POST':
        task = request.form['task']
        add_task  = Task(task=task)
        try: 
            if task:
                db.session.add(add_task)
                db.session.commit()
                return redirect('/Add')
            else:
                return redirect('/Add')
        except:
            return 'You had an error in adding task to database'
    else:    
        tasks = Task.query.order_by(asc(Task.date_created))
        return render_template('index.html',title=title,tasks =tasks)
@app.route('/completed/<int:id>')
def completed(id):
    taskCompleted = Task.query.get_or_404(id)
    try:
        if taskCompleted.completed:
            taskCompleted.completed = False
        else:
            taskCompleted.completed = True
        db.session.commit()
        return redirect('/Add')
    except:
        return 'There is an error while updating for completion'
@app.route('/delete/<int:id>',methods=['POST','GET'])
def delete(id):
    task_to_delete = Task.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/Add')
    except:
        return 'There occured an error in Deleting a task!!'
