from flask import Flask, render_template, request, redirect, session, url_for
from werkzeug.security import generate_password_hash, check_password_hash 
from datetime import timedelta
from todo import todo_bp
from extension import db
'''
werkzeug.security is a library from Werkzeug, a WSGI toolkit. Note: WSGI: Web Server Gateway Interface
generate_password_hash and check_password_hash are for encrypting and decrypting the password, respectively
'''

app = Flask(__name__)
app.secret_key = "nbhapl128844"
app.register_blueprint(todo_bp, url_prefix = "/todo")  

#Configuring SQLAlchemy to work with Flask
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False #Tells SQLAlchemy not to track modifications

db.init_app(app)

#Database model
#Represent a single row in the database => every user has their own row like id, username, password
class User_Database(db.Model): #inherit from db.Model
    #Class variables: id, username, password
    __tablename__ = "user_database"
    id = db.Column(db.Integer, primary_key = True) #the id is going to be the primary key
    
    #unique = True => no two users can have the same username
    #nullable = False => the username cannot be null
    #db.String(50) => maximum length of 50 characters
    username = db.Column(db.String(50), unique = True, nullable = False) 

    #password: cannot be NULL ==> nullable = False
    #db.String(50) => maximum length of 50 characters
    password_hash = db.Column(db.String(100), nullable = False) 

    def set_password(self, password_input):
        self.password_hash = generate_password_hash(password_input)
        
    def check_password(self, password):
       return check_password_hash(self.password_hash, password)

#Home page 
@app.route("/")
def index():
    if("username" in session):
        return redirect(url_for("dashboard"))
    else:
        error = session.pop("error", None)
        return render_template("index.html", error = error)

#Login page
#methods = ["POST"] means we're sending information
@app.route("/login", methods = ["POST"])
def login():
   #First thing: collect username and password from the form    
    username_input = request.form["username"]
    password_input = request.form["password"]
    remember = request.form.get("remember-me")
    
    # Check if the username and password are empty 
    if(username_input.strip() == "" and password_input.strip() == ""): 
        session["error"] = "Username and Password cannot be left blank!"
        return redirect(url_for("index"))
    
    # queries the User table for the record where username matches username_input 
    # and returns the first matching result by using the first() method
    user = User_Database.query.filter_by(username = username_input).first()
    
    # Check if the user exists and the password is correct
    # If yes, redirect to the dashboard page
    if not user: 
        session["error"] = "No username found! Please either check your username or sign up!"
        return redirect(url_for("index"))
    elif not user.check_password(password_input): #check if the user enter a wrong password
        session["error"] = "Wrong password"
        return redirect(url_for("index"))
    elif(user and user.check_password(password_input)):
        session["username"] = username_input
        session["user_id"] = user.id # Create a new session
        # Check if the remember-me checkbox is checked
        if(remember == "on"):
            session.permanent = True
            
            # Remember the user for 7 days
            app.permanent_session_lifetime = timedelta(days = 7) 
        else:
            session.permanent = False
        return redirect(url_for("todo.show_task")) # Redirect to the dashboard page with the tasks


# Redirect to Sign-up page
@app.route("/show_sign_up", methods = ["GET"])
def show_sign_up():
    error = session.pop("error", None)
    return render_template("sign_up.html", error = error)   

# Here we're trying to send the information to the database
# ==> methods = ["POST"] 
@app.route("/sign_up", methods = ["POST"])
def sign_up():
    username_input = request.form["username"]
    password_input = request.form["password"]
    confirm_password = request.form["confirm_password"]
    
    if(password_input != confirm_password):
        session["error"] = "Passwords do not match! Please check again"
        return redirect(url_for("show_sign_up"))
    
    user = User_Database.query.filter_by(username = username_input).first()
    
    if(user):
        session["error"] = "User already exists"
        return redirect(url_for("show_sign_up"))
    else:
        new_user = User_Database(username = username_input)
        new_user.set_password(password_input)
        
        #send new_user to User_Database
        db.session.add(new_user) 
        db.session.commit()
        session["username"] = username_input
        session["user_id"] = new_user.id #Store the id of the new user
        return redirect(url_for("dashboard"))
        
@app.route("/dashboard")    
def dashboard():
    if("username" in session):
        return redirect(url_for("todo.show_task"))
    else:
        return redirect(url_for("index"))    


@app.route("/logout")
def logout():
    if("username" in session):
        session.pop("username", None)   
        return redirect(url_for("index"))  
        
# For running the application
if __name__ in "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug = True)