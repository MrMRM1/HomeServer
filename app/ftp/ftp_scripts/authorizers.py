from hashlib import sha256

from pyftpdlib.authorizers import DummyAuthorizer, AuthenticationFailed


class DummySha256Authorizer(DummyAuthorizer):

    def validate_authentication(self, username, password, handler):
        hash_password = sha256(password.encode()).hexdigest()
        try:
            if username != 'anonymous' and self.user_table[username]['pwd'] != hash_password:
                raise KeyError
        except KeyError:
            raise AuthenticationFailed
