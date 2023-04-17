def test_home_page(test_client):
    response = test_client.get("/")
    assert response.status_code == 302
    assert response.headers["Location"] == "/openapi"
