from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from passlib.context import CryptContext

Base = declarative_base()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

association_table = Table(
    'note_tag', Base.metadata,
    Column('note_id', ForeignKey('notes.id')),
    Column('tag_id', ForeignKey('tags.id'))
)

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    created_at = Column(DateTime, default=datetime.now())

    notes = relationship('Note', back_populates='owner')

    def verify_password(self, plain_password):
        return pwd_context.verify(plain_password, self.hashed_password)

    def hash_password(self, plain_password):
        self.hashed_password = pwd_context.hash(plain_password)

class Note(Base):
    __tablename__ = 'notes'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(Text)
    created_at = Column(DateTime, default=lambda: datetime.now(), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(), onupdate=lambda: datetime.now(), nullable=False)

    tags = relationship('Tag', secondary=association_table, back_populates='notes')

    owner_id = Column(Integer, ForeignKey('users.id'))
    owner = relationship('User', back_populates='notes')

class Tag(Base):
    __tablename__ = 'tags'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, unique=True)

    notes = relationship('Note', secondary=association_table, back_populates='tags')
