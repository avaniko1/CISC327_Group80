
from unittest.mock import patch

from app import store
from app.models.renter import Renter
from app.models.rental import Rental
from datetime import date
from app.models.equipment import Equipment

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
#Equipment Route
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

#Rental Route
#Test 1

def test_list_rentals_by_equipment_id(client):
    rental_one = Rental(
        id = 1,
        equipment_id = 4,
        renter_id = 20,
        due_date = date.today()
    )

    rental_two = Rental(
        id = 2,
        equipment_id = 2,
        renter_id = 30,
        due_date = date.today()
    )

    store.rentals[1] = rental_one
    store.rentals[2] = rental_two

    response = client.get("/rentals?equipment_id=4")

    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 1
    assert data[0]["id"] == 1
    assert data[0]["equipment_id"] == 4

#Test 2
def test_checkout_nonexistent_equipment(client):
    response = client.post("/rentals", json={
        "equipment_id": 999,
        "renter_id": 1
    })

    assert response.status_code == 404
    assert response.get_json() == { "error": "Equipment not found"}

#Test 3
def test_deposit_nonexistent_rental(client):
    response = client.put("/rentals/999/deposit/release")

    assert response.status_code == 404
    assert response.get_json() == { "error": "Rental not found"
    }

#Test 4
def test_deposit_unreturned_rental(client):
    rental = Rental(
        id = 1,
        equipment_id = 1,
        renter_id = 1,
        due_date = date.today()
    )

    store.rentals[1] = rental

    response = client.put("/rentals/1/deposit/release")

    assert response.status_code == 400
    assert response.get_json() == {"error": "Equipment has not been returned yet"
    }

#Test 5
def test_deposit_rental_returned(client):
    rental = Rental(
        id = 1,
        equipment_id = 1,
        renter_id = 1,
        due_date = date.today(),
        return_date =date.today(),
        deposit_released = False
    )

    store.rentals[1] = rental

    response = client.put("/rentals/1/deposit/release")

    assert response.status_code == 200
    assert response.get_json() == {"rental_id": 1, "deposit_released" : True}
    

#View Route

#Test 1
def test_homepage(client):
    response = client.get("/")

    assert response.status_code == 200
    assert b"html" in response.data

#Test 2

def test_return_rental_page(client):
    equipment = Equipment(
        id = 1,
        name = "Skis",
        category = "Winter Sports",
        total_units = 6,
        available_units = 3
    )

    rental = Rental(
        id = 1,
        equipment_id = 1,
        renter_id = 1,
        due_date = date.today()
    )

    store.equipment[1] = equipment
    store.rentals[1] = rental

    response = client.post("/ui/rentals/1/return")

    assert response.status_code == 302
    assert rental.return_date == date.today()
    assert equipment.available_units == 4

#Test 3
def test_nonexistent_rental_return_page(client):
    response = client.post("/ui/rentals/999/return")

    assert response.status_code == 302
    assert 999 not in store.rentals

#Test 4
def test_returned_rental_page(client):
    equipment = Equipment(
        id = 1,
        name = "Skis",
        category = "Winter Sports",
        total_units = 6,
        available_units = 3
    )

    rental = Rental(
        id = 1,
        equipment_id = 1,
        renter_id = 1,
        due_date = date.today(),
        return_date = date.today()
    )

    store.equipment[1] = equipment
    store.rentals[1] = rental

    response = client.post("/ui/rentals/1/return")

    assert response.status_code == 302
    assert equipment.available_units == 3