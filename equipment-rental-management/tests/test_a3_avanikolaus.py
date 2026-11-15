
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


#--------COVERAGE TESTS--------
#Test 1
def test_nonexistent_equipment(client):
    response = client.put("/equipment/999", json={"name": "Nonexistent Item"}
    )

    assert response.status_code == 404
    assert response.get_json() == { "error": "Equipment not found" }

#Test 2
def test_damaged_equipment(client):
    response = client.post("/equipment", json={
        "name": "Skis",
        "category": "Winter Sports",
        "total_units": 6
    })

    equipment_id = response.get_json()["id"]
    item = store.equipment[equipment_id]
    item.is_damaged_units = None

    response = client.patch(f"/equipment/{equipment_id}/status", json={"is_available": True, "is_damaged": False}
    )

    assert response.status_code == 200
    assert item.is_damaged_units == 0
    assert response.get_json()["is_damaged_units"] == 0


#Test 3
def test_out_of_service(client):
    response = client.post("/equipment", json={
        "name": "Skis",
        "category": "Winter Sports",
        "total_units": 6
    })

    equipment_id = response.get_json()["id"]
    item = store.equipment[equipment_id]
    item.out_of_service_units = None

    response = client.patch(f"/equipment/{equipment_id}/status", json={"is_available": True, "is_damaged": False}
    )

    assert response.status_code == 200
    assert item.out_of_service_units == 0
    assert response.get_json()["out_of_service_units"] == 0

#Test 4
def test_reset_available_units(client):
    response = client.post("/equipment", json={
        "name": "Skis",
        "category": "Winter Sports",
        "total_units": 6
    })

    equipment_id = response.get_json()["id"]
    item = store.equipment[equipment_id]
    item.available_units = 1

    response = client.patch(f"/equipment/{equipment_id}/status", json={"is_available": True, "is_damaged": False}
    )

    assert response.status_code == 200
    assert item.available_units == 6
    assert response.get_json()["available_units"] == 6

