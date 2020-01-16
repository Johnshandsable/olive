# built-in
import csv
import os
import unittest
from app import app, db
from app.config import Config
from app.funcs import get_month, get_unique, get_query, get_last, write_csv, get_csvfile, get_db
from app.models import User, CheckIn

# requires install
import pandas as pd
import sqlite3


"""
Notes


    TODO - create a better looking footer including one that has social media links
    TODO - create a way to write to a csv file and then empty it afterwards, the file should
           be useful in sending reports to users

    TODO - create ab absolute solution for dealing with relative and absolute file paths
           especially on Linux

    TODO - create a way for users to input specific dates possibly include it on the /testing page
    TODO - decide whether to use .csv files for returning files or json files
    

"""


"""
Ideas for functions

def export():

    q = session.query(State)

    file = './data/states.csv'

    with open(file, 'w') as csvfile:
        outcsv = csv.writer(csvfile, delimiter=',',quotechar='"', quoting = csv.QUOTE_MINIMAL)

        header = State.__table__.columns.keys()

        outcsv.writerow(header)

        for record in q.all():
            outcsv.writerow([getattr(record, c) for c in header ])
"""


def create_csv():
    """
    returns csv

    We may need to manipulate the results before returning as a __str__
    """
    file_path = get_csvfile()
    with open(file_path, newline="\n") as file:
        csv_writer = csv.writer(file, delimiter=',')
        print("WE MADE IT")

def testing():
    directory = os.path.dirname("/downloads")
    if not os.path.exists(directory):
        os.makedirs(directory)

def func(query):
    con = sqlite3.connect(get_db())
    outfile = open(get_csvfile(), 'wb')
    outcsv = csv.writer(outfile)

    for c in con.execute(str(query)):
        print(c)
# query = get_query(month='1', year='2020', organization='Global FC')
    """
    SELECT checkins.id AS checkins_id, checkins.organization AS checkins_organization,
    checkins.timestamp AS checkins_timestamp, checkins.user_id AS checkins_user_id
    FROM checkins
    WHERE checkins.organization = ? AND checkins.timestamp >= ? AND checkins.timestamp <= ?
    """

    # dump column titles (optional)
    # outcsv.writerow(x[0] for x in cursor.description)
    # dump rows
    # outcsv.writerows(cursor.fetchall())

    # outfile.close()
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
