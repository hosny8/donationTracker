import unittest
import json
from app import app

class DonationAPITestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
    
    def test_add_donation(self):
        response = self.app.post('/donation', json={
            "donor": "Alice",
            "donation_type": "USD",
            "amount": 50
        }
        )

        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data["donation"]["donor"], "Alice")

    def test_delete_all_donations(self):
        response = self.app.post('/donation', json={
            "donor": "Alice",
            "donation_type": "USD",
            "amount": 50
        }
        )

        response = self.app.delete('/donations')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data["message"], "All donations deleted")

    def test_delete_donation(self):
        response = self.app.post('/donation', json={
            "donor": "Alice",
            "donation_type": "USD",
            "amount": 50
        }
        )

        response = self.app.delete('/donation/1')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data["message"], "Donation deleted successfully!")

    def test_total_donations(self):
        response = self.app.post('/donation', json={
            "donor": "Alice",
            "donation_type": "USD",
            "amount": 50
        }
        )

        response = self.app.get('/donations/total')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data["total_donations"], 50)

    def test_total_donations_usd(self):
        response = self.app.post('/donation', json={
            "donor": "Alice",
            "donation_type": "USD",
            "amount": 50
        }
        )    

        response = self.app.get('/donations/total/USD')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data["total_usd_donations"], 50)
    
    def test_total_donations_euro(self):
        response = self.app.post('/donation', json={
            "donor": "Alice",
            "donation_type": "EURO",
            "amount": 50
        }
        )

        response = self.app.get('/donations/total/EURO')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data["total_euro_donations"], 0)
    
    def test_get_donations(self):
        response = self.app.post('/donation', json={
            "donor": "Alice",
            "donation_type": "USD",
            "amount": 50
        }
        )

        response = self.app.get('/donations')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data), 1)

    def test_find_donation_by_donor(self):
        response = self.app.post('/donation', json={
            "donor": "Alice",
            "donation_type": "USD",
            "amount": 50
        }
        )

        response = self.app.get('/donations/donor/Alice')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data["total_by_donor"], 50)

    def test_get_top_donations(self):
        response = self.app.post('/donation', json={
            "donor": "Alice",
            "donation_type": "USD",
            "amount": 50
        }
        )

        response = self.app.get('/donations/top')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data["top_donations"], 50)
    
    def test_delete_request(self):
        response = self.app.delete('/donations')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data["message"], "All donations deleted")

    def test_donations_in_date_range(self):
        response = self.app.post('/donation', json={
            "donor": "Alice",
            "donation_type": "USD",
            "amount": 50,
            "donation_date": "2021-04-01"
        }
        )

        response = self.app.get('/donations/date/2021-04-01/2021-04-01')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data["donations_in_date_range"], 50)
    
    def test_donations_in_date_range_USD(self):
        response = self.app.post('/donation', json={
            "donor": "Alice",
            "donation_type": "USD",
            "amount": 50,
            "donation_date": "2021-04-01"
        }
        )

        response = self.app.get('/donations/date/2021-04-01/2021-04-01/USD')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data["donations_in_date_range_usd"], 50)
    
    def test_donations_in_date_range_EURO(self):
        response = self.app.post('/donation', json={
            "donor": "Alice",
            "donation_type": "EURO",
            "amount": 50,
            "donation_date": "2021-04-01"
        }
        )

        response = self.app.get('/donations/date/2021-04-01/2021-04-01/EURO')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data["donations_in_date_range_euro"], 0)
