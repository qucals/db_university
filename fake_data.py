from itertools import chain

from sqlalchemy.orm import Session

import random
import os

from faker import Faker
from sqlalchemy import create_engine, select

from models_types import *
from models import *

fake = Faker('ru_Ru')


def generate_users(a_session=None, a_count=50) -> list[Users]:
    """Генерация пользовательских данных"""

    users = []
    for i in range(a_count):
        first_name = fake.first_name()
        last_name = fake.last_name()
        has_pro = bool(random.randint(0, 1))
        desc = fake.text()
        country = fake.address()
        raiting = float('%2.f' % random.uniform(0, 5))
        type_ = random.choice(list(user_type))

        users.append(
            Users(
                first_name=first_name,
                last_name=last_name,
                has_pro=has_pro,
                description=desc,
                country=country,
                raiting=raiting,
                type=type_
            )
        )
    return users


def generate_orders(a_session, a_count=50) -> list[Orders]:
    """Генерация заказов"""

    freelancer_ids = a_session.execute(
        select(Users.id).where(Users.type == user_type.freelancer)).all()
    freelancer_ids = list(chain(*freelancer_ids))

    client_ids = a_session.execute(
        select(Users.id).where(Users.type == user_type.client)).all()
    client_ids = list(chain(*client_ids))

    orders = []
    for i in range(a_count):
        f_id = random.choice(freelancer_ids)
        c_id = random.choice(client_ids)
        begin_date = fake.date_time()
        end_date = fake.date_time()
        while end_date < begin_date:
            end_date = fake.date_time()
        deadline_in_days = (end_date - begin_date).days
        type = random.choice(list(order_type))
        status = random.choice(list(order_status))
        orders.append(
            Orders(
                id_freelancer=f_id if status != order_status.opened else None,
                id_client=c_id,
                begin_date=begin_date,
                end_date=end_date,
                deadline_in_days=deadline_in_days,
                type=type,
                status=status
            )
        )
    return orders


def generate_responds(a_session, a_count=50) -> list[OrderResponds]:
    """Генерация предложений по выполнению заказа"""

    opened_respond_ids = a_session.execute(
        select(Orders.id).where(Orders.status == order_status.opened)).all()
    opened_respond_ids = list(chain(*opened_respond_ids))

    freelancer_ids = a_session.execute(
        select(Users.id).where(Users.type == user_type.freelancer)).all()
    freelancer_ids = list(chain(*freelancer_ids))

    order_responds = []
    for i in range(a_count):
        o_id = random.choice(opened_respond_ids)
        f_id = random.choice(freelancer_ids)
        cost = random.randint(100, 10000)
        message = ''
        deadline_in_days = random.randint(1, 30)
        order_responds.append(
            OrderResponds(
                id_order=o_id,
                id_sender=f_id,
                cost=cost,
                message=message,
                deadline_in_days=deadline_in_days
            )
        )
    return order_responds


def generate_comments(a_session, a_count=50) -> list[Comments]:
    """Генерация комментариев"""

    freelancer_ids = a_session.execute(
        select(Users.id).where(Users.type == user_type.freelancer)).all()
    freelancer_ids = list(chain(*freelancer_ids))

    client_ids = a_session.execute(
        select(Users.id).where(Users.type == user_type.client)).all()
    client_ids = list(chain(*client_ids))

    comments = []
    for i in range(a_count):
        f_id = random.choice(freelancer_ids)
        c_id = random.choice(client_ids)
        comments.append(
            Comments(
                id_receiver=f_id,
                id_sender=c_id,
                mark=random.randint(0, 5)
            )
        )
        comments.append(
            Comments(
                id_receiver=c_id,
                id_sender=f_id,
                mark=random.randint(0, 5)
            )
        )
    return comments


if __name__ == '__main__':
    engine = create_engine('postgresql+psycopg2://localhost/public', echo=True)
    os.system('alembic upgrade head')

    funcs = [
        generate_users,
        generate_orders,
        generate_responds,
        generate_comments
    ]

    with Session(engine) as session:
        for func in funcs:
            session.add_all(func(session))
        session.commit()
