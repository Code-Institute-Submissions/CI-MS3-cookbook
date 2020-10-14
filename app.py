import os
from os import path
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)

if path.exists('env.py'):
    import env

app.config['MONGO_DBNAME'] = os.environ.get('MONGO_DBNAME')
app.config['MONGO_URI'] = os.environ.get('MONGO_URI')

mongo = PyMongo(app)


# index.html / homepage
@app.route('/')
@app.route('/index_page')
def index_page():
    return render_template("index.html", recipes=mongo.db.recipes.find())


# Browse Recipes
@app.route('/recipes_list')
def recipes_list():
    return render_template("recipes_list.html", recipes=mongo.db.recipes.find())


# Post Recipe
@app.route('/add_recipe')
def add_recipe():
    return render_template("add_recipe.html", recipes=mongo.db.recipes.find())


@app.route('/insert_recipe', methods=['POST'])
def insert_recipe():
    recipes = mongo.db.recipes
    recipes.insert_one(request.form.to_dict())
    return redirect(url_for('recipes_list'))


@app.route('/edit_recipe/<recipe_id>')
def edit_recipe(recipe_id):
    the_recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    all_meals = mongo.db.meal.find()
    return render_template('edit_recipe.html', recipe=the_recipe,
                           meal=all_meals)


@app.route('/delete_recipe/<recipe_id>')
def delete_recipe(recipe_id):
    mongo.db.recipes.remove({'_id': ObjectId(recipe_id)})
    return redirect(url_for('recipes_list'))


# Contact Us


@app.route('/contact_us')
def contact_us():
    return render_template('contact_us.html')


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
