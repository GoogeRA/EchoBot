from sqlalchemy import create_engine, ForeignKey, Column, Integer, VARCHAR, Float, TIMESTAMP, Boolean
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from config import settings

Base = declarative_base()


class Employee(Base):
    __tablename__ = "employees"
    __table_args__ = {'schema': 'authorization'}
    emp_id = Column('id', Integer, primary_key=True, nullable=False)
    full_name = Column('name', VARCHAR)
    tg_id = Column('tg_id', Integer)

    def __init__(self, emp_id, full_name, tg_id):
        self.emp_id = emp_id
        self.full_name = full_name
        self.tg_id = tg_id

    def __repr__(self):
        return f"ФИО: {self.full_name}) Тг_айди: {self.tg_id}"


engine = create_engine(
    url=settings.database_url,
    echo=False
)

Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()

# employee = Employee(1, 'Толмачев Виталий Владимирович', tg_id=None)
#
# session.add(employee)
# session.commit()

def is_authorized(tg_id: int):
    query = session.query(Employee.tg_id)
    results = query.all()

    # Extract the tg_id values from the result tuples
    tg_ids = [result[0] for result in results]
    return  tg_id in tg_ids

# print(is_authorized(1234))