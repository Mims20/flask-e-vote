# Test the "/" route
def test_home_route(app, client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"E-Vote" in response.data


# Test the "/register" route
def test_register_route(app, client):
    response = client.get("/register")
    assert response.status_code == 200
    assert b"Register" in response.data


# Test the "/login" route
def test_login_route(app, client):
    response = client.get("/login")
    assert response.status_code == 200
    assert b"Login" in response.data


# Test the "/candidate" route
def test_all_candidate_route(app, client):
    response = client.get("/candidate/all")
    assert response.status_code == 200
    assert b"All Candidates" in response.data


def test_candidate_route(app, client):
    response = client.get("/candidate")
    assert response.status_code == 401
    assert b"Unauthorized Access" in response.data


# Test the "/update" route
# def test_update_route(app, client):
#     response = client.get("/update/1")
#     assert response.status_code == 401
#     assert b"Unauthorized Access" in response.data


# Test the "/vote" route
def test_vote_route(app, client):
    response = client.get("/vote")
    assert response.status_code == 401
    assert b"Unauthorized Access" in response.data


# Test the "/results" route
def test_results_route(app, client):
    response = client.get("/results")
    assert response.status_code == 200
    assert b"Results" in response.data
