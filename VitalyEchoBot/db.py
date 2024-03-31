from sqlalchemy import create_engine, ForeignKey, Column, Integer, VARCHAR, Float, TIMESTAMP, Boolean
from sqlalchemy.orm import sessionmaker, declarative_base
from config import settings
import datetime

Base = declarative_base()


class DivisionType(Base):
    __tablename__ = "division_type"
    type_id = Column('id', Integer, primary_key=True, nullable=False)
    name = Column('name', VARCHAR)

    def __init__(self, type_id, name):
        self.type_id = type_id
        self.name = name

    def __repr__(self):
        return f"(ID: {self.type_id}) Разрез:{self.name}"


class Division(Base):
    __tablename__ = "division"
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
    type_id = Column('id', Integer, primary_key=True)
    name = Column('name', VARCHAR)

    def __init__(self, type_id, name):
        self.type_id = type_id
        self.name = name

    def __repr__(self):
        return f"(ID: {self.type_id} {self.name})"


class Metric(Base):
    __tablename__ = "metric"
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


class MetricFact(Base):
    __tablename__ = "metric_fact"
    fact_id = Column('id', Integer, primary_key=True)
    metric_id = Column('metric_id', Integer, ForeignKey("metric.id"))
    value = Column('metric_value', Float)
    value_date = Column('value_date', TIMESTAMP)
    div_id = Column('div_id', Integer, ForeignKey("division.id"))
    created_at = Column('created_at', TIMESTAMP)

    def __init__(self, fact_id, metric_id, value, value_date, div_id, created_at):
        self.fact_id = fact_id
        self.metric_id = metric_id
        self.value = value
        self.value_date = value_date
        self.div_id = div_id
        self.created_at = created_at

    def __repr__(self):
        return f"(ID: {self.fact_id} {self.value} {self.value_date} {self.created_at})"


class MetricPlan(Base):
    __tablename__ = "metric_plan"
    plan_id = Column('id', Integer, primary_key=True)
    metric_id = Column('metric_id', Integer, ForeignKey("metric.id"))
    value = Column('metric_value', Float)
    value_date = Column('value_date', TIMESTAMP)
    div_id = Column('div_id', Integer, ForeignKey("division.id"))
    created_at = Column('created_at', TIMESTAMP)

    def __init__(self, plan_id, metric_id, value, value_date, div_id, created_at):
        self.plan_id = plan_id
        self.metric_id = metric_id
        self.value = value
        self.value_date = value_date
        self.div_id = div_id
        self.created_at = created_at

    def __repr__(self):
        return f"(ID: {self.plan_id} {self.value} {self.value_date} {self.created_at})"


engine = create_engine(
    url=settings.database_url,
    echo=False
)

Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()

"""
div_type1 = DivisionType(1, 'Территориальная структура')
div_type2 = DivisionType(2, 'Фукнциональная структура')

div1 = Division(1, 'Регион', None, div_type1.type_id)
div2 = Division(2, 'Проект', div1.div_id, div_type1.type_id)
div3 = Division(3, 'Объект', div2.div_id, div_type1.type_id)
div4 = Division(4, 'Блок', None, div_type2.type_id)
div5 = Division(5, 'Департамент', div4.div_id, div_type2.type_id)
div6 = Division(6, 'Отдел', div5.div_id, div_type2.type_id)

metric_type1 = MetricCalcType(1, 'На дату')
metric_type2 = MetricCalcType(2, 'На конец месяца')
metric_type3 = MetricCalcType(3, 'На конец квартала')
metric_type4 = MetricCalcType(4, 'На конец года')

metric1 = Metric(1, 'Выручка', 'руб', metric_type1.type_id, increasing=True)
metric2 = Metric(2, 'Выручка', 'руб', metric_type2.type_id, increasing=True)
metric3 = Metric(3, 'Выручка', 'руб', metric_type3.type_id, increasing=True)
metric4 = Metric(4, 'Выручка', 'руб', metric_type4.type_id, increasing=True)
metric5 = Metric(5, 'Затраты', 'руб', metric_type1.type_id, increasing=False)
metric6 = Metric(6, 'Затраты', 'руб', metric_type2.type_id, increasing=False)
metric7 = Metric(7, 'Затраты', 'руб', metric_type3.type_id, increasing=False)
metric8 = Metric(8, 'Затраты', 'руб', metric_type4.type_id, increasing=False)
metric9 = Metric(9, 'Прибыль', 'руб', metric_type1.type_id, increasing=True)
metric10 = Metric(10, 'Прибыль', 'руб', metric_type2.type_id, increasing=True)
metric11 = Metric(11, 'Прибыль', 'руб', metric_type3.type_id, increasing=True)
metric12 = Metric(12, 'Прибыль', 'руб', metric_type4.type_id, increasing=True)

metric_fact1 = MetricFact(1, 1, 1000.26, datetime.datetime(2024, 3, 23, 12, 0, 0), 1, datetime.datetime(2024, 3, 23, 12, 0, 0))
metric_fact2 = MetricFact(2, 2, 2000.23, datetime.datetime(2024, 3, 31, 12, 0, 0), 1, datetime.datetime(2024, 3, 31, 12, 0, 0))
metric_fact3 = MetricFact(3, 3, 3000.54, datetime.datetime(2024, 4, 30, 12, 0, 0), 1, datetime.datetime(2024, 4, 30, 12,0, 0))
metric_fact4 = MetricFact(4, 4, 4000.12, datetime.datetime(2024, 12, 31, 12, 0, 0), 1, datetime.datetime(2024, 12, 31, 12, 0, 0))
metric_fact5 = MetricFact(5, 5, 500.12, datetime.datetime(2024, 3, 23, 12, 0, 0), 1, datetime.datetime(2024, 3, 23, 12, 0, 0))
metric_fact6 = MetricFact(6, 6, 430.47, datetime.datetime(2024, 3, 31, 12, 0, 0), 1, datetime.datetime(2024, 3, 31, 12, 0, 0))
metric_fact7 = MetricFact(7, 7, 1000.95, datetime.datetime(2024, 4, 30, 12, 0, 0), 1, datetime.datetime(2024, 4, 30, 12, 0, 0))
metric_fact8 = MetricFact(8, 8, 1100.12, datetime.datetime(2024, 12, 31, 12, 0, 0), 1, datetime.datetime(2024, 12, 31, 12, 0, 0))
metric_fact9 = MetricFact(9, 9, metric_fact1.value - metric_fact5.value, datetime.datetime(2024, 3, 23, 12, 0, 0), 1, datetime.datetime(2024, 3, 23, 12, 0, 0))
metric_fact10 = MetricFact(10, 10, metric_fact2.value - metric_fact6.value, datetime.datetime(2024, 3, 31, 12, 0, 0), 1, datetime.datetime(2024, 3, 31, 12, 0, 0))
metric_fact11 = MetricFact(11, 11, metric_fact3.value - metric_fact7.value, datetime.datetime(2024, 4, 30, 12, 0, 0), 1, datetime.datetime(2024, 4, 30, 12, 0, 0))
metric_fact12 = MetricFact(12, 12, metric_fact4.value - metric_fact8.value, datetime.datetime(2024, 12, 31, 12, 0, 0), 1, datetime.datetime(2024, 12, 31, 12, 0, 0))

metric_plan1 = MetricPlan(1, 1, 1000.26, datetime.datetime(2024, 3, 23, 12, 0, 0), 1,  datetime.datetime(2024, 3, 1, 12, 0, 0))
metric_plan2 = MetricPlan(2, 2, 2000.23, datetime.datetime(2024, 3, 31, 12, 0, 0), 1, datetime.datetime(2024, 3, 1, 12, 0, 0))
metric_plan3 = MetricPlan(3, 3, 3000.54, datetime.datetime(2024, 4, 30, 12, 0, 0), 1, datetime.datetime(2024, 1, 1, 12, 0, 0))
metric_plan4 = MetricPlan(4, 4, 4000.12, datetime.datetime(2024, 12, 31, 12, 0, 0), 1, datetime.datetime(2024, 1, 1, 12, 0, 0))
metric_plan5 = MetricPlan(5, 5, 500.12, datetime.datetime(2024, 3, 23, 12, 0, 0), 1,  datetime.datetime(2024, 3, 1, 12, 0, 0))
metric_plan6 = MetricPlan(6, 6, 430.47, datetime.datetime(2024, 3, 31, 12, 0, 0), 1, datetime.datetime(2024, 3, 1, 12, 0, 0))
metric_plan7 = MetricPlan(7, 7, 1000.95, datetime.datetime(2024, 4, 30, 12, 0, 0), 1, datetime.datetime(2024, 1, 1, 12, 0, 0))
metric_plan8 = MetricPlan(8, 8, 1100.12, datetime.datetime(2024, 12, 31, 12, 0, 0), 1, datetime.datetime(2024, 1, 1, 12, 0, 0))
metric_plan9 = MetricPlan(9, 9, metric_plan1.value - metric_plan5.value, datetime.datetime(2024, 3, 23, 12, 0, 0), 1,  datetime.datetime(2024, 3, 1, 12, 0, 0))
metric_plan10 = MetricPlan(10, 10, metric_plan2.value - metric_plan6.value, datetime.datetime(2024, 3, 31, 12, 0, 0), 1, datetime.datetime(2024, 3, 1, 12, 0, 0))
metric_plan11 = MetricPlan(11, 11, metric_plan3.value - metric_plan7.value, datetime.datetime(2024, 4, 30, 12, 0, 0), 1, datetime.datetime(2024, 1, 1, 12, 0, 0))
metric_plan12 = MetricPlan(12, 12, metric_plan4.value - metric_plan8.value, datetime.datetime(2024, 12, 31, 12, 0, 0), 1, datetime.datetime(2024, 1, 1, 12, 0, 0))

session.add_all([
    div_type1,
    div_type2,
    metric_type1,
    metric_type2,
    metric_type3,
    metric_type4
])
session.commit()


session.add_all([
    div1,
    div2,
    div3,
    div4,
    div5,
    div6,
    metric1,
    metric2,
    metric3,
    metric4,
    metric5,
    metric6,
    metric7,
    metric8,
    metric9,
    metric10,
    metric11,
    metric12
])
session.commit()

session.add_all([
    metric_fact1,
    metric_fact2,
    metric_fact3,
    metric_fact4,
    metric_fact5,
    metric_fact6,
    metric_fact7,
    metric_fact8,
    metric_fact9,
    metric_fact10,
    metric_fact11,
    metric_fact12,
    metric_plan1,
    metric_plan2,
    metric_plan3,
    metric_plan4,
    metric_plan5,
    metric_plan6,
    metric_plan7,
    metric_plan8,
    metric_plan9,
    metric_plan10,
    metric_plan11,
    metric_plan12,
])
session.commit()
"""


def get_data(metric: str, date_calc_type: str, div_type: str,  date: datetime.date = None):
    query = session.query(MetricFact) \
        .filter(MetricFact.metric_id == Metric.metric_id) \
        .filter(Metric.name == metric) \
        .filter(Metric.calc_type_id == MetricCalcType.type_id) \
        .filter(MetricCalcType.name == date_calc_type) \
        .filter(MetricFact.div_id == Division.div_id) \
        .filter(Division.name == div_type)

    if date:
        query = query.filter(MetricFact.value_date >= date)\
            .filter(MetricFact.value_date <= datetime.date(date.year, date.month, date.day + 1))

    return query

"""
metric = "Выручка"
date_type = "На дату"
div_type = "Регион"
date = datetime.date(2024, 3, 23)
data = get_data(metric, date_type, div_type)
for i in data:
    print(i)
"""
