# Reference Example Application for Bandwidth Multi-Factor Authentication customers

A "reference" example application for using the Bandwidth MFA Two-Factor Authentication Service
Developers should follow this guide for configuring this example application to run,
then use this reference application as a guide for either building a new application
or modifying an existing application to leverage Bandwidth MFA for enhanced user security.

## Code characteristics

* Tested on Python 3.7
* Well organized directories with lots of comments
    * app
        * commands
        * models
        * static
        * templates
        * views
    * tests
* Includes test framework (`py.test` and `tox`)
* Includes database migration framework (`alembic`)
* Sends error emails to admins for unhandled exceptions

## Setting up a development environment

We assume that you have `git` and `venv` virtual environment manager installed.

    # Clone the code repository into ~/my_code/mfa-python-example-app
    mkdir -p ~/my_code
    cd ~/my_code
    git clone https://bandwidth.com/mfa-python-example-app.git mfa-python-example-app

    # Create the 'mfa-python-example-app' virtual environment
    cd mfa-python-example-app
    python3 -m venv .venv
    source .venv/bin/activate

    # Install the required Python packages
    pip install -r requirements.txt

# Configuring SMTP

Edit the `local_settings.py` file.

Specifically set all the MAIL_... settings to match your SMTP settings

Note that Google's SMTP server requires the configuration of "less secure apps".
See https://support.google.com/accounts/answer/6010255?hl=en

Note that Yahoo's SMTP server requires the configuration of "Allow apps that use less secure sign in".
See https://help.yahoo.com/kb/SLN27791.html

## Initializing the Database

    # Create DB tables and populate the roles and users tables
    python manage.py init_db

## Configuring the app

Find the "Customer-specific configuration" section near the top of app/views/main_views.py and set your values for:

    base64_encoded_username_and_password
    account_id
    messaging_application_id
    from_phone_num
    to_phone_num

## Running the app

    # Start the Flask development web server
    python manage.py runserver

Point your web browser to http://localhost:5000 (or http://127.0.0.1:5000 if you prefer)

You can make use of the following users:

- email `member@example.com` with password `Password1`.
- email `admin@example.com` with password `Password1`.

## Running the automated tests

    # Start the Flask development web server
    py.test tests/

## Trouble shooting

If you make changes in the Models and run into DB schema issues, delete the sqlite DB file `app.sqlite`.

## See also

* [FlaskDash](https://github.com/twintechlabs/flaskdash) is a starter app for Flask
  with [Flask-User](https://readthedocs.org/projects/flask-user/)
  and [CoreUI](https://coreui.io/) (A Bootstrap Admin Template).

## Acknowledgements

We appreciate the following Flask extensions:

* [Alembic](http://alembic.zzzcomputing.com/)
* [Flask](http://flask.pocoo.org/)
* [Flask-Login](https://flask-login.readthedocs.io/)
* [Flask-Migrate](https://flask-migrate.readthedocs.io/)
* [Flask-Script](https://flask-script.readthedocs.io/)
* [Flask-User](http://flask-user.readthedocs.io/en/v0.6/)

[Flask-User-starter-app](https://github.com/lingthio/Flask-User-starter-app) was used as a starting point for this code repository.
