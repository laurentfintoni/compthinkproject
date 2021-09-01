#IMPORT SECTION
import csv #to read the data
import re #to use regex
import pprint #to make things pretty because life is beautiful 
import networkx as nx 
import matplotlib.pyplot as plt
import operator 
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
    #same as above but this time we look for matches between DOIs in citing and cited and the years in their respective creation columns          
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
        return 'There are no published documents in the previous two years to compute the Impact Factor with \U0001F622.'
    else: 
        #Calculate IF and round it up to 2 decimal points
        impact_factor = round(citations_count / docs_published, 2)
        #use formatted string literal to make the result pretty  
        return (f'There were {citations_count} citations for all dois in {year}, {docs_published} documents published in the previous two years, and the impact factor is {impact_factor}.') 

#A variable with a set of test DOIS for impact factor 
test_DOIS = {'10.3390/vaccines7040201', '10.3389/fimmu.2018.02532', '10.1007/s00134-019-05862-0', '10.1016/b978-0-323-35761-6.00063-8', '10.1007/s40506-020-00219-4'}

#print(do_compute_impact_factor(data, test_DOIS, '2018'))

#FUNCTION 3 (ENRICA)

#data:the data returned by process_citations
#doi1: the DOI string of the first article
#doi2: the DOI string of the second article
#It returns an integer defining how many times the two input documents are cited together by other documents.

def do_get_co_citations(data, doi1, doi2):
    #return error if doi inputs are not strings or are empty 
    if type(doi1) is not str or doi1 == '': #return error if doi isn't a string 
        return 'The first doi input must be a string with at least one character \U0001F645.'
    if type(doi2) is not str or doi2 == '': #return error if doi isn't a string 
        return 'The second doi input must be a string with at least one character \U0001F645.'
    #initialize two empty lists, look for citations and store them in list
    doi1sublist = []
    doi2sublist = []
    for row in data:
        if row['cited'] == doi1:
            doi1sublist.append(row)
        if row['cited'] == doi2:
            doi2sublist.append(row)
    #create variable to count joint citations 
    co_citations = 0
    #look for joint citations and count them
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

#maybe it could be more economic for the code (?) writing just one different function to be recalled with the different value of cited VS citing

def do_get_bibliographic_coupling(data, doi1, doi2):
    #return error if doi inputs are not strings or are empty 
    if type(doi1) is not str or doi1 == '': #return error if doi isn't a string 
        return 'The first doi input must be a string with at least one character \U0001F645.'
    if type(doi2) is not str or doi2 == '': #return error if doi isn't a string 
        return 'The second doi input must be a string with at least one character \U0001F645.'
    #initialize two empty lists, look for citations and store them in list    
    doi1sublist = []
    doi2sublist = []
    for row in data:
        if row['citing'] == doi1:
            doi1sublist.append(row)
        if row['citing'] == doi2:
            doi2sublist.append(row)
    #create variable to count joint citations
    bibliographic_coupling = 0
    #look for joint citations and count them
    for doiA in doi1sublist:
        for doiB in doi2sublist:
            if doiA['cited'] == doiB['cited']:
                bibliographic_coupling += 1
    return (f'The total number of shared citations by the input documents is: {bibliographic_coupling}.')

#print(do_get_bibliographic_coupling(data, '10.1007/978-1-4614-7438-8_5', '10.2217/cer-2016-0035'))

#FUNCTION 5 (CAMILLA)

#data: the data returned by process_citations
#start: a string defining the starting year to consider (format: YYYY)
#end: a string defining the ending year to consider (format: YYYY) - it must be equal to or
#greater than start
#It returns a directed graph containing all the articles involved in citations if both of them
#have been published within the input start-end interval (start and end included).
#Use the DOIs of the articles involved in citations as name of the nodes.

def do_get_citation_network(data, start, end):
    #catch if end is before start 
    if end < start:
        return 'The end year must be after the start year \U0001F645.'
    #return error if start/end inputs aren't a string + catch eroneous strings w/ regex
    if type(start) is not str or start == '': 
        return 'The start year input must be a string with four characters \U0001F645.'
    else: 
        str_pattern = r'(\d{4}$)'
        match = re.fullmatch(str_pattern, start)
        if match == None: 
            return 'The start year must be a string with a YYYY format \U0001F913.'
    if type(end) is not str or end == '': 
        return 'The end year input must be a string with four characters \U0001F645.'
    else: 
        str_pattern = r'(\d{4}$)'
        match = re.fullmatch(str_pattern, end)
        if match == None: 
            return 'The end year must be a string with a YYYY format \U0001F913.'
    #intiliaze graph 
    G = nx.MultiDiGraph()
    #populate graph w/ relevant inputs 
    for row in data:
        if start <= row["citing_year"] <= end and start <= row["cited_year"] <= end:
            G.add_edge(row['citing'], row['cited'])
	
#-------------------------------displays the graph not actually part of the exam---------------------------------------------------------------
    pos = nx.spring_layout(G)
    nx.draw_networkx_nodes(G,pos,cmap=plt.get_cmap('Blues'),node_size=300)
    nx.draw_networkx_edges(G, pos, edgelist=G.edges(), edge_color="green")
    nx.draw_networkx_labels(G, pos, font_size=9)
    plt.show()
#--------------------------------------------------------------------------------------------------------------------------------------------------
    return G

#print(do_get_citation_network(data, '2015', '2019'))

#FUNCTION 6 (CAMILLA)

#data: the data returned by process_citations
#g1: the first graph to consider
#g2: the second graph to consider
#It returns a new graph being the merge of the two input graphs if these are of the same type
#(e.g. both DiGraphs). In case the types of the graphs are different, return None.

def do_merge_graphs(data, g1, g2):
    if type(g1) is type(g2):
        new_graph = nx.compose(g1, g2)
        return new_graph
    else:
        return None

#test_graph_1 = do_get_citation_network(data, '2018', '2019')
#test_graph_2 = do_get_citation_network(data, '2015', '2019')
#print(do_merge_graphs(data, test_graph_1, test_graph_2))

#FUNCTION 7 (LAURENT)

#data: the data returned by process_citations or by other search/filter activities
#prefix: a string defining the precise prefix (i.e. the part before the first slash) of a DOI
#is_citing: a boolean telling if the operation should be run on citing articles or not
#It returns a sub-collection of citations in data where either the citing DOI (if is_citing is True)
#or the cited DOI (if is_citing is False) is characterised by the input prefix.

#This is a working version w/ dictionary

def do_search_by_prefix(data, prefix, is_citing):
    #return error if prefix input is not a string + catch eroneous prefix strings w/ regex
    if type(prefix) is not str or prefix == '': 
        return 'The prefix must be a string with at least one character \U0001F913.'
    else:
        str_pattern = r'(\d{2}\.\d{0,5})'
        match = re.fullmatch(str_pattern, prefix)
        if match == None: 
            return 'The prefix must be a string with a pattern of 2 digits followed by a full stop and another set of digits up to 5 \U0001F913.'
    #return error if is_citing input is not boolean
    if type(is_citing) is not bool:  
        return 'We need a boolean option for the third input \U0001F913.'    
    #create an empty list for the results 
    result = [] 
    #select the column to do search on based on boolean input 
    if is_citing: 
        col = 'citing'
    else:
        col = 'cited'
    #search for the prefix in the relevant column of each dict entry in data and append them to result
    for row in data:  
        if prefix in row[col]:
            result.append(row)
    #return message if results are empty 
    if len(result) == 0: 
        return 'There are no results for your search, please try again \U0001F647.'
    else: 
        return (f'These are the DOIS in column \'{col}\' that match your prefix search: \n {pprint.pformat(result)}')

#print(do_search_by_prefix(data, '10.3821', False))

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
    #return error if input query is not a string 
    if type(query) is not str or query == '': 
        return 'The input query must be a string with at least one character \U0001F913.'
    #return error if input field is not a string + catch eroneous field inputs w/ regex 
    if type(field) is not str: 
        return 'The chosen field for queries must be a string \U0001F913.'
    else:
        field_pattern = r'(citing|cited|creation|timespan)'
        field_match = re.fullmatch(field_pattern, field)
        if field_match == None: 
            return 'The chosen field must be either citing, cited, creation or timespan \U0001F913.'    
    #lower case input for insensitive match
    query = query.lower()
# -------------------------------------------------------------------------------------------------------------------
    # check if there is a boolean operator in query and split the query into a list of terms
    if re.search('not|or|and', query):
        query_words_list = query.split(" ")

        # check if the query contains more or less than tree terms
        if len(query_words_list) != 3:
            return 'boolean query must have "<tokens 1> <operator> <tokens 2>" format, there seems to be too many or too little words'
        # check if the second term of the query is a bolean
        if not re.match('not|or|and', str(query_words_list[1])):
            return 'boolean query must have "<tokens 1> <operator> <tokens 2>" format, the booleans operator seems to be in the wrong place'
        # check if there is more than a bolean
        if len(re.findall('not|or|and', query)) > 1:
            return 'this functions accept the use of only one boolean operator, query must have "<tokens 1> <operator> <tokens 2>" format'

        if "and" in query_words_list:
            term_1 = do_search(data, str(query_words_list[0]),field)# repeat the whole function substituting the single terms of the query to the original query
            if term_1 == []:
             return []
            else:
                term_2 = do_search(term_1, str(query_words_list[2]),field)# here i search for the second term not in data but in the result of the first term
                term_1.extend(term_2)
                return term_1

        if "or" in query_words_list:
            term_1 = do_search(data, str(query_words_list[0]), field)
            term_2 = do_search(data, str(query_words_list[2]), field)
            term_1.extend(term_2)
            return term_1

        elif "not" in query_words_list:  # same procedure(ex : animal not cat )
            term_1 = do_search(data, str(query_words_list[0]), field)  # ANIMAL
            term_2 = do_search(data, str(query_words_list[2]), field)  # CAT
            if term_1 == []:
                return []
            else:
                for i in term_1:
                    if i in term_2:
                        term_1.remove(i)# the result is the difference between the first and second term
                return term_1

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ 
    #check if the query input contains either ? or * wildcards, if so initialize an empty query variable and iterate over the input query to look for wildcards and replace them with equivalent regex value
    if re.search(r'\*|\?', query):
        re_query = ''
        for l in query:
            if l == '*':
                re_query += '.*'
            elif l == '?':
                re_query += '.'
            elif l in '.^${}+-()[]\|': #not sure we need this tbh 
                re_query += '\\'+l
            else:
                re_query += l 
        #initialize an empty result list
        result = []
        #iterate over data using input field as col, append results
        for row in data:
            if re.search(re_query, row[field].lower()):
                result.append(row)                
    else:
        result = []
        for row in data:
            if re.fullmatch(query, row[field].lower()):
                result.append(row)                
    return result

print(do_search(data, 'vaccin*s', 'citing'))

#FUNCTION 9 DO_FILTER_BY_VALUE (EVERYONE>ENRICA)

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
#This is new version on data dictionary with comparisons and boolens, really naif in some parts but working! Give it a glance; at the end when all will be working we can compress some parts of the other functions using this:



#b_ops = {'and' : operator.and_, 'or' : operator.or_, 'not' : operator.not_} unfortunately not usable because they does not work as comparisons operators, we cannot use them as functions with arguments
def do_filter_by_value(data, query, field):
    #I did not put any control at the beginnig on string format or values to add but we can add them, similarly to do_search
    c_ops = {'<': operator.lt, '<=': operator.le, '>': operator.gt, '>=': operator.ge, '==': operator.eq, '!=': operator.ne}
    subcollection = []
    n_query = query.lower()
    for row in data:
        value = row[field]
        n_value = value.lower()
        if not re.search('<|>|<=|>=|==|!=| and | or | not ', n_query):
            # I assume these carachters are never used for the actual string to query
            if n_value == n_query:
                subcollection.append(row)
        else:
            spl_query = re.split(' ', n_query)
            #Assuming all the strings have to be written as Peroni said "<operator> <tokens>" if comparisons, "<tokens 1> <operator> <tokens 2>" if boolean
            #Used space to split, and 2-lenght list for if comaprisons, and 3-lenght list if with boolean
            #Not used string.partition(value) because is not working with regex, so, impossible to say string.partition('and|or|not') or re.partition('and|or|not', string)
            #Possible problem: if a space is part of the actual string to query
            #es. '2029 OR 2028' = ['2019', 'or', '2018']
            if len(spl_query) == 2:
                #when comparison is used: "<operator> <tokens>" es. '< 2019'
                co_ops = c_ops[spl_query[0]]
                #take the string of the operator, compare it with the key in the c_ops dictionary to have back an operator and be able to perform a check Operator(value1, value2)
                v_query = spl_query[1]
                if co_ops(n_value, v_query):
                    subcollection.append(row)
            if len(spl_query) == 3:
                #when boolean is used: "<tokens 1> <operator> <tokens 2>" es. '2019 or 2018'
                v1_query = spl_query[0]
                v2_query = spl_query[2]
                #I cannot find a solution as for the comparison operators
                if spl_query[1] == 'and':
                    if n_value == v1_query and n_value == v2_query:
                        subcollection.append(row)
                if spl_query[1] == 'or':
                    if n_value == v1_query or n_value == v2_query:
                        subcollection.append(row)
                if spl_query[1] == 'not':
                    if n_value == v1_query and not n_value == v2_query:
                        subcollection.append(row)
    return subcollection

'''data1 = [{'citing': '10.3390/vaccines7040201', 'cited': '10.3390/vaccines3010137', 'creation': '2019-11-29', 'timespan': 'P4Y9M3D', 'citing_year': '2019', 'cited_year': '2015'}, {'citing': '10.3390/vaccines7040201', 'cited': '10.4161/hv.26036', 'creation': '2019-11-29', 'timespan': 'P5Y11M28D', 'citing_year': '2019', 'cited_year': '2013'}, {'citing': '10.3390/vaccines7040201', 'cited': '10.7861/clinmedicine.17-6-484', 'creation': '2019-11-29', 'timespan': 'P1Y11M', 'citing_year': '2019', 'cited_year': '2017'}, {'citing': '10.3390/vaccines8020154', 'cited': '10.3390/vaccines7040201', 'creation': '2020-03-30', 'timespan': 'P0Y4M1D', 'citing_year': '2020', 'cited_year': '2019'}, {'citing': '10.3390/vaccines8040600', 'cited': '10.3390/vaccines7040201', 'creation': '2020-10-12', 'timespan': 'P0Y10M13D', 'citing_year': '2020', 'cited_year': '2019'}]
#query1 = 'p4Y9m3D'
query2 = '2019 OR 2017'
query3 = '> 2012'
field1 = 'cited_year'''

#print(do_filter_by_value(data, 'vaccine OR e', 'cited'))



