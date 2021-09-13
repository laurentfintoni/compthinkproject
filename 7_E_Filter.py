import csv
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
    filter_result = []
    #lowercase the query
    l_query = query.lower()
    #check for operators in query
    #if not re.search(r'<\s|\s<|>\s|\s>|<=\s|\s<=|>=\s|\s>=|==\s|\s==|!=\s|\s!=|\sand\s|\sor\s|\snot\s', n_query):
    if not re.search(r'^<\s|^>\s|^<=\s|^>=\s|^==\s|^!=\s|\sand\s|\sor\s|\snot\s', l_query):
        for row in data:
            if re.search(l_query, row[field].lower()):
            #perchè re?? torna un match object
                filter_result.append(row)
        if len(filter_result) == 0:
                return 'There are no results for your query, please try again \U0001F647'
        else:
            return filter_result
    #if there are operators in query
    else:
        # split the query into tokens
        spl_query = l_query.split(" ")
        #check if the query contains more than three tokens or just one token
        if 2 < len(spl_query) > 3:
            return 'Your query must follow the following format: "<operator> <tokens>" for comparisons or "<tokens 1> <operator> <tokens 2>" for boolean searches. There appears to be too many tokens \U0001F645.'
        #if query has two tokens
        elif len(spl_query) == 2:
            #check that first token is a valid operator
            if not re.fullmatch(r'<|>|<=|>=|==|!=', spl_query[0]) or re.fullmatch(r'<|>|<=|>=|==|!=', spl_query[1]):
                return 'It looks like your query is not written with the following format: "<operator> <tokens>" for comparison \U0001F645.'
            else:
                #look for first token in dictionary of operators and set it as a variable
                co_ops = c_ops[spl_query[0]]
                v_query = spl_query[1]
            #search for query in data using operator library
            for row in data:
                if co_ops(row[field].lower(), v_query):
                    filter_result.append(row)
            if len(filter_result) == 0:
                return 'There are no results for your query, please try again \U0001F647'
            else:
                return filter_result
        #if query has three tokens
        elif len(spl_query) == 3:
            #check that second token is a boolean
            #< and 2009
            if not re.match(r'and|or|not', spl_query[1]):
                return 'Your query must follow the following format: "<tokens 1> <operator> <tokens 2>." The boolean operator seems to be in the wrong place \U0001F631.'
            #check that there is only one boolean in tokens
#            if len(re.findall(r'not|or|and', l_query)) > 1:
#                return 'This function only accepts the use of one boolean operator \U0001F645. Your query must follow the following format: "<tokens 1> <operator> <tokens 2>."'
            #set the first and third tokens as query variables
            else:
                for row in data:
                    v1_query = re.search(spl_query[0], row[field].lower())
                    v2_query = re.search(spl_query[2], row[field].lower())
                    # if boolean is "and", look for both tokens in data
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
                    return 'There are no results for your query, please try again \U0001F647'
                else:
                    return filter_result
#'<< < 2016'
print(do_filter_by_value(data, 'annurev and virology', 'citing'))

