def test_list_renter(client):
    """Return an empty list when no renters have been made
    """
    response = client.get("/renters")
    assert response.status_code == 200
    assert response.get_json() == []
    

    def test_show_all_renter(client):
    """Show all renters
    """
    renter_1 = {
        "name": "James Parker",
        "email": "j.parker@gmail.com",
    }
    create_resp = client.post("/renters", json=renter_1)
    assert create_resp.status_code == 201
    
    response = client.get("/renters")
    assert response.status_code == 200

        renter_2 = {
        "name": "James Parker",
        "email": "j.2parker@gmail.com",
    }
    create_resp = client.post("/renters", json=renter_2)
    assert create_resp.status_code == 201
    renter_3 = {
        "name": "James Parker",
        "email": "j.3parker@gmail.com",
    }
    create_resp = client.post("/renters", json=renter_3)
    assert create_resp.status_code == 201
    renter_4 = {
        "name": "James Parker",
        "email": "j.4parker@gmail.com",
    }
    create_resp = client.post("/renters", json=renter_1)
    assert create_resp.status_code == 201

    response = client.get("/renters")
    assert response.status_code == 200
    
    def test_get_renter(client):
    """Get one renter
    """
    renter_1 = {
        "name": "James Parker",
        "email": "j.parker@gmail.com",
    }
    create_resp = client.post("/renters", json=renter_1)
    renter_id = create_resp.get_json()["id"]
    response = client.get("/renters", "renter_id":renter_id)
    assert response.status_code == 200
    def test_get_nonex_renter(client):
        
    """Get one nonexistent renter
    """
    "renter_id"=1
    response = client.get("/renters", "renter_id":renter_id)
    assert response.status_code != 200
    
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

def test_delete_renter(client):
    """delete a renter
    """
    renter_1 = {
        "name": "Julian Andrews",
        "email": "j.andrews@gmail.com",
    }
    create_resp = client.post("/renters", json=renter_1)
    assert create_resp.status_code == 201

    renter_id = create_resp.get_json()["id"]

    del_resp = client.delete("/renters", "renter_id":renter_id)
    assert del_resp.status_code == 204

def test_doub_delete_renter(client):
    """delete an already deleted renter
    """
    renter_1 = {
        "name": "Julian Andrews",
        "email": "j.andrews@gmail.com",
    }
    create_resp = client.post("/renters", json=renter_1)
    assert create_resp.status_code == 201

    renter_id = create_resp.get_json()["id"]

    del_resp = client.delete("/renters", "renter_id":renter_id)
    assert del_resp.status_code == 204

    del_resp = client.delete("/renters", {"renter_id":renter_id)
    assert del_resp.status_code != 204

def test_delete_nonex_renter(client):
    """delete a nonexistent renter
    """

    "renter_id" : 1

    del_resp = client.delete("/renters", "renter_id":renter_id)
    assert del_resp.status_code != 204


def test_update_renter(client):
    """update a renter
    """
    renter_1 = {
        "name": "Julian Andrews",
        "email": "j.andrews@gmail.com",
    }
    create_resp = client.post("/renters", json=renter_1)
    assert create_resp.status_code == 201

    renter_id = create_resp.get_json()["id"]

    del_resp = client.update("/renters", "renter_id" : renter_id)
    assert del_resp.status_code == 200

def test_update_nonex_renter(client):
    """update a nonexistent renter
    """
    "renter_id" : 1

    del_resp = client.update("/renters", "renter_id":renter_id)
    assert del_resp.status_code != 200

def test_list_rentals(client):
    """Return an empty list when no rentals have been made
    """
    response = client.get("/rentals")
    assert response.status_code == 200
    assert response.get_json() == []

def test_show_all_rentals(client):
    """show all rentals
    """
    renter_1 = {
        "name": "James Parker",
        "email": "j.parker@gmail.com",
    }
    create_resp = client.post("/renters", json=renter_1)
    renter_id = create_resp.get_json()["id"]

    equip = {
        "name": "Kayak",
        "category": "Boats",
        "total_units": 15,
    }
    create_resp2 = client.post("/equipment", json=equip)
    equipment_id = create_resp2.get_json()["id"]

    create_resp3=client.post("/equipment","equipment_id": equipment_id, "renter_id": renter_id)
    create_resp4=client.get("/rentals")
    assert create_resp4.status_code == 200
    equip = {
        "name": "Paddleboard",
        "category": "Boats",
        "total_units": 13,
    }
    create_resp2 = client.post("/equipment", json=equip)
    equipment_id = create_resp2.get_json()["id"]
    create_resp3=client.post("/equipment","equipment_id": equipment_id, "renter_id": renter_id)
    equip = {
        "name": "Canoe",
        "category": "Boats",
        "total_units": 10,
    }
    create_resp2 = client.post("/equipment", json=equip)
    equipment_id = create_resp2.get_json()["id"]
    create_resp3=client.post("/equipment","equipment_id": equipment_id, "renter_id": renter_id)
    equip = {
        "name": "Sailboat",
        "category": "Boats",
        "total_units": 8,
    }
    create_resp2 = client.post("/equipment", json=equip)
    equipment_id = create_resp2.get_json()["id"]
    create_resp3=client.post("/equipment","equipment_id": equipment_id, "renter_id": renter_id)

    create_resp4=client.get("/rentals")
    assert create_resp4.status_code == 200    

def test_return_rental(client):
    """show return rental
    """
    renter_1 = {
        "name": "James Parker",
        "email": "j.parker@gmail.com",
    }
    create_resp = client.post("/renters", json=renter_1)
    renter_id = create_resp.get_json()["id"]

    equip = {
        "name": "Kayak",
        "category": "Boats",
        "total_units": 15,
    }
    create_resp2 = client.post("/equipment", json=equip)
    equipment_id = create_resp2.get_json()["id"]

    create_resp3=client.post("/equipment","equipment_id": equipment_id, "renter_id": renter_id)
    create_resp4=client.put("/rentals")
    assert create_resp4.status_code == 200

def test_return_returned_rental(client):
    """show return returned rental
    """
    renter_1 = {
        "name": "James Parker",
        "email": "j.parker@gmail.com",
    }
    create_resp = client.post("/renters", json=renter_1)
    renter_id = create_resp.get_json()["id"]

    equip = {
        "name": "Kayak",
        "category": "Boats",
        "total_units": 15,
    }
    create_resp2 = client.post("/equipment", json=equip)
    equipment_id = create_resp2.get_json()["id"]

    create_resp3=client.post("/equipment","equipment_id": equipment_id, "renter_id": renter_id)
    create_resp4=client.put("/rentals", "equipment_id": equipment_id, "renter_id":renter_id)
    create_resp4=client.put("/rentals", "equipment_id": equipment_id, "renter_id":renter_id)
    assert create_resp4.status_code != 200

def test_return_nonex_rental(client):
    """show return nonexistent rental
    """
    "equipment_id"=1
    "renter_id"=1
    create_resp4=client.put("/rentals", "equipment_id": equipment_id, "renter_id":renter_id)
    assert create_resp4.status_code != 200

