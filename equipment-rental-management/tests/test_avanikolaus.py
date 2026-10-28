

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

    skis_item = next((item for item in equipment_list if item["name"] == "Skis"), None)
    assert skis_item["category"] == "Winter Sports"
    assert skis_item["total_units"] == 15

    canoe_item = next((item for item in equipment_list if item["name"] == "Canoe"), None)
    assert canoe_item["category"] == "Water Activities"
    assert canoe_item["total_units"] == 10

    tents_item = next((item for item in equipment_list if item["name"] == "Tents"), None)
    assert tents_item["category"] == "Camping"
    assert tents_item["total_units"] == 20



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

    added_item = next((item for item in equipment_list if item["name"] == "Snowboard"), None)

    assert added_item["name"] == "Snowboard"
    assert added_item["category"] == "Winter Sports"
    assert added_item["total_units"] == 150
    assert added_item["available_units"] == 150

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

    assert len(equipment_list) == 0

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

#Test 5: Get one equipment

def test_get_one_equipment(client):
    equipment_item = {
        "name": "Helmet",
        "category": "Safety Gear",
        "total_units": 30
    }


    result = client.post("/equipment", json=equipment_item)
    assert result.status_code == 201

    new_item = result.get_json()
    equipment_id = new_item["id"]

    result = client.get(f"/equipment/{equipment_id}")
    assert result.status_code == 200

    item = result.get_json()
    assert item["id"] == equipment_id
    assert item["name"] == "Helmet"
    assert item["category"] == "Safety Gear"
    assert item["total_units"] == 30
    assert item["available_units"] == 30
    assert item["available_units"] == 30

 #Test 6: Look Up Rentals

def test_look_up_rentals(client):
    equipment_item = {
        "name": "Snowboard",
        "category": "Winter Sports",
        "total_units": 65
    }

    equipment_item = client.post("/equipment", json=equipment_item)
    assert equipment_item.status_code == 201
    equipment_id = equipment_item.get_json()["id"]

    renter_info = client.post("/renters", json={
        "name": "Ava Nikolaus",
        "email": "ava.niko@cisc.com"
    })

    assert renter_info.status_code == 201
    renter_id = renter_info.get_json()["id"]

    rental_info = client.post("/rentals", json={
        "equipment_id": equipment_id,
        "renter_id": renter_id
    })

    assert rental_info.status_code == 201

    response = client.get(f"/rentals?renter_id={renter_id}")
    assert response.status_code == 200

    rentals = response.get_json()
    assert len(rentals) == 1
    assert rentals[0]["equipment_id"] == equipment_id
    assert rentals[0]["renter_id"] == renter_id

