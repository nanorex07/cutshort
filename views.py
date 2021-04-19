from flask import Blueprint, render_template, request, flash, redirect, url_for, session, jsonify
import json
from . import db, login_required, random_str, BASE_URL

views = Blueprint('views', __name__)

@views.route('/', methods=["GET"])
def home():
    return render_template("home.html")

@views.route('/dashboard', methods=["GET", "POST"])
@login_required
def dashboard():
    code = None
    if request.method=="POST":
        url = request.form.get("url")
        if not url:
            flash("Please enter the url", category='error')
        else:
            x = db.get_exisiting_url(url)
            if len(x) > 0:
                code = x[0][2]
            else:
                loops = 0
                currchar=4
                code = random_str(currchar)
                while db.code_exists(code):
                    if loops > 1000:
                        currchar+=1
                        loops = 0
                    code = random_str(currchar)
                    loops += 1
                db.add_url(url, code, session.get("user_id"))

    u = db.get_user_byid(session.get("user_id"))
    print(db.get_urls(u[0]))
    return render_template("dashboard.html", user=u, all_urls=db.get_urls(u[0]), base_url = BASE_URL, curr_code=code)
    
@views.route('/url/<string:code>')
def url(code):
    url = db.find_url(code)
    if url:
        db.inc_clicks(url[0][0])
        return redirect(url[0][1])
    return "404"

@views.route('/delete-url', methods=["POST"])
def delete_url():
    if request.method == "POST":
        db.delete_url(dict(json.loads(request.data))["code"])
        return redirect(url_for('views.dashboard'))
    return "404"
