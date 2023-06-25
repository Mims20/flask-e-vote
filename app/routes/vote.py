from flask import Blueprint, render_template, url_for, redirect, request, flash
from flask_login import login_required, current_user

from app import db
from app.forms.forms import PresidentVoteForm, ViceVoteForm, SecretaryVoteForm
from app.models import Candidate, Vote

vote = Blueprint("vote", __name__)


def get_presidential_choices():
    return [candidate for candidate in
            Candidate.query.filter_by(position="President").all()]

    # update choices list with a default that's not a candidate
    # presidential_form.president.choices.insert(0, "Click and make selection")


def get_vice_choices():
    return [candidate for candidate in
            Candidate.query.filter_by(position="Vice President").all()]


def get_secretarial_choices():
    return [candidate for candidate in
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

    if request.method == "POST":
        president_vote = request.form.get("president")
        secretary_vote = request.form.get("secretary")

        if president_vote:
            already_voted = Vote.query.filter_by(user_id=current_user.id).first()
            if already_voted and already_voted.president_id:
                flash(message="You've already voted for a president", category="warning")
            else:
                president_voted = Candidate.query.filter_by(id=president_vote).first()

                president_voted.votes += 1

                if already_voted:
                    already_voted.president_id = president_vote
                    db.session.commit()

                else:
                    user_vote_info = Vote(president_id=president_voted.id,
                                          user_id=current_user.id)
                    db.session.add(user_vote_info)

                db.session.commit()

                flash(message="Thanks for voting", category="success")

        elif secretary_vote:
            already_voted = Vote.query.filter_by(user_id=current_user.id).first()

            if already_voted and already_voted.secretary_id:
                flash(message="You've already voted for a secretary", category="warning")

            else:
                secretary_voted = Candidate.query.filter_by(id=secretary_vote).first()

                secretary_voted.votes += 1

                if already_voted:
                    already_voted.secretary_id = secretary_vote
                    db.session.commit()
                else:
                    user_vote_info = Vote(secretary_id=secretary_voted.id,
                                          user_id=current_user.id)

                    db.session.add(user_vote_info)
                db.session.commit()
                # print(user_vote_info.secretary_id)

                flash(message="Thanks for voting", category="success")

    return render_template("vote.html",
                           president_form=presidential_form,
                           vice_form=vice_presidential_form,
                           secretary_form=secretarial_form)
