import random
from datetime import datetime
from funcs_for_parse_NGU import *
from funcs_for_parse_OpenAlex import *
from funcs_for_compare import *


def main():
    """
    Основная функция для сравнения библиометрических показателей НГУ из разных источников.

    Функция выполняет полный цикл сбора и анализа данных:
    1. Парсит данные Scopus и цитирования с сайта НГУ за 2016-2024 годы
    2. Получает данные о публикациях и цитированиях из API OpenAlex
    3. Вычисляет показатели и сравнивает данные из разных источников
    4. Сохраняет результаты в Excel-файл

    Workflow:
    - Запрашивает путь к ChromeDriver
    - Парсит данные НГУ с веб-сайта
    - Получает данные из OpenAlex API
    - Сравнивает показатели и вычисляет разницу в процентах
    - Сохраняет итоговую таблицу с результатами сравнения

    Returns:
        None
    """
    print('Please enter the path to the chromedriver:')
    path_to_driver = input()
    driver = driver_setup(path_to_driver)

    # Парсинг данных с сайта НГУ
    data_dicts_scopus_NGU = []
    data_dicts_citations_NGU = []
    for year in range(2016, 2025):
        data_dicts_scopus_NGU.append(parse_data_NGU(year, driver, 'scopus'))
        data_dicts_citations_NGU.append(parse_data_NGU(year, driver, 'citations'))
        print(str(year) + ' year parsed.')
        time.sleep(random.uniform(1, 3))
    driver.quit()

    # Обработка данных НГУ
    data_scopus_NGU = merge_dicts(data_dicts_scopus_NGU, 'scopus')
    data_citations_NGU = merge_dicts(data_dicts_citations_NGU, 'citations')

    # Получение данных из OpenAlex
    data_works_count_OpenAlex = parse_data_OpenAlex('works_count')
    data_cited_by_count_OpenAlex = parse_data_OpenAlex('cited_by_count')

    # Расчет показателей
    indicators_scopus_NGU = get_indicators_NGU(data_scopus_NGU, 'scopus')
    indicators_citations_NGU = get_indicators_NGU(data_citations_NGU, 'citations')

    indicators_works_count_OpenAlex = get_indicators_OpenAlex(data_works_count_OpenAlex, 'works_count')
    indicators_cited_by_count_OpenAlex = get_indicators_OpenAlex(data_cited_by_count_OpenAlex, 'cited_by_count')

    # Сравнение показателей
    percentage_difference_publications = calc_percentage_difference(indicators_scopus_NGU,
                                                                    indicators_works_count_OpenAlex)
    percentage_difference_citations = calc_percentage_difference(indicators_citations_NGU,
                                                                 indicators_cited_by_count_OpenAlex)

    average_percentage_difference_publications = average_percentage_difference(percentage_difference_publications)
    average_percentage_difference_citations = average_percentage_difference(percentage_difference_citations)

    # Сохранение результатов
    print('Please enter the path to the directory where the resulting table will be saved:')
    name_of_dir = input()
    path = name_of_dir.strip() + '/compare_' + ((datetime.today()).isoformat()).replace(':', '-') + '.xlsx'
    create_resulting_table(path, indicators_scopus_NGU, indicators_works_count_OpenAlex,
                           percentage_difference_publications,
                           average_percentage_difference_publications, indicators_citations_NGU,
                           indicators_cited_by_count_OpenAlex,
                           percentage_difference_citations, average_percentage_difference_citations)


if __name__ == "__main__":
    main()