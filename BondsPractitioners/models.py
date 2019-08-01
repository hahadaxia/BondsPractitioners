# coding: utf-8
from sqlalchemy import Column, Text, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class BondsPractitionersModels(Base):
    __tablename__ = 'BondsPractitioners'

    com = Column(Text)
    dpt = Column(Text)
    job = Column(Text)
    name = Column(Text)
    duty = Column(Text)
    state = Column(Text)
    kind = Column(Text)
    phone = Column(Text)
    ldate = Column(Text)
    code = Column(Text)
    other = Column(Text)
    uptime = Column(Text)
    selno = Column(Integer, primary_key=True)


class SacModels(Base):
    __tablename__ = 'SAC'

    com = Column(Text)
    url = Column(Text)
    uptime = Column(Text)
    selno = Column(Integer, primary_key=True)
