import models

from sqlalchemy import create_engine


if __name__ == '__main__':
    engine = create_engine('postgresql+psycopg2://localhost/public', echo=True)
    models.Base.metadata.create_all(engine)

