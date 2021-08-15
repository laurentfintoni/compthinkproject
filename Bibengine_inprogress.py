#IMPORT SECTION

import pandas as pd
import csv
import re
import pprint #to make things pretty because life is beautiful 

#SET THE FILE FOR YOUR SAMPLE DATA 
citations_file_path = '/Users/laurentfintoni/Desktop/University/COURSE DOCS/YEAR 1/Q1/COMPUTATIONAL THINKING/Project/citations_sample.csv'

#FUNCTION 1 PROCESS CITATIONS: 2 OPTIONS, ONE W/ CSV + DICT, ONE WITH PANDAS, COMMENT OUT THE ONE YOU DONT WANT TO USE OTHERWISE IT WILL BREAK BECAUSE THEY HAVE SAME NAME 

#Dictionary version
def process_citations(citations_file_path):
    matrix = []
    with open(citations_file_path, mode='r') as file:
        csvFile = csv.DictReader(file)
        for row in csvFile:
            matrix.append(row)
        return matrix 

""" #Pandas version w/ parse-dates
def process_citations(citations_file_path):
    citationpd = pd.read_csv(citations_file_path, header=0, parse_dates=['creation']) #header sets column names, parsedates converts to singular date format 
    return citationpd """

#SET A DATA VARIABLE THAT PROCESSES THE SAMPLE 
data = process_citations(citations_file_path)

#ANCILLARY FUNCTION TO MANAGE DATE AND TIMESPAN:

"""#This is an Enrica woring version of functions to transform "creation string" in a normalized datetime object and compute differences between date and timedelta:
#already able to manage YYYY-MM-DD, YYYY or YYYY-MM creation strings
#already completed with corret parsing of ISO duration from 'P0Y5M15D' to (years=0, months=5, days=15): maybe possible to do it more elegant without repetition.
#I used pasing in y, m and d beacuse it was easier for me than transform on the overall days
#You find a lot of print function to see intermediated steps
"""
import re
from datetime import datetime
from dateutil.relativedelta import relativedelta

def get_cited_date(created, timespan):
    while len(created) < 10:
        created = created + '-01'
    print(created)
    citing_n_date = datetime.strptime(created, '%Y-%m-%d')
    print(citing_n_date)
    timespan_n = (re.split('[a-zA-Z]', timespan, 4)[1:-1])
    print(timespan_n)
    if len(timespan_n) == 1:
        a_n = int(timespan_n[0])
        delta_n = relativedelta(years=a_n)
    if len(timespan_n) == 2:
        a_n = int(timespan_n[0])
        m_n = int(timespan_n[1])
        delta_n = relativedelta(years=a_n, months=m_n)
    if len(timespan_n) == 3:
        a_n = int(timespan_n[0])
        m_n = int(timespan_n[1])
        g_n = int(timespan_n[2])
        print(a_n, m_n, g_n)
        delta_n = relativedelta(years=a_n, months=m_n, days=g_n)
    print(delta_n)
    cited_n_date = citing_n_date - delta_n
    print(cited_n_date)
    cited_year = (str(cited_n_date)[0:4])
    return cited_year

creation1='2020'
timespan1 = 'P1Y10M15D'
print(get_cited_date(creation1, timespan1))

'''
#Enrica: we can complete the extraction of both citing and cited year and transform them in integer for other purposes when required, with a dynamic programming that stores year YYYY string for each doi in a dictionary
#This is a really preliminary, not-tested draft, about what I think, we can recall the compilation of dictionary every time we need it and find the years values already stored there

def doi_dates(data, doi, doi_date_dict):
    doi_date_dict = {}
    if doi in solution_dict:
        return doi_date_dict[doi]
    else:
        doi_in_citing = do_filter_by_value(data, doi, 'citing_doi')
        if len(doi_in_citing) > 0:
            doi_date_dict[doi] = ((doi_in_citing['created'])[0:4])
            print(doi_date_dict)
            return = doi_date_dict[doi]
        else:
            doi_in_cited = do_filter_by_value(data, doi, 'cited_doi')
            created = doi_in_cited[0['created']]
            timespan = doi_in_cited[0['timespan']]
            cited_year = get_cited_date(created, timespan)
            doi_date_dict[doi] = ((cited_year)
            return = doi_date_dict[doi]
'''

#FUNCTION 2 

#data: the data returned by process_citations
#dois: a set of DOIs identifying articles
#year: a string in format YYYY to consider
#It returns a number which is the result of the computation of the Impact Factor (IF) for such documents.
#The IF of a set of documents dois on a year year is computed by counting the number of citations all
#the documents in dois have received in year year, and then dividing such a value by the number of
#documents in dois published in the previous two years (i.e. in year-1 and year-2)"""

#This is an unfinished Pandas version

""" def do_compute_impact_factor(data, dois, year):
    citations_count = 0
    docs_published = 0
    filtered = [data[data['cited'].isin(dois)], data[data['citing'].isin(dois)]]
    filtered_df = pd.concat(filtered).sort_values(by=['creation'])
    something = filtered_df.loc[filtered_df['creation'].dt.year == int(year)].loc[filtered_df['cited']]
    return something  """
 
#This is a working dictionary version 

def do_compute_impact_factor(data, dois, year):
    if type(year) is not str: #return error if year isn't a string 
        return 'The year input must be a string \U0001F645.' 
    if len(dois) == 0: #return error if set is empty 
        return 'There are no input DOIS \U0001F645.'
    citations_count = 0 #create a variable to count citations 
    for row in data: #look at all dict instances in list 
        for i in dois: #look at the DOIS in input 
            if i in row["cited"] and year in row["creation"]: #if a DOI in input and the year match in the respective columns add a count
                citations_count +=1
    if citations_count == 0: #return error if counts are empty  
        return 'Looks like there are no citations \U0001F622.'
    docs_published = 0 #create a variable to count published docs 
    year_int = int(year) #change the year input to an integer so we can change it 
    year_1 = str(year_int - 1) #change the year integer back into a string minus 1 and 2 
    year_2 = str(year_int - 2)        
    for row in data: #same as above but this time we look for matches in other columns 
        for i in dois:       
            if i in row["citing"] and year_1 in row["creation"]:
                docs_published +=1
            if i in row["citing"] and year_2 in row["creation"]:
                docs_published +=1
    if docs_published == 0: #return error if counts are empty, also avoid ZeroDivisionError 
        return 'Looks like there are no published documents in previous two years to compute IF with \U0001F622.'
    else: 
        impact_factor = citations_count / docs_published #Do the thing! 
        return (f'There were {citations_count} citations for all dois in {year}, {docs_published} documents published in the previous two years, and the impact factor is {impact_factor}.') #use formatted string literal to make the result pretty 

#A variable with a set of test DOIS for impact factor 
test_DOIS = {'10.1016/s0140-6736(97)11096-0', '10.1097/nmc.0000000000000337', '10.3389/fmars.2018.00106', '10.1007/978-3-319-94694-8_26', '10.1080/13590840020013248'}

#You can uncomment this print call and change the years and see the results (works for 2018, 19, 20)
#print(do_compute_impact_factor(data, test_DOIS, 2010))

#FUNCTION 3 (ENRICA)

#data:the data returned by process_citations
#doi1: the DOI string of the first article
#doi2: the DOI string of the second article
#It returns an integer defining how many times the two input documents are cited together by other documents.

#This is an unfinished version Laurent started working on, we can delete later but keeping in case it's useful, it's like half the function 
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

#This is an Enrica woking dictionary version using do_filter_by_value function:
def do_get_co_citations(data, doi1, doi2):
    doi1sublist = do_filter_by_value(data, doi1, 'cited')
    doi2sublist = do_filter_by_value(data, doi2, 'cited')
    co_citations = 0
    for doiA in doi1sublist:
        for doiB in doi2sublist:
            if doiA['citing'] == doiB['citing']:
                co_citations += 1
    return co_citations    # It returns an integer defining how many times the two input documents are cited together by other documents.

#FUNCTION 4 (ENRICA)

#data: the data returned by process_citations
#doi1: the DOI string of the first article
#doi2: the DOI string of the first article
#It returns an integer defining how many times the two input documents cite both the same document.

#def do_get_bibliographic_coupling(data, doi1, doi2)
#This is an Enrica working dictionaryversion using do_filter_by_value function; 
#maybe it could be more economic for the code (?) writing just one different function to be recalled with the different value of cited VS citing:

def do_get_bibliographic_coupling(data, doi1, doi2):
    doi1sublist = do_filter_by_value(data, doi1, 'citing')
    doi2sublist = do_filter_by_value(data, doi2, 'citing')
    bibliographic_coupling = 0
    for doiA in doi1sublist:
        for doiB in doi2sublist:
            if doiA['cited'] == doiB['cited']:
                bibliographic_coupling += 1
    return bibliographic_coupling

#FUNCTION 5 (CAMILLA)

#data: the data returned by process_citations
#start: a string defining the starting year to consider (format: YYYY)
#end: a string defining the ending year to consider (format: YYYY) - it must be equal to or
#greater than start
#It returns a directed graph containing all the articles involved in citations if both of them
#have been published within the input start-end interval (start and end included).
#Use the DOIs of the articles involved in citations as name of the nodes.

#This is a test I did today to return the citing DOIS using dictionary, if you wanna use it 

""" def do_get_citation_network(data, start, end):
    timediff = [year for year in range(int(start), int(end)+1)] 
    citinglist = []
    for row in data:
        for i in timediff:
            if str(i) in row["creation"]:
                citinglist.append(row)
    number = int(end) - int(start)

    return number

print(do_get_citation_network(data, '2018', '2020')) """


#FUNCTION 6 (CAMILLA)

#data: the data returned by process_citations
#g1: the first graph to consider
#g2: the second graph to consider
#It returns a new graph being the merge of the two input graphs if these are of the same type
#(e.g. both DiGraphs). In case the types of the graphs are different, return None.

#def do_merge_graphs(data, g1, g2)

#FUNCTION 7 (LAURENT)

#data: the data returned by process_citations or by other search/filter activities
#prefix: a string defining the precise prefix (i.e. the part before the first slash) of a DOI
#is_citing: a boolean telling if the operation should be run on citing articles or not
#It returns a sub-collection of citations in data where either the citing DOI (if is_citing is True)
#or the cited DOI (if is_citing is False) is characterised by the input prefix.

#This is a working version w/ dictionary, needs: constrain string input to 2 numbers, dot, 4 numbers using regex 

def do_search_by_prefix(data, prefix, is_citing):
    if type(prefix) is not str: #return error is prefix is not a string 
        return 'The prefix must be a string \U0001F913.'
    if type(is_citing) is not bool: #return error is citing option is not boolean 
        return 'We need a boolean option \U0001F913.'
    result = [] #create an empty list for the results 
    if is_citing: #select the column to do search on based on boolean input 
        col = 'citing'
    else:
        col = 'cited'
    for row in data: #search for the prefix in the relevant column of each dict entry and append them to result 
        if prefix in row[col]:
            result.append(row)
    pretty_result = pprint.pformat(result)
    return (f'These are the DOIS in {col} that match your prefix: \n {pretty_result}')

#print(do_search_by_prefix(data, 10, True))

#FUNCTION 8 (EVERYONE)

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

#FUNCTION 9 (EVERYONE>ENRICA)

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
#This is a working version on data dictionary; used for coupling and co-citation

def do_filter_by_value(data, query, field):
    subcollection = []
    for row in data:
        #verify if it is necessary to convert every field value in string and if we can have to add a pre-lowercase 
        if row[field] == query:
	        subcollection.append(row)
    return subcollection
