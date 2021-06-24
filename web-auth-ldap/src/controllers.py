import os
import domain
import logging
from modules import ldapauth
import json
from flask import (
    render_template,
    redirect,
    make_response,
    request,
    Flask
)


class InvalidCrendential(RuntimeError):
    pass


class EmptyCredentials(RuntimeError):
    pass


AUTH_COOKIE = os.getenv('AUTH_COOKIE', "nginxauth")


def configure_routes(app: Flask):
    @app.errorhandler(EmptyCredentials)
    def empty_credentials(e: EmptyCredentials):
        logging.debug('credentials empty', exc_info=e)
        response = make_response()
        response.set_cookie('Cache-Control', 'no-cache')
        response.status_code = 403
        return response

    @app.errorhandler(Exception)
    def invalid_credentials(e: Exception):
        logging.warning('credentials denied', exc_info=e)
        
        response = make_response()
        realm = request.headers.get('X-Ldap-Realm')

        if realm:
            response.headers['WWW-Authenticate'] = f'Basic realm="{realm}"'
        else:
            response.headers['WWW-Authenticate'] = f'Basic realm="Restricted"'

        response.set_cookie('Cache-Control', 'no-cache')
        response.status_code = 401

        return response

    @app.route("/login", methods=["GET"])
    def login_get():
        passwd_warning = request.args.get('passwd_warning')
        show_passwd_warning = True if passwd_warning == '1' else False

        header_target = request.headers.get('X-Target')

        if not header_target or 'login' in header_target:
            header_target = '/'

        return render_template(
            'auth-form.htm',
            show_passwd_warning=show_passwd_warning,
            label_auth_form_app_name=os.getenv('LABEL_AUTH_FORM_APP_NAME', 'Awesome Application'),
            label_auth_form_app_description=os.getenv('LABEL_AUTH_FORM_APP_DESCRIPTION', 'This application is awesome'),
            label_auth_form_app_footer=os.getenv('LABEL_AUTH_FORM_APP_FOOTER', 'created by @augustoliks'),
            target=header_target
        )

    @app.route("/login", methods=["POST"])
    def login_post():
        username = request.form['username']
        password = request.form['password']
        target = request.form['target']

        logging.info(f'user trying auth: {username}')

        seal_encrypted_b64 = domain.seal_auth(username, password)
        redirect_response = redirect(target, code=302)
        redirect_response.set_cookie(AUTH_COOKIE, seal_encrypted_b64, httponly=True)

        logging.debug(seal_encrypted_b64)

        return redirect_response

    @app.route("/logout", methods=["GET"])
    def logout_post():
        redirect_response = redirect('/', code=302)
        redirect_response.delete_cookie(AUTH_COOKIE)

        return redirect_response

    @app.route("/auth-sub-request", methods=["GET"])
    def auth_ldap():
        ldap_params = ldapauth.LDAPParameters(
            url=request.headers['X-Ldap-URL'],
            bind_dn=request.headers['X-Ldap-BindDN'],
            bind_passwd=request.headers['X-Ldap-BindPass'],
            base_dn=request.headers['X-Ldap-BaseDN'],
            search_filter=request.headers['X-Ldap-SearchFilter'],
            disable_referrals=request.headers['X-Ldap-DisableReferrals'],
            starttls=request.headers['X-Ldap-Starttls']
        )

        auth_cookie_name = request.headers['X-AuthCookieName']
        auth_seal = request.cookies[auth_cookie_name]

        if not auth_seal:            
            raise EmptyCredentials(f'request auth-cookie empty')

        user, password = domain.unseal_auth(auth_seal)

        if not user and not password:            
            raise EmptyCredentials(f'username and password empty')

        if not user or not password:            
            raise InvalidCrendential(f'username or password empty')

        domain.check_credentials_in_ldap_server(ldap_params, user, password)

        logging.info(f'user authenticated | user: {user}')
        
        response = make_response()
        response.status_code = 200
        response.headers['X-User'] = user

        return response


def create_app() -> Flask:
    app = Flask(
        __name__,
        template_folder='frontend/templates'
    )
    configure_routes(app)

    return app
