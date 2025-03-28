import unittest
from app.views import app, db


class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        self.computers = [
            {
                "hard_drive_type": "SSD",
                "processor": "Intel Core i7",
                "ram_amount": 16,
                "maximum_ram": 32,
                "hard_drive_space": 512,
                "form_factor": "Laptop",
            },
            {
                "hard_drive_type": "HDD",
                "processor": "Intel Core i5",
                "ram_amount": 8,
                "maximum_ram": 16,
                "hard_drive_space": 1024,
                "form_factor": "Desktop",
            },
            {
                "hard_drive_type": "SSD",
                "processor": "AMD Ryzen 7",
                "ram_amount": 32,
                "maximum_ram": 64,
                "hard_drive_space": 2048,
                "form_factor": "Laptop",
            },
            {
                "hard_drive_type": "SSD",
                "processor": "Intel Core i9",
                "ram_amount": 64,
                "maximum_ram": 128,
                "hard_drive_space": 4096,
                "form_factor": "Server",
            },
            {
                "hard_drive_type": "HDD",
                "processor": "Intel Core i3",
                "ram_amount": 4,
                "maximum_ram": 8,
                "hard_drive_space": 500,
                "form_factor": "Desktop",
            },
            {
                "hard_drive_type": "SSD",
                "processor": "Apple M1",
                "ram_amount": 16,
                "maximum_ram": 16,
                "hard_drive_space": 256,
                "form_factor": "Laptop",
            },
            {
                "hard_drive_type": "HDD",
                "processor": "AMD Ryzen 5",
                "ram_amount": 8,
                "maximum_ram": 32,
                "hard_drive_space": 2000,
                "form_factor": "Desktop",
            },
        ]

        with app.app_context():
            db.create_all()

    def populate_db(self):

        for computer in self.computers:
            self.app.post("/computer", json=computer)

    def tearDown(self):

        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_get_computer_from_db(self):
        self.populate_db()
        response = self.app.get("/computer/4")
        data = response.get_json()
        self.assertEqual(
            data["computer"],
            {
                "id": 4,
                "hard_drive_type": "SSD",
                "processor": "Intel Core i9",
                "ram_amount": 64,
                "maximum_ram": 128,
                "hard_drive_space": 4096,
                "form_factor": "Server",
            },
        )

    def test_get_computer_nonexistent(self):
        self.populate_db()
        response = self.app.get("/computer/40")
        self.assertEqual(response.status_code, 404)

    def test_get_computers(self):
        response = self.app.get("/computers?page=1&per_page=10")
        self.assertEqual(response.status_code, 200)

        data = response.get_json()
        self.assertIsInstance(data, dict)
        self.assertIn("computers", data)
        self.assertIn("total", data)
        self.assertIn("pages", data)
        self.assertIn("current_page", data)
        self.assertIn("per_page", data)

        self.assertEqual(data["computers"], [])
        self.assertEqual(data["total"], 0)
        self.assertEqual(data["pages"], 0)
        self.assertEqual(data["current_page"], 1)
        self.assertEqual(data["per_page"], 10)

    def test_get_computers_pagination(self):
        self.populate_db()
        response = self.app.get("/computers?page=1&per_page=3")
        data = response.get_json()

        self.assertEqual(
            data["computers"],
            [
                {
                    "id": 1,
                    "hard_drive_type": "SSD",
                    "processor": "Intel Core i7",
                    "ram_amount": 16,
                    "maximum_ram": 32,
                    "hard_drive_space": 512,
                    "form_factor": "Laptop",
                },
                {
                    "id": 2,
                    "hard_drive_type": "HDD",
                    "processor": "Intel Core i5",
                    "ram_amount": 8,
                    "maximum_ram": 16,
                    "hard_drive_space": 1024,
                    "form_factor": "Desktop",
                },
                {
                    "id": 3,
                    "hard_drive_type": "SSD",
                    "processor": "AMD Ryzen 7",
                    "ram_amount": 32,
                    "maximum_ram": 64,
                    "hard_drive_space": 2048,
                    "form_factor": "Laptop",
                },
            ],
        )
        self.assertEqual(data["total"], 7)
        self.assertEqual(data["pages"], 3)
        self.assertEqual(data["current_page"], 1)
        self.assertEqual(data["per_page"], 3)

        response = self.app.get("/computers?page=2&per_page=3")
        data = response.get_json()

        self.assertEqual(
            data["computers"],
            [
                {
                    "id": 4,
                    "hard_drive_type": "SSD",
                    "processor": "Intel Core i9",
                    "ram_amount": 64,
                    "maximum_ram": 128,
                    "hard_drive_space": 4096,
                    "form_factor": "Server",
                },
                {
                    "id": 5,
                    "hard_drive_type": "HDD",
                    "processor": "Intel Core i3",
                    "ram_amount": 4,
                    "maximum_ram": 8,
                    "hard_drive_space": 500,
                    "form_factor": "Desktop",
                },
                {
                    "id": 6,
                    "hard_drive_type": "SSD",
                    "processor": "Apple M1",
                    "ram_amount": 16,
                    "maximum_ram": 16,
                    "hard_drive_space": 256,
                    "form_factor": "Laptop",
                },
            ],
        )
        self.assertEqual(data["total"], 7)
        self.assertEqual(data["pages"], 3)
        self.assertEqual(data["current_page"], 2)
        self.assertEqual(data["per_page"], 3)

        response = self.app.get("/computers?page=3&per_page=3")
        data = response.get_json()

        self.assertEqual(
            data["computers"],
            [
                {
                    "id": 7,
                    "hard_drive_type": "HDD",
                    "processor": "AMD Ryzen 5",
                    "ram_amount": 8,
                    "maximum_ram": 32,
                    "hard_drive_space": 2000,
                    "form_factor": "Desktop",
                },
            ],
        )

        self.assertEqual(data["total"], 7)
        self.assertEqual(data["pages"], 3)
        self.assertEqual(data["current_page"], 3)
        self.assertEqual(data["per_page"], 3)

    def test_pagination_nonexistent_page(self):
        self.populate_db()
        response = self.app.get("/computers?page=0&per_page=3")
        self.assertEqual(response.status_code, 404)
        response = self.app.get("/computers?page=4&per_page=3")
        self.assertEqual(response.status_code, 404)

    def test_add_computer(self):
        response = self.app.post("/computer", json=self.computers[0])
        self.assertEqual(response.status_code, 201)
        self.assertIn(b"Computer added successfully", response.data)

    def test_edit_computer(self):
        self.populate_db()
        response = self.app.put(
            "/computer/1",
            json={
                "hard_drive_type": "HDD",
                "processor": "Intel Core i9",
                "ram_amount": 32,
                "maximum_ram": 64,
                "hard_drive_space": 1024,
                "form_factor": "Desktop",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Computer updated successfully", response.data)

    def test_edit_computer_nonexistent(self):
        self.populate_db()
        response = self.app.put(
            "/computer/8",
            json={
                "hard_drive_type": "HDD",
                "processor": "Intel Core i9",
                "ram_amount": 32,
                "maximum_ram": 64,
                "hard_drive_space": 1024,
                "form_factor": "Desktop",
            },
        )
        self.assertEqual(response.status_code, 404)

    def test_delete_computer(self):
        self.populate_db()
        response = self.app.delete("/computer/1")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Computer deleted successfully", response.data)

    def test_delete_computer_nonexistent(self):
        self.populate_db()
        response = self.app.delete("/computer/8")
        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()
