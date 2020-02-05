from flask import render_template, url_for, flash, redirect, request, session, send_from_directory
from flask_login import login_user, current_user, login_required
from app import app, db, bcrypt
from app.forms import NewForm, ExistingForm, Report, Download, LoginForm, RegistrationForm
from app.queries import get_month, get_unique, get_query, get_last, write_query, get_csvfile, truncate_csvfile, count_csvfile, get_directory
from app.models import User, UserLogin, CheckIn


# ROUTES
@app.route("/", methods=['GET', 'POST'])
@app.route("/home", methods=['GET', 'POST'])
@app.route("/forms", methods=['GET', 'POST'])
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


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = UserLogin(username=form.username.data, password=hashed_password)
        user.add_login(user)
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    login = LoginForm()
    if login.validate_on_submit():
        user_login = UserLogin.query.filter_by(username=login.username.data).first()
        if user_login and bcrypt.check_password_hash(user_login.password, login.password.data):
            login_user(user_login, remember=login.remember.data)
            return redirect(url_for('index'))
        else:
            flash('Login unsuccessful', 'danger')
    return render_template("login.html", login=login)

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
            session["client_id"] = user.user_id
            session["organization"] = user.organization
            user.checkin(user)
            session["timestamp"] = user.timestamp
            flash("Successfully checked in", 'success')
        else:
            flash("Account does not exist", 'danger')

        return redirect(url_for('index'))


@app.route("/reports", methods=['GET', 'POST'])
@login_required
def index_reports():
    report = Report()
    download = Download()
    return render_template("reports.html", report=report, download=download)

##### REPORT #####
@app.route("/get-reports", methods=['POST'])
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
            return redirect(url_for("index_reports"))
    else:
        return redirect(url_for("index_reports"))

##### DOWNLOAD #####
@app.route("/get-downloads", methods=['POST'])
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
            return redirect(url_for('return_file'))
        else:
            return redirect(url_for("index_reports"))
    else:
        return redirect(url_for("index_reports"))

##### DOWNLOAD - FILE RETURN #####
@app.route("/return-file")
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
        return redirect(url_for('index_reports'))

# BETA TESTING NEW FEATURES
@app.route("/test", methods=['GET', 'POST'])
@login_required
def test():
    u = User.query.all()
    u2 = CheckIn.query.all()
    return render_template("test.html", u=u, u2=u2)

@app.route("/search", methods=['GET', 'POST'])
@login_required
def search():
    users = User.query.all()
    return render_template("test.html", datapoints=users)


# ERROR HANDLING
@app.errorhandler(404)
def not_found_error():
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error():
    db.session.rollback()
    return render_template('500.html'), 500
