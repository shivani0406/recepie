from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, FileField
from wtforms.validators import DataRequired, Length, EqualTo
from werkzeug.security import generate_password_hash, check_password_hash
from flask_migrate import Migrate
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from datetime import datetime
import os
from flask_login import current_user, login_required, login_user, logout_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    recipes = db.relationship('Recipe', back_populates='user')

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    ingredients = db.Column(db.Text, nullable=False)
    instructions = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    image_filename = db.Column(db.String(100), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', back_populates='recipes')

class RecipeForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    ingredients = TextAreaField('Ingredients', validators=[DataRequired()])
    instructions = TextAreaField('Instructions', validators=[DataRequired()])
    image = FileField('Image')
    submit = SubmitField('Submit')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=150)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=150)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    recipes = Recipe.query.all()
    return render_template('index_template.html', recipes=recipes)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password', 'danger')
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='pbkdf2:sha256')
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/add', methods=['GET', 'POST'])
@login_required
def add_recipe():
    form = RecipeForm()
    if form.validate_on_submit():
        image_filename = None
        if form.image.data and allowed_file(form.image.data.filename):
            image = form.image.data
            image_filename = image.filename
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], image_filename))
        recipe = Recipe(
            name=form.name.data,
            ingredients=form.ingredients.data,
            instructions=form.instructions.data,
            image_filename=image_filename,
            user_id=current_user.id
        )
        db.session.add(recipe)
        db.session.commit()
        flash('Recipe added!', 'success')
        return redirect(url_for('index'))
    return render_template('add_recipe_template.html', form=form)

@app.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update_recipe(id):
    recipe = Recipe.query.get_or_404(id)
    if recipe.user_id != current_user.id:
        flash('You do not have permission to update this recipe.', 'danger')
        return redirect(url_for('index'))

    form = RecipeForm()
    if form.validate_on_submit():
        recipe.name = form.name.data
        recipe.ingredients = form.ingredients.data
        recipe.instructions = form.instructions.data
        if form.image.data and allowed_file(form.image.data.filename):
            image = form.image.data
            recipe.image_filename = image.filename
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], image.filename))
        db.session.commit()
        flash('Recipe updated!', 'success')
        return redirect(url_for('index'))
    elif request.method == 'GET':
        form.name.data = recipe.name
        form.ingredients.data = recipe.ingredients
        form.instructions.data = recipe.instructions
    return render_template('update_recipe_template.html', form=form, recipe=recipe)

@app.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete_recipe(id):
    recipe = Recipe.query.get_or_404(id)
    if recipe.user_id != current_user.id:
        flash('You do not have permission to delete this recipe.', 'danger')
        return redirect(url_for('index'))
    
    db.session.delete(recipe)
    db.session.commit()
    flash('Recipe deleted!', 'success')
    return redirect(url_for('index'))

@app.route('/recipe/<int:id>')
def view_recipe(id):
    recipe = Recipe.query.get_or_404(id)
    return render_template('view_recipe.html', recipe=recipe)

if __name__ == '__main__':
    app.run(debug=True)
    