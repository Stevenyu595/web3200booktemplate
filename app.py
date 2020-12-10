from flask import Flask, render_template, abort, request, redirect, url_for, g, flash
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, LoginManager, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}/{}'.format(app.root_path, 'class_type.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'b2de7FkqvkMyqzNFzxCkgnPKIGP6i4Rc'

db = SQLAlchemy(app)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    subtitle = db.Column(db.Text, nullable=False)

class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

class Class_type(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    category = db.relationship('Category', backref=db.backref('Class_type', lazy=True))
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'), nullable=False)
    teacher = db.relationship('Teacher', backref=db.backref('Class_type', lazy=True))
    description = db.Column(db.Text, nullable=False)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))

db.create_all()

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/")
def index():
    categories = Category.query.all()
    return render_template("index.html", categories=categories)

@app.route("/category/<name>")
def category(name):
    category = Category.query.filter(Category.name == name).first()
    class_types = Class_type.query.join(Category).filter(Category.name == name)
    return render_template("category.html", category=category, class_types=class_types)

@app.route("/browse")
def browse():
    categories = Category.query.all()
    return render_template("browse.html", categories=categories)

@app.route("/pageone")
def pageone():
    categories = Category.query.all()
    return render_template("pageone.html", categories=categories)

@app.route("/pagetwo")
def pagetwo():
    categories = Category.query.all()
    return render_template("pagetwo.html", categories=categories)

@app.route("/pagethree")
def pagethree():
    categories = Category.query.all()
    return render_template("pagethree.html", categories=categories)

@app.route("/pagefour")
def pagefour():
    categories = Category.query.all()
    return render_template("pagefour.html", categories=categories)

@app.route("/pagefive")
def pagefive():
    categories = Category.query.all()
    return render_template("pagefive.html", categories=categories)
@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        flash('Please check your login credentials and try again.')
        return redirect(url_for('login'))

    login_user(user, remember=remember)

    return redirect(url_for('admin_categories'))

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first()

    if user:
        return redirect(url_for('signup'))

    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route("/class_type/<int:id>")
def class_type(id):
    class_type = Class_type.query.get_or_404(id)
    return render_template("class_type.html", class_type=class_type)

@app.route('/admin')
@app.route('/admin/categories')
@login_required
def admin_categories():
    categories = Category.query.all()
    return render_template('admin/category.html', categories=categories)

@app.route('/admin/category/new', methods=('GET', 'POST'))
@login_required
def create_category():
    if request.method == 'POST':
        name = request.form['name']
        title = request.form['title']
        subtitle = request.form['subtitle']

        error = None

        if not name:
            error = 'Name is required.'

        if error is None:
            category = Category(name=name, title=title, subtitle=subtitle)
            db.session.add(category)
            db.session.commit()
            return redirect(url_for('admin_categories'))
        flash(error)

    categories = Category.query.all()
    return render_template('admin/category_form.html', categories=categories)

@app.route('/admin/category/edit/<id>', methods=('GET', 'POST'))
@login_required
def edit_category(id):
    category = Category.query.get_or_404(id)

    if request.method == 'POST':
        category.name = request.form['name']
        category.title = request.form['title']
        category.subtitle = request.form['subtitle']

        error = None

        if not request.form['name']:
            error = 'Name is required.'

        if error is None:
            db.session.commit()
            return redirect(url_for('admin_categories'))
        flash(error)

    return  render_template('admin/category_form.html', name=category.name, title=category.title, subtitle=category.subtitle)

@app.route('/admin/category/delete/<id>')
@login_required
def delete_category(id):
    category_to_delete = Category.query.get_or_404(id)

    try:
        db.session.delete(category_to_delete)
        db.session.commit()
        return redirect(url_for('admin_categories'))
    except:
        return "There was a problem deleting category"

@app.route('/admin/class_types')
@login_required
def admin_class_types():
    class_types = Class_type.query.all()
    return render_template('admin/class_type.html', class_types=class_types)

@app.route('/admin/class_type/new', methods=('GET', 'POST'))
@login_required
def create_class_type():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        teacher_id = request.form['teacher']
        category_id = request.form['category']
        teacher = Teacher.query.get_or_404(teacher_id)
        category = Category.query.get_or_404(category_id)

        error = None

        if not title:
            error = 'Title is required.'

        if error is None:
            class_type = Class_type(category_id=category_id, category=category, title=title, teacher_id=teacher_id, teacher=teacher, description=description)
            db.session.add(class_type)
            db.session.commit()
            return redirect(url_for('admin_class_types'))
        flash(error)

    class_types = Class_type.query.all()
    teachers = Teacher.query.all()
    categories = Category.query.all()
    return render_template('admin/class_form.html', class_types=class_types, categories=categories, teachers=teachers)

@app.route('/admin/class_type/edit/<id>', methods=('GET', 'POST'))
@login_required
def edit_class_type(id):
    class_type = Class_type.query.get_or_404(id)

    if request.method == 'POST':
        class_type.title = request.form['title']
        class_type.description = request.form['description']
        class_type.teacher_id = request.form['teacher']
        class_type.category_id = request.form['category']
        class_type.teacher = Teacher.query.get_or_404(class_type.teacher_id)
        class_type.category = Category.query.get_or_404(class_type.category_id)

        error = None

        if not class_type.title:
            error = 'Title is required.'

        if error is None:
            db.session.commit()
            return redirect(url_for('admin_class_types'))
        flash(error)

    class_types = Class_type.query.all()
    teachers = Teacher.query.all()
    categories = Category.query.all()
    return render_template('admin/class_type_form.html', class_types=class_types, categories=categories, teachers=teachers, title=class_type.title, description=class_type.description, teacher=class_type.teacher, category=class_type.category)

@app.route('/admin/class_type/delete/<id>')
@login_required
def delete_class_type(id):
    class_type_to_delete = Class_type.query.get_or_404(id)

    try:
        db.session.delete(class_type_to_delete)
        db.session.commit()
        return redirect(url_for('admin_class_types'))
    except:
        return "There was a problem deleting class_type"

@app.route('/admin/teachers')
@login_required
def admin_teachers():
    teachers = Teacher.query.all()
    return render_template('admin/teacher.html', teachers=teachers)

@app.route('/admin/teacher/new', methods=('GET', 'POST'))
@login_required
def create_teacher():
    if request.method == 'POST':
        name = request.form['name']

        error = None

        if not name:
            error = 'Name is required.'

        if error is None:
            teacher = Teacher(name=name)
            db.session.add(teacher)
            db.session.commit()
            return redirect(url_for('admin_teachers'))
        flash(error)

    teachers = Teacher.query.all()
    return render_template('admin/teacher_form.html', teachers=teachers)

@app.route('/admin/teacher/edit/<id>', methods=('GET', 'POST'))
@login_required
def edit_teacher(id):
    teacher = Teacher.query.get_or_404(id)

    if request.method == 'POST':
        teacher.name = request.form['name']

        error = None

        if not request.form['name']:
            error = 'Name is required.'

        if error is None:
            db.session.commit()
            return redirect(url_for('admin_teachers'))
        flash(error)

    return  render_template('admin/teacher_form.html', name=teacher.name)

@app.route('/admin/teacher/delete/<id>')
@login_required
def delete_teacher(id):
    teacher_to_delete = Teacher.query.get_or_404(id)

    try:
        db.session.delete(teacher_to_delete)
        db.session.commit()
        return redirect(url_for('admin_teachers'))
    except:
        return "There was a problem deleting teacher"

