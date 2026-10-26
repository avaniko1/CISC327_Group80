def test_list_renter(client):
    """Return an empty list when no renters have been made
    """
    response = client.get("/renters")
    assert response.status_code == 200
    assert response.get_json() == []
  """ renters tests
  """

  """ empty rentals list test
  """
  """return rental
  """
  ""Check returning already returned rental
  """
  """Make nonexistent rental as returned
  """
