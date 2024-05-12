from EchoBot.FirstBot.database.db import MetricTypes


metric_type_mapping = {
    MetricTypes.MetricFact: "Фактические значения показателя:",
    MetricTypes.MetricPlan: "Плановые значения показателя:",
    MetricTypes.MetricPredict: "Прогнозные значения показателя:"
}
index_mapping = {
    'Выручка': 'Выручка',
    'Затраты': 'Затраты',
    'Прибыль': 'Прибыль'
}

date_type_mapping = {
    'На дату': {'nominative': 'на дату', 'prepositional': 'на дату'},
    'На конец месяца': {'nominative': 'на конец месяца', 'prepositional': 'на конец месяца'},
    'На конец квартала': {'nominative': 'на конец квартала', 'prepositional': 'на конец квартала'},
    'На конец года': {'nominative': 'на конец года', 'prepositional': 'на конец года'}
}

division_mapping = {
    'Регион': {'nominative': 'регион', 'prepositional': 'по региону'},
    'Проект': {'nominative': 'проект', 'prepositional': 'по проекту'},
    'Объект': {'nominative': 'объект', 'prepositional': 'по объекту'}
}

def metric_mapping(metric: MetricTypes):
    result = ''.join(metric_type_mapping.get(metric, ''))
    return  result

# request = MetricTypes.MetricFact
# print(metric_mapping(request))

def generate_result_string(request_dict):
    result_parts = []

    if 'index_type' in request_dict:
        index_type = request_dict['index_type']
        if index_type in index_mapping:
            result_parts.append(index_mapping[index_type])

    if 'date_type' in request_dict:
        date_type = request_dict['date_type']
        if date_type in date_type_mapping:
            case_forms = date_type_mapping[date_type]
            result_parts.append(case_forms.get('nominative', ''))

    if 'date' in request_dict and request_dict['date']:
        date = request_dict['date']
        if 'date_stop' in request_dict and request_dict['date_stop']:
            result_parts.append(f"с даты '{date.strftime('%d-%m-%Y')}' по дату '{request_dict['date_stop'].strftime('%d-%m-%Y')}'")
        else:
            result_parts.append(f"на дату '{date.strftime('%d-%m-%Y')}'")

    if 'div_type' in request_dict:
        div_type = request_dict['div_type']
        if div_type in division_mapping:
            case_forms = division_mapping[div_type]
            result_parts.append(case_forms.get('prepositional', ''))

    result_string = ' '.join(result_parts)
    return result_string

# request1 =  {
#     'index_type': 'Выручка',
#     'date_type': 'На дату',
#     'date': 'hh:mm dd-mm-yyyy',
#     'div_type': 'Регион'
# }
#
# request2 =  {
#     'index_type': 'Выручка',
#     'date_type': 'На дату',
#     'date': 'hh:mm dd-mm-yyyy',
#     'date_stop': 'hh:mm dd-mm-yyyy',
#     'div_type': 'Регион'
# }
#
# result_line1 = generate_result_string(request1)
# result_line2 = generate_result_string(request2)
# print(result_line1)
# print(result_line2)
