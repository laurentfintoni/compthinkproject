#IMPORT SECTION
import csv #to read the data
import re #to use regex
import pprint #to make things pretty because life is beautiful 
import networkx as nx #to make graphs 
import operator #to make comparisons easier 
from datetime import datetime #to compute cited years
from dateutil.relativedelta import relativedelta

#SET THE FILE FOR YOUR SAMPLE DATA 
citations_file_path = '/Users/laurentfintoni/Desktop/University/COURSE DOCS/YEAR 1/Q1/COMPUTATIONAL THINKING/Project/citations_sample.csv'

#FUNCTION 1

def process_citations(citations_file_path):
    #initialize an empty list to contain data
    matrix = [] 
    #populate list with raw data, each row is a dictionary with the column as key, row entry as value 
    with open(citations_file_path, mode='r') as file: 
        csvFile = csv.DictReader(file)
        for row in csvFile:
            matrix.append(row)
    #iterate over the raw data to add two new key/value pairs, citing year and cited year both in YYYY formats to use for graph function and Impact Factor while retaining creation and timespan for search functions 
    for row in matrix: 
    #create a citing year key/value pair by just grabbing the first four characters of the creation field 
        citing_year = row['creation']
        row['citing_year'] = citing_year[0:4]
        timespan_str = row['timespan']
    #create a cited year key/value pair from timespan column by using datetime library 
        while len(citing_year) < 10:
            citing_year = citing_year + '-01'
        citing_n_date = datetime.strptime(citing_year, '%Y-%m-%d')
        timespan_n = (re.split('[a-zA-Z]', timespan_str, 4)[1:-1])
        if len(timespan_n) == 1:
            a_n = int(timespan_n[0])
            delta_n = relativedelta(years=a_n)
        elif len(timespan_n) == 2:
            a_n = int(timespan_n[0])
            m_n = int(timespan_n[1])
            delta_n = relativedelta(years=a_n, months=m_n)
        else:
            a_n = int(timespan_n[0])
            m_n = int(timespan_n[1])
            g_n = int(timespan_n[2])
            delta_n = relativedelta(years=a_n, months=m_n, days=g_n)
        if timespan_str[0] == "-": #just in case there is a negative timespan 
            cited_n_date = citing_n_date + delta_n
        else:
            cited_n_date = citing_n_date - delta_n
        cited_year = (str(cited_n_date)[0:4])
        row['cited_year'] = cited_year
    return matrix

#SET A DATA VARIABLE THAT PROCESSES THE SAMPLE 
data = process_citations(citations_file_path)

def do_compute_impact_factor(data, dois, year):
    #return error if year isn't a string + catch eroneous year string w/ regex
    if type(year) is not str or year == '':
        return 'The year input must be a string with four characters \U0001F645.'
    else:
        str_pattern = r'(\d{4}$)'
        match = re.fullmatch(str_pattern, year)
        if match == None:
            return 'The year must be a string with a YYYY format \U0001F913.'
    #return error if set is empty
    if len(dois) == 0:
        return 'There are no input DOIS \U0001F645.'
    #create a variable to count citations
    citations_count = 0
    #look at all dict instances in list and DOIS in input
    # enrica: store citations for dois in a subcollection
    # enrica: store doi in dois not in cited to check the year in citing
    dois_citations = []
    dois_in_cited = set()
    dois_not_in_cited = set()
    for i in dois:
        for row in data:
            #if a DOI in input and the year match in the respective columns add a count
            if i == row["cited"]:
                # enrica
                dois_citations.append(row)
                dois_in_cited.add(row["cited"])
                if year in row["creation"]:
                    citations_count +=1
    dois_not_in_cited = dois.difference(dois_in_cited)
    #return error if count is empty
    if citations_count == 0:
        return (f'For doi in "dois", there are no citations in {year} to compute the Impact Factor with \U0001F622.')
    else:
        #create a variable to count published docs
        #docs_published = 0
        #change year input to integer to create two new year variables for the preceding years, then change those back to strings for searching
        year_int = int(year)
        year_1 = str(year_int - 1)
        year_2 = str(year_int - 2)
        #same as above but this time we look for matches between DOIs in citing and cited and the years in their respective creation columns
        # enrica: I had the impression the prevoius calculation repeats too many times the +1
        '''for row in data: 
            for i in dois:       
                if i in row["citing"] and year_1 in row["citing_year"]:
                    docs_published +=1
                if i in row["citing"] and year_2 in row["citing_year"]:
                    docs_published +=1
                if i in row["cited"] and year_1 in row["cited_year"]:
                    docs_published +=1
                if i in row["cited"] and year_2 in row["cited_year"]:
                    docs_published +=1
        '''
        # enrica: create a set, so the repeated doi in data will not counted just once
        dois_2_years = set()
        for row in dois_citations:
            if row['cited_year'] == year_1 or row['cited_year'] == year_2:
                dois_2_years.add(row['cited'])
        if len(dois_not_in_cited) > 0:
            for i in dois_not_in_cited:
                for row in data:
                    if i in row["citing"] and (row['citing_year'] == year_1 or row['citing_year'] == year_2):
                        dois_2_years.add(row['citing'])
        IF_den = len(dois_2_years)
        if IF_den < 1:
            return (f'There are no doi(s) in "dois", published in the previous two years respect to {year} to compute the Impact Factor with \U0001F622.')
        else:
            IF_num = citations_count
            IF = IF_num / IF_den
            return (f'For doi in "dois", the data report a) n. {citations_count} citation(s) received in {year} and b) n. {IF_den} doi(s) published in the previous two years. The impact factor is then a/b = {IF}.')

""" test_DOISa = {'10.3390/vaccines7040201'}
test_DOIS = {'10.3390/vaccines7040201', '10.3389/fimmu.2018.02532', '10.1007/s00134-019-05862-0', '10.1016/b978-0-323-35761-6.00063-8', '10.1007/s40506-020-00219-4'}
test3 = {'10.1136/bmj.282.6276.1595', '10.1136/bmj.2.5087.24', '10.1136/bmj.c5258', '10.1177/0961203311429318','10.1542/peds.2019-1791', '10.7326/m18-2101', '10.1007/s40506-020-00219'}
test4={'10.1001/jama.2018.0708', '10.1001/jama.1990.03440120101046', '10.3390/vaccines7040201', '10.1007/s00134-019-05862-0', '10.1136/archdischild-2017-313855'} """
test_DOIS = {'10.3390/vaccines7040201', '10.3389/fimmu.2018.02532', '10.1007/s00134-019-05862-0', '10.1016/b978-0-323-35761-6.00063-8', '10.1007/s40506-020-00219-4'}
print(do_compute_impact_factor(data, test_DOIS, '2020'))