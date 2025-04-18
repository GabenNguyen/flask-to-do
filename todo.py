from flask import Blueprint, render_template, request, redirect, session, url_for
from extension import db

todo_bp = Blueprint("todo", __name__, template_folder="templates")


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key = True)
    task_name = db.Column(db.String(1000), nullable = False)
    done = db.Column(db.Boolean, default = False) # By default, the task is not done
    
    # Foreign key
    # By default, SQLAlchemy CamelCase into snake_case. So User_Database => user__database
    # The reason for the double underscore because the D in User_Database is treated like a new word
    # Ex: If UserDatabase => user_database
    # But here because we have an underscore in the name: User_Database ==> user__database
    # Naming convention
    user_id = db.Column(db.Integer, db.ForeignKey("user_database.id"), nullable = False)
        

@todo_bp.route("/show_task")
def show_task():
    if("username" in session and "user_id" in session):
        user_id = session['user_id']
        tasks = Task.query.filter_by(user_id = user_id).all()
        return render_template("dashboard.html", user_task = tasks, username = session["username"])
    else:
        return redirect(url_for("todo.show_task"))

@todo_bp.route("/add_task", methods = ["POST"])
def add_task():
    task_name = request.form.get("task_name")
    user_id = session["user_id"]
    
    if("user_id" not in session):
        session["error"] = "Please log in first to add tasks!"
        return redirect(url_for("index"))
    
    if(task_name.strip() == ""):
        session["error"] = "Please enter a task!"
        return redirect(url_for("todo.show_task"))
    else:
        new_task = Task(task_name = task_name, done = False, user_id = user_id)
        db.session.add(new_task)
        db.session.commit()
        return redirect(url_for("todo.show_task"))
  
#Delete the task by task_id
#<int:task_id> convert the task_id to an integer
@todo_bp.route("/delete_task/<int:task_id>", methods = ["POST"])
def delete_task(task_id):
    task = Task.query.filter_by(task_id=task_id, user_id=session["user_id"]).first() #get the task_id
    
    if("user_id" not in session):
        session["error"] = "Please log in first to delete a task"
        return redirect(url_for("index"))
    
    if(task):
        db.session.delete(task) 
        db.session.commit()
        return redirect(url_for("todo.show_task"))  

# @todo_bp.route("/edit_task/<int:task_id>", methods = ["POST"])
# def edit_task(task_id):
#     task = Task.query.filter_by(task_id = task_id, user_id = session["user_id"]).first()
#     if(task.strip() == ""):
#         return redirect(url_for("todo.show_task"))
#     else:
#         new_content= request.form.get("content")     
        