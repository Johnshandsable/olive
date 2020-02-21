from flask import Blueprint, render_template, url_for, flash, redirect, request, session
from app.posts.forms import NewForm, ExistingForm, Report, Download
from app.models import CheckIn, User
from app.utils import get_month, get_unique, get_query

posts = Blueprint('posts', __name__)

@posts.route("/new", methods=['POST'])
def new():
    new_form = NewForm()
    if new_form.validate_on_submit() and request.method == 'POST':
        user = User(family_size=new_form.family_size.data,
                    family_name=new_form.family_name.data)
        user.validate_new(user)
        if user.validate_new(user):
            user.add_user(user)
            query_id = User.query.order_by(User.id.desc()).first()
            flash(f"Account successfully created for {query_id}", 'success')
        else:
            flash("Account may already exist", 'dark')
        return redirect(url_for('main.index'))


@posts.route("/existing", methods=['POST'])
def existing():
    existing_form = ExistingForm()
    if existing_form.validate_on_submit() and request.method == 'POST':
        user = CheckIn(user_id=existing_form.client_id.data,
                       organization=existing_form.organization.data)
        if user.validate_existing(user):
            session["client_id"] = user.user_id
            session["organization"] = user.organization
            user.checkin(user)
            session["timestamp"] = user.timestamp
            flash("Successfully checked in", 'success')
        else:
            flash("Account does not exist", 'danger')

        return redirect(url_for('main.index'))

##### REPORT #####
@posts.route("/get-reports", methods=['POST'])
def generate_reports():
    report = Report()
    download = Download()
    if report.validate_on_submit() and request.method == 'POST':
        if report.month.data == '0':
            report.month.data = 'All'
        query_report = get_query(
            month=report.month.data, year=report.year.data, organization=report.organization.data)
        if query_report is not None:
            return render_template("reports.html", report=report, download=download, query=query_report,
                                   month=get_month(report.month.data), unique=get_unique(month=report.month.data,
                                                                                         year=report.year.data, organization=report.organization.data),
                                   year=report.year.data)
        else:
            return redirect(url_for("main.index_reports"))
    else:
        return redirect(url_for("main.index_reports"))

##### DOWNLOAD #####
@posts.route("/get-downloads", methods=['POST'])
def generate_downloads():
    download = Download()
    if download.validate_on_submit() and request.method == 'POST':
        if download.month.data == '0':
            download.month.data = 'All'
        query_report = get_query(
            month=download.month.data, year=download.year.data, organization=download.organization.data)
        if query_report is not None:
            session['month'] = download.month.data
            session['year'] = download.year.data
            session['organization'] = download.organization.data
            return redirect(url_for('main.return_file'))
        else:
            return redirect(url_for("main.index_reports"))
    else:
        return redirect(url_for("main.index_reports"))
