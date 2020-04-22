import json
import requests

from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from flask_user import current_user, login_required, roles_required

from app import db
from app.models.user_models import UserProfileForm

main_blueprint = Blueprint('main', __name__, template_folder='templates')

'''
Customer-specific configuration is required for these fields:
'''
base64_encoded_username_and_password = '<add your base64-encoded username:password here>'
headers = {'Authorization': 'Basic ' + base64_encoded_username_and_password}

'''
URL parameters
'''
account_id = '<Your Bandwidth Account Number>'

'''
POST body parameters
'''
messaging_application_id = '<Your Bandwidth Messaging Application ID>'
from_phone_num = '<Your Source Telephone Number>'


# The Home page is accessible to anyone
@main_blueprint.route('/')
def home_page():
    return render_template('main/home_page.html')


@main_blueprint.route('/2fa', methods=['GET', 'POST'])
def two_factor_auth_page():
    to_phone_num = 'TODO: look up the User telephone number, or hard-code a number here for testing' 
    data = json.dumps({
        "applicationId": messaging_application_id,
        "scope": "example",
        "to": to_phone_num,
        "from": from_phone_num
    })
    requests.post(f'https://mfa.bandwidth.com/api/v1/accounts/{account_id}/code/messaging', headers=headers, data=data)
    flash('You must verify the authentication code you received. Enter it here:', 'success')
    return render_template('main/2fa_page.html')


@main_blueprint.route('/verify_2fa', methods=['GET', 'POST'])
def verify_two_factor_auth_page():
    to_phone_num = 'TODO: look up the User telephone number, or hard-code a number here for testing'
    data = json.dumps({
        "applicationId": messaging_application_id,
        "scope": "example",
        "to": to_phone_num,
        "from": from_phone_num,
        "code": request.form["two_factor_code"]
    })
    resp = requests.post(f'https://mfa.bandwidth.com/api/v1/accounts/{account_id}/code/verify', headers=headers, data=data)
    resp_dict = resp.json()
    if (resp.status_code == 200) and isinstance(resp_dict, dict) and resp_dict.get('valid'):
        return redirect(url_for('main.member_page'))
    else:
        # session.pop('_flashes', None)
        flash('That code is invalid, please try again.')
        return redirect(url_for('user.login'))


# The User page is accessible to authenticated users (users that have logged in)
@main_blueprint.route('/member')
@login_required  # Limits access to authenticated users
def member_page():
    return render_template('main/user_page.html')


# The Admin page is accessible to users with the 'admin' role
@main_blueprint.route('/admin')
@roles_required('admin')  # Limits access to users with the 'admin' role
def admin_page():
    return render_template('main/admin_page.html')


@main_blueprint.route('/main/profile', methods=['GET', 'POST'])
@login_required
def user_profile_page():

    # Initialize form
    form = UserProfileForm(request.form, obj=current_user)

    # Process valid POST
    if request.method == 'POST' and form.validate():

        # Copy form fields to user_profile fields
        form.populate_obj(current_user)

        # Save user_profile
        db.session.commit()

        # Redirect to home page
        return redirect(url_for('main.home_page'))

    # Process GET or invalid POST
    return render_template('main/user_profile_page.html', form=form)


