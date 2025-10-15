import pandas as pd


def get_indicators_NGU(data_NGU, search_parameter):
    """
    Извлекает показатели Новосибирского государственного университета из данных НГУ.

    Функция проходит по годам с 2016 по 2024 и для каждого года извлекает значение
    указанного параметра для Новосибирского государственного университета.

    Args:
        data_NGU (dict): Словарь с данными НГУ, структурированный по параметрам и годам
        search_parameter (str): Название параметра для извлечения (например, 'publications', 'citations')

    Returns:
        list: Список числовых значений показателя за период с 2016 по 2024 год включительно

    Example:
        >>> data = {
        ...     'publications': {
        ...         '2016': {'Новосибирский государственный университет': {'number': 150}},
        ...         '2017': {'Новосибирский государственный университет': {'number': 165}}
        ...     }
        ... }
        >>> get_indicators_NGU(data, 'publications')
        [150, 165]
    """
    indicators_NGU = []
    for year in range(2016, 2025):
        indicators_NGU.append(
            data_NGU[search_parameter][str(year)]['Новосибирский государственный университет']['number'])
    return indicators_NGU


def get_indicators_OpenAlex(data_OpenAlex, search_parameter):
    """
    Извлекает показатели из данных платформы OpenAlex.

    Функция проходит по годам с 2016 по 2024 и для каждого года извлекает значение
    указанного параметра из данных OpenAlex.

    Args:
        data_OpenAlex (dict): Словарь с данными OpenAlex, структурированный по параметрам и годам
        search_parameter (str): Название параметра для извлечения (например, 'publications', 'citations')

    Returns:
        list: Список числовых значений показателя за период с 2016 по 2024 год включительно

    Example:
        >>> data = {
        ...     'publications': {
        ...         '2016': 145,
        ...         '2017': 158
        ...     }
        ... }
        >>> get_indicators_OpenAlex(data, 'publications')
        [145, 158]
    """
    indicators_OpenAlex = []
    for year in range(2016, 2025):
        indicators_OpenAlex.append(data_OpenAlex[search_parameter][str(year)])
    return indicators_OpenAlex


def calc_percentage_difference(indicators_NGU, indicators_OpenAlex):
    """
    Вычисляет процентные различия между показателями НГУ и OpenAlex.

    Для каждой пары соответствующих показателей вычисляется процентное различие
    по формуле: 2 * |A - B| / (A + B) * 100%

    Особые случаи:
    - Если оба показателя равны 0, разница считается равной 0%
    - Если один из показателей равен 0, разница считается равной 100%

    Args:
        indicators_NGU (list): Список показателей из данных НГУ
        indicators_OpenAlex (list): Список показателей из данных OpenAlex

    Returns:
        list: Список процентных различий между соответствующими показателями

    Example:
        >>> calc_percentage_difference([100, 50, 0], [90, 50, 10])
        [10.526315789473683, 0.0, 100.0]
    """
    percentage_difference = []
    for i1, i2 in zip(indicators_NGU, indicators_OpenAlex):
        if (int(i1) == 0) and (int(i2) == 0):
            percentage_difference.append(0)
        elif (int(i1) == 0) or (int(i2) == 0):
            percentage_difference.append(100)
        else:
            dif = abs(int(i1) - int(i2)) / ((int(i1) + int(i2)) / 2) * 100
            percentage_difference.append(dif)

    return percentage_difference


def average_percentage_difference(percentage_difference):
    """
    Вычисляет среднее арифметическое значение процентных различий.

    Args:
        percentage_difference (list): Список процентных различий

    Returns:
        float: Среднее арифметическое значение всех процентных различий в списке

    Example:
        >>> average_percentage_difference([10.0, 20.0, 30.0])
        20.0
    """
    return sum(percentage_difference) / len(percentage_difference)


def create_resulting_table(path, list1, list2, list3, value1, list4, list5, list6, value2):
    """
    Создает и сохраняет результирующую таблицу сравнения показателей в файл Excel.

    Таблица содержит сравнение двух наборов данных (публикации и цитирования)
    между НГУ и OpenAlex за период с 2016 по 2024 год. В последней строке
    таблицы выводится средняя разница в процентах по каждому параметру.

    Args:
        path (str): Путь к файлу для сохранения результатов (в формате Excel)
        list1 (list): Показатели публикаций НГУ за 2016-2024 годы
        list2 (list): Показатели публикаций OpenAlex за 2016-2024 годы
        list3 (list): Процентные различия по публикациям за 2016-2024 годы
        value1 (float): Средняя разница по публикациям в процентах
        list4 (list): Показатели цитирований НГУ за 2016-2024 годы
        list5 (list): Показатели цитирований OpenAlex за 2016-2024 годы
        list6 (list): Процентные различия по цитированиям за 2016-2024 годы
        value2 (float): Средняя разница по цитированиям в процентах

    Returns:
        None: Функция сохраняет таблицу в файл и не возвращает значения

    Example:
        >>> create_resulting_table(
        ...     'results.xlsx',
        ...     [100, 110, 120], [95, 105, 115], [5.0, 4.5, 4.0], 4.5,
        ...     [500, 550, 600], [480, 530, 580], [4.0, 3.7, 3.3], 3.7
        ... )
    """
    years = list(range(2016, 2025))
    data = {
        'Число публикаций НГУ': list1,
        'Число публикаций OpenAlex': list2,
        'Разница 1, %': [str(n) for n in list3],
        'Число цитирований НГУ': list4,
        'Число цитирований OpenAlex': list5,
        'Разница 2, %': [str(n) for n in list6]
    }
    df = pd.DataFrame(data, index=years)

    average_dif_row = {
        'Число публикаций НГУ': None,
        'Число публикаций OpenAlex': None,
        'Разница 1, %': str(value1),
        'Число цитирований НГУ': None,
        'Число цитирований OpenAlex': None,
        'Разница 2, %': str(value2)
    }
    df.loc['Средняя разница, %'] = average_dif_row

    df.to_excel(path, index=True)
    return