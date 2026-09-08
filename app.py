#Evan Mitchell
#Created On: 10/7/2024
#Updated On: 9/8/2026
#Basic Crud operations to showcase knowledge of Flask and HTML
#Utilizes a SQLite db
#In the interest of saving time, the delete method is called via a get and does not utilize an alert to confirm 
#the user intends to complete the action.

####
#Refactoring to be a game review/rating/played tracking system.
####


from flask import Flask, render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///crud.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

#Athlete Model
class Game(db.Model):
    __tablename__ = 'Games'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True )
    title = db.Column(db.String(50))
    developer = db.Column(db.String(50))
    publisher = db.Column(db.String(50))
    available_platforms = db.Column(db.String(100))

class Review(db.Model):
    __tablename__ = 'Reviews'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    game_id = db.Column(db.Integer, db.ForeignKey('Games.id'))
    review = db.Column(db.String(500))
    rating = db.Column(db.Integer)
    completed = db.Column(db.Boolean)
    platform = db.Column(db.String(50))
    user_id = db.Column(db.Integer)

#Included in the index route is the ability to add new games
#this was done to showcase using a modal on the same page.
#Edit and delete will use normal templating
@app.route('/',methods = ['GET','POST'])
def index():
    if request.method == "POST":
        #retrieve form data
        title = request.form["title"]
        developer = request.form["developer"]
        publisher = request.form["publisher"]
        available_platforms = request.form["available_platforms"]
        #create new instance of model
        new_game = Game(title=title, developer=developer, publisher=publisher, available_platforms=available_platforms)

        #add game to the db
        db.session.add(new_game)
        db.session.commit()
        return redirect("/")
    elif request.method == "GET":
        #show list of games
        games = Game.query.all()
        return render_template("index.html", games=games)
    
#UPDATING GAME INFO
@app.route('/edit/<int:id>', methods=["GET","POST"])
def edit_game(id):
    game = Game.query.get(id)
    if request.method == "POST":
        game.title = request.form["title"]
        game.developer = request.form["developer"]
        game.publisher = request.form["publisher"]
        game.available_platforms = request.form["available_platforms"]
        db.session.commit()
        return redirect("/")
    else:
        return render_template("edit.html", game=game)

#DELETING A GAME
@app.route('/delete/<int:id>', methods=["POST"])
def delete_game(id):
    game = Game.query.get(id)
    db.session.delete(game)
    db.session.commit()
    return redirect("/")

@app.route('/reviews')
def reviews():
    user_id = 1  # Replace with the actual user ID as needed
    all_reviews = Review.query.filter_by(user_id=user_id).all()
    return render_template("reviews.html", reviews=all_reviews)

@app.route('/add_review', methods=["GET", "POST"])
def add_review():
    if request.method == "POST":
        game_id = request.form["game_id"]
        review = request.form["review"]
        rating = request.form["rating"]
        completed = request.form.get("completed") == "on"
        platform = request.form["platform"]
        user_id = 1  # Replace with the actual user ID as needed

        new_review = Review(game_id=game_id, review=review, rating=rating, completed=completed, platform=platform, user_id=user_id)
        db.session.add(new_review)
        db.session.commit()
        return redirect("/reviews")
    games = Game.query.all()
    return render_template("add_review.html", games=games)

if __name__ == "__main__":
    app.run(debug=True)

