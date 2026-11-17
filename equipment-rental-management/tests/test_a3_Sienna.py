from unittest.mock import patch 
from datetime import date, timedelta
from app.models.rental import Rental
from app.models.renter import Renter
from app.models.equipment import Equipment
from app import store

def test_notification_sends(client, monkeypatch):
    """True should be returned by send_notification if message is sent
    """
    def notif(recipient, subject, message):
        assert recipient=="plspls@justwork.com"
        return True
    
    monkeypatch.setattr(
        "app.routes.rentals.send_notification",
        notif
    )
    overdue_rental= Rental(
        id= 1,
        equipment_id= 1,
        renter_id= 1,
        due_date= date.today() - timedelta(days=3),
    )
    renter= Renter(
        id=1,
        name="plspls",
        email= "plspls@justwork.com"
    )
    
    store.rentals[1]=overdue_rental
    store.renters[1]=renter
    result=client.get("/rentals/overdue")

    assert result== {"result"==True}
  
def test_notification_sends_expected_message_and_subject(client, monkeypatch):
    """Testing that it sends the right message and subject to the right renter
    """

    with patch("app.routes.rentals.send_notification", return_value=True) as mock_send: 
        renter=Renter(id= 1,name="plspls",email="pleasework@plsplspls.com")
        rental= Rental(id= 1,equipment_id= 1, renter_id=1, due_date=date.today()-timedelta(days=3))
        store.renters[1]=renter
        store.rentals[1]=rental
        response=client.get("/rentals/overdue")
    mock_send.assert_called_once_with("pleasework@plsplspls.com", "Overdue Equipment", "Attention customer, your rental with Trailside Outdoor Gear Rental is overdue. Please return the equipment at your earliest convenience. Please be advised that additional fees may be added.")


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

    create_resp=client.post("/ui/rentals", data = {"equipment_id":1, "renter_id":1})
    assert create_resp.status_code == 302
    
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
    create_resp=client.post("/ui/rentals", data = {"equipment_id":1, "renter_id":1})

    assert create_resp.status_code == 302

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