# models

from datetime import Datetime
from pytz import timezone
from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Owner(Base):
    __tablename__ = 'owner'
    id = Column(Integer, primary_key=True)
    first_name = Column('first_name', String(32))
    last_name = Column('last_name', String(32))
    email = Column('email', String(32), unique=True)
    computers = relationship('Computer')
    created_on = Column('created_on', Datetime, default=Datetime.now(
        tz=timezone('America/Montreal')))


class Memory(Base):
    __tablename__ = 'memory'
    id = Column(Integer, primary_key=True)
    model = Column('model', String(32), unique=True)
    frequency = Column('frequency', Integer, default=2133)
    maker = Column('maker', String(20))
    created_on = Column('created_on', Datetime, default=Datetime.now(
        tz=timezone('America/Montreal')))


class Cpu(Base):
    __tablename__ = 'cpu'
    id = Column(Integer, primary_key=True)
    model = Column('model', String(32), unique=True)
    frequency = Column('frequency', Float, default=2.0)
    nb_cores = Column('nb_cores', Integer, default=1)
    maker = Column('maker', String(20))
    created_on = Column('created_on', Datetime, default=Datetime.now(
        tz=timezone('America/Montreal')))


class Gpu(Base):
    __tablename__ = 'gpu'
    id = Column(Integer, primary_key=True)
    model = Column('model', String(32))
    ram = Column('ram', String(10), default=1)
    maker = Column('maker', String(20))
    created_on = Column('created_on', Datetime, default=Datetime.now(
        tz=timezone('America/Montreal')))


class Motherboard(Base):
    __tablename__ = 'motherboard'
    id = Column(Integer, primary_key=True)
    model = Column('model', String(32))
    pcie_qty = Column('pcie_qty', Integer, default=1)
    sata_qty = Column('sata_qty', Integer, default=1)
    fans_qty = Column('fans_qty', Integer, default=1)
    created_on = Column('created_on', Datetime, default=Datetime.now(
        tz=timezone('America/Montreal')))


class HDD(Base):
    __tablename__ = 'hdd'
    id = Column(Integer, primary_key=True)
    model = Column('model', String(32))
    maker = Column('maker', String(20))
    capacity = Column('capacity', Integer, default=1)
    created_on = Column('created_on', Datetime, default=Datetime.now(
        tz=timezone('America/Montreal')))


class SSD(Base):
    __tablename__ = 'ssd'
    id = Column(Integer, primary_key=True)
    model = Column('model', String(32))
    maker = Column('model', String(20))
    capacity = Column('capacity', Integer, default=1)
    created_on = Column('created_on', Datetime, default=Datetime.now(
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


class Computer(Base):
    __tablename__ = 'computer'
    id = Column(Integer, primary_key=True)
    owner = Column('model', String(50))
    hdd_id = Column(Integer, ForeignKey('hdd.id'))
    hdd = relationship('hdds', back_populates='computers')
    ssd_id = Column(Integer, ForeignKey('sdd.id'))
    ssd = relationship('ssds', back_populates='computers')
    memory_id = Column(Integer, ForeignKey('memory.id'))
    memory = relationship('memory', back_populates='computers')
    motherboard_id = Column(Integer, ForeignKey('motherboard.id'))
    motherboard = relationship('motherboard', back_populates='computers')
    cpu_id = Column(Integer, ForeignKey('cpu.id'))
    cpu = relationship('cpus', back_populates='computers')
    gpu_id = Column(Integer, ForeignKey('gpu.id'))
    gpu = relationship('gpus', back_populates='computers')
    owner_id = Column(Integer, ForeignKey('owner.id'))
    created_on = Column('created_on', Datetime, default=Datetime.now(
        tz=timezone('America/Montreal')))
