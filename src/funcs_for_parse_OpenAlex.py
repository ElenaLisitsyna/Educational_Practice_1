import requests


def parse_data_OpenAlex(search_parameter):
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