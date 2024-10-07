from flask import Flask, render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///crud.db'
db = SQLAlchemy(app)

#Athlete Model
class Athlete(db.Model):
    __tablename__ = 'Athletes'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True )
    firstname = db.Column(db.String(20))
    lastname = db.Column(db.String(20))
    jersey = db.Column(db.Integer)
    positions = db.Column(db.String(20))

with app.app_context():
    db.create_all()

#Included in the index route is the ability to add new athletes
#this was done to showcase using a modal on the same page.
#Edit and delete will use normal templating
@app.route('/',methods = ['GET','POST'])
def index():
    if request.method == "POST":
        #retrieve form data
        firstname = request.form["firstname"]
        lastname = request.form["lastname"]
        jersey = request.form["jersey"]
        positions = request.form["positions"]
        #create new instance of model
        new_athlete = Athlete(firstname=firstname,lastname=lastname,jersey=jersey,positions=positions)

        #add athlete to the db
        db.session.add(new_athlete)
        db.session.commit()
        return redirect("/")
    elif request.method == "GET":
        #show list of athletes
        athletes = Athlete.query.all()
        return render_template("index.html", athletes=athletes)
    
#UPDATING ATHLETE INFO
@app.route('/edit/<int:id>', methods=["GET","POST"])
def edit_athlete(id):
    athlete = Athlete.query.get(id)
    if request.method == "POST":
        athlete.firstname = request.form["firstname"]
        athlete.lastname = request.form["lastname"]
        athlete.jersey = request.form["jersey"]
        athlete.positions = request.form["positions"]
        db.session.commit()
        return redirect("/")
    else:
        return render_template("edit.html", athlete=athlete)

#DELETING AN ATHLETE
@app.route('/delete/<int:id>', methods=["GET"])
def delete_athlete(id):
    athlete = Athlete.query.get(id)
    db.session.delete(athlete)
    db.session.commit()
    return redirect("/")
    

if __name__ == "__main__":
    app.run(debug=True)

