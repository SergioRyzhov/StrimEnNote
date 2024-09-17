from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

association_table = Table(
    'note_tag', Base.metadata,
    Column('note_id', ForeignKey('notes.id')),
    Column('tag_id', ForeignKey('tags.id'))
)

class Note(Base):
    __tablename__ = 'notes'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(Text)
    created_at = Column(DateTime, default=lambda: datetime.now(), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(), onupdate=lambda: datetime.now(), nullable=False)

    tags = relationship('Tag', secondary=association_table, back_populates='notes')

class Tag(Base):
    __tablename__ = 'tags'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, unique=True)

    notes = relationship('Note', secondary=association_table, back_populates='tags')
