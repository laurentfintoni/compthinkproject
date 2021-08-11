import pandas as pd
import csv
import re

""" def process_citations(citations_file_path):
    matrix = []
    with open(citations_file_path, mode='r') as file:
        csvFile = csv.DictReader(file)
        for row in csvFile:
            matrix.append(row)
        return matrix   """

def process_citations(citations_file_path):
    citationpd = pd.read_csv(citations_file_path, header=0) #header sets column names, parsedates converts to singular date format 
    return citationpd

citations_file_path = '/Users/laurentfintoni/Desktop/University/COURSE DOCS/YEAR 1/Q1/COMPUTATIONAL THINKING/Project/citations_sample.csv'
data = process_citations(citations_file_path)
print(data)

#data: the data returned by process_citations
#dois: a set of DOIs identifying articles
#year: a string in format YYYY to consider
#It returns a number which is the result of the computation of the Impact Factor (IF) for such documents.
#The IF of a set of documents dois on a year year is computed by counting the number of citations all
#the documents in dois have received in year year, and then dividing such a value by the number of
#documents in dois published in the previous two years (i.e. in year-1 and year-2)

""" def do_compute_impact_factor(data, dois, year):
    citations_count = 0
    docs_published = 0
    filtered = [data[data['cited'].isin(dois)], data[data['citing'].isin(dois)]]
    filtered_df = pd.concat(filtered).sort_values(by=['creation'])
    something = filtered_df.loc[filtered_df['creation'].dt.year == int(year)].loc[filtered_df['cited']]
    return something  """
 
def do_compute_impact_factor(data, dois, year):
    if year == int(year):
        return 'you damn fool'
    if len(dois) == 0:
        return 'still a fool'
    citations_count = 0
    for row in data:
        for i in dois:
            if i in row["cited"] and year in row["creation"]:
                citations_count +=1
    if citations_count == 0:
        return 'oopsie'
    docs_published = 0
    year_int = int(year)
    year_1 = str(year_int - 1)
    year_2 = str(year_int - 2)        
    for row in data:
        for i in dois:       
            if i in row["citing"] and year_1 in row["creation"]:
                docs_published +=1
            if i in row["citing"] and year_2 in row["creation"]:
                docs_published +=1
    if docs_published == 0:
        return 'nah bra'
    else: 
        impact_factor = citations_count / docs_published
        return citations_count, docs_published, impact_factor

test_DOIS = {'10.1016/s0140-6736(97)11096-0', '10.1097/nmc.0000000000000337', '10.3389/fmars.2018.00106', '10.1007/978-3-319-94694-8_26', '10.1080/13590840020013248'}
#print(do_compute_impact_factor(data, test_DOIS, '2010'))


#data:the data returned by process_citations
#doi1: the DOI string of the first article
#doi2: the DOI string of the second article
#It returns an integer defining how many times the two input documents are cited
#together by other documents.

""" def do_get_co_citations(data, doi1, doi2):
    citations_count = 0
    citation_dict = dict()
    for row in data:
        for doi in row["citing"].split():
            if doi not in citation_dict:
                citation_dict[doi] = []
            if doi1 and doi2 in row["cited"]:
                citation_dict[doi].append(row["cited"])
                citations_count +=1
    return citations_count, citation_dict
print(do_get_co_citations(data, '10.1016/s0140-6736(97)11096-0', '10.5993/ajhb.29.1.7')) """

#data: the data returned by process_citations
#doi1: the DOI string of the first article
#doi2: the DOI string of the first article
#It returns an integer defining how many times the two input documents cite both the same document.

#def do_get_bibliographic_coupling(data, doi1, doi2)


#data: the data returned by process_citations
#start: a string defining the starting year to consider (format: YYYY)
#end: a string defining the ending year to consider (format: YYYY) - it must be equal to or
#greater than start
#It returns a directed graph containing all the articles involved in citations if both of them
#have been published within the input start-end interval (start and end included).
#Use the DOIs of the articles involved in citations as name of the nodes.

def do_get_citation_network(data, start, end):
    timediff = [year for year in range(int(start), int(end)+1)] 
    citinglist = []
    for row in data:
        for i in timediff:
            if str(i) in row["creation"]:
                citinglist.append(row)
    number = int(end) - int(start)

    return number

#print(do_get_citation_network(data, '2018', '2020'))


#data: the data returned by process_citations
#g1: the first graph to consider
#g2: the second graph to consider
#It returns a new graph being the merge of the two input graphs if these are of the same type
#(e.g. both DiGraphs). In case the types of the graphs are different, return None.

#def do_merge_graphs(data, g1, g2)

#data: the data returned by process_citations or by other search/filter activities
#prefix: a string defining the precise prefix (i.e. the part before the first slash) of a DOI
#is_citing: a boolean telling if the operation should be run on citing articles or not
#It returns a sub-collection of citations in data where either the citing DOI (if is_citing is True)
#or the cited DOI (if is_citing is False) is characterised by the input prefix.

def do_search_by_prefix(data, prefix, is_citing):
    if type(prefix) is not str: 
        return 'oopsie'
    if type(is_citing) is not bool:
        return 'oooooopsie'
    result = []
    if is_citing:
        col = 'citing'
    else:
        col = 'cited'
    for row in data:
        if prefix in row[col]:
            result.append(row)
    return result

#print(do_search_by_prefix(data, '10.1177', True))




#data: the data returned by process_citations or by other search/filter activities
#query: a string defining the query to do on the data
#field: a string defining the column (it can be either citing, cited, creation, timespan)
#on which running the query
#It returns a sub-collection of citations in data where the query matched on the input field.
#It is possible to use wildcards in the query. If no wildcards are used, there should be a
#complete match with the string in query to return that citation in the results.
#Multiple wildcards * can be used in query. E.g. World*Web looks for all the strings that
#matches with the word World followed by zero or more characters, followed by the word Web
#(examples: World Wide Web, World Spider Web, etc.).
#Boolean operators can be used: and, or, not
#<tokens 1> <operator> <tokens 2>
#All matches are case insensitive – e.g. specifying World as query will match also strings
#that contain world

#def do_search(data, query, field)

#data: the data returned by process_citations or by other search/filter activities
#query: a string defining the query to do on the data
#field: a string defining column (it can be either citing, cited, creation, timespan) on
#which running the query
#It returns a sub-collection of citations in data where the query matched on the input field.
#No wildcarts are permitted in the query, only comparisons.
#Comparison operator can be used in query: <, >, <=, >=, ==, !=
#<operator> <tokens>
#Boolean operators can be used: and, or, not
#<tokens 1> <operator> <tokens 2>
#All matches are case insensitive – e.g. specifying World as query will match also strings
#that contain world

#def do_filter_by_value(data, query, field) 