""" database setup using sqlalchemy. """
import datetime
from sqlalchemy import create_engine, Column, String
from sqlalchemy import Integer, Text, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()


class User(Base):
    """ user table contain pass and photo link and mail"""
    __tablename__ = "user"

    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String)
    photo = Column(String)
    id = Column(Integer, primary_key=True)


class Category(Base):
    """ catalog table contain catalog names"""
    __tablename__ = "category"

    name = Column(String, nullable=False)
    id = Column(Integer, primary_key=True)

    @property
    def jsonreq(self):
        """ return json format for category table"""

        return {
            "name": self.name,
            "id": self.id
        }


class Items(Base):
    """ items table for info about every item in catalog"""
    __tablename__ = "items"

    title = Column(String, nullable=False)
    details = Column(Text, nullable=False)
    created = Column(DateTime, default=datetime.datetime.now(),
                     nullable=False)
    id = Column(Integer, primary_key=True)
    # category_name = Column(String, nullable=False)
    category_id = Column(Integer, ForeignKey("category.id"),
                         nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    user = relationship(User)
    category = relationship(Category)

    @property
    def jsonreq(self):
        """ return json format for items table"""

        return {
            "title": self.title,
            "id": self.id,
            "details": self.details
        }


engine = create_engine("sqlite:///catalog.db")
# Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)
