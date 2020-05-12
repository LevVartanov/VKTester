import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session
import sqlalchemy.ext.declarative as dec
import Models

SqlAlchemyBase = dec.declarative_base()

def init_connection(db_file):
    if not db_file or not db_file.strip():
        raise Exception("Необходимо указать файл базы данных.")

    conn_str = f'sqlite:///{db_file.strip()}?check_same_thread=False'
    print(f"Подключение к базе данных по адресу {conn_str}")

    engine = sa.create_engine(conn_str, echo=False)
    factory = orm.sessionmaker(bind=engine)

    SqlAlchemyBase.metadata.create_all(engine)
    return factory


def create_session(factory) -> Session:
    return factory()

