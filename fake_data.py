from sqlalchemy.orm import Session

import models
import random
import os

from faker import Faker
from sqlalchemy import create_engine
from models_types import user_type

fake = Faker('ru_Ru')


def generate_users() -> list[models.Users]:
    """Генерация пользовательских данных"""

    users = []
    for i in range(50):
        first_name = fake.first_name()
        last_name = fake.last_name()
        has_pro = bool(random.randint(0, 1))
        desc = fake.text()
        country = fake.address()
        raiting = float('%2.f' % random.uniform(0, 5))
        type_ = random.choice(list(user_type))

        users.append(
            models.Users(
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


if __name__ == '__main__':
    engine = create_engine('postgresql+psycopg2://localhost/public', echo=True)
    os.system('alembic upgrade head')

    funcs = [
        generate_users
    ]

    with Session(engine) as session:
        for func in funcs:
            session.add_all(func())
        session.commit()
