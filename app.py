from django.shortcuts import redirect
from flask import Flask ,render_template,url_for,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# __name__ is for the file name
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    content = db.Column(db.String(200),nullable=False)
    completed = db.Column(db.Integer,default=0)
    date_created = db.Column(db.DateTime,default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id



@app.route('/',methods=['POST','GET'])
def index():
    #request.method to check POSt GET
    if request.method == 'POST':
        # request.form for getting the variables
        task_content = request.form['content']
        new_task = Todo(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There is something wrong'
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()

        return render_template('index.html',tasks=tasks)

@app.route('/delete/<int:id>')
def delete(id):
    task_delete = Todo.query.get_or_404(id)
    try:
        db.session.delete(task_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem in deleting'

@app.route('/update/<int:id>',methods=['POST','GET'])
def update(id):
    # here it is creating a database object
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        # here setting the task content
        task.content = request.form['content']
        try:
            # making the update
            db.session.commit()
            return redirect('/')
        except:
            return 'Something went wrong'

    else:
        return render_template('update.html',task=task)

if __name__ == "__main__":
    app.run(debug=False)