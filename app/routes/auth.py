from flask import Blueprint, render_template, url_for, redirect, request, flash

from app.forms.forms import LoginForm
from app import utils, models

from flask_login import login_user, logout_user, current_user


auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))

    form = LoginForm()

    if request.method == "POST":
        if form.validate_on_submit():
            user = models.User.query.filter_by(email=form.email.data).first()

            if not user:
                flash("That email is not registered, please register", "info")
                return redirect(url_for("auth.login"))

            elif not utils.verify_password(hashed_password=user.password,
                                           plain_password=form.password.data):
                flash('Password incorrect, please try again.', "danger")
                return redirect(url_for('auth.login'))

            else:
                login_user(user)
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('main.home'))

    return render_template("signin.html", form=form, current_user=current_user)


@auth.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main.home"))