from flask import Blueprint, render_template, url_for, redirect, request, flash
from flask_login import login_required, current_user

from app import db
from app.forms.forms import PresidentVoteForm, ViceVoteForm, SecretaryVoteForm
from app.models import Candidate, Vote

vote = Blueprint("vote", __name__)


def get_presidential_choices():
    return [(candidate.first_name + " " + candidate.last_name, candidate.image) for candidate in
            Candidate.query.filter_by(position="President").all()]

    # update choices list with a default that's not a candidate
    # presidential_form.president.choices.insert(0, "Click and make selection")


def get_vice_choices():
    return [(candidate.first_name + " " + candidate.last_name, candidate.image) for candidate in
            Candidate.query.filter_by(position="Vice President").all()]


def get_secretarial_choices():
    return [(candidate.first_name + " " + candidate.last_name, candidate.image) for candidate in
            Candidate.query.filter_by(position="Secretary").all()]


@vote.route("/vote", methods=["GET", "POST"])
@login_required
def cast_vote():
    presidential_form = PresidentVoteForm()
    vice_presidential_form = ViceVoteForm()
    secretarial_form = SecretaryVoteForm()

    # query candidate db and update form choices with candidates
    presidential_form.president.choices = get_presidential_choices()
    vice_presidential_form.vice.choices = get_vice_choices()
    secretarial_form.secretary.choices = get_secretarial_choices()

    if request.form.get("submit_president") and presidential_form.validate_on_submit():
        # if presidential_form.president.data != "Click and make selection":
        candidate_name = request.form.get("president")
        print(candidate_name)
        candidate_voted_for = Candidate.query.filter(Candidate.first_name == candidate_name.split(" ")[0],
                                                     Candidate.last_name == candidate_name.split(" ")[1]).first()
        print(candidate_voted_for.id)
        candidate_voted_for.votes += 1
        db.session.commit()

        pres_vote = presidential_form.president.data
        user_id = current_user.id
        new_vote = Vote(president=pres_vote, user_id=user_id)

        db.session.add(new_vote)
        db.session.commit()

        flash("thanks for voting for a president", category="success")

        return redirect(url_for("vote.cast_vote"))

    elif request.form.get("submit_vice") and vice_presidential_form.validate_on_submit():
        vice_vote = vice_presidential_form.vice.data
        user_id = current_user.id
        new_vote = Vote(vice_president=vice_vote, user_id=user_id)

        db.session.add(new_vote)
        db.session.commit()

        flash("thanks for voting for a vice president", category="success")

    elif secretarial_form.validate_on_submit() and request.form.get("submit_secretary"):
        # flash("secretary", category="info")
        secretary_vote = secretarial_form.secretary.data
        user_id = current_user.id
        new_vote = Vote(secretary=secretary_vote, user_id=user_id)

        db.session.add(new_vote)
        db.session.commit()

        flash("thanks for voting for a secretary", category="success")

    return render_template("vote.html",
                           president_form=presidential_form,
                           vice_form=vice_presidential_form,
                           secretary_form=secretarial_form)
#
# @app.route('/results')
# def results():
#     president_candidates = Candidate.query.filter_by(category='President').all()
#     secretary_candidates = Candidate.query.filter_by(category='Secretary').all()
#     return render_template('results.html', president_candidates=president_candidates,
#                            secretary_candidates=secretary_candidates)
