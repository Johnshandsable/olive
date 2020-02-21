from flask import Blueprint, render_template, url_for, redirect, session, send_from_directory, current_app
from flask_login import login_required
from app import db
from app.posts.forms import NewForm, ExistingForm, Report, Download
from app.models import CheckIn, User
from app.utils import get_last, write_query, count_csvfile, get_directory


main = Blueprint('main', __name__)


@main.route("/", methods=['GET', 'POST'])
@main.route("/home", methods=['GET', 'POST'])
@main.route("/forms", methods=['GET', 'POST'])
@login_required
def index():
    new_form = NewForm()
    existing_form = ExistingForm()
    if "client_id" and "organization" and "timestamp" in session:
        return render_template("forms.html", new_form=new_form, existing_form=existing_form,
                               client_id=session["client_id"], organization=session["organization"],
                               timestamp=session["timestamp"], checkin=get_last(session["client_id"]))
    else:
        return render_template("forms.html", new_form=new_form, existing_form=existing_form)


@main.route("/reports", methods=['GET', 'POST'])
@login_required
def index_reports():
    report = Report()
    download = Download()
    return render_template("reports.html", report=report, download=download)


##### DOWNLOAD - FILE RETURN #####
@main.route("/return-file")
@login_required
def return_file():
    if 'month'and 'year' and 'organization' in session:
        count_csvfile()
        write_query(month=session['month'], year=session['year'],
                    organization=session['organization'])
        try:
            return send_from_directory(get_directory(), filename="report.csv", as_attachment=True)
        except FileNotFoundError:
            abort(404)
    else:
        return redirect(url_for('main.index_reports'))
