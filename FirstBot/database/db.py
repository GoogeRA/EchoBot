from sqlalchemy import create_engine, ForeignKey, Column, Integer, VARCHAR, Float, TIMESTAMP, Boolean
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from config import settings

from typing import Type
import datetime

Base = declarative_base()


class DivisionType(Base):
    __tablename__ = "division_type"
    # __table_args__ = {'schema': 'public'}
    type_id = Column('id', Integer, primary_key=True, nullable=False)
    name = Column('name', VARCHAR)

    def __init__(self, type_id, name):
        self.type_id = type_id
        self.name = name

    def __repr__(self):
        return f"(ID: {self.type_id}) Разрез:{self.name}"


class Division(Base):
    __tablename__ = "division"
    # __table_args__ = {'schema': 'public'}
    div_id = Column('id', Integer, primary_key=True, nullable=False)
    name = Column('name', VARCHAR)
    parent_id = Column('parent_id', Integer)
    type_id = Column('type_id', Integer, ForeignKey('division_type.id'))

    def __init__(self, div_id, name, parent_id, type_id):
        self.div_id = div_id
        self.name = name
        self.parent_id = parent_id
        self.type_id = type_id

    def __repr__(self):
        return f"(ID: {self.div_id}) {self.name}"


class MetricCalcType(Base):
    __tablename__ = "metric_calc_type"
    __table_args__ = {'schema': 'public'}
    type_id = Column('id', Integer, primary_key=True)
    name = Column('name', VARCHAR)

    def __init__(self, type_id, name):
        self.type_id = type_id
        self.name = name

    def __repr__(self):
        return f"(ID: {self.type_id} {self.name})"


class Metric(Base):
    __tablename__ = "metric"
    # __table_args__ = {'schema': 'public'}
    metric_id = Column('id', Integer, primary_key=True)
    name = Column('name', VARCHAR)
    measure_unit = Column('unit_of_measure', VARCHAR)
    calc_type_id = Column('calc_type_id', Integer, ForeignKey("metric_calc_type.id"))
    is_increasing = Column('is_increasing', Boolean)

    def __init__(self, m_id, name, unit, calc_type, increasing):
        self.metric_id = m_id
        self.name = name
        self.measure_unit = unit
        self.calc_type_id = calc_type
        self.is_increasing = increasing

    def __repr__(self):
        return f"(ID: {self.metric_id} {self.name} ед.: {self.measure_unit})"


class MetricTypes:
    class MetricFact(Base):
        __tablename__ = "metric_fact"
        # __table_args__ = {'schema': 'public'}
        fact_id = Column('id', Integer, primary_key=True)
        metric_id = Column('metric_id', Integer, ForeignKey("metric.id"))
        value = Column('metric_value', Float)
        value_date = Column('value_date', TIMESTAMP)
        div_id = Column('div_id', Integer, ForeignKey("division.id"))
        created_at = Column('created_at', TIMESTAMP)

        metric = relationship("Metric")

        def __init__(self, fact_id, metric_id, value, value_date, div_id, created_at):
            self.fact_id = fact_id
            self.metric_id = metric_id
            self.value = value
            self.value_date = value_date
            self.div_id = div_id
            self.created_at = created_at

        def __repr__(self):
            metric_name = self.metric.name if self.metric else "Unkown"
            self.value_date = self.value_date.strftime('%H:%M %d-%m-%Y')
            self.created_at = self.created_at.strftime('%H:%M %d-%m-%Y')
            return f'Значение показателя "{metric_name}": {self.value},\nНа дату: {self.value_date},\nБыл записан: {self.created_at}'


    class MetricPlan(Base):
        __tablename__ = "metric_plan"
        # __table_args__ = {'schema': 'public'}
        plan_id = Column('id', Integer, primary_key=True)
        metric_id = Column('metric_id', Integer, ForeignKey("metric.id"))
        value = Column('metric_value', Float)
        value_date = Column('value_date', TIMESTAMP)
        div_id = Column('div_id', Integer, ForeignKey("division.id"))
        created_at = Column('created_at', TIMESTAMP)

        metric = relationship('Metric')

        def __init__(self, plan_id, metric_id, value, value_date, div_id, created_at):
            self.plan_id = plan_id
            self.metric_id = metric_id
            self.value = value
            self.value_date = value_date
            self.div_id = div_id
            self.created_at = created_at

        def __repr__(self):
            metric_name = self.metric.name if self.metric else "Unkown"
            self.value_date = self.value_date.strftime('%H:%M %d-%m-%Y')
            self.created_at = self.created_at.strftime('%H:%M %d-%m-%Y')
            return f'Значение показателя "{metric_name}": {self.value},\nНа дату: {self.value_date},\nБыл записан: {self.created_at}'

    class MetricPredict(Base):
        __tablename__ = "metric_predict"
        # __table_args__ = {'schema': 'public'}
        predict_id = Column('id', Integer, primary_key=True)
        metric_id = Column('metric_id', Integer, ForeignKey("metric.id"))
        value = Column('metric_value', Float)
        value_date = Column('value_date', TIMESTAMP)
        div_id = Column('div_id', Integer, ForeignKey("division.id"))
        created_at = Column('created_at', TIMESTAMP)

        metric = relationship('Metric')

        def __init__(self, predict_id, metric_id, value, value_date, div_id, created_at):
            self.predict_id = predict_id
            self.metric_id = metric_id
            self.value = value
            self.value_date = value_date
            self.div_id = div_id
            self.created_at = created_at

        def __repr__(self):
            metric_name = self.metric.name if self.metric else "Unkown"
            self.value_date = self.value_date.strftime('%H:%M %d-%m-%Y')
            self.created_at = self.created_at.strftime('%H:%M %d-%m-%Y')
            return f'Значение показателя "{metric_name}": {self.value},\nНа дату: {self.value_date},\nБыл записан: {self.created_at}'


engine = create_engine(
    url=settings.database_url,
    echo=False
)

Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()



# metricFact = MetricTypes.MetricFact
# metricPlan = MetricTypes.MetricPlan
# metricPredict = MetricTypes.MetricPredict



def get_data(metric_type: Type[MetricTypes], index_type: str, date_calc_type: str, div_type: str,  date: datetime.date = None, date_stop: datetime.date = None):
    query = session.query(metric_type.value, metric_type.value_date, metric_type.created_at) \
        .join(Metric, metric_type.metric_id == Metric.metric_id) \
        .filter(Metric.name == index_type) \
        .filter(Metric.calc_type_id == MetricCalcType.type_id) \
        .filter(MetricCalcType.name == date_calc_type) \
        .filter(metric_type.div_id == Division.div_id) \
        .filter(Division.name == div_type)

    if date_stop:
        query = query.filter(metric_type.value_date >= date) \
            .filter(metric_type.value_date <= datetime.date(date_stop.year, date_stop.month, date_stop.day))
    elif date:
        query = query.filter(metric_type.value_date >= date) \
            .filter(metric_type.value_date <= datetime.date(date.year, date.month, date.day + 1))
    return query



# metric_type = MetricTypes.MetricFact
# metric = "Выручка"
# date_type = "На дату"
# div_type = "Проект"
# date_start = datetime.date(2020, 3, 23)
# date_stop = datetime.date(2025, 4, 29)
#
# all_metric_data = get_data(metric_type, metric, date_type, div_type, date_start, date_stop )
#
# print(all_metric_data.all())

