from flask import Blueprint , render_template ,request, flash , redirect , url_for
from .models import User
from werkzeug.security import generate_password_hash , check_password_hash
from website import db
from flask_login import login_user , login_required , logout_user , current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email=request.form.get('email')
        Password=request.form.get('password')
        print(Password)
        user = User.query.filter_by(email=email).first()
        print(user.password)
        print(check_password_hash(user.password, Password))
        if user:
            if check_password_hash(user.password, Password):
                flash('Logged successfully!', category='sucess')
                login_user(user,remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('password is invalid',category='error')
        else:
            flash('No account related to this user',category='error')
    return render_template('login.html' , user=current_user)

@auth.route('/signup', methods=['GET','POST'])
def sign_up():
    if (request.method == 'POST'):
        FullName=request.form.get('Full_name')
        Email=request.form.get('email')
        Password=request.form.get('password')
        Password1=request.form.get('password1')
        user = User.query.filter_by(email=Email).first()
        if user:
            flash('email is already exist',category='error')
        elif len(Email)<4 :
            flash('email is too short' , category='error')
        elif len(FullName)<6 :
            flash('FullName is shorter than 6' , category='error')
        elif Password != Password1:
            flash('Password doesn\'t much' , category='error')
        else:
            new_user = User(email=Email , full_name=FullName , password = generate_password_hash(Password , method='sha256') )
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user,remember=True)
            flash('account created!' , category='success')
            return redirect(url_for('views.home'))


    return render_template("signup.html", user=current_user)

@auth.route('/Logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))