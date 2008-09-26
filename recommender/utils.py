from os.path import abspath, dirname, join
import sys
from site import addsitedir

path = addsitedir(abspath(join(dirname(__file__), 'site-packages')), set())
if path: sys.path = list(path) + sys.path

import stats

#Return [0..1] where -1 is not correlated, and 1 is fully correlated
def pearson_correlation(v1,v2):
    '''>>> v1=[0,10,10,0,10]
       >>> v2=[10,0,0,10,0]
       >>> pearson_correlation(v1,v2)
       0.0
       >>> v2=v1
       >>> pearson_correlation(v1,v2)
       1.0
       >>> v2=[0,10,0,10,0]
       >>> pearson_correlation(v1,v2)
       0.41666666666666669
    '''
    try:
        pc= stats.pearsonr(v1,v2)[0]        
    except :
        pc= -1
    return (pc+1.0)/2.0

def tanamoto2(v1,v2):
    ''' >>> v1=['a','b','c']
        >>> v2=['c','a','b']
        >>> tanamoto2(v1,v2)
        1.0
        >>> v2=['e','f','g']
        >>> tanamoto2(v1,v2)
        0.0
        >>> v2=['c','f','k','a']
        >>> tanamoto2(v1,v2)
        0.40000000000000002
        >>> v2=['x','f','k','a']
        >>> tanamoto2(v1,v2)
        0.16666666666666666
        >>> v2=['c','b','k','a']
        >>> tanamoto2(v1,v2)
        0.75
        >>> v2=['b','g','a','t','c']
        >>> v1=['x','y','z','t','v']
        >>> tanamoto2(v1,v2)
        0.1111111111111111
        >>> v1=['a','b']
        >>> tanamoto2(v1,v2)
        0.40000000000000002
        >>> v1=['a','b','x','y','z']
        >>> tanamoto2(v1,v2)
        0.25
    '''
    c1,c2,shr=0,0,0
    c1=len(v1)
    c2=len(v2)
    shr=0
    if c1==0 or c2==0: return 0.0
    for it in v1:
        if it in v2: shr+=1

    if c1+c2-shr==0: return 0.0
    return (float(shr)/(c1+c2-shr))


def distance_matrix_p1_p2(prefs, p1, p2):
    ''' >>> prefs={}
        >>> prefs['p1']={'item1': 0, 'item2': 0, 'item3': 10, 'item4': 10, 'item5':0}
        >>> prefs['p2']={'item1': 10, 'item2': 10, 'item3': 0, 'item4': 0, 'item5':10}
        >>> prefs['p3']={'item1': 0, 'item2': 10, 'item3': 0, 'item4': 0, 'item5':10}
        >>> prefs['p4']={'item1': 0, 'item2': 0, 'item3': 0, 'item4': 0, 'item5':10}
        >>> distance_matrix_p1_p2(prefs,'p1','p1')
        1.0
        >>> distance_matrix_p1_p2(prefs,'p1','p2')
        0.0
        >>> distance_matrix_p1_p2(prefs,'p1','p3')
        0.16666666666666669
        >>> distance_matrix_p1_p2(prefs,'p1','p4')
        0.29587585476806849
        >>> distance_matrix_p1_p2(prefs,'p2','p4')
        0.70412414523193156
        >>> distance_matrix_p1_p2(prefs,'p2','p3')
        0.83333333333333326
    '''        
    v1=[]
    v2=[]
    for item in prefs[p1]:
        if item in prefs[p2]:
            v1.append(prefs[p1][item].vote)
            v2.append(prefs[p2][item].vote)
        
    # if they have no ratings in common, return 0
    if len(v1)==0: return -1
  
    return pearson_correlation(v1,v2)
    

def get_usb_recommendations(element, matrix):
    ''' Calculates recommendations for a given element by using an average of every other element's rankings.
        Returns a pair (value,element_id), where value is [0..X] where 0 doesn't match, and X fully matches
        >>> matrix={}
        >>> matrix['user1']={'item1':-1, 'item3': 1, 'item4': 1, 'item5':0}
        >>> matrix['user2']={'item1': 1, 'item2': 1, 'item3':-1, 'item4':-1, 'item5':10,'item6':10}
        >>> matrix['user3']={'item1':-1, 'item2': 1, 'item4':-1, 'item5':10,'item6':10,'item7':-1}
        >>> matrix['user4']={'item1':-1, 'item2':-1, 'item3':-1, 'item4':-1, 'item5':10,'item7':10,'item8':10}
    '''
    totals={}
    simSums={}
    for other in matrix:
        # don't compare me to myself
        if other==element: continue
        sim=distance_matrix_p1_p2(matrix,element,other)
        # ignore scores of zero or lower
        if sim<=0: continue
        for item in matrix[other]:
            # only score events I haven't seen yet
            if item not in matrix[element]:
                # Similarity * Score
                totals.setdefault(item,0)
                totals[item]+=matrix[other][item].vote*sim
                # Sum of similarities
                simSums.setdefault(item,0)
#                    simSums[item]+=sim #book
                simSums[item]+=1 # my version !!
    # Create the normalized list...?
    rankings=[(total/simSums[item],item) for item,total in totals.items( )]
    return rankings
