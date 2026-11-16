from unittest.mock import patch 
from datetime import date, timedelta

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
    overdue=client.get(f"/rentals/overdue", json=rental)
    assert overdue["result"]==True


  
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
    assert overdue["result"]==True
    mock_send.assert_called_once_with("pleasework@plsplspls.com", "Overdue Equipment", "Attention customer, your rental with Trailside Outdoor Gear Rental is overdue. Please return the equipment at your earliest convenience. Please be advised that additional fees may be added.")