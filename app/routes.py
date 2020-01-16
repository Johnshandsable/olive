import json
from flask import render_template, url_for, flash, redirect, request, session, send_file, jsonify
from app import app, db
from app.forms import NewForm, ExistingForm, Report, Download
from app.funcs import get_month, get_unique, get_query, get_last, write_csv
from app.models import User, CheckIn, UserSchema, CheckInSchema


# ROUTES
@app.route("/", methods=['GET', 'POST'])
@app.route("/home", methods=['GET', 'POST'])
@app.route("/forms", methods=['GET', 'POST'])
def index():
    new_form = NewForm()
    existing_form = ExistingForm()
    if "client_id" and "organization" and "timestamp" in session:
        return render_template("forms.html", new_form=new_form, existing_form=existing_form,
                               client_id=session["client_id"], organization=session["organization"],
                               timestamp=session["timestamp"], checkin=get_last(session["client_id"]))
    else:
        return render_template("forms.html", new_form=new_form, existing_form=existing_form)


@app.route("/new", methods=['POST'])
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
        return redirect(url_for('index'))


@app.route("/existing", methods=['POST'])
def existing():
    existing_form = ExistingForm()
    if existing_form.validate_on_submit() and request.method == 'POST':
        user = CheckIn(user_id=existing_form.client_id.data,
                       organization=existing_form.organization.data)
        if user.validate_existing(user):
            # SESSION DATA
            session["client_id"] = user.user_id
            session["organization"] = user.organization
            user.checkin(user)
            session["timestamp"] = user.timestamp
            flash("Successfully checked in", 'success')
        else:
            flash("Account does not exist", 'danger')

        return redirect(url_for('index'))


@app.route("/reports", methods=['GET', 'POST'])
def index_reports():
    report = Report()
    download = Download()
    return render_template("reports.html", report=report, download=download)


@app.route("/get-reports", methods=['POST'])
def generate_reports():
    report = Report()
    download = Download()
    ##### REPORT #####
    if report.validate_on_submit() and request.method == 'POST':
        if report.month.data == '0':
            report.month.data = 'All'
        query_report = get_query(month=report.month.data, year=report.year.data, organization=report.organization.data)
        if query_report is not None:
            return render_template("reports.html", report=report, download=download, query=query_report,
                                   month=get_month(report.month.data), unique=get_unique(month=report.month.data,
                                   year=report.year.data, organization=report.organization.data),
                                   year=report.year.data)
        else:
            return redirect(url_for("index_reports"))
    else:
        return redirect(url_for("index_reports"))


@app.route("/get-downloads", methods=['POST'])
def generate_downloads():
    download = Download()
    ##### DOWNLOAD #####
    if download.validate_on_submit() and request.method == 'POST':
        if download.month.data == '0':
            download.month.data = 'All'
        query_report = get_query(month=download.month.data, year=download.year.data, organization=download.organization.data)
        if query_report is not None:
            user_schema = CheckInSchema(many=True)
            output = user_schema.dump(query_report)
            json_output = jsonify(output)
            return render_template("file_downloads.html", response=output)
        else:
            return redirect(url_for("index_reports"))
    else:
        return redirect(url_for("index_reports"))


# TESTING
@app.route("/test", methods=['GET', 'POST'])
def test():
    u = User.query.all()
    u2 = CheckIn.query.all()
    return render_template("test.html", u=u, u2=u2)


@app.route("/return-file")
def return_file():
    users = CheckIn.query.all()

    # for user in users:
    # app.logger.error(user.__dict__)

    user_schema = CheckInSchema(many=True)
    output = user_schema.dump(users)  # output is list
    json_output = jsonify(output)
    """
    with open('personal.json', 'w') as json_file:
        for user in users:
            json.dump(user.__dict__, json_file)
    """
    return render_template("file_downloads.html", response=output)
    # return jsonify(output)


# ERROR HANDLING
@app.errorhandler(404)
def not_found_error():
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error():
    db.session.rollback()
    return render_template('500.html'), 500
