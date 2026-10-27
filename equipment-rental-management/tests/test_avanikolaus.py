

#Test 1: List all equipment
def test_list_all_equipment(client):

    equipment_list = [
        {
            "name": "Skis",
            "category": "Winter Sports",
            "total_units": 15
        },
        {
            "name": "Canoe",
            "category": "Water Activities",
            "total_units": 10
        },
        {
            "name": "Tents",
            "category": "Camping",
            "total_units": 20
        }
    ]
    
    for item in equipment_list:
        result = client.post("/equipment", json=item)
        assert result.status_code == 201
    
    result = client.get("/equipment")

    assert result.status_code == 200

    equipment_list = result.get_json()

    assert len(equipment_list) == 3

    equipment_names = [item["name"] for item in equipment_list]
    assert "Skis" in equipment_names
    assert "Canoe" in equipment_names
    assert "Tents" in equipment_names


#Test 2: Add equipment
def test_add_equipment(client):
    equipment_item = {
        "name": "Snowboard",
        "category": "Winter Sports",
        "total_units": 150
    }

    result = client.post("/equipment", json=equipment_item)
    assert result.status_code == 201

    added_item = result.get_json()
    assert added_item["name"] == "Snowboard"
    assert added_item["category"] == "Winter Sports"
    assert added_item["total_units"] == 150
    assert added_item["available_units"] == 150

    result = client.get("/equipment")
    assert result.status_code == 200

    equipment_list = result.get_json()
    assert any(item["name"] == "Snowboard" for item in equipment_list)

#Test 3: Delete Equipment
def test_delete_equipment(client):
    equipment_item = {
        "name": "Snowshoes",
        "category": "Winter Sports",
        "total_units": 60
    }

    result = client.post("/equipment", json=equipment_item)
    assert result.status_code == 201

    added_item = result.get_json()
    equipment_id = added_item["id"]

    result = client.delete(f"/equipment/{equipment_id}")
    assert result.status_code in[200, 204]

    result = client.get("/equipment")
    assert result.status_code == 200

    equipment_list = result.get_json()
    equipment_id = [item["id"] for item in equipment_list]
    assert equipment_id not in equipment_id

#Test 4: Check out equipment
def test_checkout_equipment(client):
    equipment_item = {
        "name": "Jet Ski",
        "category": "Water Activities",
        "total_units": 75
    }
    
    result = client.post("/equipment", json=equipment_item)
    assert result.status_code == 201

    equipment_id = result.get_json()["id"]

    renter_info = {
        "name": "Ava Nikolaus",
        "email": "ava.niko@cisc.com"
    }

    result = client.post("/renters", json=renter_info)
    assert result.status_code == 201

    renter_id = result.get_json()["id"]

    checkout = {
        "equipment_id": equipment_id,
        "renter_id": renter_id

    }

    result = client.post("/rentals", json=checkout)
    assert result.status_code == 201

    result = client.get("/equipment")
    assert result.status_code == 200

    equipment_list = result.get_json()
    for item in equipment_list:
        if item["id"] == equipment_id:
            assert item["available_units"] == 74


