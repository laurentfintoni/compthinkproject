#IMPORT SECTION
import csv #to read the data
import re #to use regex
import pprint #to make things pretty because life is beautiful 
import networkx as nx #to make graphs 
import operator #to make comparisons easier 
from datetime import datetime #to compute cited years
from dateutil.relativedelta import relativedelta
from networkx.classes.digraph import DiGraph
from networkx.classes.graph import Graph
from networkx.classes.multidigraph import MultiDiGraph
from networkx.classes.multigraph import MultiGraph
from networkx.classes.ordered import OrderedDiGraph, OrderedGraph, OrderedMultiDiGraph, OrderedMultiGraph

#FUNCTION 1 (LAURENT AND ENRICA)

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

#FUNCTION 2 (LAURENT)

def do_compute_impact_factor(data, dois, year):
    #return error if year isn't a string + catch eroneous year strings w/ regex
    if type(year) is not str or year == '': 
        return 'The year input must be a string with four characters \U0001F645.' 
    else:
        str_pattern = r'(\d{4}$)'
        match = re.fullmatch(str_pattern, year)
        if match == None: 
            return 'The year must be a string in the YYYY format \U0001F913.'
    #return error if set is empty 
    if len(dois) == 0: 
        return 'There are no input DOIS \U0001F645.'
    #create a variable to count citations 
    citations_count = 0 
    #look at all dict instances in list and DOIS in input
    for row in data: 
        for i in dois: 
            #if a DOI in input and the year match in the respective column add a count
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
    #same as above but this time we look for matches between DOIs in citing and cited years        
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

#FUNCTION 3 (ENRICA)

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
    #return error if count is empty
    if co_citations == 0:
        return 'The two input documents are never cited together by other documents \U0001F622'
    else:
        return (f'The total number of co-citations for the two input documents is: {co_citations}.')

#FUNCTION 4 (ENRICA)

def do_get_bibliographic_coupling(data, doi1, doi2):
    #return error if doi inputs are not strings or are empty 
    if type(doi1) is not str or doi1 == '': 
        return 'The first doi input must be a string with at least one character \U0001F645.'
    if type(doi2) is not str or doi2 == '': 
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
    #return error if count is empty
    if bibliographic_coupling == 0:
        return 'The two input documents never cite the same document \U0001F622'
    else:
        return (f'The total number of shared citations by the input documents is: {bibliographic_coupling}.')

#FUNCTION 5 (CAMILLA)

def do_get_citation_network(data, start, end):
    #catch if end is before start 
    if end < start:
        return 'The end year must be after the start year \U0001F645.'
    #return error if start/end inputs aren't strings + catch eroneous strings w/ regex
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
    graph = nx.MultiDiGraph()
    #populate graph w/ relevant inputs 
    for row in data:
        if start <= row["citing_year"] <= end and start <= row["cited_year"] <= end:
            graph.add_edge(row['citing'], row['cited'])
    return graph

#FUNCTION 6 (CAMILLA)

def do_merge_graphs(data, g1, g2):
    #check if inputs are networkx graphs
    graph_types = [type(Graph()), type(DiGraph()), type(MultiGraph()), type(MultiDiGraph()), type(OrderedGraph()), type(OrderedDiGraph()), type(OrderedMultiGraph()), type(OrderedMultiDiGraph())]
    if type(g1) not in graph_types:
        return 'The input graphs must be generated with the networkx library \U0001F645.'
    if type(g2) not in graph_types:
        return 'The input graphs must be generated with the networkx library \U0001F645.'
    #check if input graphs are of same type, if so compute new graph, else return none
    if type(g1) is type(g2):
        new_graph = nx.compose(g1, g2)
        return new_graph
    else:
        return None

#FUNCTION 7 (LAURENT)

def do_search_by_prefix(data, prefix, is_citing):
    #return error if prefix input is not a string + catch eroneous prefix strings w/ regex
    if type(prefix) is not str or prefix == '': 
        return 'The prefix must be a string with at least one character \U0001F913.'
    else:
        str_pattern = r'(\d*/\w*)'
        match = re.search(str_pattern, prefix)
        if match: 
            return 'There is a forward slash in your prefix input. The prefix must be a string with a pattern of digits and numbers only \U0001F913.'
    #return error if is_citing input is not boolean
    if type(is_citing) is not bool:  
        return 'The third input must be a boolean value of TRUE or FALSE \U0001F913.'    
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
        return (f'These are the results that match your search for \'{prefix}\' in column \'{col}\': \n {pprint.pformat(result)}')

#FUNCTION 8 (EVERYONE)

def do_search(data, query, field):
    #return error if input query is not a string 
    if type(query) is not str or query == '': 
        return 'The input query must be a string with at least one character \U0001F913.'
    #return error if input field is not a string + catch eroneous field inputs w/ regex 
    if type(field) is not str or field == '': 
        return 'The chosen field for queries must be a string \U0001F913.'
    else:
        field_pattern = r'(citing|cited|creation|timespan)'
        field_match = re.fullmatch(field_pattern, field)
        if field_match == None: 
            return 'The field input must be either citing, cited, creation or timespan \U0001F913.' 
    #lower case input for insensitive match
    query = query.lower()  
    #check for boolean in query 
    if not re.search(r'(\snot\s|\sand\s|\sor\s)', query):
        #check if the query input contains either ? or * wildcards, if so initialize an empty query variable and iterate over the input query to look for wildcards and replace them with equivalent regex value
        if re.search(r'\*|\?', query):
            re_query = ''
            for l in query:
                if l == '*':
                    re_query += '.*'
                elif l == '?':
                    re_query += '.'
                elif l in '.^$+-()[]\|':
                    re_query += '\\'+l
                else:
                    re_query += l 
            #initialize an empty result list
            result = []
            #iterate over data using input field as col, append results
            for row in data:
                if re.search(re_query, row[field].lower()):
                    result.append(row)  
            if len(result) == 0:
                return 'There are no results for your search, please try again \U0001F647'
        #if no wildcard just process          
        else:
            result = []
            for row in data:
                if re.fullmatch(query, row[field].lower()):
                    result.append(row)  
        return result
    #if there is a boolean operator in query 
    else: 
        #split the query into tokens
        if re.search(r'\snot\s|\sor\s|\sand\s', query):
            query_words_list = query.split(" ")
        #check if the query contains more or less than three tokens
        if len(query_words_list) != 3:
            return 'Your query must follow the following format: "<tokens 1> <operator> <tokens 2>." There appears to be too many or too few tokens \U0001F645.'
        #check if the second token of the query is a boolean operator
        if not re.match(r'not|or|and', query_words_list[1]):
            return 'Your query must follow the following format: "<tokens 1> <operator> <tokens 2>." The boolean operator seems to be in the wrong place \U0001F631.'
        #check if there is more than one boolean operator in the tokens
        if len(re.findall(r'\snot\s|\sor\s|\sand\s', query)) > 1:
            return 'This function only accepts the use of one boolean operator \U0001F645. Your query must follow the following format: "<tokens 1> <operator> <tokens 2>."'
        #if operator is and run the function with the first token and store it as a variable, else return an error message or continue with the second token and run the function using term1 as input instead of data, then return term2 variable 
        if "and" in query_words_list:
            term_1 = do_search(data, query_words_list[0],field)
            if len(term_1) == 0:
                return 'There are no results for your search, please try again \U0001F647'
            else:
                term_2 = do_search(term_1, query_words_list[2],field)
                return term_2
        #if operator is or run the function with first and second tokens, return error message if results are empty else concatenate 
        elif "or" in query_words_list:
            term_1 = do_search(data, str(query_words_list[0]), field)
            term_2 = do_search(data, str(query_words_list[2]), field)
            if len(term_1 + term_2) == 0:
                return 'There are no results for your search, please try again \U0001F647'
            else:
                return term_1 + term_2
        #if operator is not run the function with first and second tokens, then look for any instances of term2 results in term1 results and remove them
        elif "not" in query_words_list:  
            term_1 = do_search(data, str(query_words_list[0]), field)   
            term_2 = do_search(data, str(query_words_list[2]), field)   
            for i in term_2:
                if i in term_1:
                    term_1.remove(i)
            if len(term_1) == 0:
                return 'There are no results for your search, please try again \U0001F647'
            else:
                return term_1

#FUNCTION 9 DO_FILTER_BY_VALUE (EVERYONE)

def do_filter_by_value(data, query, field):
    #return error if input query is not a string 
    if type(query) is not str or query == '': 
        return 'The input query must be a string with at least one character \U0001F913.'
    #return error if input field is not a string + catch eroneous field inputs w/ regex 
    if type(field) is not str or field == '': 
        return 'The chosen field for queries must be a string \U0001F913.'
    else:
        field_pattern = r'(citing|cited|creation|timespan)'
        field_match = re.fullmatch(field_pattern, field)
        if field_match == None: 
            return 'The field input must be either citing, cited, creation or timespan \U0001F913.' 
    #create a dictionary containing possible comparison operators using operator library 
    c_ops = {'<': operator.lt, '<=': operator.le, '>': operator.gt, '>=': operator.ge, '==': operator.eq, '!=': operator.ne}
    #create a list for results
    subcollection = []
    #lowercase the query
    n_query = query.lower()
    #check for operators in query 
    if not re.search(r'<\s|>\s|<=\s|>=\s|==\s|!=\s|and|or|not', n_query):
        for row in data:
            value = row[field]
            #lowercase the search field 
            n_value = value.lower()
            #search for query in search field 
            if re.search(n_query, n_value):
                subcollection.append(row)
        if len(subcollection) == 0:
                return 'There are no results for your search, please try again \U0001F647'
        else:
            return [subcollection]
    #if there are operators in query
    else:
        # split the query into tokens
        spl_query = n_query.split(" ")
        #check if the query contains more than three tokens
        if len(spl_query) > 3:
            return 'Your query must follow the following format: "<operator> <tokens>" for comparisons or "<tokens 1> <operator> <tokens 2>" for boolean searches. There appears to be too many tokens \U0001F645.'        
        #check if the query contains more than three tokens
        if len(spl_query) == 1:
            return 'Your query must follow the following format: "<operator> <tokens>" for comparisons or "<tokens 1> <operator> <tokens 2>" for boolean searches. There appears to be only one token \U0001F645.'  
        #if query has two tokens 
        if len(spl_query) == 2:
            #check that first token is a valid operator 
            if not re.fullmatch(r'<|>|<=|>=|==|!=', spl_query[0]):
                return 'It looks like your first token is not a valid comparison operator \U0001F645.'
            else:
                #look for first token in dictionary of operators and set it as a variable
                co_ops = c_ops[spl_query[0]]
            if re.fullmatch(r'<|>|<=|>=|==|!=', spl_query[1]):
                return 'It looks like your second token is a comparison operator \U0001F645. Your query must follow the following format: "<operator> <tokens>" for comparisons.'
            else:
                #set second token as the query
                v_query = spl_query[1]
            #search for query in data using operator library
            for row in data:
                value = row[field] 
                n_value = value.lower()
                if co_ops(n_value, v_query):
                    subcollection.append(row)
            if len(subcollection) == 0:
                return 'There are no results for your search, please try again \U0001F647'
            else:
                return [subcollection]
        #if query has three tokens    
        if len(spl_query) == 3:
            #check that second token is a boolean
            if not re.match(r'and|or|not', spl_query[1]):
                return 'Your query must follow the following format: "<tokens 1> <operator> <tokens 2>." The boolean operator seems to be in the wrong place \U0001F631.'
            #check that there is only one boolean in tokens
            if len(re.findall(r'not|or|and', n_query)) > 1:
                return 'This function only accepts the use of one boolean operator \U0001F645. Your query must follow the following format: "<tokens 1> <operator> <tokens 2>."'
            #set the first and third tokens as query variables
            v1_query = spl_query[0]
            v2_query = spl_query[2]
            #if boolean is and look for both tokens in data 
            if spl_query[1] == 'and':
                for row in data:
                    value = row[field] 
                    n_value = value.lower()
                    if re.search(v1_query, n_value) and re.search(v2_query, n_value):
                        subcollection.append(row)
                if len(subcollection) == 0:
                    return 'There are no results for your search, please try again \U0001F647'
                else:
                    return [subcollection]
            #if boolean is or look for either token in data
            elif spl_query[1] == 'or':
                for row in data:
                    value = row[field] 
                    n_value = value.lower()
                    if re.search(v1_query, n_value) or re.search(v2_query, n_value):
                        subcollection.append(row)
                if len(subcollection) == 0:
                    return 'There are no results for your search, please try again \U0001F647'
                else:
                    return [subcollection]
            #if boolean is not look for only the first token in data
            elif spl_query[1] == 'not':
                for row in data:
                    value = row[field] 
                    n_value = value.lower()
                    if re.search(v1_query, n_value) and not re.search(v2_query, n_value):
                        subcollection.append(row)
                if len(subcollection) == 0:
                    return 'There are no results for your search, please try again \U0001F647'
                else:
                    return [subcollection]