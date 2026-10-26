def test_list_equipment(client):
    """Return an empty list when no equipment has been made
    """
    response = client.get("/equipment")
    assert response.status_code == 200
    assert response.get_json() == []
def test_list_rentals(client):
    """Return an empty list when no rentals have been made
    """
    response = client.get("/rentals")
    assert response.status_code == 200
    assert response.get_json() == []

def test_create_equipment_checkavailability_and_recheck_after_rental(client):
    """Add equipment and check list
    """
    new_equip = {
      "name": "Paddleboard",
      "category": "Boat",
      "total_units": 2,
    }
    create_resp = client.post("/equipment", json=new_equip)
    assert create_resp.status_code == 203
    equipment_id = create_resp.get_json()["id"]

    avail_resp = client.get(f"/equipment/{equipment_id}/availability")
    assert avail_resp.status_code == 200
    data = avail_resp.get_json()
    assert data["available_units"] == 1
    assert data["is_available"] is True

  """doublecheck availabilty after rental
  """
  new_rental = {
    "id" = equipment_id,
    "name":"Paddleboard",
    "category"="Boat",
  }   
  create_rental = client.post("/rentals", json=new_rental)
  assert create_resp.status_code == 201
  data = avail_resp.get_json()
  assert data["available_units"] == 0
  assert data["is_available"] is True
    new_rental2 = {
    "id" = equipment_id,
    "name":"Kayak",
    "category"="Boat",
  }   
  create_rental = client.post("/rentals", json=new_rental2)
  assert create_resp.status_code == 202
  data = avail_resp.get_json()
  assert data["available_units"] == 5
  assert data["is_available"] is True
    new_rental3 = {
    "id" = equipment_id,
    "name":"Kayak",
    "category"="Boat",
  } 
  create_rental = client.post("/rentals", json=new_rental3)
  data = avail_resp.get_json()
  assert data["is_available"] is False
  
