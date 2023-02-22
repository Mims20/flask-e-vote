from flask import Blueprint, render_template, url_for, redirect, request, json, flash

from flask_pydantic import validate
from app.forms.forms import RegisterForm

from app import schemas, models, db, utils

user = Blueprint("user", __name__)


@user.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        # print(form.data)
        form_data = schemas.Register(**form.data)
        form_data.password = utils.hash_password(plain_password=form_data.password)
        new_user = models.User(**form_data.dict())

        db.session.add(new_user)
        db.session.commit()

        flash(message="Registration Successful. Please Login.",
              category="success")

        return redirect(url_for("auth.login"))
    return render_template("register.html", form=form)
