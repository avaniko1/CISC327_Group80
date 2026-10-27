

#Test 1: List 
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