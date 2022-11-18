import models_types

from sqlalchemy import Column, Integer, Boolean, VARCHAR, Float, Enum, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    first_name = Column(VARCHAR)
    last_name = Column(VARCHAR)
    has_pro = Column(Boolean)
    description = Column(VARCHAR)
    country = Column(VARCHAR)
    raiting = Column(Float)
    type = Column(Enum(models_types.user_type))

    # user_specialization = relationship('UserSpecialization')
    # order = relationship('Orders')


class UserSpecialization(Base):
    __tablename__ = 'user_specialization'

    id = Column(Integer, primary_key=True)
    id_user = Column(Integer, ForeignKey('users.id'))
    specialization = Column(Enum(models_types.specialization))


class Orders(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    id_freelancer = Column(Integer, ForeignKey('users.id'))
    id_client = Column(Integer, ForeignKey('users.id'))
    begin_date = Column(DateTime)
    end_date = Column(DateTime)
    deadline_in_days = Column(Integer)
    type = Column(Enum(models_types.order_type))
    status = Column(Enum(models_types.order_status))


class OrderResponds(Base):
    __tablename__ = 'order_responds'

    id = Column(Integer, primary_key=True)
    id_order = Column(Integer, ForeignKey('users.id'))
    id_sender = Column(Integer, ForeignKey('users.id'))
    cost = Column(Float)
    message = Column(VARCHAR)
    deadline_in_days = Column(Integer)


class OrderChats(Base):
    __tablename__ = 'order_chats'

    id = Column(Integer, primary_key=True)
    id_order = Column(Integer, ForeignKey('orders.id'))
    id_sender = Column(Integer, ForeignKey('users.id'))


class Comments(Base):
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True)
    id_receiver = Column(Integer, ForeignKey('users.id'))
    id_sender = Column(Integer, ForeignKey('users.id'))
    mark = Column(Float)


class Checks(Base):
    __tablename__ = 'checks'

    id = Column(Integer, primary_key=True)
    id_receiver = Column(Integer, ForeignKey('users.id'))
    type = Column(Enum(models_types.operation_type))
    amount = Column(Float)
