#FUNCTION 3 (ENRICA)
#It returns an integer defining how many times the two input documents are cited both by the same document.

def do_get_co_citations(data, doi1, doi2):
    #return error if doi inputs are not strings or are empty
#code condensation
    if type(doi1) is not str or doi1 == '':
        return 'The first doi input must be a string with at least one character \U0001F645.'
    elif type(doi2) is not str or doi2 == '':
        return 'The second doi input must be a string with at least one character \U0001F645.'
    #initialize two empty lists, look for citations and store them in list
    else:
        cited_doi1_sublist = []
        citing_for_doi1 = set()
        for row in data:
            if row['cited'] == doi1:
                cited_doi1_sublist.append(row)
                citing_for_doi1.add(row['citing'])
        if len(citing_for_doi1) < 1:
            return f'According to the data, there are no citations for the fist input doi ({doi1}) to compute the co-citation(s) with \U0001F622'
        else:
            cited_doi2_sublist = []
            citing_for_doi2 = set()
            for row in data:
                if row['cited'] == doi2:
                    cited_doi2_sublist.append(row)
                    citing_for_doi2.add(row['citing'])
            if len(citing_for_doi2) < 1:
                return f'According to the data, there are no citations for the second input doi ({doi2}) to compute the co-citation(s) with \U0001F622'
            else:
                co_citations = len(citing_for_doi1.intersection(citing_for_doi2))
                return f'The two input dois are cited together by n. {co_citations} other documents [doi(s)].'

#FUNCTION 4 (ENRICA)
#It returns an integer defining how many times the two input documents cite both the same document.
def do_get_bibliographic_coupling(data, doi1, doi2):
    #return error if doi inputs are not strings or are empty
    if type(doi1) is not str or doi1 == '':
        return 'The first doi input must be a string with at least one character \U0001F645.'
    elif type(doi2) is not str or doi2 == '':
        return 'The second doi input must be a string with at least one character \U0001F645.'
    #initialize two empty lists, look for citations and store them in list
    else:
        citing_doi1_sublist = []
        cited_by_doi1 = set()
        for row in data:
            if row['citing'] == doi1:
                citing_doi1_sublist.append(row)
                cited_by_doi1.add(row['cited'])
        if len(cited_by_doi1) < 1:
            return f'According to the data, there are no citations for the fist input doi ({doi1}) to compute the bibliographic coupling with\U0001F622'
        else:
            citing_doi2_sublist = []
            cited_by_doi2 = set()
            for row in data:
                if row['citing'] == doi2:
                    citing_doi2_sublist.append(row)
                    cited_by_doi2.add(row['cited'])
            if len(cited_by_doi1) < 1:
                return f'According to the data, there are no citations for the second input doi ({doi2}) to compute the bibliographic coupling with\U0001F622'
            else:
                coupling = len(cited_by_doi1.intersection(cited_by_doi2))
                return f'The two input dois have both cited a total of n. {coupling} same doi(s)'
                #(f'The total number of shared citations by the input documents is: {bibliographic_coupling}.')


print(do_get_co_citations(data1,'10.1007/s10979-009-9201-0', '10.1016/j.jclinepi.2005.09.002'))
print(do_get_bibliographic_coupling(data1,'10.7243/2052-935x-4-1', '10.7326/m18-2101'))
#10.1016/j.jclinepi.2005.09.002
print(end-start)
