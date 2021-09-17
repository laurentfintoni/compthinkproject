#IMPORT SECTION
import csv
import re #to use regex
import networkx as nx #to make graphs 
import operator #to make comparisons easier 
from datetime import date #to compute cited years
from dateutil.relativedelta import relativedelta
from networkx.classes.digraph import DiGraph
from networkx.classes.graph import Graph
from networkx.classes.multidigraph import MultiDiGraph
from networkx.classes.multigraph import MultiGraph
from networkx.classes.ordered import OrderedDiGraph, OrderedGraph, OrderedMultiDiGraph, OrderedMultiGraph

#FUNCTION 1 (LAURENT AND ENRICA)

def process_citations(citations_file_path):
    # initialize an empty list to contain data
    matrix = []
    doi_date_dict = {}
    # populate list with raw data, each row is a dictionary with the column as key, row entry as value
    with open(citations_file_path, mode='r') as file:
        csvFile = csv.DictReader(file)
        for row in csvFile:
            matrix.append(row)
            # add two extra-column for 'citing_year' and 'cited_year' with empty value to be filled by using dynamic programming approach
            row.update([('citing_year', ''), ('cited_year', '')])
            # check for 'citing_year' value in doi_date_dict; if not already present, compute the calculation and store the result in doi_date_dict to be used later for same imput doi 
            citing_doi = row['citing']
            if citing_doi in doi_date_dict:
                row['citing_year'] = doi_date_dict[citing_doi]
            else:
                citing_date = row['creation']
                row['citing_year'] = citing_date[0:4]
                doi_date_dict[citing_doi] = row['citing_year']
            # check for 'cited_year' value in doi_date_dict; if not already present, compute the calculation and store the result in doi_date_dict to be used later for same imput doi 
            cited_doi = row['cited']
            if cited_doi in doi_date_dict:
                row['cited_year'] = doi_date_dict[cited_doi]
            else:
                timespan_str = row['timespan']
                # create a cited year key/value pair by using datetime computations
                
                # we can use citing_date witouth assign new variable
                #n_creation = row['creation']
                #while len(n_creation) < 10:
                #    n_creation = n_creation + '-01'
                #citing_n_date = datetime.strptime(n_creation, '%Y-%m-%d')
                #[or citing_n_date = datetime.strptime(creation, '%Y-%m-%d').date() #it compute less data (without time), as weel as ISOFORMAT]
                #timespan_n = (re.split('[a-zA-Z]', timespan_str, 4)[1:-1]) #removed 4, just useful if full ISO duration format is used P(n)Y(n)M(n)DT(n)H(n)M(n)S
                
                #normalize the leght of creation to have an ISOformat date YYYY-MM-DD, when a group is lacking, it is assumed the values are 01
                while len(citing_date) < 10:
                    citing_date = citing_date + '-01'
                #transform the ISOformat string in a date object
                citing_n_date = date.fromisoformat(citing_date) 
                #split the timespan string in a list of values for Y, M, D and assigne them to a relativedelta that is able to have values for yars and months instead of just dayes like for timedelta
                timespan_n = (re.split('[P|Y|M|D]', timespan_str)[1:-1]) #removed all carachters and insert just the four used in timespan; \D not working with negative timespan
                a_n = int(timespan_n[0])
                    if len(timespan_n) == 1:
                        delta_n = relativedelta(years=a_n)
                    else:
                        m_n = int(timespan_n[1])
                        if len(timespan_n) == 2:
                            delta_n = relativedelta(years=a_n, months=m_n)
                        elif len(timespan_n) == 3:
                            g_n = int(timespan_n[2])
                            delta_n = relativedelta(years=a_n, months=m_n, days=g_n)
                #take in consideration negative timespan and change the +/- of relativedelta
                if timespan_str[0] == "-":  # just in case there is a negative timespan
                    delta_n = delta_n*-1
                    #cited_n_date = citing_n_date + delta_n
                #else:
                 #   cited_n_date = citing_n_date - delta_n
                
                #calculate the cited_n_date as date object, subtractig relativedelta from citing_n_date
                cited_n_date = citing_n_date - delta_n
                
                #transform the data object in string and take in consideration just the first four carachters
                #cited_year = (str(cited_n_date)[0:4])
                cited_year = cited_n_date.strftime('%Y') #apparently the right way to transfor a dataobject to a string
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
    #create a list to hold results of citation search
    citation_results = []
    #create set to hold found DOIs 
    dois_cited = set()
    #look at all dict instances in list and DOIS in input
    for row in data: 
        for i in dois: 
            #if DOI in cited add row to results, DOI to cited set
            if i in row["cited"]:
                citation_results.append(row)
                dois_cited.add(row["cited"])
            #if year matches the creation column add a count
                if year in row["creation"]: 
                    citations_count +=1
    #create set to hold input DOIs with no citation
    dois_not_cited = set()
    dois_not_cited = dois.difference(dois_cited)
    #return error if count is empty 
    if citations_count == 0: 
        return 'There are no citations to compute the Impact Factor with \U0001F622.'
    else: 
        #change year input to integer to create two new year variables for the preceding years, then change those back to strings for searching  
        year_int = int(year) 
        year_1 = str(year_int - 1) 
        year_2 = str(year_int - 2)
        #create a set to hold publishing results
        published_dois = set()
        #same as above but this time we look for matches between DOIs and citing/cited years within results subset        
        for row in citation_results: 
            if row["cited_year"] == year_1 or row["cited_year"] == year_2:
                published_dois.add(row["cited"])
        if len(dois_not_cited) > 0:
            for row in data: 
                for i in dois_not_cited:
                    if i in row["citing"] and (row['citing_year'] == year_1 or row['citing_year'] == year_2):
                        published_dois.add(row["citing"])
        #return error if count is empty, also avoids ZeroDivisionError 
        if len(published_dois) == 0: 
            return 'There are no published documents in the previous two years to compute the Impact Factor with \U0001F622.'
        else: 
            #Calculate IF and round it up to 2 decimal points
            impact_factor = round(citations_count / len(published_dois), 2)
            print(f'There were {citations_count} citations for all dois in {year}, {len(published_dois)} documents published in the previous two years, and the impact factor is {impact_factor}.')
            #use formatted string literal to make the result pretty  
            return impact_factor

'''
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
        print(f'The total number of co-citations for the two input documents is: {co_citations}.')
        return co_citations

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
        print(f'The total number of shared citations by the input documents is: {bibliographic_coupling}.')
        return bibliographic_coupling
'''

#FUNCTION 3 (ENRICA)

def do_get_co_citations(data, doi1, doi2):
    # return error alert if doi inputs are not strings or are empty
    if type(doi1) is not str or doi1 == '':
        return 'The first doi input must be a string with at least one character \U0001F645.'
    elif type(doi2) is not str or doi2 == '':
        return 'The second doi input must be a string with at least one character \U0001F645.'

    else:
        # initialize an empty lists for doi1 citations and store them in list; initialize an empty set for dois citing doi1 and store them in set
        cited_doi1_sublist = []
        citing_for_doi1 = set()
        for row in data:
            if row['cited'] == doi1:
                cited_doi1_sublist.append(row)
                citing_for_doi1.add(row['citing'])
        # check for the citing_for_doi1 set lenght, if empty, return an alert; if not empty, check for the doi2
        if len(citing_for_doi1) < 1:
            return f'According to the data, there are no citations for the fist input doi ({doi1}) to compute the co-citation(s) with \U0001F622'
        else:
            # initialize an empty lists for doi2 citations and store them in list; initialize an empty set for dois citing doi2 and store them in set
            cited_doi2_sublist = []
            citing_for_doi2 = set()
            for row in data:
                if row['cited'] == doi2:
                    cited_doi2_sublist.append(row)
                    citing_for_doi2.add(row['citing'])
            # check for the citing_for_doi2 set lenght, if empty, return an alert; if not empty, compute co-citations
            if len(citing_for_doi2) < 1:
                return f'According to the data, there are no citations for the second input doi ({doi2}) to compute the co-citation(s) with \U0001F622'
            else:
                co_citations = len(citing_for_doi1.intersection(citing_for_doi2))
                print(f'The two input dois are cited together by n. {co_citations} other documents or doi(s).')
                return co_citations


# FUNCTION 4 (ENRICA)

def do_get_bibliographic_coupling(data, doi1, doi2):
    # return an alert if doi inputs are not strings or are empty
    if type(doi1) is not str or doi1 == '':
        return 'The first doi input must be a string with at least one character \U0001F645.'
    elif type(doi2) is not str or doi2 == '':
        return 'The second doi input must be a string with at least one character \U0001F645.'

    else:
        # initialize an empty lists for doi1 citations and store them in list; initialize an empty set for dois cited by doi1 and store them in set
        citing_doi1_sublist = []
        cited_by_doi1 = set()
        for row in data:
            if row['citing'] == doi1:
                citing_doi1_sublist.append(row)
                cited_by_doi1.add(row['cited'])
        # check for the cited_by_doi1 set lenght, if empty, retunr an alert; if not empty, check for the doi2
        if len(cited_by_doi1) < 1:
            return f'According to the data, there are no citations for the fist input doi ({doi1}) to compute the bibliographic coupling with \U0001F622'
        else:
            # initialize an empty lists for doi2 citations and store them in list; initialize an empty set for dois cited by doi2 and store them in set
            citing_doi2_sublist = []
            cited_by_doi2 = set()
            for row in data:
                if row['citing'] == doi2:
                    citing_doi2_sublist.append(row)
                    cited_by_doi2.add(row['cited'])
            # check for the cited_by_doi2 set lenght, if empty, print an alert; if not empty, compute bib_coupling
            if len(cited_by_doi2) < 1:
                return f'According to the data, there are no citations for the second input doi ({doi2}) to compute the bibliographic coupling with \U0001F622'
            else:
                bib_coupling = len(cited_by_doi1.intersection(cited_by_doi2))
                print(f'The two input dois have both cited a total of n. {bib_coupling} same doi(s)')
                return bib_coupling
            
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
        return result

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
    errormsg = 'There are no results for your search, please try again \U0001F647'
    if not re.search(r'(\snot\s|\sand\s|\sor\s)', query):
        #check if the query input contains either ? or * wildcards, if so initialize an empty query variable and iterate over the input query to look for wildcards and replace them with equivalent regex value
        if re.search(r'\*|\?', query):
            re_query = ''
            for l in query:
                if l == '*':
                    re_query += '.*'
                elif l == '?':
                    re_query += '.'
                elif l in '.^${}+-?()[]\|':
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
                return errormsg
            else:   
                return result 
        #if no wildcard just process          
        else:
            result = []
            for row in data:
                if re.fullmatch(query, row[field].lower()):
                    result.append(row)
            if len(result) == 0:
                return errormsg
            else:
                return result
    #if there is a boolean operator in query 
    else: 
        #split the query into tokens
        query_words_list = query.split(" ")
        #check if the query contains more or less than three tokens
        if len(query_words_list) != 3:
            return 'Your query must follow the following format: "<tokens 1> <operator> <tokens 2>." There appears to be too many or too few tokens \U0001F645.'
        #check if the second token of the query is a boolean operator
        if not re.match(r'not|or|and', query_words_list[1]):
            return 'Your query must follow the following format: "<tokens 1> <operator> <tokens 2>." The boolean operator seems to be in the wrong place \U0001F631.'
        #if operator is and run the function with the first token and store it as a variable, else return an error message or continue with the second token and run the function using term1 as input instead of data, then return term2 variable 
        if "and" in query_words_list[1]:
            term_1 = do_search(data, query_words_list[0],field)
            if len(term_1) == 0 or term_1 == errormsg:
                return 'There are no results for your search, please try again \U0001F647'
            else:
                term_2 = do_search(term_1, query_words_list[2],field)
                return term_2
        #if operator is or run the function with first and second tokens, return error message if results are empty else concatenate 
        elif "or" in query_words_list[1]:
            term_1 = do_search(data, query_words_list[0], field)
            if term_1 == errormsg:
                term_1 = []
            term_2 = do_search(data, query_words_list[2], field)
            if term_2 == errormsg:
                term_2 = []
            if len(term_1 + term_2) == 0:
                return 'There are no results for your search, please try again \U0001F647'
            else:
                return term_1 + term_2
        #if operator is not run the function with first and second tokens, then look for any instances of term2 results in term1 results and remove them
        elif "not" in query_words_list[1]:
            term_1 = do_search(data, query_words_list[0], field)
            if term_1 == errormsg:
                term_1 = []   
            term_2 = do_search(data, query_words_list[2], field)
            if term_2 == errormsg:
                term_2 = []   
            for i in term_2:
                if i in term_1:
                    term_1.remove(i)
            if len(term_1) == 0:
                return 'There are no results for your search, please try again \U0001F647'
            else:
                return term_1

#FUNCTION 9 DO_FILTER_BY_VALUE (EVERYONE)

def do_filter_by_value(data, query, field):
    # print an alert and return initial filter_result if input query is not a string or input field is not a string + catch eroneous field inputs w/ regex
    if type(query) is not str or query == '':
        return 'The input query must be a string with at least one character \U0001F913.'
    elif type(field) is not str or field == '':
        return 'The chosen field for queries must be a string with the values citing, cited, creation or timespan \U0001F913.'
    else:
        field_pattern = r'(citing|cited|creation|timespan)'
        field_match = re.fullmatch(field_pattern, field)
        if field_match == None:
            return 'The field input must be either citing, cited, creation or timespan \U0001F913.'

        else:
            # create a list for results
            filter_result = []
            # lowercase the query
            l_query = query.lower()

            # check for operators in query: comparisons operators at the beginning of the string, boolean with space after and before
            if not re.search(r'^<\s|^>\s|^<=\s|^>=\s|^==\s|^!=\s|\sand\s|\sor\s|\snot\s', l_query):
                for row in data:
                    if re.search(l_query, row[field].lower()):
                        filter_result.append(row)
                if len(filter_result) == 0:
                    print('There are no results for your query, please try again \U0001F647.')

            # if there are operators in query
            else:
                # split the query into tokens
                spl_query = l_query.split(" ")
                # check if the query contains more than three tokens or just one token
                if 2 < len(spl_query) > 3:
                    return 'Your query must follow the following format: "<operator> <tokens>" for comparisons or "<tokens 1> <operator> <tokens 2>" for boolean searches. There appears to be too many tokens \U0001F645.'
                # if query has two tokens
                elif len(spl_query) == 2:
                    # check that first token is a valid operator
                    if not re.fullmatch(r'<|>|<=|>=|==|!=', spl_query[0]):  # or re.fullmatch(r'<|>|<=|>=|==|!=', spl_query[1]):
                        return 'It looks like your query is not written with the following format: "<operator> <tokens>" for comparison \U0001F645.'
                    else:
                        # create a dictionary containing possible comparison operators using operator library
                        c_ops = {'<': operator.lt, '<=': operator.le, '>': operator.gt, '>=': operator.ge,
                                 '==': operator.eq,
                                 '!=': operator.ne}
                        # look for first token in dictionary of operators and set it as a variable
                        co_ops = c_ops[spl_query[0]]
                        v_query = spl_query[1]
                        # search for query in data using operator library
                        for row in data:
                            if co_ops(row[field].lower(), v_query):
                                filter_result.append(row)
                        if len(filter_result) == 0:
                            print('There are no results for your query, please try again \U0001F647.')
                # if query has three tokens
                elif len(spl_query) == 3:
                    # check that second token is a boolean
                    if not re.match(r'and|or|not', spl_query[1]):
                        return 'Your query must follow the following format: "<tokens 1> <operator> <tokens 2>." The boolean operator seems to be in the wrong place \U0001F631.'
                    else:
                        for row in data:
                            v1_query = re.search(spl_query[0], row[field].lower())
                            v2_query = re.search(spl_query[2], row[field].lower())
                            # combine queries based on boolean
                            if spl_query[1] == 'and':
                                if v1_query and v2_query:
                                    filter_result.append(row)
                            elif spl_query[1] == 'or':
                                if v1_query or v2_query:
                                    filter_result.append(row)
                            elif spl_query[1] == 'not':
                                if v1_query and not v2_query:
                                    filter_result.append(row)
                        if len(filter_result) == 0:
                            print('There are no results for your query, please try again \U0001F647.')
            return filter_result
