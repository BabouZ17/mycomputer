# models

import json

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from datetime import datetime
from pytz import timezone
from uuid import UUID
from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta


Base = declarative_base()


class EncodableModel():
    RELATIONSHIPS_TO_DICT = False

    def __iter__(self):
        return self.to_dict().iteritems()

    def to_dict(self, rel=None, backref=None, exclude=()):
        if rel is None:
            rel = self.RELATIONSHIPS_TO_DICT
        res = {column.key: getattr(self, attr)
               for attr, column in self.__mapper__.c.items()
               if column.key not in exclude}
        if rel:
            for attr, relation in self.__mapper__.relationships.items():
                # Avoid recursive loop between to tables.
                if backref == relation.table:
                    continue
                value = getattr(self, attr)
                if value is None:
                    res[relation.key] = None
                elif isinstance(value.__class__, DeclarativeMeta):
                    res[relation.key] = value.to_dict(backref=self.__table__)
                else:
                    res[relation.key] = [i.to_dict(backref=self.__table__)
                                         for i in value]
        return res

    def to_json(self, rel=None, exclude=None):
        def extended_encoder(x):
            if isinstance(x, datetime):
                return x.isoformat()
            if isinstance(x, UUID):
                return str(x)
        if rel is None:
            rel = self.RELATIONSHIPS_TO_DICT
        return json.dumps(self.to_dict(rel, exclude=exclude),
                          default=extended_encoder)


class Owner(Base, EncodableModel):
    __tablename__ = 'owner'
    id = Column(Integer, primary_key=True)
    first_name = Column('first_name', String(32))
    last_name = Column('last_name', String(32))
    email = Column('email', String(32), unique=True)
    computers = relationship('Computer')
    created_on = Column('created_on', DateTime, default=datetime.now(
        tz=timezone('America/Montreal')))


class Memory(Base, EncodableModel):
    __tablename__ = 'memory'
    id = Column(Integer, primary_key=True)
    model = Column('model', String(32), unique=True)
    frequency = Column('frequency', Integer, default=2133)
    maker = Column('maker', String(20))
    created_on = Column('created_on', DateTime, default=datetime.now(
        tz=timezone('America/Montreal')))


class Cpu(Base, EncodableModel):
    __tablename__ = 'cpu'
    id = Column(Integer, primary_key=True)
    model = Column('model', String(32), unique=True)
    frequency = Column('frequency', Float, default=2.0)
    nb_cores = Column('nb_cores', Integer, default=1)
    maker = Column('maker', String(20))
    created_on = Column('created_on', DateTime, default=datetime.now(
        tz=timezone('America/Montreal')))


class Gpu(Base, EncodableModel):
    __tablename__ = 'gpu'
    id = Column(Integer, primary_key=True)
    model = Column('model', String(32))
    memory = Column('memory', String(10), default=1)
    maker = Column('maker', String(20))
    created_on = Column('created_on', DateTime, default=datetime.now(
        tz=timezone('America/Montreal')))


class Motherboard(Base, EncodableModel):
    __tablename__ = 'motherboard'
    id = Column(Integer, primary_key=True)
    model = Column('model', String(32))
    pcie_qty = Column('pcie_qty', Integer, default=1)
    sata_qty = Column('sata_qty', Integer, default=1)
    fans_qty = Column('fans_qty', Integer, default=1)
    created_on = Column('created_on', DateTime, default=datetime.now(
        tz=timezone('America/Montreal')))


class HDD(Base, EncodableModel):
    __tablename__ = 'hdd'
    id = Column(Integer, primary_key=True)
    model = Column('model', String(32))
    maker = Column('maker', String(20))
    capacity = Column('capacity', Integer, default=1)
    created_on = Column('created_on', DateTime, default=datetime.now(
        tz=timezone('America/Montreal')))


class SSD(Base, EncodableModel):
    __tablename__ = 'ssd'
    id = Column(Integer, primary_key=True)
    model = Column('model', String(32))
    maker = Column('maker', String(20))
    capacity = Column('capacity', Integer, default=1)
    created_on = Column('created_on', DateTime, default=datetime.now(
        tz=timezone('America/Montreal')))


# Many to Many tables
memory_association_table = Table('memory_association', Base.metadata,
                                 Column('memory_id', Integer,
                                        ForeignKey('memory.id')),
                                 Column('computer_id', Integer,
                                        ForeignKey('computer.id'))
                                 )

hdd_association_table = Table('hdd_association', Base.metadata,
                              Column('hdd_id', Integer, ForeignKey('hdd.id')),
                              Column('computer_id', Integer,
                                     ForeignKey('computer.id'))
                              )

ssd_association_table = Table('ssd_association', Base.metadata,
                              Column('ssd_id', Integer, ForeignKey('ssd.id')),
                              Column('computer_id', Integer,
                                     ForeignKey('computer.id'))
                              )

motherboard_association_table = Table('motherboard_association', Base.metadata,
                                      Column('motherboard_id', Integer,
                                             ForeignKey('motherboard.id')),
                                      Column('computer_id', Integer,
                                             ForeignKey('computer.id'))
                                      )

cpu_association_table = Table('cpu_association', Base.metadata,
                              Column('cpu_id', Integer, ForeignKey('cpu.id')),
                              Column('computer_id', Integer,
                                     ForeignKey('computer.id'))
                              )

gpu_association_table = Table('gpu_association', Base.metadata,
                              Column('gpu_id', Integer, ForeignKey('gpu.id')),
                              Column('computer_id', Integer,
                                     ForeignKey('computer.id'))
                              )


class Computer(Base, EncodableModel):
    __tablename__ = 'computer'
    id = Column(Integer, primary_key=True)
    owner = Column('model', String(50))
    owner_id = Column(Integer, ForeignKey('owner.id'))
    hdd = relationship('HDD', secondary=hdd_association_table)
    ssd = relationship('SSD', secondary=ssd_association_table)
    memory = relationship('Memory', secondary=memory_association_table)
    motherboard = relationship(
        'Motherboard', secondary=motherboard_association_table)
    cpu = relationship('Cpu', secondary=cpu_association_table)
    gpu = relationship('Gpu', secondary=gpu_association_table)
    created_on = Column('created_on', DateTime, default=datetime.now(
        tz=timezone('America/Montreal')))


engine = create_engine(
    'postgresql://babou:testing@postgres:5432/mycomputer_app')

session = sessionmaker()
session.configure(bind=engine)
Base.metadata.create_all(engine)
