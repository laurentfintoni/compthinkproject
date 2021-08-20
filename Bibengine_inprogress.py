#IMPORT SECTION
import csv #to read the data
import re #to use regex
import pprint #to make things pretty because life is beautiful 
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
    #create a cited year key/value pair by using datetime computations 
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

#FUNCTION 2 

#data: the data returned by process_citations
#dois: a set of DOIs identifying articles
#year: a string in format YYYY to consider
#It returns a number which is the result of the computation of the Impact Factor (IF) for such documents.
#The IF of a set of documents dois on a year year is computed by counting the number of citations all
#the documents in dois have received in year year, and then dividing such a value by the number of
#documents in dois published in the previous two years (i.e. in year-1 and year-2)"""
 
#NEEDS TO ADD SEARCH FOR TIMESPAN COLUMN AS PER ENRICA SUGGESTION (LO)

def do_compute_impact_factor(data, dois, year):
    #return error if year isn't a string 
    if type(year) is not str or year == '': 
        return 'The year input must be a string with four characters \U0001F645.' 
    #return error if set is empty 
    if len(dois) == 0: 
        return 'There are no input DOIS \U0001F645.'
    #catch eroneous year string w/ regex
    str_pattern = r'(\d{4}$)'
    match = re.match(str_pattern, year)
    if match == None: 
        return 'The year must be a string with a YYYY format \U0001F913.'
    #create a variable to count citations 
    citations_count = 0 
    #look at all dict instances in list and DOIS in input
    for row in data: 
        for i in dois: 
            #if a DOI in input and the year match in the respective columns add a count
            if i in row["cited"] and year in row["creation"]: 
                citations_count +=1
    #return error if count is empty 
    if citations_count == 0: 
        return 'There are no citations to compute the Impact Factor with \U0001F622.'
    #create a variable to count published docs 
    docs_published = 0 
    #change year input to integer to create two new year variables for the preceding years, then change those back to strings for searching  
    year_int = int(year) 
    year_1 = str(year_int - 1) 
    year_2 = str(year_int - 2)
    #same as above but this time we look for matches in other columns         
    for row in data: 
        for i in dois:       
            if i in row["citing"] and year_1 in row["citing_year"]:
                docs_published +=1
            if i in row["citing"] and year_2 in row["citing_year"]:
                docs_published +=1
            if i in row["cited"] and year_1 in row["cited_year"]:
                docs_published +=1
            if i in row["cited"] and year_2 in row["cited_year"]:
                docs_published +=1
    #return error if count is empty, also avoids ZeroDivisionError 
    if docs_published == 0: 
        return 'There are no published documents in the previous two years to compute Impact Factor with \U0001F622.'
    else: 
        #Calculate IF and round it up to 2 decimal points
        impact_factor = round(citations_count / docs_published, 2)
        #use formatted string literal to make the result pretty  
        return (f'There were {citations_count} citations for all dois in {year}, {docs_published} documents published in the previous two years, and the impact factor is {impact_factor}.') 

#A variable with a set of test DOIS for impact factor 
test_DOIS = {'10.3390/vaccines7040201', '10.3389/fimmu.2018.02532', '10.1007/s00134-019-05862-0', '10.1016/b978-0-323-35761-6.00063-8', '10.1007/s40506-020-00219-4'}

print(do_compute_impact_factor(data, test_DOIS, '2019'))

#FUNCTION 3 (ENRICA)

#data:the data returned by process_citations
#doi1: the DOI string of the first article
#doi2: the DOI string of the second article
#It returns an integer defining how many times the two input documents are cited together by other documents.

#This is an Enrica woking dictionary version using do_filter_by_value function:
def do_get_co_citations(data, doi1, doi2):
    if type(doi1) is not str or doi1 == '': #return error if doi isn't a string 
        return 'The first doi input must be a string with at least one character \U0001F645.'
    if type(doi2) is not str or doi2 == '': #return error if doi isn't a string 
        return 'The second doi input must be a string with at least one character \U0001F645.'
    doi1sublist = []
    doi2sublist = []
    for row in data:
        if row['cited'] == doi1:
            doi1sublist.append(row)
        if row['cited'] == doi2:
            doi2sublist.append(row)
    co_citations = 0
    for doiA in doi1sublist:
        for doiB in doi2sublist:
            if doiA['citing'] == doiB['citing']:
                co_citations += 1
    return (f'The total number of co-citations for the two input documents is: {co_citations}.')

#print(do_get_co_citations(data, '10.1016/s0140-6736(97)11096-0', '10.1080/15265161.2010.519226'))

#FUNCTION 4 (ENRICA)

#data: the data returned by process_citations
#doi1: the DOI string of the first article
#doi2: the DOI string of the first article
#It returns an integer defining how many times the two input documents cite both the same document.

#def do_get_bibliographic_coupling(data, doi1, doi2)
#This is an Enrica working dictionaryversion using do_filter_by_value function; 
#maybe it could be more economic for the code (?) writing just one different function to be recalled with the different value of cited VS citing:

def do_get_bibliographic_coupling(data, doi1, doi2):
    if type(doi1) is not str or doi1 == '': #return error if doi isn't a string 
        return 'The first doi input must be a string with at least one character \U0001F645.'
    if type(doi2) is not str or doi2 == '': #return error if doi isn't a string 
        return 'The second doi input must be a string with at least one character \U0001F645.'
    doi1sublist = []
    doi2sublist = []
    for row in data:
        if row['citing'] == doi1:
            doi1sublist.append(row)
        if row['citing'] == doi2:
            doi2sublist.append(row)
    bibliographic_coupling = 0
    for doiA in doi1sublist:
        for doiB in doi2sublist:
            if doiA['cited'] == doiB['cited']:
                bibliographic_coupling += 1
    return (f'The total number of shared citations by the input documents is: {bibliographic_coupling}.')

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

#This is a working version w/ dictionary

def do_search_by_prefix(data, prefix, is_citing):
    if type(prefix) is not str or prefix == '': #return error, prefix is not a string 
        return 'The prefix must be a string with at least one character \U0001F913.'
    if type(is_citing) is not bool: #return error, is citing option is not boolean 
        return 'We need a boolean option \U0001F913.'
    str_pattern = r'(\d{0,2}\.\d{0,5})'
    match = re.match(str_pattern, prefix)
    if match == None: #catch eroneous prefix strings w/ regex
        return 'The prefix must be a string with a pattern of 2 digits followed by a full stop and another set of digits \U0001F913.'
    result = [] #create an empty list for the results 
    if is_citing: #select the column to do search on based on boolean input 
        col = 'citing'
    else:
        col = 'cited'
    for row in data: #search for the prefix in the relevant column of each dict entry and append them to result 
        if prefix in row[col]:
            result.append(row[col])
    if len(result) == 0: #catch if results are empty 
        return 'There are no results for your search, please try again \U0001F647.'
    else: 
        pretty_result = pprint.pformat(result)
        return (f'These are the DOIS in {col} that match your prefix: \n {pretty_result}')

#print(do_search_by_prefix(data, '10.3928', True))

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

#something about matching different date formats? right now it only match yyyy-mm-dd + still needs wildcard matching and booleans 

def do_search(data, query, field):
    if type(query) is not str or query == '': #return error query is not a string 
        return 'The input query must be a string with at least one character \U0001F913.'
    if type(field) is not str: #return error field is not a string 
        return 'The chosen field for queries must be a string \U0001F913.'
    field_pattern = r'(citing|cited|creation|timespan)'
    field_match = re.match(field_pattern, field)
    if field_match == None: #catch eroneous field strings w/ regex
        return 'The chosen field must be either citing, cited, creation or timespan \U0001F913.'
    query = query.lower() #lower case input for insensitive match
    result = []
    if field == 'citing':
        search_row = 'citing'
        for row in data:
            if query in row[search_row].lower():
                result.append(row[search_row])                
    elif field == 'cited':
        search_row = 'cited'
        for row in data:
            if query in row[search_row].lower():
                result.append(row[search_row])   
    elif field == 'creation':
        search_row = 'creation'
        for row in data:
            if query in row[search_row].lower():
                result.extend([row['citing'], row['cited']])   
    else:
        search_row = 'timespan'
        for row in data:
            if query in row[search_row].lower():
                result.extend([row['citing'], row['cited']])
    if len(result) == 0:
        return 'There were no citations for your search, please try again \U0001F647.'
    else:
        pretty_result = pprint.pformat(result)
        return (f'These are the matching citations for query \'{query}\' in field \'{field}\': \n {pretty_result}')

#print(do_search(data, 'A?MG', 'citing'))

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

""" def do_filter_by_value(data, query, field):
    subcollection = []
    for row in data:
        #verify if it is necessary to convert every field value in string and if we can have to add a pre-lowercase 
        if row[field] == query:
	        subcollection.append(row)
    return subcollection
 """
