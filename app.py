from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SECRET_KEY'] = '624ccc489f7140c8a60dc71b7dca42ab'
SQLALCHEMY_TRACK_MODIFICATIONS = True

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Todo(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(200))



@app.route("/home", methods=["GET", "POST"])
@app.route("/")
def home():
    if request.method == "POST":
        title = request.form["title"]
        todo = Todo(title = title)
        db.session.add(todo)
        db.session.commit()
        return redirect('/')
    datas = Todo.query.all()
    return render_template('index.html', data=datas)


@app.route("/remove/<int:todoid>")
def removeTodo(todoid):
    todo = db.session.query(Todo).filter_by(id=todoid).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')

@app.route("/update/<int:todoid>")
def update(todoid):
    todo = db.session.query(Todo).filter_by(id=todoid).first()
    return render_template('update.html', todo=todo)
  
    return redirect('/')

@app.route('/updatetodo', methods=[ "POST"])
def updateTodo():
    title = request.form['title']
    id = request.form['todoid']
    todo = db.session.query(Todo).filter_by(id=id).first()
    todo.title = title
    db.session.commit()
   
    return redirect('/')
 


if __name__ == "__main__":
    app.run(debug=True)