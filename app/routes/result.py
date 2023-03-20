from flask import Blueprint, render_template

from app.models import Candidate

result = Blueprint("result", __name__)


@result.route("/results")
def results():
    presidential_results = [(candidate.first_name + " " + candidate.last_name, candidate.votes)
                            for candidate in Candidate.query.filter_by(position="President")]

    secretarial_results = [(candidate.first_name + " " + candidate.last_name, candidate.votes)
                           for candidate in Candidate.query.filter_by(position="Secretary")]

    return render_template("results.html", presidential_results=presidential_results, secretarial_results=secretarial_results)