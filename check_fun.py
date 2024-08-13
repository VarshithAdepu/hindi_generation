import constant 
import sys
from utils import *
import os

def check_named_entity(word_data):
    if word_data[2] == 'ne':
        return True
    return False

def check_noun(word_data):
    '''
    Functionality:
        1. Check semantic data has place/ ne
        2. Check if GNP row has number info sg or pl

    Parameters:
        word_data: tuple of concept with all its information

    Returns:
        True - if any of the above condition is met
        False - otherwise

    For eg.     :
        rAma,xo_1,rotI_1,xAla_1,KA_1-yA_1
        1,2,3,4,5,6
        male per,,,,
        sg,,sg,sg,
        6:k1,3:card,6:k2,6:k2,0:main
        ,,,,,
        ,,,,,
        ,,,,,
        affirmative
        conj:[3,4]

        word_data = (1, 'rAma', 'male per', 'sg', '6:k1', '', '', '')
        Result     : True (as word_data[3] == 'sg')
    '''

    try:
        if word_data[2] in ('place','Place','ne','NE') and '^' not in word_data[1]:
            return True

        if word_data[3] in ('pl'):
            return True
        return False
    except IndexError:
        log(f'Index Error for GNP Info. Checking noun for {word_data[1]}', 'ERROR')
        # sys.exit()
        return None

def check_pronoun(word_data):
    '''
    Functionality:
        1. Check if the concept belongs to PRONOUN_TERMS list ('speaker', 'kyA', 'Apa', 'jo', 'koI' etc.)
        2. Check if dependency relation is not r6 and discourse data is coref

    Parameters:
        word_data: tuple of concept with all its information

    Returns:
        True - if any of the above condition is met
        False - otherwise

    For eg.     :
        speaker,Aja_1,snAna+kara_1-yA_1
        1,2,3
        anim male,,
        sg,,
        3:k1,3:k7t,0:main
        ,,
        ,,
        ,,
        affirmative

        word_data     : (1, 'speaker', 'anim male', 'sg', '3:k1', '', '', '')
    Result:
        True (as 'speaker' exists in PRONOUN_TERMS list)
    '''

    try:
        if clean(word_data[1]) in constant.PRONOUN_TERMS:
            return True
        elif 'coref' in word_data[5]:
            if 'r6' not in word_data[4]: # for words like apanA
                return True
        else:
            return False
    except IndexError:
        log(f'Index Error for GNP Info. Checking pronoun for {word_data[1]}', 'ERROR')
        sys.exit()

def check_adjective(word_data):
    '''
    Functionality:
        1. Check if dependency data is any of the following - 'card', 'mod', 'meas', 'ord', 'intf'
        2. Check if dependency relation is k1s and does not have GNP info
        3. Check if dependency relation is r6 and discourse data is coref

    Parameters:
        word_data: tuple of concept with all its information

    Returns:
        True - if any of the above condition is met
        False - otherwise

    For eg.     :
        rAma,xo_1,rotI_1,xAla_1,KA_1-yA_1
        1,2,3,4,5,6
        male per,,,,
        sg,,sg,sg,
        6:k1,3:card,6:k2,6:k2,0:main
        ,,,,,
        ,,,,,
        ,,,,,
        affirmative
        conj:[3,4]

        word_data     : (2, 'xo_1', '', '', '3:card', '', '', '')
    Result:
        True (as dependency relation is card)
    '''

    word_data_list = list(word_data)

    if word_data_list[4] != '':
        rel = word_data_list[4].strip().split(':')[1]
        if rel in constant.ADJECTIVE_DEPENDENCY:
            return True
        if word_data_list[3] == '' and rel not in constant.ADJECTIVE_DEPENDENCY and word_data_list[5] != '0:main':
            word_data_list[3] = 'sg'
        if rel == 'k1s' and word_data_list[3] == '': # k1s and no GNP -> adj
            return True

        if word_data_list[5] != '':
            if ':' in word_data_list[5]:
                coref = word_data_list[5].strip().split(':')[1]
                if rel == 'r6' and coref == 'coref': # for words like apanA
                    return True

    word_data = tuple(word_data_list)

    return False

def check_nonfinite_verb(word_data):
    '''Check if word is a non-fininte verb by the USR info'''

    if word_data[4] != '':
        rel = word_data[4].strip().split(':')[1]
        if rel in ('rpk','rbk', 'rvks', 'rbks','rsk', 'rbplk'):
            return True
    return False

def check_verb(word_data):
    '''
    Functionality:
        1. Check for both finite and non-finite verbs-
            nonfinite verbs     : checked by dependency
            main verb     : identified by '-' in it
    Parameters:
        word_data: tuple of concept with all its information

    Returns:
        True - if any of the above condition is met
        False - otherwise

    For eg.     :
        speaker,Aja_1,snAna+kara_1-yA_1
        1,2,3
        anim male,,
        sg,,
        3:k1,3:k7t,0:main
        ,,
        ,,
        ,,
        affirmative

        word_data     : (3, 'snAna+kara_1-yA_1', '', '', '0:main', '', '', '')
    Result:
        True (as '-' in 'snAna+kara_1-yA_1')

    '''

    if '-' in word_data[1]:
        rword = word_data[1].split('-')[0]
        if rword in extract_tamdict_hin():
            return True
        else:
            log(f'Verb "{rword}" not found in TAM dictionary', 'WARNING')
            return True
    else:
        if word_data[4] != '':
            rel = word_data[4].strip().split(':')[1]
            if rel in constant.NON_FINITE_VERB_DEPENDENCY:
                return True
    return False

def check_adverb(word_data):
    '''
    Functionality: Check for kr_vn/ krvn in dependency row.

    Parameters:
        word_data: tuple of concept with all its information

    Returns:
        True - if any of the above condition is met
        False - otherwise
    '''
    if word_data[4] != '':
        rel = word_data[4].strip().split(':')[1]
        if rel in ('kr_vn','krvn'):
            return True
    return False

def check_foreign_words(word_data):
    '''checks ^ is present infront of word 
    if it is present then it is a foreign word'''

    if word_data[1][0]=='^':
        return True
    else:
        return False

def check_indeclinable(word_data):
    '''
    Functionality:
        Return True as indeclinable if:
        1. the semantic info of the concept is 'unit'
        2. Check if word is in INDECLINABLE_WORDS or UNITS list in constant.py

    Parameters:
        word_data: tuple of concept with all its information

    Returns:
        True - if any of the above condition is met
        False - otherwise

    For eg.:
        speaker,Aja_1,snAna+kara_1-yA_1
        1,2,3
        anim male,,
        sg,,
        3:k1,3:k7t,0:main
        ,,
        ,,
        ,,
        affirmative

        word_data = (2, 'Aja_1', '', '', '3:k7t', '', '', '')

    Result:
        True (as Aja exists in constant.INDECLINABLE_WORDS)

    '''
    if word_data[2] == 'unit':
        return True

    if clean(word_data[1]) in constant.UNITS:
        return True

    if clean(word_data[1]) in constant.INDECLINABLE_WORDS:
        return True

    return False

def check_digit(word_data):
    '''
    Functionality:
        Return True if:
        1. the concept has digits or float value

    Parameters:
        word_data: tuple of concept with all its information

    '''
    num = word_data[1]
    if '_' in num:
        num = num.strip().split('_')[0]
    if num.isdigit():
        return True
    else:
        try:
            float_value = float(num)
            return True
        except ValueError:
            return False
    return False

def check_nominal_verb(word_data):
    '''
    Functionality: Check if dependency value belongs to NOMINAL_VERB_DEPENDENCY list and there is no GNP information

    Parameters:
        word_data: tuple of concept with all its information

    Returns:
        True - if any of the above condition is met
        False - otherwise
    '''
    if word_data[4].strip() != '':
        relation = word_data[4].strip().split(':')[1]
        gnp_info = word_data[3]
        term=clean(word_data[1])
        tags = find_tags_from_dix_as_list(term)
        for tag in tags:
            if tag == ('cat', 'v') and relation not in constant.NON_FINITE_VERB_DEPENDENCY:
                # noun_type = category = 'vn'
                return True
                    # term += 'nA'
                # log(f'{term} processed as nominal verb with index {index} gen:{gender} num:{number} person:{person} noun_type:{noun_type} case:{case} and postposition:{postposition}')
                # break
    else:
        return False

def find_tags_from_dix_as_list(word):
#     print('Running find_tags_from_dix_as_list')
    """
    >>> find_tags_from_dix("mAz")
    {'cat': 'n', 'case': 'd', 'gen': 'f', 'num': 'p', 'form': 'mA'}
    """
    dix_command = "echo {} | apertium-destxt | lt-proc -ac hi.morfLC.bin | apertium-retxt".format(word)
    morph_forms = os.popen(dix_command).read()
    p_m=parse_morph_tags_as_list(morph_forms)
#     print('find_tags_from_dix_as_list : ',p_m)
    return p_m

def parse_morph_tags_as_list(morph_form):
    """
    >>> parse_morph_tags("mA<cat:n><case:d><gen:f><num:p>")
    {'cat': 'n', 'case': 'd', 'gen': 'f', 'num': 'p', 'form': 'mA'}
    """
    form = morph_form.split("<")[0]
    matches = re.findall("<(.*?):(.*?)>", morph_form)
    result = [(match[0], match[1]) for match in matches]
    result.append(('form',form))
    return result

def check_is_digit(num):
    if num.isdigit():
        return True
    else:
        try:
            float_value = float(num)
            return True
        except ValueError:
            return False
    return False

def extract_tamdict_hin():
#     print('Running extract_tamdict_hin')
    extract_tamdict = []
    try:
        with open(constant.TAM_DICT_FILE, 'r') as tamfile:
            for line in tamfile.readlines():
                hin_tam = line.split('  ')[1].strip()
                extract_tamdict.append(hin_tam)
        return extract_tamdict
    except FileNotFoundError:
        log('TAM Dictionary File not found.', 'ERROR')
        sys.exit()