from datetime import datetime
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, FileField, IntegerField
from wtforms.validators import InputRequired, Length, ValidationError
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_required, login_user, current_user, logout_user

app = Flask(__name__)

app.config['SECRET_KEY'] = 'thisisforever'
app.config['SQLALCHEMY_DATABASE_URI'] = ''
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
login_manager = LoginManager(app)
login_manager.login_view = 'Login'
db = SQLAlchemy(app)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(200))
    username = db.Column(db.String(200), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(100))
    profile_pic = db.Column(db.String(200))
    returns = db.relationship('Return', backref='user', lazy='dynamic')
    def __repr__(self):
        return '<User %r>' % self.fullname, self.email, self.profile_pic, self.returns

class Return(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    ra = db.Column(db.Integer)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    color = db.Column(db.String(200))
    style = db.Column(db.String(200))
    size = db.Column(db.String(200))
    reason = db.Column(db.String(200))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


def __init__(self, name, ra,date, color, style, size, reason):
    self.name = name
    self.ra = ra
    self.date = date
    self.color = color
    self.style = style
    self.size = size
    self.reason = reason

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class RegisterForm(FlaskForm):
    fullname = StringField('fullname', validators=[InputRequired('Please fill in your Fullname')])
    username = StringField('username', validators=[InputRequired('Please fill in your Fullname')])
    email = StringField('email', validators=[InputRequired('Please fill in a valid email')])
    password = PasswordField('Password', validators=[InputRequired('Please create a password'), Length(min=8, message='Your Password must have 8 characters or more')])
    def validate_username(self,username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('username is already taken')
    def validate_emai(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError('You already have an account')



class LoginForm(FlaskForm):
    username = StringField('Username')
    password = PasswordField('Password')
    remember = BooleanField('Remember me')

class ReturnForm(FlaskForm):
    name = StringField('name', validators=[InputRequired('Please fill in the Fullname of the customer')])
    ra = IntegerField('ra', validators=[InputRequired('Please fill in RA number')])
    date = StringField('date', validators=[InputRequired('Please fill the date')])
    color = StringField('color', validators=[InputRequired('Please fill the color')])
    style = StringField('style', validators=[InputRequired('Please fill the style')])
    size = StringField('size', validators=[InputRequired('Please fill the size')])
    reason = BooleanField('reason')



admin = Admin(app, template_mode='bootstrap3')
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Return, db.session))

@app.route('/')
def home():
    return redirect(url_for('Login'))

@app.route('/Register', methods=['GET', 'POST'])
def Register():
    form = RegisterForm()
    if form.validate_on_submit():
        new_user = User(fullname=form.fullname.data, username=form.username.data, email=form.email.data,password=generate_password_hash(form.password.data))
        db.session.add(new_user)
        db.session.commit()
        
        return redirect(url_for('profile'))


    return render_template('Register.html', form=form)



@app.route('/login', methods=['GET', 'POST'])
def Login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('profile'))
        else:
            flash('Login unsuccessful, check to make sure all info are correct')
    return render_template('login.html', form=form)

@app.route('/<username>')
@login_required
def profile(username):
    
    if username:
        user= User.query.filter_by(username=username).first()
        if not:
            abort(404)
    else:
        user = current_user
    returns = Return.query.filter_by(user=user).order_by(Return.date.desc()).paginate(page=page, per_page=10).first()
    return render_template('profile.html', current_user=current_user, returns=returns)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('Login'))

app.route("/return/<int:return_id>", methods=['GET', 'POST'])
@login_required
def Return(return_id):
    Return = Return.query.filter_by(u)
    
    return redirect(url_for('Login'))


if __name__ == '__main__':
    app.run(debug=True)