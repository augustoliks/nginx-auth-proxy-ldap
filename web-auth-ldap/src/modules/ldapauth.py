from pydantic import BaseModel
import logging
import ldap
from ldap.ldapobject import LDAPObject


class LDAPAuthException(RuntimeError):
    """exception root for LDAP auth module"""


class LDAPObjectsNotFound(LDAPAuthException):
    """user not present in LDAP"""


class LDAPObjectNotDN(LDAPAuthException):
    """matched object has no dn"""


class LDAPCredentialsIsNotValid(LDAPAuthException):
    """user and passwd is not valid"""


class LDAPParameters(BaseModel):
    """LDAP parameters

    Attrs:
        bind_passwd (str): LDAP password for the bind DN (Default: unset)
        bind_dn (str): LDAP bind DN (Default: anonymous)
        template (str): LDAP filter (Default: cn=%%(username)s)
        base_dn (str): LDAP base dn (Default: unset)
        disable_referrals (str): Sets ldap.OPT_REFERRALS to zero (Default: false)
        starttls (str): Establish a STARTTLS protected session (Default: false)
        url (str): LDAP URI to query (Default: ldap://localhost:389)
    """
    url: str
    bind_dn: str
    bind_passwd: str
    base_dn: str
    disable_referrals: str
    starttls: str
    search_filter = "sAMAccountName"


class LDAPAuthHandler:
    """Verify username/password against LDAP server"""

    def __init__(
            self,
            ldap_parameters: LDAPParameters,
            init_connection=True
    ):
        self.params = ldap_parameters
        self.ldap_conn: LDAPObject = None

        if init_connection:
            self.make_connection()

    def make_connection(self) -> None:
        """
        Python-ldap module documentation advises to always
        explicitely set the LDAP version to use after running
        initialize() and recommends using LDAPv3. (LDAPv2 is
        deprecated since 2003 as per RFC3494)

        Also, the STARTTLS extension requires the
        use of LDAPv3 (RFC2830).
        """
        ldap_obj = ldap.initialize(self.params.url)
        ldap_obj.protocol_version = ldap.VERSION3

        # Establish a STARTTLS connection if required by the headers
        if self.params.starttls == '1':
            ldap_obj.start_tls_s()

        # See https://www.python-ldap.org/en/latest/faq.html
        if self.params.disable_referrals == '1':
            ldap_obj.set_option(ldap.OPT_REFERRALS, 0)

        logging.debug('binding as search user')
        ldap_obj.bind_s(
            self.params.bind_dn,
            self.params.bind_passwd,
            ldap.AUTH_SIMPLE
        )

        self.ldap_conn = ldap_obj

    def check_credentials(self, user, password) -> None:
        logging.debug('preparing search filter')
        search_filter = f"{self.params.search_filter.format(USERNAME=user)}"
        # search_filter = f"{self.params.search_filter}={user}"

        logging.debug(
            f"searching on server '{self.params.url}' with base dn"
            f"'{self.params.base_dn}' with filter '{search_filter}'"
        )

        logging.debug('running search query')
        results = self.ldap_conn.search_s(
            base=self.params.base_dn,
            scope=ldap.SCOPE_SUBTREE,
            filterstr=search_filter,
            attrlist=['objectclass'],
            attrsonly=1
        )

        logging.debug('verifying search query results')

        if not results:
            raise LDAPObjectsNotFound('no objects found')
        else:
            user_entry = results[0]
            ldap_dn = user_entry[0]

        if len(results) > 1:
            logging.debug(
                f"filter match multiple objects: {results}, "
                f"using first, {user_entry} - {ldap_dn} "
            )
        else:
            logging.debug(f"filter match object: {user_entry} - {ldap_dn}")

        if not ldap_dn:
            raise LDAPObjectNotDN('matched object has no dn')

        try:
            logging.debug(f'attempting to bind using dn "{ldap_dn}"')
            self.ldap_conn.bind_s(
                who=ldap_dn,
                cred=password,
                method=ldap.AUTH_SIMPLE
            )
        except Exception as e:
            logging.debug(f'credentials is not valid for user: {user}', exc_info=e)
            raise LDAPCredentialsIsNotValid(f'credentials is not valid for user "{user}"')
