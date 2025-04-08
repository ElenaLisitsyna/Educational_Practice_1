import random
from datetime import datetime
from funcs_for_parse_NGU import *
from funcs_for_parse_OpenAlex import *
from funcs_for_compare import *

#print('Please enter the path to the chromedriver:')
#path_to_driver = input()
path_to_driver = 'C:/chromedriver/chromedriver.exe'
driver = driver_setup(path_to_driver)

data_dicts_scopus_NGU = []
data_dicts_citations_NGU = []
for year in range(2016, 2025):
    data_dicts_scopus_NGU.append(parse_data_NGU(year, driver, 'scopus'))
    data_dicts_citations_NGU.append(parse_data_NGU(year, driver, 'citations'))
    print(str(year) + ' year parsed.')
    time.sleep(random.uniform(1, 3))
driver.quit()

data_scopus_NGU = merge_dicts(data_dicts_scopus_NGU, 'scopus')
data_citations_NGU = merge_dicts(data_dicts_citations_NGU, 'citations')

data_works_count_OpenAlex = parse_data_OpenAlex('works_count')
data_cited_by_count_OpenAlex = parse_data_OpenAlex('cited_by_count')

indicators_scopus_NGU = get_indicators_NGU(data_scopus_NGU, 'scopus')
indicators_citations_NGU = get_indicators_NGU(data_citations_NGU, 'citations')

indicators_works_count_OpenAlex = get_indicators_OpenAlex(data_works_count_OpenAlex, 'works_count')
indicators_cited_by_count_OpenAlex = get_indicators_OpenAlex(data_cited_by_count_OpenAlex, 'cited_by_count')

percentage_difference_publications = calc_percentage_difference(indicators_scopus_NGU, indicators_works_count_OpenAlex)
percentage_difference_citations = calc_percentage_difference(indicators_citations_NGU, indicators_cited_by_count_OpenAlex)

average_percentage_difference_publications = average_percentage_difference(percentage_difference_publications)
average_percentage_difference_citations = average_percentage_difference(percentage_difference_citations)


print('Please enter the path to the directory where the resulting table will be saved:')
name_of_dir = input()
path = name_of_dir.strip() + '/compare_' + ((datetime.today()).isoformat()).replace(':', '-') + '.xlsx'
create_resulting_table(path, indicators_scopus_NGU, indicators_works_count_OpenAlex, percentage_difference_publications,
                       average_percentage_difference_publications, indicators_citations_NGU, indicators_cited_by_count_OpenAlex,
                       percentage_difference_citations, average_percentage_difference_citations)