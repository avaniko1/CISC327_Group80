
from unittest.mock import patch

from app import store
from app.models.renter import Renter
from app.models.rental import Rental

#Test 1: Testing a nonexistent email address
def test_nonexistent_email(client, monkeypatch):

    def notification_to_email(recipient, subject, message):
        assert recipient == "doesnotexist@test.com"
        return False

    monkeypatch.setattr(
        "app.routes.rentals.send_notification", 
        notification_to_email
        )


    renter = Renter(
        id = 1,
        name = "John Smith",
        email = "doesnotexist@test.com"
    )

    rental= Rental(
        id = 1,
        equipment_id = 1,
        renter_id = 1,
        due_date = date.today() - timedelta(days=1)
    )

    store.renters[1] = renter
    store.rentals[1] = rental

    response = client.get("/rentals/overdue")

    assert response.status_code == 200
    assert response.get_json()[0]["id"] == 1

#Test 2: Testing during an outage
def test_notification_outage(client, monkeypatch):

    monkeypatch.setattr(
        "app.routes.rentals.notification_available", 
        lambda: False
        )


    renter = Renter(
        id = 1,
        name = "John Smith",
        email = "doesnotexist@test.com"
    )

    rental= Rental(
        id = 1,
        equipment_id = 1,
        renter_id = 1,
        due_date = date.today() - timedelta(days=1)
    )

    store.renters[1] = renter
    store.rentals[1] = rental

    response = client.get("/rentals/overdue")

    assert response.status_code == 200
    assert response.get_json()[0]["id"] == 1


