def test_list_renter(client):
    """Return an empty list when no renters have been made
    """
    response = client.get("/renters")
    assert response.status_code == 200
    assert response.get_json() == []
    
    """Show all renters
    """
    
def test_create_renter(client):
    """Create a renter successfully
    """
    renter_1 = {
        "name": "James Parker",
        "email": "j.parker@gmail.com",
    }
    create_resp = client.post("/renters", json=renter_1)
    assert create_resp.status_code == 201

def test_protect_when_creating_renter(client):
    """Don't create renters with bad values, ex. no values, or weird values ex. jparker.com for the email
    """
    renter_1 = {
        "name": "James Parker",
        "email": "",
    }
    create_resp = client.post("/renters", json=renter_1)
    assert create_resp.status_code != 201
    renter_1 = {
        "name": "",
        "email": "",
    }
    create_resp = client.post("/renters", json=renter_1)
    assert create_resp.status_code != 201
    renter_1 = {
        "name": "",
        "email": "j.parker@gmail.com",
    }
    create_resp = client.post("/renters", json=renter_1)
    assert create_resp.status_code != 201
    renter_1 = {
        "name": "#$^***^%$#()_+~||",
        "email": "j.parker@gmail.com",
    }
    create_resp = client.post("/renters", json=renter_1)
    assert create_resp.status_code != 201
    renter_1 = {
        "name": "James Parker",
        "email": "jparker",
    }
    create_resp = client.post("/renters", json=renter_1)
    assert create_resp.status_code != 201
    renter_1 = {
        "name": "James Parker",
        "email": "jparker@",
    }
    create_resp = client.post("/renters", json=renter_1)
    assert create_resp.status_code != 201
        renter_1 = {
        "name": "James Parker",
        "email": "jparker@gmail.",
    }
    create_resp = client.post("/renters", json=renter_1)
    assert create_resp.status_code != 201
    renter_1 = {
        "name": "James Parker",
        "email": "jparker@@",
    }
    create_resp = client.post("/renters", json=renter_1)
    assert create_resp.status_code != 201
        renter_1 = {
        "name": "James Parker",
        "email": "jparker@.",
    }
    create_resp = client.post("/renters", json=renter_1)
    assert create_resp.status_code != 201
    renter_1 = {
        "name": "James Parker",
        "email": "jparker.com",
    }
    create_resp = client.post("/renters", json=renter_1)
    assert create_resp.status_code != 201
    renter_1 = {
        "name": "James Parker",
        "email": "jparker@@.com",
    }
    create_resp = client.post("/renters", json=renter_1)
    assert create_resp.status_code != 201
    
def test_create_dup_renter(client):
    """Create a duplicate renter, the second test should not return 201,
    because it's a duplicate renter. Having duplicate renters would be a
    problem so there should be measures put in place to prevent this.
    """
    renter_1 = {
        "name": "Julian Andrews",
        "email": "j.andrews@gmail.com",
    }
    create_resp = client.post("/renters", json=renter_1)
    assert create_resp.status_code == 201
    
    create_resp2 = client.post("/renters", json=renter_1)
    assert create_resp2.status_code != 201
    
  """delete a renter
  """

  """delete an already deleted renter
  """

def test_list_rentals(client):
    """Return an empty list when no rentals have been made
    """
    response = client.get("/rentals")
    assert response.status_code == 200
    assert response.get_json() == []

  """return rental
  """
  """Check returning already returned rental
  """
  """Make nonexistent rental as returned
  """
