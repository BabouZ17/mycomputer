# models

from datetime import Datetime
from pytz import timezone
from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship

class Memory():
    __tablename__ = 'memory'
    id = Column(Integer, primary_key=True)
    model = Column('model', String(32), unique=True)
    frequency = Column('frequency', Integer, default=2133)
    maker = Column('maker', String(20))
    created_on = Column('created_on', Datetime, default=Datetime.now(tz=timezone('America/Montreal')))


class Cpu():
    __tablename__ = 'cpu'
    id = Column(Integer, primary_key=True)
    model = Column('model', String(32), unique=True)
    frequency = Column('frequency', Float, default=2.0)
    nb_cores = Colum('nb_cores', Integer, default=1)
    maker = Column('maker', String(20))
    created_on = Column('created_on', Datetime, default=Datetime.now(tz=timezone('America/Montreal')))


class Gpu():
    __tablename__ = 'gpu'
    id = Column(Integer, primary_key=True)
    model = Column('model', String(32))
    ram = Column('ram', String(10), default=1)
    maker = Column('maker', String(20))
    created_on = Column('created_on', Datetime, default=Datetime.now(tz=timezone('America/Montreal')))


class Motherboard():
    __tablename__ = 'motherboard'
    id = Column(Integer, primary_key=True)
    model = Column('model', String(32))
    pcie_qty = Column('pcie_qty', Integer, default=1)
    sata_qty = Column('sata_qty', Integer, default=1)
    fans_qty = Column('fans_qty', Integer, default=1)
    created_on = Column('created_on', Datetime, default=Datetime.now(tz=timezone('America/Montreal')))


class HDD():
    __tablename__ = 'hdd'
    id = Column(Integer, primary_key=True)
    model = Column('model', String(32))
    maker = Column('maker', String(20))
    capacity = Column('capacity', Integer, default=1)
    created_on = Column('created_on', Datetime, default=Datetime.now(tz=timezone('America/Montreal')))


class SSD():
    __tablename__ = 'ssd'
    id = Column(Integer, primary_key=True)
    model = Column('model', String(32))
    maker = Column('model', String(20))
    capacity = Column('capacity', Integer, default=1)
    created_on = Column('created_on', Datetime, default=Datetime.now(tz=timezone('America/Montreal')))


class Computer():
    __tablename__ = 'computer'
    id = Column(Integer, primary_key=True)
    owner = Column('model', String(50))
    hdd_id = Column(Integer, ForeignKey('hdd.id'))
    hdd = relationship('HDD', back_populates='computers')
    ssd_id = Column(Integer, ForeignKey('sdd.id'))
    ssd = relationship('HDD', back_populates='computers')
    memory_id = Column(Integer, ForeignKey('memory.id'))
    memory = relationship('HDD', back_populates='computers')
    motherboard_id = Column(Integer, ForeignKey('motherboard.id'))
    motherboard = 
    cpu_id = Column(Integer, ForeignKey('cpu.id'))
    cpu = 
    gpu_id = Column(Integer, ForeignKey('gpu.id'))
    gpu =  
    created_on = Column('created_on', Datetime, default=Datetime.now(tz=timezone('America/Montreal')))