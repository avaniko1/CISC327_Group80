

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

    skis_item = None
    for item in equipment_list:
        if item["name"] == "Skis":
            skis_item = item
            break

    assert skis_item["category"] == "Winter Sports"
    assert skis_item["total_units"] == 15

    canoe_item = None
    for item in equipment_list:
        if item["name"] == "Canoe":
            canoe_item = item
            break

    assert canoe_item["category"] == "Water Activities"
    assert canoe_item["total_units"] == 10

    tents_item = None
    for item in equipment_list:
        if item["name"] == "Tents":
            tents_item = item
            break
    
    assert tents_item["category"] == "Camping"
    assert tents_item["total_units"] == 20



#Test 1.1: List all equipment when empty
def test_list_all_equipment_empty(client):
    result = client.get("/equipment")

    assert result.status_code == 200

    equipment_list = result.get_json()

    assert len(equipment_list) == 0



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


#Test 3.1: Delete Equipment that does not exist
def test_delete_equipment_not_found(client):
    equipment_id = 999
    result = client.delete(f"/equipment/{equipment_id}")
    assert result.status_code == 404




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

    renter_info = client.post("/renters", json=renter_info)
    assert renter_info.status_code == 201

    renter_id = renter_info.get_json()["id"]

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

#Test 4.1: Check out equipment when no units are available
def test_checkout_no_units_available(client):
    equipment_item = {
        "name": "Canoe",
        "category": "Water Activities",
        "total_units": 1
    }

    result = client.post("/equipment", json=equipment_item)
    assert result.status_code == 201

    equipment_id = result.get_json()["id"]

    renter_info = client.post("/renters", json={
        "name": "Ava Nikolaus",
        "email": "ava.niko@cisc.com"
    })
    
    assert renter_info.status_code == 201
    renter_id = renter_info.get_json()["id"]

    checkout_info = {
        "equipment_id": equipment_id,
        "renter_id": renter_id
    }
    
    checkout_one = client.post("/rentals", json=checkout_info)

    assert checkout_one.status_code == 201

    result = client.get(f"/equipment/{equipment_id}")
    assert result.status_code == 200
    assert result.get_json()["available_units"] == 0

    checkout_info = {
        "equipment_id": equipment_id,
        "renter_id": renter_id
    }
    
    checkout_two = client.post("/rentals", json=checkout_info)

    assert checkout_two.status_code in [400, 409]

    result = client.get(f"/equipment/{equipment_id}")
    assert result.status_code == 200
    assert result.get_json()["available_units"] == 0

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

#Test 5.1 Get equipment that does not exist

def test_get_equipment_not_exist(client):
    equipment_id = 999
    result = client.get(f"/equipment/{equipment_id}")
    assert result.status_code == 404

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

    rental_info ={
        "equipment_id": equipment_id,
        "renter_id": renter_id
    }

    rental_info = client.post("/rentals", json=rental_info)

    assert rental_info.status_code == 201

    response = client.get(f"/rentals?renter_id={renter_id}")
    assert response.status_code == 200

    rentals = response.get_json()
    assert len(rentals) == 1
    assert rentals[0]["equipment_id"] == equipment_id
    assert rentals[0]["renter_id"] == renter_id

#Test 6.1: Look Up Rentals for a renter with none

def test_look_up_rentals_no_rentals(client):
    renter_info = client.post("/renters", json={
        "name": "Ava Nikolaus",
        "email": "ava.niko@cisc.com"
    })
    
    assert renter_info.status_code == 201
    renter_id = renter_info.get_json()["id"]

    response = client.get(f"/rentals?renter_id={renter_id}")
    assert response.status_code == 200
    assert response.get_json() == []


#Test 7: Update Equipment

def test_update_equipment(client):
    equipment_item = {
        "name": "Sleeping Bag",
        "category": "Camping",
        "total_units": 45
    }

    result = client.post("/equipment", json=equipment_item)
    assert result.status_code == 201

    equipment_id = result.get_json()["id"]

    updated_item = {
        "name": "Deluxe Sleeping Bag",
        "category": "Camping",
        "total_units": 10,
        "available_units": 10
    }

    update_result = client.put(f"/equipment/{equipment_id}", json=updated_item)
    assert update_result.status_code == 200

    result = client.get(f"/equipment/{equipment_id}")
    assert result.status_code == 200

    equipment = result.get_json()
    assert equipment["name"] == "Deluxe Sleeping Bag"
    assert equipment["category"] == "Camping"
    assert equipment["total_units"] == 10
    assert equipment["available_units"] == 10