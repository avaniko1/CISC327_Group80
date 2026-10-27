

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