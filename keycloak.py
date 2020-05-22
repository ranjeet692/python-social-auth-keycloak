from .oauth import BaseOAuth2


class KeycloakOAuth2(BaseOAuth2):  # pylint: disable=abstract-method

    name = 'keycloak-oauth2'

    ID_KEY = 'email'
    ACCESS_TOKEN_METHOD = 'POST'
    REDIRECT_STATE = False
    AUTHORIZATION_URL = 'http://localhost:8080/auth/realms/your-realms-name/protocol/openid-connect/auth'
    ACCESS_TOKEN_URL = 'http://localhost:8080/auth/realms/your-realms-name/protocol/openid-connect/token'
    USER_DETAILS_URL = 'http://localhost:8080/auth/realms/your-realms-name/protocol/openid-connect/userinfo'

    DEFAULT_SCOPE = [
        'openid'
    ]
    
    EXTRA_DATA = [
        ('refresh_token', 'refresh_token', True),
        ('expires_in', 'expires'),
        ('token_type', 'token_type', True)
    ]

    def authorization_url(self):
        return self.AUTHORIZATION_URL or self.setting('AUTHORIZATION_URL')

    def access_token_url(self):
        return self.ACCESS_TOKEN_URL or self.setting('ACCESS_TOKEN_URL')

    def user_details_url(self):
        return self.USER_DETAILS_URL or self.setting('USER_DETAILS_URL')
   
    def audience(self):
        return self.KEY or self.setting('KEY')

    def user_data(self, access_token, *args, **kwargs):  # pylint: disable=unused-argument
        """Loads user data from service"""
        return self.get_json(
            self.user_details_url(),
            headers={
                'Authorization': 'Bearer {}'.format(access_token),
            }
        )
                                                

    def get_user_details(self, response):
        """Map fields in user_data into Django User fields"""
        return {
            'username': response.get('email'),
            'email': response.get('email'),
            'fullname': response.get('name'),
            'first_name': response.get('given_name'),
            'last_name': response.get('family_name')
        }

    def get_user_id(self, details, response):
        """Get and associate Django User by the field indicated by ID_KEY"""
        return details.get(self.ID_KEY)
