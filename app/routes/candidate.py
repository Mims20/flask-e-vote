import os
import secrets

from PIL import Image

from flask import Blueprint, render_template, url_for, redirect, request, flash, current_app
from flask_login import login_required

from app.forms.forms import CandidateForm

from app import schemas, db
from app.models import Candidate

candidate = Blueprint("candidate", __name__)


def save_picture(profile_picture):
    random_hex = secrets.token_hex(8)
    _, file_ext = os.path.splitext(profile_picture.filename)
    picture_name = random_hex + file_ext
    picture_path = os.path.join(current_app.root_path, "static/candidate_pics", picture_name)

    output_size = (100, 100)
    image = Image.open(profile_picture)
    image.thumbnail(output_size)
    image.save(picture_path)

    return picture_name


@candidate.route("/candidate", methods=["GET", "POST"])
@login_required
def add_candidate():
    form = CandidateForm()
    if form.validate_on_submit():
        form_data = schemas.Candidate(**form.data)
        new_candidate = Candidate(**form_data.dict())
        new_candidate.image = save_picture(form.profile_picture.data)
        # print(new_candidate.first_name, new_candidate.last_name, new_candidate.image)
        db.session.add(new_candidate)
        db.session.commit()

        flash(message="Candidate added successfully",
              category="success")

        return redirect(url_for("candidate.add_candidate"))

    return render_template("candidate.html", form=form)


@candidate.route("/candidate/all", methods=["GET", "POST"])
def all_candidates():
    candidate_data = Candidate.query.all()

    return render_template("all_candidates.html", candidates=candidate_data)


# update candidate info
@candidate.route("/update/<int:candidate_id>", methods=["GET", "POST"])
@login_required
def update_candidate(candidate_id):
    form = CandidateForm()
    candidate_to_update = Candidate.query.filter_by(id=candidate_id).first()
    if request.method == "GET":
        if candidate_to_update:
            return render_template("update.html", form=form, candidate=candidate_to_update)

    elif request.method == "POST":
        form_data = schemas.UpdateForm(**form.data)

        candidate_to_update.first_name = form_data.first_name
        candidate_to_update.last_name = form_data.last_name
        candidate_to_update.position = form_data.position

        db.session.commit()

        flash(message="Candidate info successfully updated",
              category="success")
        # print(candidate_to_update.id)

        return redirect(url_for("candidate.all_candidates"))


# delete candidate
@candidate.route("/delete")
@login_required
def delete_candidate():
    candidate_id = request.args.get("candidate_id")
    candidate_to_delete = Candidate.query.get(candidate_id)

    db.session.delete(candidate_to_delete)
    db.session.commit()

    return redirect(url_for("candidate.all_candidates"))
