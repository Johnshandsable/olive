# built-in
import calendar
import csv
import datetime
import os

# needs install
from sqlalchemy import and_
from app.models import User, CheckIn


# Grabbing file path for writing to csv
# WORKS
def get_directory():
    dirname = os.path.abspath('.')
    filename = os.path.join(dirname, 'app', 'downloads')
    return filename

def get_csvfile():
    dirname = os.path.abspath('.')
    # dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, 'app', 'downloads', 'report.csv')
    return filename

def count_csvfile():
    with open(get_csvfile(), 'r') as file:
        fileReader = csv.reader(file)
        row_count = sum(1 for row in fileReader)  # fileObject is your csv.reader
        if row_count >= 1:
            truncate_csvfile()

def truncate_csvfile():
    file = open(get_csvfile(), "w")
    file.truncate()
    file.close()

# Grabbing file path for sqllite database
# WORKS
def get_db():
    dirname = os.path.abspath('.')
    filename = os.path.join(dirname, 'app', 'site.db')
    return filename

# Writes query from routes to a .csv file for downloading
# WORKS
def write_query(month, year, organization):
    outfile = open(get_csvfile(), 'a')
    fieldnames = ['client_id', 'organization', 'datetime']
    outcsv = csv.writer(outfile)
    outcsv.writerow(fieldnames)
    records = get_query(month=month, year=year, organization=organization)  # list
    [outcsv.writerow([getattr(curr, column.name) for column in CheckIn.__mapper__.columns]) for curr in records]
    outfile.close()

# Grabbing Datetime Objects
def get_month(month):
    """
    returns month string for displaying in html
    return: String
    """
    if month == 'All':
        return 'All'
    month = int(month) - 1
    months_choices = []
    for i in range(1, 13):
        months_choices.append((i, datetime.date(2008, i, 1).strftime('%B')))
    # returns the second value, otherwise the tuple would return (n, 'month')
    return months_choices[month][1]


# QUERIES
def get_query(month, year, organization, token=False):
    """
    if no organization is passed in, 'Master' is assumed. If month is passed in as
    'All', returns the checkins for the entire year.

    If token is passed in the function returns a query object rather than a list. token is assumed false otherwise.
    """
    # WORKS
    if organization == 'Master' and month == 'All' and year is not None:
        year = int(year)
        start_date = datetime.date(year, 1, 1)
        end_date = datetime.date(year, 12, 31)
        if not token:
            return CheckIn.query.filter(and_(CheckIn.timestamp >= start_date, CheckIn.timestamp <= end_date)).all()
        else:
            return CheckIn.query.filter(and_(CheckIn.timestamp >= start_date, CheckIn.timestamp <= end_date))

    # WORKS
    elif organization != 'Master' and month == 'All' and year is not None:
        year = int(year)
        start_date = datetime.date(year, 1, 1)
        end_date = datetime.date(year, 12, 31)
        if not token:
            return CheckIn.query.filter_by(organization=organization).filter(
                and_(CheckIn.timestamp >= start_date, CheckIn.timestamp <= end_date)).all()
        else:
            return CheckIn.query.filter_by(organization=organization).filter(
                and_(CheckIn.timestamp >= start_date, CheckIn.timestamp <= end_date))

    # WORKS
    elif organization == 'Master' and month is not None and year is not None:
        month = int(month)
        year = int(year)
        num_days = calendar.monthrange(year, month)[1]
        start_date = datetime.date(year, month, 1)
        end_date = datetime.date(year, month, num_days)
        if not token:
            return CheckIn.query.filter(and_(CheckIn.timestamp >= start_date, CheckIn.timestamp <= end_date)).all()
        else:
            return CheckIn.query.filter(and_(CheckIn.timestamp >= start_date, CheckIn.timestamp <= end_date))

    # WORKS
    elif organization != 'Master' and month is not None and year is not None:
        month = int(month)
        year = int(year)
        num_days = calendar.monthrange(year, month)[1]
        start_date = datetime.date(year, month, 1)
        end_date = datetime.date(year, month, num_days)
        if not token:
            return CheckIn.query.filter_by(organization=organization).filter(
                and_(CheckIn.timestamp >= start_date, CheckIn.timestamp <= end_date)).all()
        else:
            return CheckIn.query.filter_by(organization=organization).filter(
                and_(CheckIn.timestamp >= start_date, CheckIn.timestamp <= end_date))


# WORKS
def get_unique(month, year, organization):
    """
    returns number of unique users using id on the User db model
    return: Object BaseQuery
    """
    query = get_query(month=month, year=year, organization=organization, token=True)
    return query.order_by(CheckIn.user_id.desc()).all()


# WORKS
def get_last(id):
    """
    returns second-to-last result for display on forms.html
    return: Object BaseQuery
    """
    return CheckIn.query.filter_by(user_id=id).order_by(CheckIn.timestamp.desc()).offset(1).first()
