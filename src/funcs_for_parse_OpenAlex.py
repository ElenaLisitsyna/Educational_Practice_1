import requests


def parse_data_OpenAlex(search_parameter):
    """
    Получает статистические данные по годам для указанного параметра из API OpenAlex.

    Функция обращается к API OpenAlex для получения информации об институте (ID: I188973947)
    и извлекает данные за последние 5 лет (исключая текущий год) для заданного параметра.

    Args:
        search_parameter (str): Название параметра для извлечения данных (например:
                              'works_count', 'cited_by_count', 'oa_works_count' и т.д.)

    Returns:
        dict: Словарь с данными в формате:
              {search_parameter: {'год1': 'значение1', 'год2': 'значение2', ...}}
              Возвращает пустой словарь {} в случае ошибки.

    Example:
        >>> data = parse_data_OpenAlex('works_count')
        >>> print(data)
        {'works_count': {'2020': '150', '2021': '180', '2022': '200'}}
    """
    url = 'https://api.openalex.org/institutions/I188973947'
    try:
        response = requests.get(url)
        data = response.json()
    except Exception as e:
        print('Error receiving data: {}'.format(e))
        return {}

    counts_by_year = data['counts_by_year']
    d = {search_parameter: {}}
    for i in range(len(counts_by_year) - 5, 0, -1):
        d[search_parameter][str(counts_by_year[i]['year'])] = str(counts_by_year[i][search_parameter])

    return d