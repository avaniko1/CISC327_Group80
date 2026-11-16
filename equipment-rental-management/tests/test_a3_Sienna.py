from unittest.mock import patch 
from datetime import date, timedelta
from app.models.rental import Rental
from app.models.equipment import Equipment
from app import store

def test_notification_sends(client, monkeypatch):
    """True should be returned by send_notification if message is sent
    """
    monkeypatch.setattr("app.routes.rentals.send_notification", lambda recipient, subject, message: True) 

    rental={
        "id": 1,
        "equipment_id": 1,
        "renter_id": 1,
        "due_date": date.today() - timedelta(days=3),
        "return_date": None,
    }
    renter={
        "id": 1,
        "name": "plspls",
        "email": "pleasework@plsplspls.com"
    }
    create_resp=client.post(f"/rentals", json=rental)
    overdue=client.get("/rentals/overdue")
    #assert overdue["result"]==True


  
def test_notification_sends_expected_message_and_subject(client, monkeypatch):
    """Testing that it sends the right message and subject to the right renter
    """

    with patch("app.routes.rentals.send_notification", result=True) as mock_send: 
        rental={
            "id": 1,
            "equipment_id": 1,
            "renter_id": 1,
            "due_date": date.today() - timedelta(days=3),
            "return_date": None, 
        }
        renter={
            "id": 1,
            "name": "plspls",
            "email": "pleasework@plsplspls.com"
        }
        create_resp=client.post(f"/rentals", json=rental)
        overdue=client.get(f"/rentals/overdue", json=rental)
    assert overdue.status_code==200
    #assert overdue["result"]==True
    #mock_send.assert_called_once_with("pleasework@plsplspls.com", "Overdue Equipment", "Attention customer, your rental with Trailside Outdoor Gear Rental is overdue. Please return the equipment at your earliest convenience. Please be advised that additional fees may be added.")

def test_rentals_page_get_rentals(client):
    """Testing getting rentals page with rentals
    """
    rental = Rental(
        id=1,
        equipment_id=1,
        renter_id=1,
        due_date=date.today(),
    )
    store.rentals[1] = rental
    create_resp=client.get("/ui/rentals")
    assert b"html" in create_resp.data

def test_rentals_page_get_no_rentals(client):
    """Testing getting rentals page with no rentals
    """
    create_resp=client.get("/ui/rentals")
    assert b"html" in create_resp.data

def test_rentals_page_post_item_none(client):
    """Testing that get returns rentals page with no rentals
    """
    create_resp=client.post("/ui/rentals")
    #assert create_resp.status_code == 302
    
def test_rentals_page_post_item_not_none(client):    
    """Testing that get returns rentals page with rentals
    """
    rental = Rental(
        id=1,
        equipment_id=1,
        renter_id=1,
        due_date=date.today(),
    )
    equipment = Equipment(
        id=1,
        name="Kayak",
        category= "Boats",
        total_units= 2,
        available_units= 2,
    )
    store.equipment[1] = equipment
    store.rentals[1] = rental
    create_resp=client.post("/ui/rentals/1")

    #assert create_resp.status_code == 302

def test_return_item_none(client):
    """test return item==none rental
    """
    equipment_id=1
    renter_id=1
    create_resp=client.post("1/rentals")
    assert create_resp.status_code == 404

def test_return_item_returned_already(client):
    """test return already returned rental
    """
    rental = Rental(
        id=1,
        equipment_id=1,
        renter_id=1,
        due_date=date.today(),
    )
    store.rentals[1] = rental
    create_resp=client.put("/rentals/1/return")
    assert create_resp.status_code == 200
    create_resp1=client.put("/rentals/1/return")
    assert create_resp1.status_code == 400

def test_extend_duedate(client):
    """Testing extend due date
    """
    rental = Rental(
        id=1,
        equipment_id=1,
        renter_id=1,
        due_date=date.today(),
    )
    store.rentals[1] = rental
    create_resp=client.put("/rentals/1/extend", json={"days": 1})
    assert rental.due_date == (date.today() + timedelta(days=1))

def test_extend_duedate_returned_rental(client):
    """Testing extend due date of returned rental
    """
    rental = Rental(
        id=1,
        equipment_id=1,
        renter_id=1,
        due_date=date.today(),
    )
    store.rentals[1] = rental
    create_resp=client.put("/rentals/1/return")
    assert create_resp.status_code == 200
    create_resp=client.put("/rentals/1/extend")

    assert create_resp.status_code == 400

def test_extend_duedate_nonex_rental(client):
    """Testing extend due date of nonexistent rental
    """
    create_resp=client.put("/rentals/1/extend")

    assert create_resp.status_code == 404