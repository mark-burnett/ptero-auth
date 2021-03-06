from .base import Base
from sqlalchemy import Column, ForeignKey, Integer, Text
from sqlalchemy import Table, PrimaryKeyConstraint
from sqlalchemy.orm import relationship


__all__ = ['Scope']


class Scope(Base):
    __tablename__ = 'scope'

    scope_pk = Column(Integer, primary_key=True)
    value = Column(Text, index=True, unique=True, nullable=False)


allowed_scope_table = Table('allowed_scope_bridge', Base.metadata,
    Column('client_pk', Integer, ForeignKey('confidential_client.client_pk',
        ondelete='CASCADE')),
    Column('scope_pk', Integer, ForeignKey('scope.scope_pk',
        ondelete='CASCADE')),
    PrimaryKeyConstraint('client_pk', 'scope_pk')
)


default_scope_table = Table('default_scope_bridge', Base.metadata,
    Column('client_pk', Integer, ForeignKey('confidential_client.client_pk',
        ondelete='CASCADE')),
    Column('scope_pk', Integer, ForeignKey('scope.scope_pk',
        ondelete='CASCADE')),
    PrimaryKeyConstraint('client_pk', 'scope_pk')
)


grant_scope_table = Table('grant_scope_bridge', Base.metadata,
    Column('grant_pk', Integer, ForeignKey('authorization_code_grant.grant_pk',
        ondelete='CASCADE')),
    Column('scope_pk', Integer, ForeignKey('scope.scope_pk',
        ondelete='CASCADE')),
    PrimaryKeyConstraint('grant_pk', 'scope_pk')
)

refresh_token_scope_table = Table('refresh_token_scope_bridge', Base.metadata,
    Column('refresh_token_pk', Integer,
        ForeignKey('refresh_token.refresh_token_pk', ondelete='CASCADE')),
    Column('scope_pk', Integer, ForeignKey('scope.scope_pk',
        ondelete='CASCADE')),
    PrimaryKeyConstraint('refresh_token_pk', 'scope_pk')
)
