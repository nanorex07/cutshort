from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from . import db, login_required

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        if (not email or not password):
            flash("fill out all fields..", category='error')
        else:
            user = db.get_user(email)
            if len(user) > 0:
                if db.check_password(user, password):
                    session["user_id"] = user[0][0]
                    flash("successfully logged in !", category='success')
                    return redirect(url_for('views.dashboard'))
                else:
                    flash("incorrect password, try again", category='error')    
            else:
                flash("not such user exists...", category='error')
    return render_template("login.html")

@auth.route('/register', methods=["GET", "POST"])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        fullname = request.form.get('fullname')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        if not email or not fullname or not password1 or not password2:
            flash("please fill out all fields...", category='error')
        elif len(fullname) > 30:
            flash("please use shorter fullname (< 30)", category='error')
        elif password1 != password2:
            flash("passwords dont match", category='error') 
        else:
            try:
                db.add_user(fullname, email, password1)
                flash("account created", category='success')
                return redirect(url_for('views.home'))
            except:
                flash("server error", category='error')
            
                
    return render_template("register.html")

@auth.route("/logout")
@login_required
def logout():
    session.clear()
    return redirect(url_for("views.home"))