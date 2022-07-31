from flask import Blueprint,render_template,request,flash,redirect,url_for
from werkzeug.security import generate_password_hash,check_password_hash
from .models import User
from . import db
from flask_login import login_user,login_required,logout_user,current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        check_user = User.query.filter_by(email=email).first()
        
        if check_user:
            if check_password_hash(check_user.password, password):
                login_user(check_user, remember=True)
                flash("Log in Successfully", category="success")
                return redirect(url_for('views.index'))
            else:
                flash("Incorrect Email or Password!", category="error")
        else:
            flash("Email does not Exist", category="error")
        
    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET','POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        full_name = request.form.get('fullName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        
        check_user1 = User.query.filter_by(email=email).first()
        
        if check_user1:
            flash("User Already Registered, pls login!", category="error")
        elif password1 != password2:
            flash("Password does not match!",category="error")
        elif len(password1) < 8:
            flash("Password must be at least 8 Characters.",category="error")            
        else:  
            new_user = User(email=email,fullname=full_name,password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            
            check_user2 = User.query.filter_by(email=email).first()
            login_user(check_user2, remember=True)
            
            flash("Account Created, You are logged In!",category="success")
            return redirect(url_for('views.index'))
            # return redirect(url_for("auth.login"))
        
    return render_template("sign_up.html", user=current_user)