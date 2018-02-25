from datetime import datetime

from flask import Flask, g, render_template, flash, redirect, url_for, abort
from flask_bcrypt import check_password_hash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

import forms
import models

DEBUG = True
PORT = 8000
HOST = '0.0.0.0'

notebox = Flask(__name__)
notebox.secret_key = "G^86fi>78rfv%DCFTVdughsd78t3456@><FOIn"

login_manager = LoginManager()
login_manager.init_app(notebox)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
	try:
		return models.User.get(models.User.id == user_id)
	except models.DoesNotExist:
		return None

@notebox.before_request
def before_request():
	g.db = models.DATABASE
	g.db.connect()
	g.user = current_user

@notebox.after_request
def after_request(response):
	g.db.close()
	return response

@notebox.route("/")
def index():
	return redirect(url_for("login"))

@notebox.route("/login", methods=("GET", "POST"))
def login():
	form = forms.LoginForm()
	if current_user.is_authenticated:
		return redirect(url_for("home"))
	if form.validate_on_submit():
		try:
			user = models.User.get(models.User.username == form.username.data)
			if check_password_hash(user.password, form.password.data):
				login_user(user)
				return redirect(url_for("home"))
			else:
				flash("Your username or password is wrong", "error")	
		except models.DoesNotExist:
			flash("Your username or password is wrong", "error")
	else:
		pass
	return	render_template("login.html", form=form)

@notebox.route("/logout")
@login_required
def logout():
	logout_user()
	return redirect(url_for("index"))

@notebox.route("/home", methods=("GET", "POST"))
def home():
	list = current_user.get_notes()
	form = forms.NoteForm()
	if form.validate_on_submit():
		models.Note.create(user=g.user.id, text=form.text.data, timestamp=datetime.now())
		return redirect(url_for("home"))
	return render_template("home.html", form=form, list=list)	

@notebox.route("/delete/<int:note_id>")
def delete_note(note_id):
	to_delete = models.Note.select().where(models.Note.id == note_id).first()
	to_delete.delete_instance()
	return redirect(url_for("home"))

@notebox.route("/view/<int:note_id>")
def view_note(note_id):
	view = models.Note.select().where(models.Note.id == note_id).first()
	return render_template("view.html", view=view)

@notebox.route("/postscript/<int:note_id>", methods=("GET", "POST"))
def add_postscript(note_id):
	view = models.Note.select().where(models.Note.id == note_id).first()
	form = forms.PostscriptForm()
	if form.validate_on_submit():
		postscript = form.postscript.data
		new_text = view.text + " " + postscript
		query = models.Note.update(text=new_text).where(models.Note.id == note_id)
		query.execute()
		return redirect(url_for("home"))
	return render_template("postscript.html", form=form, view=view)

if __name__ == "__main__":
	models.initialise()
	try:
		models.User.create_user(
			username="ashley",
			password="password",
		)
	except ValueError:
		pass
	notebox.run(debug=DEBUG, host=HOST, port=PORT)