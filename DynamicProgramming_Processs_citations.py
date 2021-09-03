#Now it seems to work, try it!

# IMPORT SECTION
import csv  # to read the data
import re  # to use regex
from datetime import datetime  # to compute cited years
from dateutil.relativedelta import relativedelta

# SET THE FILE FOR YOUR SAMPLE DATA
citations_file_path = '/Users/laurentfintoni/Desktop/University/COURSE DOCS/YEAR 1/Q1/COMPUTATIONAL THINKING/Project/citations_sample.csv'


# FUNCTION 1
def process_citations(citations_file_path):
    # initialize an empty list to contain data
    matrix = []
    doi_date_dict = {}
    # populate list with raw data, each row is a dictionary with the column as key, row entry as value
    with open(citations_file_path, mode='r') as file:
        csvFile = csv.DictReader(file)
        for row in csvFile:
            matrix.append(row)
            row.update([('citing_year', ''), ('cited_year', '')])

            citing_doi = row['citing']
            if citing_doi in doi_date_dict:
                row['citing_year'] = doi_date_dict[citing_doi]
            else:
                citing_date = row['creation']
                row['citing_year'] = citing_date[0:4]
                doi_date_dict[citing_doi] = row['citing_year']

            cited_doi = row['cited']
            if cited_doi in doi_date_dict:
                row['cited_year'] = doi_date_dict[cited_doi]
            else:
                timespan_str = row['timespan']
                # create a cited year key/value pair by using datetime computations
                n_creation = row['creation']
                while len(n_creation) < 10:
                    n_creation = n_creation + '-01'
                citing_n_date = datetime.strptime(n_creation, '%Y-%m-%d')
                timespan_n = (re.split('[a-zA-Z]', timespan_str, 4)[1:-1])
                a_n = int(timespan_n[0])
                delta_n = relativedelta(years=a_n)
                if len(timespan_n) == 2:
                    m_n = int(timespan_n[1])
                    delta_n = relativedelta(years=a_n, months=m_n)
                if len(timespan_n) == 3:
                    m_n = int(timespan_n[1])
                    g_n = int(timespan_n[2])
                    delta_n = relativedelta(years=a_n, months=m_n, days=g_n)
                if timespan_str[0] == "-":  # just in case there is a negative timespan
                    cited_n_date = citing_n_date + delta_n
                else:
                    cited_n_date = citing_n_date - delta_n
                cited_year = (str(cited_n_date)[0:4])
                row['cited_year'] = cited_year
    return matrix

# SET A DATA VARIABLE THAT PROCESSES THE SAMPLE
#data = process_citations(citations_file_path)
