import unittest
from fastapi.testclient import TestClient
import main

client = TestClient(main.app)


# defining basic static test cases
class ApiTestCases(unittest.TestCase):
    correct_vin = "1XPWD40X1ED215307"
    incorrect_vin = "1XPWD40X1ED21530"

    def test_default_endpoint(self):
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"message": "Welcome to the default endpoint"}

    def test_lookup_endpoint_error(self):
        response = client.get("/lookup?vin={}".format(self.correct_vin))
        assert response.status_code == 200
        assert response.json() == {'message': 'Error in getting data for the request VIN'}

    def test_delete_error(self):
        response = client.get("/remove?vin={}".format(self.correct_vin))
        assert response.status_code == 200
        assert response.json() == {'message': 'Error in deleting VIN from the database'}

    def test_export_error(self):
        response = client.get("/export")
        assert response.status_code == 200
        assert response.json() == {'message': 'Error in exporting the database cache'}

    def test_is_vin_valid(self):
        assert main.is_vin_valid(self.correct_vin) is True

    def test_is_vin_invalid(self):
        assert main.is_vin_valid(self.incorrect_vin) is False
