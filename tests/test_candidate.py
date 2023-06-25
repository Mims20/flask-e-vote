import os
from random import random

from flask import url_for
from flask_login import current_user
from werkzeug.datastructures import FileStorage

from app import schemas
from app.forms.forms import CandidateForm
from app.models import Candidate, User

# Assuming the mock image is located in the same 'tests' folder
MOCK_IMAGE_PATH = os.path.join(os.path.dirname(__file__), 'mock_image.jpg')


def test_get_all_candidates(client, add_candidate1, add_candidate2):
    response = client.get("/candidate/all")
    assert response.status_code == 200
    assert Candidate.query.count() == 2


def test_add_candidate(client, app, login_dummy_user):
    # assert current_user.id == 1
    # Create a mock image file
    image_file = FileStorage(
        stream=open(MOCK_IMAGE_PATH, 'rb'),
        filename='mock_image.jpg',
        content_type='image/jpeg'
    )

    candidate = {
        "first_name": "Selase",
        "last_name": "Zuttah",
        "position": "President",
        "image": image_file
    }

    response = client.post("/candidate",
                           data=candidate,
                           follow_redirects=True)
    # print(response.data)
    assert response.status_code == 200

    # with app.app_context():
    #     candidate = Candidate.query.filter_by(first_name=candidate["first_name"],
    #                                           last_name=candidate["last_name"]).first()
    #
    # assert candidate is not None
    # assert candidate.position == candidate["position"]

# def test_update_candidate(client, add_candidate1, add_candidate2):
#     candidate_id = random.randint(1, 2)
#     for
#     client.put(f"/update/{candidate_id}", )
