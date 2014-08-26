from ..base import Base
from ..util import generate_id
from sqlalchemy import Boolean, Column, DateTime, Integer, Text
from sqlalchemy.orm import relationship
import datetime
import re


__all__ = ['Client', 'ConfidentialClient', 'PublicClient']


class Client(Base):
    __tablename__ = 'client'
    __mapper_args__ = {
        'polymorphic_on': 'client_type',
    }

    client_pk = Column(Integer, primary_key=True)
    client_id = Column(Text, index=True, unique=True, nullable=False,
            default=lambda: generate_id('ci'))
    client_name = Column(Text, index=True)
    client_type = Column(Text, index=True, nullable=False)

    active = Column(Boolean, index=True, default=True)
    created_at = Column(DateTime(timezone=True), index=True, nullable=False,
            default=datetime.datetime.utcnow())
    deactivated_at = Column(DateTime(timezone=True), index=True)

    redirect_uri_regex = Column(Text, nullable=False)

    valid_scopes = Column(Text, nullable=False)

    def authenticate(self, client_id, client_secret=None):
        return NotImplemented

    def is_valid_redirect_uri(self, redirect_uri):
        return re.match(self.redirect_uri_regex, redirect_uri)

    def is_valid_scope_set(self, scope_set):
        return scope_set.issubset(self.valid_scope_set)

    @property
    def valid_scope_set(self):
        return set(self.valid_scopes.split(' '))


class ConfidentialClient(Client):
    __mapper_args__ = {
        'polymorphic_identity': 'confidential',
    }

    client_secret = Column(Text, default=lambda: generate_id('cs'))

    def authenticate(self, client_id, client_secret=None):
        return (self.active
                and self.client_id == client_id
                and self.client_secret == client_secret)

    _VALID_GRANT_TYPES = set([
        'authorization_code',
        'client_credentials',
        'refresh_token',
    ])
    def is_valid_grant_type(self, grant_type):
        return grant_type in self._VALID_GRANT_TYPES

    def is_valid_response_type(self, response_type):
        return response_type == 'code'


class PublicClient(Client):
    __mapper_args__ = {
        'polymorphic_identity': 'public',
    }

    def authenticate(self, client_id, client_secret=None):
        return self.active

    def is_valid_grant_type(self, grant_type):
        # XXX This should probably raise an exception.
        return False

    _VALID_RESPONSE_TYPES = set([
        'token',
        'id_token token',
        'token id_token',
    ])
    def is_valid_response_type(self, response_type):
        return response_type in self._VALID_RESPONSE_TYPES
