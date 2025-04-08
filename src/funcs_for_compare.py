import pandas as pd


def get_indicators_NGU(data_NGU, search_parameter):
    indicators_NGU = []
    for year in range(2016, 2025):
        indicators_NGU.append(data_NGU[search_parameter][str(year)]['Новосибирский государственный университет']['number'])
    return indicators_NGU


def get_indicators_OpenAlex(data_OpenAlex, search_parameter):
    indicators_OpenAlex = []
    for year in range(2016, 2025):
        indicators_OpenAlex.append(data_OpenAlex[search_parameter][str(year)])
    return indicators_OpenAlex


def calc_percentage_difference(indicators_NGU, indicators_OpenAlex):
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
    return sum(percentage_difference) / len(percentage_difference)


def create_resulting_table(path, list1, list2, list3, value1, list4, list5, list6, value2):
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
