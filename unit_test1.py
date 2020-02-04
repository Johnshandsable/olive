# built-in
import csv
import os
import unittest
from app import app, db
from app.config import Config
from app.funcs import get_month, get_unique, get_query, get_last, get_csvfile, get_db
from app.models import User, CheckIn


class ClientModelCase(unittest.TestCase):
    def setUp(self):
        app.config.from_object(Config)
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_user(self):
        u1 = User(family_size=2, family_name='Doe')
        u2 = User(family_size=34, family_name='Test')
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        self.assertEqual(u1.family_size, 2)
        self.assertEqual(u1.family_name, 'Doe')
        self.assertEqual(u2.family_size, 34)
        self.assertEqual(u2.family_name, 'Test')

if __name__ == "__main__":
    unittest.main()
