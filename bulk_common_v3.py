import os
import sys
import re
import subprocess
import constant
from wxconv import WXC
# from generate_input_modularize_new import additional_words_dict,spkview_dict
# from Table import store_data
from verb import Verb
from concept import Concept
from utils import *
from check_fun import *
additional_words_dict = {}
processed_postpositions_dict = {}
construction_dict = {}
spkview_dict = {}
MORPHO_SEMANTIC_DICT = {}

def read_file(file_path):
    """
    Functionality: To read the file from mentioned file_path.
    Exception: If file_path is incorrect raise an exception - "No such File found." and exit the program.
    Parameters:
        file_path - path of file to be read.
    Returns:
        Returns array of lines for data given in file.
    """
    log(f'File ~ {file_path}')
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            if len(lines) > 10 and lines[10].strip() == '':
                lines = lines[:10]
        log('File data read.')
    except FileNotFoundError:
        log('No such File found.', 'ERROR')
        sys.exit()
    return lines


def write_hindi_text(hindi_output, POST_PROCESS_OUTPUT, OUTPUT_FILE):
    """Append the hindi text into the file"""
    with open(OUTPUT_FILE, 'w') as file:
        file.write(POST_PROCESS_OUTPUT)
        file.write('\n')
        file.write(hindi_output)
        log('Output data write successfully')
    return "Output data write successfully"

def generate_rulesinfo(file_data):
    '''
    Functionality: Extract all rows of USR, remove spaces from Running and end and break the entire row on the basis of comma and convert into list of strings.
    Exception: If length of file_data array is less than 10 raise an exception - Invalid USR. USR does not contain 10 lines.' and exit the program.
    Parameters:
        file_data - This is an array of lines read from input file.
    Returns:
        Return list of rows of USR as list of lists.
    '''

    if len(file_data) < 10:
        log('Invalid USR. USR does not contain 10 lines.', 'ERROR')
        sys.exit()

    src_sentence = file_data[0]
    root_words = file_data[1].strip().split(',')
    index_data = file_data[2].strip().split(',')
    seman_data = file_data[3].strip().split(',')
    gnp_data = file_data[4].strip().split(',')
    depend_data = file_data[5].strip().split(',')
    discourse_data = file_data[6].strip().split(',')
    spkview_data = file_data[7].strip().split(',')
    scope_data = file_data[8].strip().split(',')
    sentence_type = file_data[9].strip()
    construction_data = ''
    if len(file_data) > 10:
        construction_data = file_data[10].strip()

    log('Rules Info extracted succesfully fom USR.')
    return [src_sentence, root_words, index_data, seman_data, gnp_data, depend_data, discourse_data, spkview_data,
            scope_data, sentence_type, construction_data]

def populate_spkview_dict(spkview_info):
    populate_spk_dict = False
    a = 'after'
    b = 'before'
    for i, info in enumerate(spkview_info):
        clean_spk_info = info.rstrip('_1234567890')
        if clean_spk_info in constant.spkview_list or clean_spk_info == 'result':
            populate_spk_dict = True
            temp = (a, clean_spk_info) if clean_spk_info in constant.spkview_list else (b, 'pariNAmasvarUpa,')
            spkview_dict[i + 1] = [temp]
    return populate_spk_dict

def generate_wordinfo(root_words, index_data, seman_data, gnp_data, depend_data, discourse_data, spkview_data,
                      scope_data):
    '''
    Functionality:
        1. To check USR format
        2. Combine each concept with its corresponding information at the same index in all rows in tuples. Group all these tuples as word_info list.

    Parameters:
        1. root_words - second row of USR. Contains all concepts/ root words
        2. index_data - third row of USR. Contains indexing of concepts from 1, 2, 3 and onwards
        3. seman_data - fourth row of USR. Contains semantic information about all concepts
        4. gnp_data - fifth row of USR. Contains number information of the concept
        5. depend_data - sixth row of USR. Contains dependency information of the concept
        6. discourse_data - seventh row of USR. Contains discourse information of the concept
        7. spkview_data - eighth row of USR. Contains speaker's view information of the concept
        8. scope_data - ninth row of USR. Contains scope information of the concept

    Returns:
        Generates an array of tuples containing word and its USR info i.e USR info word wise.
        '''
    return list(
        zip(index_data, root_words, seman_data, gnp_data, depend_data, discourse_data, spkview_data, scope_data))

def identify_cat(words_list):
    '''
    Functionality: There are various categorizations of the concepts such as - nouns, pronouns etc. This function Checks word for its type to process
    accordingly and add that word to its corresponnding list.

    Parameters:
        1. words_list: It is an array of tuples. Each tuple consists of concept wise USR info.

    Returns:
        All the categorized lists of nouns, pronouns etc. with input concept tuple appended in it

    For eg.
        jaMgala_1, Sera_1, hE_1-past
        1,2,3
        ,anim male,
        sg,,
        3:k7p, 3:k1,0:main
        ,,
        def,,
        ,,
        affirmative

    Result -
        indeclinables = []
        pronouns = []
        nouns = [(1, 'jaMgala_1', '', 'sg', '3:k7p', '', 'def', ''), (2, 'Sera_1', 'anim male', '', '3:k1', '', '', '')]
        adjectives = []
        verbs = [(3, 'hE_1-past', '', '', '0:main', '', '', '')]
        adverbs = []
        others = []
        nominal_verbs = []
    '''
    foreign_words=[]
    indeclinables = []
    pronouns = []
    nouns = []
    adjectives = []
    verbs = []
    others = []
    adverbs = []
    nominal_verb = []
    for word_data in words_list:
        if check_foreign_words(word_data):
            log(f'{word_data[1]} identified as indeclinable.')
            foreign_words.append(word_data)
        elif check_indeclinable(word_data):
            log(f'{word_data[1]} identified as indeclinable.')
            indeclinables.append(word_data)
        elif check_digit(word_data):
            log(f'{word_data[1]} identified as noun.')
            nouns.append(word_data)
        elif check_verb(word_data):
            log(f'{word_data[1]} identified as verb.')
            verbs.append(word_data)
        elif check_adjective(word_data):
            log(f'{word_data[1]} identified as adjective.')
            adjectives.append(word_data)
        elif check_pronoun(word_data):
            log(f'{word_data[1]} identified as pronoun.')
            pronouns.append(word_data)
        elif check_adverb(word_data):
            log(f'{word_data[1]} identified as adverb.')
            adverbs.append(word_data)
        elif check_nominal_verb(word_data):
            log(f'{word_data[1]} identified as nominal form.')
            nominal_verb.append(word_data)
        elif check_noun(word_data):
            log(f'{word_data[1]} identified as noun.')
            nouns.append(word_data)
        elif check_named_entity(word_data):
            log(f'{word_data[1]} identified as named entity and processed as other word.')
            others.append(word_data)
        else:
            log(f'{word_data[1]} identified as other word, but processed as noun with default GNP.')  # treating other words as noun
            nouns.append(word_data)
    return foreign_words,indeclinables, pronouns, nouns, adjectives, verbs, adverbs, others, nominal_verb

def create_auxiliary_verb(index, term, tam, main_verb: Verb):
    # print(index)
    verb = Verb()
    verb.index = main_verb.index + (index + 1)/10
    verb.gender, verb.number, verb.person = main_verb.gender, main_verb.number, main_verb.person
    verb.term = term
    verb.tam = tam
    if verb.term == 'cAha':
            verb.person = 'm_h'
    verb.type = 'auxillary'
    log(f'{verb.term} processed as auxillary verb with index {verb.index} gen:{verb.gender} num:{verb.number} and tam:{verb.tam}')
    return verb


def get_all_form(morph_forms):
    """
    >>> get_first_form("^mAz/mA<cat:n><case:d><gen:f><num:p>/mAz<cat:n><case:d><gen:f><num:s>/mAz<cat:n><case:o><gen:f><num:s>$")
    'mA<cat:n><case:d><gen:f><num:p>/mAz<cat:n><case:d><gen:f><num:s>/mAz<cat:n><case:o><gen:f><num:s>'
    """
    morph=morph_forms.split("$")[1]
    return morph

def get_first_form(morph_forms):
    """
    >>> get_first_form("^mAz/mA<cat:n><case:d><gen:f><num:p>/mAz<cat:n><case:d><gen:f><num:s>/mAz<cat:n><case:o><gen:f><num:s>$")
    'mA<cat:n><case:d><gen:f><num:p>'
    """
    morph=morph_forms.split("/")[1]
    return morph

def get_root_for_kim(relation, anim, gnp):

    animate = ['anim', 'per']
    if relation in ('k2p', 'k7p'):
        return 'kahAz'
    elif relation == 'k5' and has_GNP(gnp):
        return 'kahAz'
    elif relation == 'k7t':
        return 'kaba'
    elif relation == 'rh' and not has_GNP(gnp):
        return 'kyoM'
    elif relation == 'rt' and not has_GNP(gnp): #generate kisa
        return 'kOna'
    elif relation == 'krvn': #generate kEse
        return 'kEsA'
    elif relation == 'k1s':
        return 'kEsA'
    elif has_GNP(gnp) and anim not in animate:
        return 'kyA'
    elif has_GNP(gnp) and anim in animate:
        return 'kOna'
    else:
        return 'kim'

def get_default_GNP():
    gender,number,person,case = 'm','s','a','o'

    return gender, number, person, case

def get_gnpcase_from_concept(concept): #computes GNP values from noun or

    if concept[2] == 'v':
        gender = concept[3]
        number= concept[4]
        person = concept[5]
        case =  concept[7]

    elif concept[2] in ('n', 'p'):
        gender = concept[4]
        number= concept[5]
        person = concept[6]
        case = concept[3]
    else:
        gender, number, person, case = get_default_GNP()
    return gender, number, person, case

def get_TAM(term, tam):
    """
    >>> get_TAM('hE', 'pres')
    'hE'
    >>> get_TAM('hE', 'past')
    'WA'
    >>> get_TAM('asdf', 'gA')
    'gA'
    """
    if term == 'hE' and tam in ('pres', 'past'):
        alt_tam = {'pres': 'hE', 'past': 'WA'}
        return alt_tam[tam]
    else:
        if term == 'jA':
            tam = 'yA1'
            return tam
    return tam

def get_main_verb(term):
    ''' return main verb from a term'''

    pass

def getDataByIndex(value: int, searchList: list, index=0):
    '''search and return data by index in an array of tuples.
        Index should be first element of tuples.
        Return False when index not found.'''
    try:
        res = False
        for dataele in searchList:
            if (dataele[index]) == value:
                res = dataele
    except IndexError:
        log(f'Index out of range while searching index:{value} in {searchList}', 'WARNING')
        return False
    return res

def getComplexPredicateGNP(term):
    CP_term = clean(term.split('+')[0])
    gender = 'm'
    number = 's'
    person = 'a'

    tags = find_tags_from_dix(CP_term)  # getting tags from morph analyzer to assign gender and number for agreement
    if '*' not in tags['form']:
        gender = tags['gen']
        number = tags['num']
    return gender, number, person

def getGNP_using_k2(k2exists, searchList):
    casedata = getDataByIndex(k2exists, searchList)
    if (casedata == False):
        log('Something went wrong. Cannot determine GNP for verb.', 'ERROR')
        sys.exit()
        # return None
    verb_gender, verb_number, verb_person = casedata[4], casedata[5], casedata[6]
    return verb_gender, verb_number, verb_person[0]

def getGNP_using_k1(k1exists, searchList):
    casedata = getDataByIndex(k1exists, searchList)
    if (casedata == False):
        log('Something went wrong. Cannot determine GNP for verb k1 is missing.', 'ERROR')
        sys.exit()
        # return None
    verb_gender, verb_number, verb_person = casedata[4], casedata[5], casedata[6]
    return verb_gender, verb_number, verb_person

def getVerbGNP_new(concept_term, full_tam, is_cp, seman_data, depend_data, sentence_type, processed_nouns, processed_pronouns):
    '''
    '''
    if sentence_type in ('Imperative','imperative') or 'o' in full_tam:
        verb_gender = 'm'
        verb_number = 's'
        verb_person = 'm'
        return verb_gender, verb_number, verb_person

    k1exists = False
    k2exists = False
    k1_case = ''
    k2_case = ''
    verb_gender, verb_number, verb_person, case= get_default_GNP()
    searchList = processed_nouns + processed_pronouns

    for cases in depend_data:
        if cases == '':
            continue
        k1exists = (depend_data.index(cases) + 1) if 'k1' == cases[-2:] else k1exists
        k2exists = (depend_data.index(cases) + 1) if 'k2' == cases[-2:] else k2exists

    if k1exists:
        casedata = getDataByIndex(k1exists, searchList)
        if (casedata == False):
            log('Something went wrong. Cannot determine case for k1.', 'ERROR')
        else:
            k1_case = casedata[3]

    if k2exists:
        casedata = getDataByIndex(k2exists, searchList)
        if (casedata == False):
            log('Something went wrong. Cannot determine case for k2.', 'ERROR')
        else:
            k2_case = casedata[3]

    if is_cp:
        cp_term = concept_term.split('+')[0]
        if not k1exists and not k2exists:
            verb_gender, verb_number, verb_person = getComplexPredicateGNP(cp_term)
        elif k1exists and k1_case == 'd':
            if getGNP_using_k1(k1exists, searchList):
                verb_gender, verb_number, verb_person = getGNP_using_k1(k1exists, searchList)
        elif k1exists and k1_case == 'o' and k2exists and k2_case == 'o':
            verb_gender, verb_number, verb_person = getComplexPredicateGNP(cp_term)
        return verb_gender, verb_number, verb_person[0]

    if 'yA' in full_tam:
        if k1exists and k1_case == 'd':
            if getGNP_using_k1(k1exists, searchList):
                verb_gender, verb_number, verb_person = getGNP_using_k1(k1exists, searchList)
        elif k1exists and k1_case == 'o' and k2exists and k2_case == 'd':
            # if getGNP_using_k2(k2exists, searchList):
            verb_gender, verb_number, verb_person = getGNP_using_k2(k2exists, searchList)
            return verb_gender, verb_number, verb_person[0]
            # else:
            #     return None

    if full_tam in constant.nA_list:
        return verb_gender, verb_number, verb_person[0]

    else:
        # if getGNP_using_k1(k1exists, searchList):
        verb_gender, verb_number, verb_person = getGNP_using_k1(k1exists, searchList)
        return verb_gender, verb_number, verb_person[0]
        # else:
        #     return None

def is_tam_ya(verbs_data):

    ya_tam = '-yA_'
    if len(verbs_data) > 0 and verbs_data != ()     :
        term = verbs_data[1]
        if ya_tam in term:
            return True
    return False

def is_kim(term):
    if term == 'kim':
        return True

    return False

def is_complex_predicate(concept):
    return "+" in concept

def is_CP(term):
    """
    >>> is_CP('varRA+ho_1-gA_1')
    True
    >>> is_CP("kara_1-wA_hE_1")
    False
    """
    if "+" in term:
        return True
    else:
        return False

def is_update_index_NC(i, processed_words):
    for data in processed_words:
        temp = tuple(data)
        if len(temp) > 7 and float(i) == temp[0] and temp[7] == 'NC':
            return True

    return False

def is_nonfinite_verb(concept):
    return concept.type == 'nonfinite'

def has_tam_ya():
    '''Check if USR has verb with TAM "yA".
        It sets the global variable HAS_TAM to true
    '''
    global HAS_TAM
    if HAS_TAM == True:
        return True
    else:
        return False

def has_GNP(gnp_info):
    if len(gnp_info) and ('sg', 'pl') in gnp_info:
        return True
    return False

def has_ques_mark(POST_PROCESS_OUTPUT,sentence_type):

    if sentence_type[1:] in ("yn_interrogative", "yn_interrogative_negative", "pass-yn_interrogative", "interrogative",
                        "Interrogative", "pass-interrogative"):
        return 'kyA ' + POST_PROCESS_OUTPUT + ' ?'
    elif sentence_type[1:] in ('pass-affirmative','affirmative', 'Affirmative', 'negative', 'Negative', 'imperative', 'Imperative',"fragment","term","title","heading"):
        return POST_PROCESS_OUTPUT + ' |'

def identify_case(verb, dependency_data, processed_nouns, processed_pronouns):
    return getVerbGNP_new(verb.term, verb.tam, dependency_data, processed_nouns, processed_pronouns)

def identify_main_verb(concept_term):
    """
    >>> identify_main_verb("kara_1-wA_hE_1")
    'kara'
    >>> identify_main_verb("varRA+ho_1-gA_1")
    'ho'
    """
    if ("+" in concept_term):
        concept_term = concept_term.split("+")[1]
    con=clean(concept_term.split("-")[0])
    return con

def identify_default_tam_for_main_verb(concept_term):
    """
    >>> identify_default_tam_for_main_verb("kara_1-wA_hE_1")
    'wA'
    >>> identify_default_tam_for_main_verb("kara_1-0_rahA_hE_1")
    '0'
    """
    try:
        con = concept_term.split("-")[1].split("_")[0]
        return con
    except IndexError:
        print(f"IndexError: concept_term '{concept_term}' does not have the expected format")
        return None


def identify_complete_tam_for_verb(concept_term):
    """
    >>> identify_complete_tam_for_verb("kara_1-wA_hE_1")
    'wA_hE'
    >>> identify_complete_tam_for_verb("kara_1-0_rahA_hE_1")
    'rahA_hE'
    >>> identify_complete_tam_for_verb("kara_1-nA_howA_hE_1")
    'nA_howA_hE'
    >>> identify_complete_tam_for_verb("kara_o")
    'o'
    """
    if "-" not in concept_term:
        return concept_term.split("_")[1]
    tmp = concept_term.split("-")[1]
    tokens = tmp.split("_")
    non_digits = filter(lambda x: not x.isdigit(), tokens)
    tam_v="_".join(non_digits)
    return tam_v

def identify_auxillary_verb_terms(term):
    """
    >>> identify_auxillary_verb_terms("kara_1-wA_hE_1")
    ['hE']
    >>> identify_auxillary_verb_terms("kara_1-0_rahA_hE_1")
    ['rahA', 'hE']
    """
    aux_verb_terms = term.split("-")[1].split("_")[1:]
    cleaned_terms = map(clean, aux_verb_terms)
    el=list(filter(lambda x: x != '', cleaned_terms))
    return el            # Remove empty strings after cleaning

def identify_verb_type(verb_concept):
    '''
    >>identify_verb_type([])
    '''
    dependency = verb_concept.dependency
    dep_rel = dependency.strip().split(':')[1]
    v_type = ''
    if dep_rel == 'main':
        v_type = "main"
    elif dep_rel in ('rpk', 'rbk', 'rvks', 'rbks', 'rsk', 'rblpk','rblak'):
        v_type = "nonfinite"
    else:
        v_type = "main"
    return v_type

# def findExactMatch(value: int, searchList: list, index=0):
#     '''search and return data by index in an array of tuples.
#         Index should be first element of tuples.

#         Return False when index not found.'''

#     try:
#         for dataele in searchList:
#             if value == dataele[index].strip().split(':')[1]:
#                 return (True, dataele)
#     except IndexError:
#         log(f'Index out of range while searching index:{value} in {searchList}', 'WARNING')
#         return (False, None)
#     return (False, None)

# def findValue(value: int, searchList: list, index=0):
#     '''search and return data by index in an array of tuples.
#         Index should be first element of tuples.

#         Return False when index not found.'''

#     try:
#         for dataele in searchList:
#             if value == dataele[index]:
#                 return (True, dataele)
#     except IndexError:
#         log(f'Index out of range while searching index:{value} in {searchList}', 'WARNING')
#         return (False, None)
#     return (False, None)

def find_tags_from_dix(word):
    """
    >>> find_tags_from_dix("mAz")
    {'cat': 'n', 'case': 'd', 'gen': 'f', 'num': 'p', 'form': 'mA'}
    """
    dix_command = "echo {} | apertium-destxt | lt-proc -ac hi.morfLC.bin | apertium-retxt".format(word)
    morph_forms = os.popen(dix_command).read()
    p_m=parse_morph_tags(morph_forms)
    return p_m

def find_tags_from_dix_as_list(word):
    """
    >>> find_tags_from_dix("mAz")
    {'cat': 'n', 'case': 'd', 'gen': 'f', 'num': 'p', 'form': 'mA'}
    """
    dix_command = "echo {} | apertium-destxt | lt-proc -ac hi.morfLC.bin | apertium-retxt".format(word)
    morph_forms = os.popen(dix_command).read()
    p_m=parse_morph_tags_as_list(morph_forms)
    return p_m

def find_exact_dep_info_exists(index, dep_rel, words_info):
    for word in words_info:
        dep = word[4]
        dep_head = word[4].strip().split(':')[0]
        dep_val = word[4].strip().split(':')[1]
        if dep_val == dep_rel and int(dep_head) == index:
            return True

    return False

def find_match_with_same_head(data_head, term, words_info, index):
     for dataele in words_info:
        dataele_index = dataele[0]
        dep_head = dataele[index].strip().split(':')[0]
        dep_value = dataele[index].strip().split(':')[1]
        if str(data_head) == dep_head and term == dep_value:
            return True, dataele_index
     return False, -1

def parse_morph_tags(morph_form):
    """
    >>> parse_morph_tags("mA<cat:n><case:d><gen:f><num:p>")
    {'cat': 'n', 'case': 'd', 'gen': 'f', 'num': 'p', 'form': 'mA'}
    """
    form = morph_form.split("<")[0]
    matches = re.findall("<(.*?):(.*?)>", morph_form)
    result = {match[0]: match[1] for match in matches}
    result["form"] = form
    return result

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

def generate_input_for_morph_generator(input_data):
    """Process the input and generate the input for morph generator"""
    morph_input_data = []
    for data in input_data:
        if data[2] == 'p':
            if data[8] != None and isinstance(data[8], str):
                morph_data = f'^{data[1]}<cat:{data[2]}><parsarg:{data[7]}><fnum:{data[8]}><case:{data[3]}><gen:{data[4]}><num:{data[5]}><per:{data[6]}>$'
            else:
                morph_data = f'^{data[1]}<cat:{data[2]}><case:{data[3]}><parsarg:{data[7]}><gen:{data[4]}><num:{data[5]}><per:{data[6]}>$'
        elif data[2] == 'n' and data[7] in ('proper', 'digit'):
            morph_data = f'{data[1]}'
        elif data[2] == 'n' and data[7] == 'vn':
            morph_data = f'^{data[1]}<cat:{data[7]}><case:{data[3]}>$'
        elif data[2] == 'n' and data[7] != 'proper':
            morph_data = f'^{data[1]}<cat:{data[2]}><case:{data[3]}><gen:{data[4]}><num:{data[5]}>$'

        elif data[2] == 'v' and data[8] in ('main','auxillary'):
            morph_data = f'^{data[1]}<cat:{data[2]}><gen:{data[3]}><num:{data[4]}><per:{data[5]}><tam:{data[6]}>$'
        elif data[2] == 'v' and data[6] == 'kara' and data[8] in ('nonfinite','adverb')     :
            morph_data = f'^{data[1]}<cat:{data[2]}><gen:{data[3]}><num:{data[4]}><per:{data[5]}><tam:{data[6]}>$'
        elif data[2] == 'v' and data[6] != 'kara' and data[8] =='nonfinite':
            morph_data = f'^{data[1]}<cat:{data[2]}><gen:{data[3]}><num:{data[4]}><case:{data[7]}><tam:{data[6]}>$'
        elif data[2] == 'adj':
            morph_data = f'^{data[1]}<cat:{data[2]}><case:{data[3]}><gen:{data[4]}><num:{data[5]}>$'
        elif data[2] == 'indec':
            morph_data = f'{data[1]}'
        elif data[2] == 'other':
            morph_data = f'{data[1]}'
        else:
            morph_data = f'^{data[1]}$'
        morph_input_data.append(morph_data)
    return morph_input_data

def write_data(writedata):
    """Write the Morph Input Data into a file"""
    final_input = " ".join(writedata)
    with open("morph_input.txt", 'w', encoding="utf-8") as file:
        file.write(final_input + "\n")
    return "morph_input.txt"

def run_morph_generator(input_file):
    """ Pass the morph generator through the input file"""
    fname = f'{input_file}-out.txt'
    f = open(fname, 'w')
    subprocess.run(f"sh ./run_morph-generator.sh {input_file}", stdout=f, shell=True)
    return "morph_input.txt-out.txt"

def generate_morph(processed_words):
    """Run Morph generator"""
    morph_input = generate_input_for_morph_generator(processed_words)
    MORPH_INPUT_FILE = write_data(morph_input)
    OUTPUT_FILE = run_morph_generator(MORPH_INPUT_FILE)
    return OUTPUT_FILE

def read_output_data(output_file):
    """Check the output file data for post processing"""

    with open(output_file, 'r') as file:
        data = file.read()
    return data

def analyse_output_data(output_data, morph_input):
    print(output_data, morph_input, 'morph_input')
    output_data = output_data.strip().split(" ")
    combine_data = []

    for i in range(len(output_data)):
        try:
            morph_input_list = list(morph_input[i])
            morph_input_list[1] = output_data[i]
            combine_data.append(tuple(morph_input_list))
        except IndexError:
            print(f"IndexError: output_data and morph_input lengths are mismatched at index {i}")
            break
    return combine_data


def handle_compound_nouns(noun, processed_nouns, category, case, gender, number, person, postposition):
    dnouns = noun[1].split('+')
    for k in range(len(dnouns)):
        index = noun[0] + (k * 0.1)
        noun_type = 'NC'
        clean_dnouns = clean(dnouns[k])
        if k == len(dnouns) - 1:
            noun_type = 'NC_head'
            dict_index = index
            processed_nouns.append(
                (index, clean_dnouns, category, case, gender, number, person, noun_type, postposition))
        else:
            processed_nouns.append((index, clean_dnouns, category, case, gender, number, person, noun_type, ''))

    if noun[0] in processed_postpositions_dict:
        processed_postpositions_dict[dict_index] = processed_postpositions_dict.pop(noun[0])
    return processed_nouns

def handle_unprocessed(outputData, processed_nouns):
    """swapping gender info that does not exist in dictionary."""
    output_data = outputData.strip().split(" ")
    has_changes = False
    dataIndex = 0  # temporary [to know index value of generated word from sentence]
    for data in output_data:
        dataIndex = dataIndex + 1
        if data[0] == '#':
            for i in range(len(processed_nouns)):
                ind = round(processed_nouns[i][0])
                if round(processed_nouns[i][0]) == dataIndex:
                    if processed_nouns[i][7] not in ('proper','NC','CP_noun', 'abs', 'vn'):
                        has_changes = True
                        temp = list(processed_nouns[i])
                        temp[4] = 'f' if processed_nouns[i][4] == 'm' else 'm'
                        processed_nouns[i] = tuple(temp)
                        log(f'{temp[1]} reprocessed as noun with gen:{temp[4]}.')
                    else:
                        break
    return has_changes, processed_nouns

def nextNounData_fromFullData(fromIndex, PP_FullData):
    index = fromIndex
    for data in PP_FullData:
        if data[0] > index:
            if data[2] == 'n':
                return data

    return ()
def nextNounData(fromIndex, word_info):
    index = fromIndex
    for i in range(len(word_info)):
        for data in word_info:
            if index == data[0]:
                if data[3] != '' and index != fromIndex:
                    return data
    return False

def fetchNextWord(index, words_info):
    next_word = ''
    for data in words_info:
        if index == data[0]:
            next_word = clean(data[1])
    return next_word

def change_gender(current_gender):
    """
    >>> change_gender('m')
    'f'
    >>> change_gender('f')
    'm'
    """
    return 'f' if current_gender == 'm' else 'm'

def set_gender_make_plural(processed_words, g, num):
    process_data = []
    for i in range(len(processed_words)):
        word_list = list(processed_words[i])
        if word_list[2] == 'adj':
            word_list[4] = g
            word_list[5] = num
        elif word_list[2] == 'v':
            word_list[3] = g
            word_list[4] = num
        process_data.append(tuple(word_list))
    return process_data

def set_main_verb_tam_zero(verb: Verb):
    verb.tam = 0
    return verb

def set_tam_for_nonfinite(dependency):
    '''
    Sets the TAM (Tense-Aspect-Mood) for non-finite verb forms based on the given dependency code.

    Parameters:
        dependency (str): The dependency code indicating the type of non-finite form.

    Returns:
        str: The TAM code for the given non-finite form.

    Examples:
        >>> set_tam_for_nonfinite('rvks')
        'adj_wA_huA'
        >>> set_tam_for_nonfinite('rbks')
        'yA_huA'
        >>> set_tam_for_nonfinite('rsk')
        'wA_huA'
        >>> set_tam_for_nonfinite('rpk')
        'kara'
    '''
    tam = {
        'rvks': 'adj_wA_huA',
        'rpk': 'kara',
        'rsk': 'adj_wA_huA',
        'rbks': 'adj_yA_huA',
        'rblpk': 'nA',
        'rbk': 'yA_gayA'
    }.get(dependency, '')
    return tam

def update_ppost_dict(data_index, param):
    processed_postpositions_dict[data_index] = param

def extract_gnp_noun(noun_data):
    gender = 'm'
    number = 's'
    person = 'a'

    if len(noun_data):
        noun_term = noun_data[1]
        if check_is_digit(noun_term):
            noun_term = noun_term
        elif '+' in noun_term:
            cn_terms = noun_term.strip().split('+')
            for i in range(len(cn_terms)):
                if i == len(cn_terms) - 1:
                    noun_term = clean(cn_terms[i])
        else:
            noun_term = clean(noun_term)

        seman_data = noun_data[2].strip()
        if len(seman_data) > 0:
            if 'male' in seman_data:
                gender = 'm'
            elif 'female' in seman_data:
                gender = 'f'
        else:
            tags = find_tags_from_dix(noun_term)
            if '*' not in tags['form']:
                gender = tags['gen']

        if len(noun_data[3]):
            number = noun_data[3].strip()[0]

        if noun_term == 'speaker':
            person = 'u'
        elif noun_term == 'addressee':
            person = 'm'
        else:
            person = 'a'
    return gender, number, person

def extract_gnp(data):
    gender = 'm'
    number = 's'
    person = 'a'

    if len(data):
        term = clean(data[1])

        seman_data = data[2].strip()
        if len(seman_data) > 0:
            if 'male' in seman_data:
                gender = 'm'
            elif 'female' in seman_data:
                gender = 'f'

        if len(data[3]):
            number = data[3].strip()[0]

        if term == 'speaker':
            person = 'u'
        elif term == 'addressee':
            person = 'm'
        else:
            person = 'a'
    return gender, number, person

def fetch_NC_head(i, processed_words):
    for data in processed_words:
        temp = tuple(data)
        if int(temp[0]) == int(i) and temp[7] == 'NC_head':
            return temp[0]

def auxmap_hin(aux_verb):
    """
    Finds auxillary verb in auxillary mapping file. Returns its root and tam.
    >>> auxmap_hin('sakawA')
    ('saka', 'wA')
    """
    try:
        with open(constant.AUX_MAP_FILE, 'r') as tamfile:
            for line in tamfile.readlines():
                aux_mapping = line.strip().split(',')
                if aux_mapping[0] == aux_verb:
                    return aux_mapping[1], aux_mapping[2]
        log(f'"{aux_verb}" not found in Auxillary mapping.', 'WARNING')
        return None, None       # TODO Figure out the fallback
    except FileNotFoundError:
        log('Auxillary Mapping File not found.', 'ERROR')
        sys.exit()

def update_additional_words_dict(index, tag, add_word):
    value = (tag, add_word)
    value_found = False
    if index in additional_words_dict:
        value_list = additional_words_dict[index]
        for data in value_list:
            if data[0] == tag and data[1] == add_word:
                value_found = True
        if not value_found:
            additional_words_dict[index].append(value)
            print('update_additional_words_dict : ',additional_words_dict[index])
    else:
        additional_words_dict[index] = [value]
        print('update_additional_words_dict : ',additional_words_dict[index])

def to_tuple(verb: Verb):
    return (verb.index, verb.term, verb.category, verb.gender, verb.number, verb.person, verb.tam, verb.case, verb.type)

def postposition_finalization(processed_nouns, processed_pronouns,processed_foreign_words, words_info):
    for data in words_info:
        data_index = data[0]
        dep = data[4].strip().split(':')[1]
        head = data[4].strip().split(':')[0]

        if dep == 'r6':
            for noun in processed_nouns:
                index = noun[0]
                case = noun[3]
                if head == str(index) and case == 'o':
                    update_ppost_dict(data_index, 'ke')

            for pronoun in processed_pronouns:
                index = pronoun[0]
                case = pronoun[3]
                if head == str(index) and case == 'o':
                    update_ppost_dict(data_index, 'ke')

def collect_processed_data(processed_foreign_words,processed_pronouns, processed_nouns, processed_adjectives, processed_verbs,
                           processed_auxverbs, processed_indeclinables, processed_others):
    """collect sort and return processed data."""
    sorted_data=sorted(processed_foreign_words+processed_pronouns + processed_nouns + processed_adjectives + processed_verbs + processed_auxverbs + processed_indeclinables + processed_others)
    return sorted_data

def join_compounds(transformed_data, construction_data):
    '''joins compound words without spaces'''
    resultant_data = []
    prevword = ''
    previndex = -1

    for data in sorted(transformed_data):
        if (data[0]) == previndex and data[2] == 'n':
            temp = list(data)
            temp[1] = prevword + ' ' + temp[1]
            data = tuple(temp)
            resultant_data.pop()
        resultant_data.append(data)
        previndex = data[0]
        prevword = data[1]
    return resultant_data

def populate_morpho_semantic_dict(gnp_info, PPfull_data,words_info):
    populate_morpho_semantic_dict = False
    morpho_seman = ['comper_more', 'comper-more', 'comper_less', 'comper-less', 'superl', 'mawupa', 'mawup','ditva']
    a = 'after'
    b = 'before'
    for i in range(len(gnp_info)):
        input_string = gnp_info[i]
        matches = re.findall(r'\[(.*?)\]', input_string)
        strings = [s.strip() for s in matches]

        for term in strings:
            if term in morpho_seman:
                populate_morpho_semantic_dict = True
                if term == 'superl':
                    temp = (b, 'sabase')

                elif term in ('comper_more', 'comper-more'):
                    temp = (b, 'aXika')

                elif term in ('comper_less', 'comper-less'):
                    temp = (b, 'kama')
                elif term == 'ditva':
                    dup_word = clean(words_info[i][1])
                    if dup_word in PPfull_data[i][1]:
                        dup_word1 = dup_word + ' '
                        PPfull_data[i] = list(PPfull_data[i])
                        PPfull_data[i][1] = PPfull_data[i][1].replace(dup_word, dup_word1)
                        PPfull_data[i] = tuple(PPfull_data[i])

                        temp = (b, dup_word)

                else:
                    curr_index = i + 1
                    noun_data = nextNounData_fromFullData(curr_index + 1, PPfull_data)
                    if noun_data != ():
                        g = noun_data[4]
                        n = noun_data[5]
                        p = noun_data[6]
                        if g == 'f':
                            temp = (a, 'vAlI')
                        elif n == 'p':
                            temp = (a, 'vAle')
                        elif n == 's':
                            temp = (a, 'vAlA')
                if i + 1 in MORPHO_SEMANTIC_DICT:
                    MORPHO_SEMANTIC_DICT[i + 1].append(temp)
                else:
                    MORPHO_SEMANTIC_DICT[i + 1] = [temp]
    return populate_morpho_semantic_dict,PPfull_data

def join_indeclinables(transformed_data, processed_indeclinables, processed_others):

    """Joins Indeclinable data with transformed data and sort it by index number."""
    return sorted(transformed_data + processed_indeclinables + processed_others)

def rearrange_sentence(fulldata):
    '''Function comments'''
    finalData = sorted(fulldata)
    final_words = [x[1].strip() for x in finalData]
    r_s=" ".join(final_words)
    return r_s

def collect_hindi_output(source_text):
    print(source_text)
    """Take the output text and find the hindi text from it."""
    hindi_format = WXC(order="wx2utf", lang="hin")
    generate_hindi_text = hindi_format.convert(source_text)
    return generate_hindi_text

def process_coref(input_text):
    coref_list=[]
    folder_path = sys.argv[1].split('/')[0]
    file_name_line = None    
    for i in range(len(input_text)):
        if 'coref' in input_text[i] and '.' in input_text[i]:
            coref_list.append(i)
            file_name_line = input_text[i]
            file_name = file_name_line.split('.')[0]
            digit = file_name_line.split('.')[1].split(':')[0]

            file_path = os.path.join(folder_path, f'{file_name}')
            if not os.path.exists(file_path):
                file_path += '.txt'
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"File '{file_path}' not found")
            with open(file_path, 'r', encoding='utf-8') as file:
                file_contents = file.readlines()

            coref_word=file_contents[1].split(',')[int(digit)-1]
            coref_list.append(coref_word)
            return coref_list
    else:
        return None

def reset_global_dicts():
    global additional_words_dict, processed_postpositions_dict, construction_dict, spkview_dict, MORPHO_SEMANTIC_DICT
    additional_words_dict.clear()
    processed_postpositions_dict.clear()
    construction_dict.clear()
    spkview_dict.clear()
    MORPHO_SEMANTIC_DICT.clear()


if __name__ == '__main__':
    import doctest
    doctest.run_docstring_examples(identify_complete_tam_for_verb, globals())

