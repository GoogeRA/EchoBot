from sqlalchemy import create_engine, ForeignKey, Column, Integer, CHAR, VARCHAR, Boolean, Float, TIMESTAMP
from sqlalchemy.orm import sessionmaker, declarative_base
from config import settings


Base = declarative_base()


class DivisionType(Base):
    __tablename__ = "division_type"
    type_id = Column('id', Integer, primary_key=True)
    name = Column('name', VARCHAR)

    def __init__(self, type_id, name):
        self.type_id = type_id
        self.name = name

    def __repr__(self):
        return [self.type_id, self.name]


class MetricCalcType(Base):
    __tablename__ = "metric_calc_type"
    type_id = Column('id', Integer, primary_key=True)
    name = Column('name', VARCHAR)

    def __init__(self, type_id, name):
        self.type_id = type_id
        self.name = name

    def __repr__(self):
        return [self.type_id, self.name]


class Metric(Base):
    __tablename__ = "metric"
    metric_id = Column('id', Integer, primary_key=True)
    name = Column('name', VARCHAR)
    measure_unit = Column('unit_of_measure', VARCHAR)
    calc_type_id = Column('calc_type_id', Integer, ForeignKey("metric_calc_type.id"))
#    is_increasing = Column('is_increasing', Boolean)

    def __init__(self, m_id, name, unit, calc_type, ):
        self.metric_id = m_id
        self.name = name
        self.measure_unit = unit
        self.calc_type_id = calc_type
#       self.is_increasing = increasing

    def __repr__(self):
        return [self.metric_id, self.name, self.measure_unit, self.calc_type_id]


class MetricFact(Base):
    __tablename__ = "metric_fact"
    fact_id = Column('id', Integer, primary_key=True)
    metric_id = Column('metric_id', Integer, ForeignKey("metric.id"))
    value = Column('metric_value', Float)
    value_date = Column('value_date', TIMESTAMP)
    div_id = Column('div_id', Integer, ForeignKey("division_type.id"))
    created_at = Column('created_at', TIMESTAMP)

    def __init__(self, fact_id, metric_id, value, value_date, div_id, created_at):
        self.fact_id = fact_id
        self.metric_id = metric_id
        self.value = value
        self.value_date = value_date
        self.div_id = div_id
        self.created_at = created_at

    def __repr__(self):
        return [self.fact_id, self.name, self.metric_id, self.value, self.value_date, self.div_id, self.created_at]


class MetricPlan(Base):
    __tablename__ = "metric_plan"
    fact_id = Column('id', Integer, primary_key=True)
    metric_id = Column('metric_id', Integer, ForeignKey("metric.id"))
    value = Column('metric_value', Float)
    value_date = Column('value_date', TIMESTAMP)
    div_id = Column('div_id', Integer, ForeignKey("division_type.id"))
    created_at = Column('created_at', TIMESTAMP)
    def __init__(self, fact_id, metric_id, value, value_date, div_id, created_at):
        self.fact_id = fact_id
        self.metric_id = metric_id
        self.value = value
        self.value_date = value_date
        self.div_id = div_id
        self.created_at = created_at

    def __repr__(self):
        return [self.fact_id, self.name, self.metric_id, self.value, self.value_date, self.div_id, self.created_at]


engine = create_engine(
    url=settings.DATABASE_URL,
    echo=True
)

Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()









