import os
import sys
import re
import subprocess
import constant
from wxconv import WXC
from verb import Verb
from concept import Concept

noun_attribute = dict()
USR_row_info = ['root_words', 'index_data', 'seman_data', 'gnp_data', 'depend_data', 'discourse_data', 'spkview_data', 'scope_data']
nA_list = ['nA_paDa', 'nA_padZA', 'nA_padA', 'nA_hE', 'nA_WA', 'nA_hogA', 'nA_cAhie', 'nA_cAhiye']
spkview_list = ['hI', 'BI', 'jI', 'wo', 'waka', 'lagaBaga', 'lagAwAra', 'kevala']
kisase_k2g_verbs = ['bola', 'pUCa', 'kaha', 'nikAla', 'mAzga']
kisase_k2_verbs = ['mila', 'pyAra']
kisase_k5_verbs = ['dara', 'baca', 'rakSA']
kahAz_k5_verbs = ['A', 'uga', 'gira']
processed_postpositions_dict = {}
construction_dict = {}
spkview_dict = {}
MORPHO_SEMANTIC_DICT = {}
additional_words_dict = {}
discourse_dict = {'samuccaya': ['Ora', 'evaM', 'waWA', 'nA kevala'], 'AvaSyakawApariNAma': ['wo', 'nahIM wo'], 'kAryakAraNa': ['kyoMki', 'cUzki', 'cUMki', 'isake kAraNa'], 'pariNAma': ['isIlie', 'isalie', 'awaH', 'isake pariNAmasvarUpa', 'isI kAraNa', 'isa kAraNa'], 'viroXI_xyowaka': ['jabaki'], 'vyaBicAra': ['yaxyapi', 'waWApi', 'hAlAzki', 'Pira BI','isake bAvajZUxa'], 'viroXI': ['lekina', 'kiMwu', 'paraMwu', 'isake viparIwa', 'viparIwa'], 'anyawra': ['yA', 'aWavA'], 'samuccaya x': ['isake alAvA', 'isake awirikwa', 'isake sAWa-sAWa', 'isake sAWa sAWa']}


def read_file(file_path):
    print('Running read_file')
    '''
    Functionality: To read the file from mentioned file_path.
    Exception: If file_path is incorrect raise an exception - "No such File found." and exit the program
    Parameters:
        file_path - path of file to be read
    Returns:
        Returns array of lines for data given in file
    '''

    log(f'File ~ {file_path}')
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            file_rows = []
            for i in range(len(lines)):
                lineContent = lines[i]
                if i == 10:
                    if lineContent.strip() == '':
                        break
                    else:
                        file_rows.append(lineContent)

            log('File data read.')
    except FileNotFoundError:
        log('No such File found.', 'ERROR')
        sys.exit()
    print('read_file : ',lines)
    return lines

def log(mssg, logtype='OK'):
    '''Generates log message in predefined format.'''

    print(f'log : [{logtype}]:{mssg}')
    if logtype == 'ERROR':
        path = sys.argv[1]
        write_hindi_test(' ', 'Error', mssg, 'test.csv', path)

def write_hindi_text(hindi_output, POST_PROCESS_OUTPUT, OUTPUT_FILE):
    print('Running write_hindi_text')
    """Append the hindi text into the file"""
    with open(OUTPUT_FILE, 'w') as file:
        file.write(POST_PROCESS_OUTPUT)
        file.write('\n')
        file.write(hindi_output)
        log('Output data write successfully')
    return "Output data write successfully"

def write_hindi_test(hindi_output, POST_PROCESS_OUTPUT, src_sentence, OUTPUT_FILE, path):
    print('Running write_hindi_test')
    """Append the hindi text into the file"""
    OUTPUT_FILE = 'TestResults.csv'# temporary for presenting
    str = path.strip('lion_story/')
    if str == '1':
        with open(OUTPUT_FILE, 'w') as file:
            file.write("")

    with open(OUTPUT_FILE, 'a') as file:
        file.write(path.strip('../hindi_gen/lion_story') + '\t')
        file.write(src_sentence.strip('"').strip('\n').strip('#') + '\t')
        file.write(POST_PROCESS_OUTPUT + '\t')
        file.write(hindi_output + '\t')
        file.write('\n')
        log('Output data write successfully')
    return "Output data write successfully"

def write_masked_hindi_test(hindi_output, POST_PROCESS_OUTPUT, src_sentence, masked_data, OUTPUT_FILE, path):
    print('Running write_masked_hindi_test')
    """Append the hindi text into the file"""
    OUTPUT_FILE = 'TestResults_masked.csv'  # temporary for presenting
    with open(OUTPUT_FILE, 'a') as file:
        file.write(path.strip('lion_story/') + ',')
        file.write(src_sentence.strip('#') + ',')
        file.write(POST_PROCESS_OUTPUT + ',')
        file.write(hindi_output + ',')
        file.write(masked_data)
        file.write('\n')
        log('Output data write successfully')
    return "Output data write successfully"

def masked_postposition(processed_words, words_info, processed_verbs):
    print('Running masked_postposition')
    '''Calculates masked postposition to words wherever applicable according to rules.'''
    masked_PPdata = {}

    for data in processed_words:
        if data[2] not in ('p', 'n', 'other'):
            continue
        data_info = getDataByIndex(data[0], words_info)
        try:
            data_case = False if data_info == False else data_info[4].split(':')[1].strip()
        except IndexError:
            data_case = False
        ppost = ''
        ppost_value = '<>'
        if data_case in ('k1', 'pk1'):
            if findValue('yA', processed_verbs, index=6)[0]:  # has TAM "yA"
                if findValue('k2', words_info, index=4)[0]: # or findExactMatch('k2p', words_info, index=4)[0]:
                    ppost = ppost_value
        elif data_case in ('r6', 'k3', 'k5', 'k5prk', 'k4', 'k4a', 'k7t', 'jk1','k7', 'k7p','k2g', 'k2','rsk', 'ru' ):
            ppost = ppost_value
        elif data_case == 'krvn' and data_info[2] == 'abs':  #abstract noun as adverb
            ppost = ppost_value
        elif data_case in ('k2g', 'k2') and data_info[2] in ("anim", "per"):
            ppost = ppost_value #'ko'
        elif data_case in ('rsm', 'rsma'):
            ppost = ppost_value+ ' ' + ppost_value #ke pAsa
        elif data_case == 'rt':
            ppost = ppost_value+ ' ' + ppost_value #'ke lie'
        elif data_case == 'rv':
            ppost = ppost_value+ ' ' + ppost_value + ' ' + ppost_value#'kI tulanA meM'
        elif data_case == 'r6':
            ppost = ppost_value # 'kI' if data[4] == 'f' else 'kA'
            nn_data = nextNounData(data[0], words_info)
            if nn_data != False:
                if nn_data[4].split(':')[1] in ('k3', 'k4', 'k5', 'k7', 'k7p', 'k7t', 'mk1', 'jk1', 'rt'):
                    ppost = ppost_value
                elif nn_data[3][1] != 'f' and nn_data[3][3] == 'p':
                    ppost = ppost_value#'ke'
                else:
                    pass
        else:
            pass
        if data[2] == 'p':
            temp = list(data)
            temp[7] = ppost if ppost != '' else 0
            data = tuple(temp)
        if data[2] == 'n' or data[2] == 'other':
            temp = list(data)
            temp[8] = ppost if ppost != '' else None
            data = tuple(temp)
            masked_PPdata[data[0]] = ppost
    return masked_PPdata

def clean(word, inplace=''):
    print('Running clean')
    """
    Clean concept words by removing numbers and special characters from it using regex.
    >>> clean("kara_1-yA_1")
    'karayA'
    >>> clean("kara_1")
    'kara'
    >>> clean("padZa_1")
    'pada'
    >>> clean("caDZa_1")
    'caDa'

    """
    newWord = word
    if 'dZ' in word:  # handling words with dZ/jZ -Kirti - 15/12
        newWord = word.replace('dZ', 'd')
    elif 'jZ' in word:
        newWord = word.replace('jZ', 'j')
    elif 'DZ' in word:
        newWord = word.replace('DZ', 'D')

    clword = re.sub(r'[^a-zA-Z]+', inplace, newWord)
    print('clean : ',clword)
    return clword

def generate_rulesinfo(file_data):
    print('Running generate_rulesinfo')
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
    print('generate_rulesinfo : ',[src_sentence, root_words, index_data, seman_data, gnp_data, depend_data, discourse_data, spkview_data,
            scope_data, sentence_type, construction_data])
    return [src_sentence, root_words, index_data, seman_data, gnp_data, depend_data, discourse_data, spkview_data,
            scope_data, sentence_type, construction_data]

def populate_spkview_dict(spkview_info):
    populate_spk_dict = False
    a = 'after'
    b = 'before'
    for i in range(len(spkview_info)):
        clean_spk_info = spkview_info[i].rstrip('_1234567890')
        if clean_spk_info in spkview_list:
            populate_spk_dict = True
            temp = (a, clean_spk_info)
            spkview_dict[i + 1] = [temp]
        elif clean_spk_info == 'result':
            populate_spk_dict = True
            temp = (b, 'pariNAmasvarUpa,')
            spkview_dict[i + 1] = [temp]

    return populate_spk_dict

def generate_wordinfo(root_words, index_data, seman_data, gnp_data, depend_data, discourse_data, spkview_data,
                      scope_data):
    print('Running generate_wordinfo')
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
    print('generate_wordinfo : ',root_words, index_data, seman_data, gnp_data, depend_data, discourse_data, spkview_data, scope_data)
    return list(
        zip(index_data, root_words, seman_data, gnp_data, depend_data, discourse_data, spkview_data, scope_data))











def identify_cat(words_list):
    print('Running identify_cat')
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
    print('identify_cat : ',foreign_words,indeclinables, pronouns, nouns, adjectives, verbs, adverbs, others, nominal_verb)
    return foreign_words,indeclinables, pronouns, nouns, adjectives, verbs, adverbs, others, nominal_verb


def check_named_entity(word_data):
    print('Running check_named_entity')
    if word_data[2] == 'ne':
        return True
    return False

def check_noun(word_data):
    print('Running check_noun')
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
        print(word_data[3],'vss')

        if word_data[3] in ('pl'):
            return True
        return False
    except IndexError:
        log(f'Index Error for GNP Info. Checking noun for {word_data[1]}', 'ERROR')
        sys.exit()


def check_pronoun(word_data):
    print('Running check_pronoun')
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
    print('Running check_adjective')
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
    print('Running check_nonfinite_verb')
    '''Check if word is a non-fininte verb by the USR info'''

    if word_data[4] != '':
        rel = word_data[4].strip().split(':')[1]
        if rel in ('rpk','rbk', 'rvks', 'rbks','rsk', 'rbplk'):
            return True
    return False

def check_verb(word_data):
    print('Running check_verb')
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
    print('Running check_adverb')
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
    print('Running check_indeclinable')
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
    print('Running check_digit')
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
    print('Running check_nominal_verb')
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
        if relation in constant.NOMINAL_VERB_DEPENDENCY and gnp_info == '':
            return True
    return False

def check_is_digit(num):
    print('Running check_is_digit')
    if num.isdigit():
        return True
    else:
        try:
            float_value = float(num)
            return True
        except ValueError:
            return False
    return False

def process_foreign_word(foreign_words_data,words_info,verbs_data):
    print('Running process_foreign_word')
    for verb in verbs_data:
       if verb[4].strip().split(':')[1] == 'main':
           main_verb = verb
           break
    processed_foreign_words=[]
    for i in range(len(foreign_words_data)):
        index=foreign_words_data[i][0]
        gender, number, person, case = get_default_GNP()
        category='n'
        type=''
        foreign_list = list(foreign_words_data[i])
        
        foreign_list[1] = foreign_list[1].replace('^','')
        if '_' in foreign_list[1]:
            foreign_list[1]=clean(foreign_list[1])
        foreign_words_data[i] = tuple(foreign_list)
        case,postposition = preprocess_postposition_new('noun', foreign_words_data[i], words_info, main_verb)
        print(postposition,foreign_words_data[i],'ttt')

        processed_foreign_words.append((index,foreign_words_data[i][1],category,case,gender,number,person,type,postposition))
        
    print('process_foreign_word : ',processed_foreign_words)
    return processed_foreign_words


def preprocess_postposition_new(concept_type, np_data, words_info, verb_data):
    print('Running preprocess_postposition_new')
    '''Calculates postposition to words wherever applicable according to rules.'''
    cp_verb_list = ['prayApreprsa+kara','sahAyawA+kara']
    if len(verb_data) > 0:
        verb_term = verb_data[1]
        if len(verb_term) > 0:
            root_main = verb_term.strip().split('-')[0].split('_')[0]
    if np_data != ():
        data_case = np_data[4].strip().split(':')[1]
        data_head = np_data[4].strip().split(':')[0]
        data_index = np_data[0]
        data_seman = np_data[2]
    ppost = ''
    new_case = 'o'
    if data_case in ('k1', 'pk1'):
        if is_tam_ya(verb_data): # has TAM "yA" or "yA_hE" or "yA_WA" marA WA
            k2exists, k2_index = find_match_with_same_head(data_head, 'k2', words_info, index=4) # or if CP_present, then also ne - add #get exact k2, not k2x
            vk2exists, vk2_index = find_match_with_same_head(data_head, 'vk2', words_info, index=4)
            if k2exists:
                ppost = 'ne'
                if is_CP(verb_term):
                    cp_parts = verb_term.strip().split('+')
                    clean_cp_term = ''
                    for part in cp_parts:
                        part = part.split("-")[0]
                        clean_cp_term = clean_cp_term + clean(part) + '+'
                    clean_cp_term = clean_cp_term[0:-1]
                    if clean_cp_term in cp_verb_list:
                        update_additional_words_dict(k2_index, 'after', 'kA')

            elif vk2exists:
                ppost = 'ne'
            else:
                ppost = ''
                log('Karma k2 not found. Output may be incorrect')

        elif identify_complete_tam_for_verb(verb_term) in nA_list:
            ppost = 'ko'
        else:
            log('inside tam ya else')

    elif data_case == 'k2g':
        ppost = process_dep_k2g(data_case, verb_data)
    elif data_case == 'k2': #if CP present, and if concept is k2 for verb of CP, and the verb is not in specific list, then kA
        if data_seman and data_seman!=''and data_seman.split()[0] in ("anim", "per"):
            if clean(root_main) in kisase_k2_verbs:
                ppost = 'se'
            else:
                ppost = 'ko'
        else:
            new_case = 'd'

    elif data_case == 'k2p':
        ppost = '' # modified from meM 22/06
    elif data_case in ('k3', 'k5', 'k5prk'):
        ppost = 'se'
    elif data_case in ('k4', 'k4a', 'k7t', 'jk1'):
        ppost = 'ko'
    elif data_case == 'k7p':
        ppost = 'meM'
    elif data_case =='k7':
        ppost = 'para'
    elif data_case == 'krvn' and data_seman == 'abs':
        ppost = 'se'
    elif data_case == 'rt':
        ppost = 'ke lie'
    elif data_case in ('rsm', 'rsma'):
        ppost = 'ke pAsa'
    elif data_case == 'rhh':
        ppost = 'ke'
    elif data_case == 'rsk':
        ppost = 'hue'
    elif data_case == 'rn':
        ppost = 'meM'
    elif data_case == 'rib':
        ppost = 'se'
    elif data_case == 'ru':
        ppost = 'jEsI'
    elif data_case == 'rkl':
        next_word = fetchNextWord(data_index + 1, words_info)
        if next_word == 'bAxa':
            ppost = 'ke'
        elif next_word == 'pahale':
            ppost = 'se'

    elif data_case == 'rdl':
        next_word = fetchNextWord(data_index + 1, words_info)
        if next_word in ('anxara', 'bAhara', 'Age', 'sAmane', 'pICe', 'Upara', 'nIce', 'xAyeM',
                         'bAyeM', 'cAroM ora', 'bIca', 'pAsa'):
            ppost = 'ke'
        elif next_word == 'xUra':
            ppost = 'se'

    elif data_case == 'rv':
        ppost = 'se'
    elif data_case == 'rh':
        ppost = 'ke_kAraNa'
    elif data_case == 'rd':
        ppost = 'kI ora'
    elif 'rask' in data_case:
        ppost = 'ke sAWa'
    elif data_case == 'r6':
        ppost = 'kA' #if data[4] == 'f' else 'kA'
        nn_data = nextNounData(data_index, words_info)
        if nn_data != False:
            if nn_data[4].split(':')[1] in ('k3', 'k4', 'k5', 'k7', 'k7p', 'k7t', 'r6', 'mk1', 'jk1', 'rt'):
                ppost = 'ke'
                if nn_data[3][2] == 's':#agreement with gnp
                    if nn_data[3][1] == 'f':
                        ppost = 'kI'
                    else:
                        ppost = 'kA'
                else:
                    pass
    else:
        pass
    if ppost == '':
        new_case = 'd'

    if concept_type == 'noun':
        if ppost == '':
            ppost = None
        processed_postpositions_dict[data_index] = ppost

    if concept_type == 'pronoun':
        if ppost == '':
            ppost = 0
        processed_postpositions_dict[data_index] = ppost
    print('preprocess_postposition_new : ',new_case, ppost)
    return new_case, ppost



def process_nominal_verb(nominal_verbs_data, processed_noun, words_info, verbs_data):
   print('Running process_nominal_verb')

   nominal_verbs = []
   for verb in verbs_data:
       if verb[4].strip().split(':')[1] == 'main':
           main_verb = verb
           break

   for nominal_verb in nominal_verbs_data:
        index = nominal_verb[0]
        term = clean(nominal_verb[1])
        gender = 'm'
        number = 's'
        person = 'a'
        category = 'n'
        noun_type = 'common'
        case = 'o'
        postposition = ''
        log_msg = f'{term} identified as nominal, re-identified as other word and processed as common noun with index {index} gen:{gender} num:{number} person:{person} noun_type:{noun_type} case:{case} and postposition:{postposition}'

        relation = ''
        if nominal_verb[4] != '':
            relation = nominal_verb[4].strip().split(':')[1]

        case, postposition = preprocess_postposition_new('noun', nominal_verb, words_info, main_verb)
        tags = find_tags_from_dix_as_list(term)
        for tag in tags:
            if (tag[0] == 'cat' and tag[1] == 'v'):
                noun_type = 'vn'
                category = 'vn'
                if relation in ('k2', 'rt', 'rh'):
                    term = term + 'nA'
                log_msg = f'{term} processed as nominal verb with index {index} gen:{gender} num:{number} person:{person} noun_type:{noun_type} case:{case} and postposition:{postposition}'
                break

        noun = (index, term, category, case, gender, number, person, noun_type, postposition)
        processed_noun.append(noun)
        log(log_msg)
   print('process_nominal_verb : ',nominal_verbs)
   return nominal_verbs

def process_adverb_as_noun(concept, processed_nouns):
    print('Running process_adverb_as_noun')
    index = concept[0]
    case = 'd'
    if ('+se_') in concept[1]:
        draft_term = concept[1].strip().split('+')[0]
        term = clean(draft_term)
        case = 'o'
    category = 'n'
    gender = 'm'
    number = 'p'
    person = 'a'
    noun_type = 'abstract'
    postposition = 'se'
    processed_postpositions_dict[index] = postposition
    adverb = (index, term, category, case, gender, number, person, noun_type, postposition)
    processed_nouns.append(adverb)
    log(f' Adverb {term} processed as an abstract noun with index {index} gen:{gender} num:{number} case:{case},noun_type:{noun_type} and postposition:{postposition}')
    return

def process_adverb_as_verb(concept, processed_verbs):
    print('Running process_adverb_as_verb')
    adverb = []
    index = concept[0]
    term = clean(concept[1])
    gender = 'm'
    number = 's'
    person = 'a'
    category = 'v'
    type = 'adverb'
    case = 'd'
    tags = find_tags_from_dix_as_list(term)
    for tag in tags:
        if ( tag[0] =='cat' and tag[1] == 'v' ):
            tam = 'kara'
            adverb = (index, term, category, gender, number, person, tam, case, type)
            processed_verbs.append(adverb)
            log(f'{term} adverb processed as a verb with index {index} gen:{gender} num:{number} person:{person}, and tam:{tam}')
            return

def process_adverbs(adverbs, processed_nouns, processed_verbs, processed_indeclinables, reprocessing):
    print('Running process_adverbs')
    for adverb in adverbs:
        if ('+se_') in adverb[1] or adverb[2] == 'abs':  # for jora+se kind of adverbs
                if not reprocessing:
                    process_adverb_as_noun(adverb,processed_nouns)
        else: #check morph tags
            term = clean(adverb[1])
            tags = find_tags_from_dix_as_list(term)
            for tag in tags:
                if (tag[0] == 'cat' and tag[1] == 'v'): # term type is verb in morph dix
                    return process_adverb_as_verb(adverb, processed_verbs)
                    
                elif (tag[0] == 'cat' and tag[1] == 'adj'): # term type is adjective in morph dix
                    term = term + 'rUpa se'
                    processed_indeclinables.append((adverb[0], term, 'indec'))
                    log(f'adverb {adverb[1]} processed indeclinable with form {term}')
                else:
                    for processed in processed_indeclinables:
                        if clean(adverb[1]) == processed[1]:
                            log(f'adverb {adverb[1]} already processed indeclinable, no processing done')
                            return
                    processed_indeclinables.append((adverb[0], term, 'indec')) #to be updated, when cases arise.
                    log(f'adverb {adverb[1]} processed indeclinable with form {term}, no processing done')
                    return
def process_indeclinables(indeclinables):
    print('Running process_indeclinables')
    '''
    Functionality:
        1. They do not require any furthur processing
        2. Make a tuple with - index, term, type(indec)

    Parameters:
        indeclinables: List of indeclinable data

    Returns:
        list of tuples.

    for eg.     :
        indeclinables: [(2, 'Aja_1', '', '', '3:k7t', '', '', '')]

    Result:
       processed_indeclinables: [(2, 'Aja', 'indec')]
    '''

    processed_indeclinables = []
    for indec in indeclinables:
        clean_indec = clean(indec[1])
        processed_indeclinables.append((indec[0], clean_indec, 'indec'))
    print('processed_indeclinables : ',processed_indeclinables)
    return processed_indeclinables


def process_nouns(nouns, words_info, verbs_data):
    print('Running process_nouns')
    '''
    Functionality:
        1. Make a noun tuple
        2. We update update_additional_words_dict(index, 'before', 'eka'), if number == 's' and noun[6] == 'some'

    Parameters:
        1. nouns - List of noun data
        2. words_info - List of USR info word wise
        3. verbs_data - List of verbs data

    Returns:
        processed_nouns = List of noun tuples where each tuple looks like - (index, word, category, case, gender, number, proper/noun type= proper, common, NC, nominal_verb, CP_noun or digit, postposition)

    For eg.:
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

        nouns     : [(1, 'rAma', 'male per', 'sg', '6:k1', '', '', ''), (3, 'rotI_1', '', 'sg', '6:k2', '', '', ''), (4, 'xAla_1', '', 'sg', '6:k2', '', '', '')]
        words_info     : [(1, 'rAma', 'male per', 'sg', '6:k1', '', '', ''), (2, 'xo_1', '', '', '3:card', '', '', ''), (3, 'rotI_1', '', 'sg', '6:k2', '', '', ''), (4, 'xAla_1', '', 'sg', '6:k2', '', '', ''), (5, 'KA_1-yA_1', '', '', '0:main', '', '', '')]
        verbs_data     : [(5, 'KA_1-yA_1', '', '', '0:main', '', '', '')]

    Result:
        processed_nouns     : [(1, 'rAma', 'n', 'o', 'm', 's', 'a', 'proper', 'ne'), (3, 'rotI', 'n', 'd', 'f', 's', 'a', 'common', None), (4, 'xAla', 'n', 'd', 'f', 's', 'a', 'common', None)]
    '''

    processed_nouns = []
    main_verb = ''
    for verb in verbs_data:
        if len(verb[4]) > 0 and verb[4].strip().split(':')[1] == 'main':
            main_verb = verb
            break
    if not len(main_verb):
        log('USR error. Main verb not identified. Check the USR.')
        sys.exit()

    for noun in nouns:
        category = 'n'
        index = noun[0]
        dependency = noun[4].strip().split(':')[1]
        gender, number, person = extract_gnp_noun(noun)

        if noun[6] == 'respect': # respect for nouns
            number = 'p'
        noun_type = 'common' if '_' in noun[1] else 'proper'

        case, postposition = preprocess_postposition_new('noun', noun, words_info, main_verb)

        

        if '+' in noun[1]:
            processed_nouns = handle_compound_nouns(noun, processed_nouns, category, case, gender, number, person, postposition)
        else:
            term = noun[1]
            if check_is_digit(term):
                if '_' in term:
                    clean_noun = term.strip().split('_')[0]
                else:
                    clean_noun = term
                noun_type = 'digit'
            else:
                clean_noun = clean(noun[1])

            processed_nouns.append((noun[0], clean_noun, category, case, gender, number, person, noun_type, postposition))

            if number == 's' and noun[6] == 'some':
                update_additional_words_dict(index, 'before', 'eka')

        log(f'{noun[1]} processed as noun with case:{case} gen:{gender} num:{number} noun_type:{noun_type} postposition: {postposition}.')
    print('process_nouns : ',processed_nouns)
    return processed_nouns

def process_pronouns(pronouns, processed_nouns, processed_indeclinables, words_info, verbs_data):
    print('Running process_pronouns')
    '''
        Functionality:
            1. Make a pronoun tuple
            2. If the term is kim, there is separate handling
            3. If term is yahAz or vahAz along with discourse data as 'emphasis' we convert it to yahIM, vahIM and treat them as indeclinables which do not require furthur processing
            4. If dependency is r6, then use the dependency_head to fetch the related noun data, and pick fnum, gender and case of this pronoun term same as related noun.
            5. Except for r6 relation, fnum is by default None

        Parameters:
            1. pronouns - List of pronoun data
            2. processed_nouns - List of processed noun data
            3. processed_indeclinables - List of processed indeclinable data
            2. words_info - List of USR info word wise
            3. verbs_data - List of verbs data

        Returns:
            processed_pronouns = List of pronoun tuples where each tuple looks like - (index, word, category, case, gender, number, person, parsarg, fnum)

        For eg.:
            yaha_1,aBiprAya_8,yaha_1,hE_1-pres
            1,2,3,4
            ,,,
            ,,sg,
            2:r6,4:k1,4:k1s,0:main
            ,,Geo_ncert_6stnd_4ch_0031d:coref,
            ,,,
            ,,,
            affirmative

            pronouns     : [(1, 'yaha_1', '', '', '2:r6', '', '', ''), (3, 'yaha_1', '', 'sg', '4:k1s', 'Geo_ncert_6stnd_4ch_0031d:coref', '', '')]
            words_info     : [(1, 'yaha_1', '', '', '2:r6', '', '', ''), (2, 'aBiprAya_8', '', '', '4:k1', '', '', ''), (3, 'yaha_1', '', 'sg', '4:k1s', 'Geo_ncert_6stnd_4ch_0031d:coref', '', ''), (4, 'hE_1-pres', '', '', '0:main', '', '', '')]
            verbs_data     : [(4, 'hE_1-pres', '', '', '0:main', '', '', '')]

        Result:
            processed_nouns     : [(1, 'yaha', 'p', 'd', 'm', 's', 'a', 'kA', 's'), (3, 'yaha', 'p', 'd', 'm', 's', 'a', 0, None)]
        '''

    processed_pronouns = []
    for verb in verbs_data:
        if verb[4].strip().split(':')[1] == 'main':
            main_verb = verb
            break

    for pronoun in pronouns:
        index = pronoun[0]
        term = clean(pronoun[1])
        anim = pronoun[2]
        gnp = pronoun[3]
        relation_head = pronoun[4].strip().split(':')[0]
        relation = pronoun[4].strip().split(':')[1]
        spkview_data = pronoun[6]

        if is_kim(term):
            processed_pronouns, processed_indeclinables = process_kim(index, relation, anim, gnp, pronoun, words_info,
                                                                      main_verb, processed_pronouns, processed_indeclinables, processed_nouns)
        else:
            category = 'p'
            case = 'o'
            parsarg = 0


            if term in ['yahAz', 'vahAz'] and spkview_data == 'emphasis':
                term = term.replace('Az', 'IM')
                category = 'indec'
                processed_indeclinables.append((index, term, category))
                break


            case, postposition = preprocess_postposition_new('pronoun', pronoun, words_info, main_verb)
            if postposition != '':
                parsarg = postposition

            fnum = None
            gender, number, person = extract_gnp(pronoun)

            if term == 'addressee':
                addr_map = {'respect': 'Apa', 'informal': 'wU', '': 'wU'}
                pronoun_per = {'respect': 'm', 'informal': 'm', '': 'm_h1'}
                pronoun_number = {'respect': 'p', 'informal': 's', '': 'p'}
                word = addr_map.get(spkview_data.strip().lower(), 'wU')
                person = pronoun_per.get(spkview_data.strip().lower(), 'm_h1')
                number = pronoun_number.get(spkview_data.strip(), 'p')
            elif term == 'speaker':
                word = 'mEM'
            elif term == 'wyax':
                if gnp =='pl' and spkview_data == "distal":
                    word = 've'
                elif gnp =='pl' and spkview_data == "proximal":
                    word = 'ye'
                elif spkview_data == "distal" and relation=='dem':
                    word = 'vaha'
                    case='o'
                elif spkview_data == "distal":
                    word = 'vaha'
                elif spkview_data == "proximal":
                    word = 'yaha'
                else:
                    word = term
            else:
                word = term

            if relation == "r6":
                fnoun = int(relation_head)
                fnoun_data = getDataByIndex(fnoun, processed_nouns, index=0)
                if fnoun_data:
                    gender = fnoun_data[4]  # To-ask
                    fnum = number = fnoun_data[5]
                    case = fnoun_data[3]
                if term == 'apanA':
                    parsarg = '0'

            processed_pronouns.append((index, word, category, case, gender, number, person, parsarg, fnum))
            log(f'{term} processed as pronoun with case:{case} par:{parsarg} gen:{gender} num:{number} per:{person} fnum:{fnum}')
    print('process_pronouns : ',processed_pronouns)
    return processed_pronouns

def process_others(other_words):
    print('Running process_others')
    '''Process other words. Right now being processed as noun with default gnp'''
    processed_others = []
    for word in other_words:
        gender = 'm'
        number = 's'
        person = 'a'
        processed_others.append((word[0], clean(word[1]), 'other', gender, number, person))
    print('process_others : ',processed_others)
    return processed_others

def process_verbs(verbs_data, seman_data, depend_data, sentence_type, spkview_data, processed_nouns, processed_pronouns, words_info, reprocess=False):
    print('Running process_verbs')
    '''
    Functionality:
        1. In the list of verbs data, identify
            a) if it is complex predicate - it is appended in processed_nouns
            b) if verb_type == 'nonfinite': - process the concept and append in processed_verbs
            c) otherwise process main verb and auxilliary verbs and append in respective lists
    Parameters:
         verbs_data: List of verbs data
         seman_data: Semantic data row of USR
         depend_data: Dependency data row of USR
         sentence_type: Sentence type
         spkview_data: Speaker's view data row of USR
         processed_nouns: List of processed_nouns
         processed_pronouns: List of processed_pronouns
         words_info: List of USR info word wise
         reprocess: for first time processing, it is False. In case of changes, it is made True and sent as parameter

        :Returns:
        List of processed_verbs and processed_auxverbs
    '''
    processed_verbs = []
    processed_auxverbs = []
    for concept in verbs_data:
        concept_dep_head = concept[4].strip().split(':')[0]
        concept_dep_val = concept[4].strip().split(':')[1]
        concept = Concept(index=concept[0], term=concept[1], dependency=concept[4])
        if(concept_dep_val == 'vk2'):
            update_additional_words_dict(int(concept_dep_head), 'after', 'ki')
        is_cp = is_CP(concept.term)
        if is_cp:
            if not reprocess:
                CP = process_main_CP(concept.index, concept.term)
                if CP != [] and CP[2] == 'n':
                    log(f'{CP[1]} processed as noun with index {CP[0]} case:d gen:{CP[4]} num:{CP[5]} per:{CP[6]}, noun_type:{CP[7]}, default postposition:{CP[8]}.')
                    processed_nouns.append(tuple(CP))
        verb_type = identify_verb_type(concept)
        if verb_type == 'nonfinite':
            verb = process_nonfinite_verb(concept, seman_data, depend_data, sentence_type, processed_nouns, processed_pronouns, words_info)
            processed_verbs.append(to_tuple(verb))
        else:
            verb, aux_verbs = process_verb(concept, seman_data, depend_data, sentence_type, spkview_data, processed_nouns, processed_pronouns, reprocess)
            processed_verbs.append(to_tuple(verb))
            log(f'{verb.term} processed as main verb with index {verb.index} gen:{verb.gender} num:{verb.number} case:{verb.case}, and tam:{verb.tam}')
            processed_auxverbs.extend([to_tuple(aux_verb) for aux_verb in aux_verbs])
    print('process_verbs : ',processed_verbs, processed_auxverbs)
    return processed_verbs, processed_auxverbs


def process_adjectives(adjectives, processed_nouns, processed_verbs):
    print('Running process_adjectives')
    '''Process adjectives as (index, word, category, case, gender, number)
        '''
    processed_adjectives = []
    gender, number, person, case = get_default_GNP()
    for adjective in adjectives:
        index = adjective[0]
        category = 'adj'
        adj = clean(adjective[1])

        relConcept = int(adjective[4].strip().split(':')[0]) # noun for regular adjcetives, and verb for k1s-samaadhikaran
        relation = adjective[4].strip().split(':')[1]
        if relation == 'k1s':
            if adj =='kim':
                adj = 'kEsA'
            relConcept_data = getDataByIndex(relConcept, processed_verbs)
        else:
            relConcept_data = getDataByIndex(relConcept, processed_nouns)

        if not relConcept_data:
            log(f'Associated noun/verb not found with the adjective {adjective[1]}. Using default m,s,a,o ')
        else:
            gender, number, person, case = get_gnpcase_from_concept(relConcept_data)
            if relation == 'k1s':
                case = 'd'

        if adj == 'kim' and relation == 'krvn':
            adj = 'kEsA'
        adjective = (index, adj, category, case, gender, number)
        processed_adjectives.append((index, adj, category, case, gender, number))
        log(f'{adjective[1]} processed as an adjective with case:{case} gen:{gender} num:{number}')
    print('process_adjectives : ',processed_adjectives)
    return processed_adjectives


def process_kim(index, relation, anim, gnp, pronoun, words_info, main_verb, processed_pronouns, processed_indeclinables, processed_nouns):
    print('Running process_kim')
    term = get_root_for_kim(relation, anim, gnp)
    if term == 'kyoM':
        processed_indeclinables.append((index, term, 'indec'))
    else:
        category = 'p'
        case = 'o'
        parsarg = 0
        case, postposition = preprocess_postposition_new('pronoun', pronoun, words_info, main_verb)
        if postposition != '':
            parsarg = postposition

        fnum = None
        gender, number, person = extract_gnp(pronoun[3])

        if "r6" in pronoun[4]:
            fnoun = int(pronoun[4][0])
            fnoun_data = getDataByIndex(fnoun, processed_nouns, index=0)
            gender = fnoun_data[4]  # To-ask
            fnum = number = fnoun_data[5]
            case = fnoun_data[3]
            if term == 'apanA':
                parsarg = '0'

        if term in ('kahAz'):
            parsarg = 0
        processed_pronouns.append((pronoun[0], term, category, case, gender, number, person, parsarg, fnum))
        log(f'kim processed as pronoun with term: {term} case:{case} par:{parsarg} gen:{gender} num:{number} per:{person} fnum:{fnum}')
    print('process_kim : ',processed_pronouns, processed_indeclinables)
    return processed_pronouns, processed_indeclinables


def process_imp_sentence(words_info, processed_pronouns):
    print('Running process_imp_sentence')
    k1exists = findExactMatch('k1', words_info, index=4)[0]
    if not k1exists:
        temp = (0.9, 'wU', 'p', 'd', 'm', 's', 'm_h1', 0, None)
        processed_pronouns.insert(0, temp)
    print('process_imp_sentence : ',processed_pronouns)
    return processed_pronouns


def process_main_CP(index, term):
    print('Running process_main_CP')
    """
    >>> process_main_CP(2,'varRA+ho_1-gA_1')
    [1.9, 'varRA', 'n', 'd', 'm', 's', 'a', 'CP_noun', None]
    """
    CP_term = clean(term.split('+')[0])
    CP_index = index - 0.1
    gender = 'm'
    number = 's'
    person = 'a'
    postposition = None
    CP = []
    tags = find_tags_from_dix(CP_term)  # getting tags from morph analyzer to assign gender and number for agreement
    if '*' not in tags['form']:
        gender = tags['gen']
        number = tags['num']
        category = tags['cat']
    CP = [CP_index, CP_term, 'n','d', gender, number, person, 'CP_noun', postposition]
    print('process_main_CP : ',CP)
    return CP


def process_construction(processed_words, construction_data, depend_data, gnp_data, index_data):
    print('Running process_construction')
    construction_dict.clear()
    process_data = processed_words
    dep_gender_dict = {}
    a = 'after'
    b = 'before'
    if gnp_data != []:
        gender = []
        for i in range(len(gnp_data)):
            gnp_info = gnp_data[i]
            gnp_info = gnp_info.strip().strip('][')
            gnp = gnp_info.split(' ')
            gender.append(gnp[0])

    if depend_data != []:
        dependency = []
        for dep in depend_data:
            if dep != '':
                dep_val = dep.strip().split(':')[1]
                dependency.append(dep_val)

    for i, dep, g in zip(index_data, dependency, gender):
        dep_gender_dict[str(i)] = dep + ':' + g

    if construction_data != '*nil' and len(construction_data) > 0:
        construction = construction_data.strip().split(' ')
        for cons in construction:
            conj_type = cons.split(':')[0].strip().lower()
            index = cons.split('@')[1].strip().strip('][').split(',')
            length_index = len(index)
            if conj_type == 'conj' or conj_type == 'disjunct':
                cnt_m = 0
                cnt_f = 0
                PROCESS = False
                for i in index:
                    relation = dep_gender_dict[i]
                    dep = relation.split(':')[0]
                    gen = relation.split(':')[1]

                    if dep == 'k1':
                        PROCESS = True
                        if gen == 'm':
                            cnt_m = cnt_m + 1
                        elif gen == 'f':
                            cnt_f = cnt_f + 1

                if PROCESS:
                    if cnt_f == length_index:
                        g = 'f'
                        num = 'p'
                    else:
                        g = 'm'
                        num = 'p'
                    process_data = set_gender_make_plural(processed_words, g, num)

                update_index = index[length_index - 2]
                for i in index:
                    if i == update_index:
                        if is_update_index_NC(i, processed_words):
                            index_NC_head = fetch_NC_head(i, processed_words)
                            i = index_NC_head
                        if conj_type == 'conj':
                            temp = (a, 'Ora')
                        elif conj_type == 'disjunct':
                            temp = (a, 'yA')
                        break
                    else:
                        temp = (a, ',')
                        if float(i) in construction_dict:
                            construction_dict[float(i)].append(temp)
                        else:
                            construction_dict[float(i)] = [temp]

                        if float(i) in processed_postpositions_dict:
                            del processed_postpositions_dict[float(i)]

                if float(i) in construction_dict:
                    construction_dict[float(i)].append(temp)
                else:
                    construction_dict[float(i)] = [temp]

                if float(i) in processed_postpositions_dict:
                    del processed_postpositions_dict[float(i)]

            elif conj_type == 'list':
                length_list = len(index)
                for i in range(len(index)):
                    if i == length_list - 1:
                        break

                    if i == 0:
                        temp = (b, 'jEse')
                        if index[i] in construction_dict:
                            construction_dict[index[i]].append(temp)
                        else:
                            construction_dict[index[i]] = [temp]
                        temp = (a, ',')

                    elif i < length_list - 1:
                        temp = (a, ',')

                    if index[i] in construction_dict:
                        construction_dict[index[i]].append(temp)
                    else:
                        construction_dict[index[i]] = [temp]
    print('process_construction : ',process_data)
    return process_data

def process_construction_span(processed_words, construction_data, depend_data, gnp_data, index_data):
    print('Running process_construction')
    construction_dict.clear()
    process_data = processed_words
    dep_gender_dict = {}
    a = 'after'
    b = 'before'
    
    if construction_data != '*nil' and len(construction_data) > 0:
        construction = construction_data.strip().split(' ')
        for cons in construction:

            conj_type = cons.split(':')[0].strip().lower()
            index = cons.split(':')[1].strip(' ').strip().strip('][').split(',')
            print(index,cons,'vlllllllllllll')
            length_index = len(index)
            if conj_type == '*span':
                cnt_m = 0
                cnt_f = 0
                PROCESS = False
                start_idx = index[0].split('@')[0]
                end_idx = index[1].split('@')[0]
                index=[start_idx,end_idx]
                print(index,'kkkk')
                update_index = index[length_index - 2]
                for i in range(len(index)):
                    if index[i] == update_index:
                        if start_idx=='':
                            temp= (a, 'waka')
                        elif end_idx == '':
                            temp = (a, 'se')
                        elif start_idx != '@'and end_idx != '@':
                            temp = (a, 'se')
                            temp1= (a, 'waka')
                        break
                    else:
                        temp = (a, ',')
                        if float(index[i]) in construction_dict:
                            construction_dict[float(index[i])].append(temp)
                        else:
                            construction_dict[float(index[i])] = [temp]

                        if float(index[i]) in processed_postpositions_dict:
                            del processed_postpositions_dict[float(i)]

                if index[i]!='' and float(index[i]) in construction_dict:
                    if index[i]!='':
                        construction_dict[float(index[i])].append(temp)
                    if index[i+1]!='':
                        construction_dict[float(index[i+1])].append(temp1)
                else:
                    if start_idx!='' and end_idx!='':
                        construction_dict[float(index[i])] = [temp]
                        construction_dict[float(index[i+1])]=[temp1]
                    elif start_idx!='':
                        construction_dict[float(index[i])] = [temp]
                    elif end_idx!='':
                        construction_dict[float(index[i+1])] = [temp]
                    
                if index[i]!='' and float(index[i]) in processed_postpositions_dict:
                    del processed_postpositions_dict[float(i)]
            
                
    print('process_construction_span : ',process_data)
    return process_data


def create_auxiliary_verb(index, term, tam, main_verb: Verb):
    print('Running create_auxiliary_verb')
    verb = Verb()
    verb.index = main_verb.index + (index + 1)/10
    verb.gender, verb.number, verb.person = main_verb.gender, main_verb.number, main_verb.person
    verb.term = term
    verb.tam = tam
    if verb.term == 'cAha':
            verb.person = 'm_h'
    verb.type = 'auxillary'
    log(f'{verb.term} processed as auxillary verb with index {verb.index} gen:{verb.gender} num:{verb.number} and tam:{verb.tam}')
    print('create_auxiliary_verb : ',verb)
    return verb


def process_auxiliary_verbs(verb: Verb, concept, spkview_data) -> [Verb]:
    print('Running process_auxiliary_verbs')
    """
    >>> [to_tuple(aux) for aux in process_auxiliary_verbs(Verb(index=4, term = 'kara', gender='m', number='s', person='a', tam='hE', type= 'Auxillary'), concept_term='kara_17-0_sakawA_hE_1')]
    [(4.1, 'saka', 'v', 'm', 's', 'a', 'wA', 'Auxillary'), (4.2, 'hE', 'v', 'm', 's', 'a', 'hE',''Auxillary'')]
    """
    concept_term = concept.term
    concept_index = concept.index
    HAS_SHADE_DATA = False
    auxiliary_term_tam = []
    shade_index = 1
    for data in spkview_data:
        if data != '':
            data = data.strip().strip('][')
            if 'shade' in data and concept_index == shade_index:
                term = clean(data.split(':')[1])
                tam = identify_default_tam_for_main_verb(concept_term)
                HAS_SHADE_DATA = True
                break
        shade_index = shade_index + 1

    if HAS_SHADE_DATA:
        if term == 'jA' and tam == 'yA':
            tam = 'yA1'   # to generate gayA from jA-yA
        temp = (term, tam)
        auxiliary_term_tam.append(temp)
        verb = set_main_verb_tam_zero(verb)

    auxiliary_verb_terms = identify_auxillary_verb_terms(concept_term)
    for v in auxiliary_verb_terms:
        term, tam = auxmap_hin(v)
        temp = (term, tam)
        auxiliary_term_tam.append(temp)

    return [create_auxiliary_verb(index, pair[0], pair[1], verb) for index, pair in enumerate(auxiliary_term_tam)]

def process_dep_rbks(concept, words_info, processed_nouns, processed_pronouns):
    print('Running process_dep_rbks')
    finalData = []
    k1_exists, k1_index = find_match_with_same_head(concept.index, 'k1', words_info, index=4)
    k3_exists, k3_index = find_match_with_same_head(concept.index, 'k3', words_info, index=4)
    if k1_exists:
        case = 'o'
        ppost = 'ke xvArA'

        for i in range(len(processed_nouns)):
            data = processed_nouns[i]
            data_index = data[0]
            if data_index == k1_index:
                temp = list(data)
                temp[3] = case
                temp[8] = ppost
                processed_nouns[i] = tuple(temp)
                update_ppost_dict(data_index, ppost)

    elif k3_exists:
        case = 'o'
        ppost = 'ke xvArA'

        for i in range(len(processed_nouns)):
            data = processed_nouns[i]
            data_index = data[0]
            if data_index == k3_index:
                temp = list(data)
                temp[3] = case
                temp[8] = ppost
                processed_nouns[i] = tuple(temp)
                update_ppost_dict(data_index, ppost)


def process_verb(concept: Concept, seman_data, dependency_data, sentence_type, spkview_data, processed_nouns, processed_pronouns, reprocessing):
    print('Running process_verb')
    """
    concept pattern: 'main_verb' - 'TAM for main verb' _Aux_verb+tam...
    Example 1:
    kara_1-wA_hE_1
    main verb - kara,  main verb tam: wA, Aux -hE with TAM hE (identified from tam mapping file)

    Example 2:
    kara_1-yA_1
    main verb - kara,  main verb tam: yA,

    Example 3:
    kara_1-0_rahA_hE_1
    main verb - kara,  main verb tam: 0, Aux verb -rahA with TAM hE, Aux -hE with TAM hE (identified from tam mapping file)

    Example 4:
    kara_1-0_sakawA_hE_1
    main verb - kara,  main verb tam: 0, Aux verb -saka with TAM wA, Aux -hE with TAM hE (identified from tam mapping file)

    *Aux root and Aux TAM identified from auxillary mapping File
    """
    verb = process_main_verb(concept, seman_data, dependency_data, sentence_type, processed_nouns, processed_pronouns, reprocessing)
    auxiliary_verbs = process_auxiliary_verbs(verb, concept, spkview_data)
    print('process_verb : ',verb, auxiliary_verbs)
    return verb, auxiliary_verbs


def process_nonfinite_verb(concept, seman_data, depend_data, sentence_type, processed_nouns, processed_pronouns, words_info):
    print('Running process_nonfinite_verb')
    '''
    >>process_nonfinite_verb([], [()],[()])
    '''
    gender = 'm'
    number = 's'
    person = 'a'
    verb = Verb()
    verb.index = concept.index
    is_cp = is_CP(concept.term)
    if is_cp: #only CP_head as nonfinite verb
        draft_concept = concept.term.split('+')[1]
        verb.term  = clean(draft_concept)
    else:
        verb.term = clean(concept.term)

    verb.type = 'nonfinite'
    verb.tam = ''
    relation = concept.dependency.strip().split(':')[1]
    if relation == 'rbks':
        process_dep_rbks(concept, words_info, processed_nouns, processed_pronouns)

    verb.tam = set_tam_for_nonfinite(relation)
    full_tam = verb.tam

    gender, number, person = getVerbGNP_new(verb.term, full_tam, is_cp, seman_data, depend_data, sentence_type, processed_nouns, processed_pronouns)
    verb.gender = gender
    verb.number = number
    verb.person = person
    verb.case = 'o' # to be updated - agreement with following noun
    log(f'{verb.term} processed as nonfinite verb with index {verb.index} gen:{verb.gender} num:{verb.number} case:{verb.case}, and tam:{verb.tam}')
    print('process_nonfinite_verb : ',verb)
    return verb

def process_dep_k2g(data_case, main_verb):
    print('Running process_dep_k2g')
    verb = identify_main_verb(main_verb[1])
    if verb in kisase_k2g_verbs:
        ppost = 'se'
    else:
        ppost = 'ko'
    print('process_dep_k2g : ',ppost)
    return ppost

def process_main_verb(concept: Concept, seman_data, dependency_data, sentence_type, processed_nouns, processed_pronouns, reprocessing):
    print('Running process_main_verb')
    """
    >>> to_tuple(process_main_verb(Concept(index=2, term='varRA+ho_1-gA_1', dependency='0:main'), ['2:k7t', '0:main'], [(1, 'kala', 'n', 'o', 'm', 's', 'a', 'common', None)], [], False))
    [OK]     : varRA processed as noun with index 1.9 case:d gen:f num:s per:a, noun_type:CP_noun, default postposition:None.
    (2, 'ho', 'v', 'f', 's', 'a', 'gA')
    >>> to_tuple(process_main_verb(Concept(index=2, term='varRA+ho_1-gA_1', dependency='0:main'), ['2:k7t', '0:main'], [(1, 'kala', 'n', 'o', 'm', 's', 'a', 'common', None)], [], True))
    [OK]     : ho reprocessed as verb with index 2 gen:f num:s per:a in agreement with CP
    (2, 'ho', 'v', 'f', 's', 'a', 'gA')
    >>>
    """
    verb = Verb()
    verb.type = "main"
    verb.index = concept.index
    verb.term = identify_main_verb(concept.term)
    full_tam = identify_complete_tam_for_verb(concept.term)
    verb.tam = identify_default_tam_for_main_verb(concept.term)
    if verb.term == 'hE' and verb.tam in ('pres', 'past'):  # process TAM
        alt_tam = {'pres': 'hE', 'past': 'WA'}
        alt_root = {'pres': 'hE', 'past': 'WA'}
        verb.term = alt_root[verb.tam]  # handling past tense by passing correct root WA
        verb.tam = alt_tam[verb.tam]
    if verb.term == 'jA' and verb.tam == 'yA':
        verb.tam = 'yA1'
    is_cp = is_CP(concept.term)
    verb.gender, verb.number, verb.person = getVerbGNP_new(concept.term, full_tam, is_cp, seman_data, dependency_data, sentence_type, processed_nouns, processed_pronouns)
    print('process_main_verb : ',verb)
    return verb

def get_all_form(morph_forms):
    print('Running get_all_form')
    """
    >>> get_first_form("^mAz/mA<cat:n><case:d><gen:f><num:p>/mAz<cat:n><case:d><gen:f><num:s>/mAz<cat:n><case:o><gen:f><num:s>$")
    'mA<cat:n><case:d><gen:f><num:p>/mAz<cat:n><case:d><gen:f><num:s>/mAz<cat:n><case:o><gen:f><num:s>'
    """
    morph=morph_forms.split("$")[1]
    print('get_all_form : ',morph)
    return morph



def get_first_form(morph_forms):
    print('Running get_first_form')
    """
    >>> get_first_form("^mAz/mA<cat:n><case:d><gen:f><num:p>/mAz<cat:n><case:d><gen:f><num:s>/mAz<cat:n><case:o><gen:f><num:s>$")
    'mA<cat:n><case:d><gen:f><num:p>'
    """
    morph=morph_forms.split("/")[1]
    print('get_first_form : ',morph)
    return morph

def get_root_for_kim(relation, anim, gnp):
    print('Running get_root_for_kim')

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
    print('Running get_default_GNP')
    gender = 'm'
    number = 's'
    person = 'a'
    case  = 'o'
    print('get_default_GNP : ',gender, number, person, case)
    return gender, number, person, case


def get_gnpcase_from_concept(concept): #computes GNP values from noun or
    print('Running get_gnpcase_from_concept')

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
    print('get_gnpcase_from_concept : ',gender, number, person, case)
    return gender, number, person, case

def get_TAM(term, tam):
    print('Running get_TAM')
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
    print('get_TAM : ',tam)
    return tam

def get_main_verb(term):
    print('Running get_main_verb')
    ''' return main verb from a term'''

    pass

def getDataByIndex(value: int, searchList: list, index=0):
    print('Running getDataByIndex')
    '''search and return data by index in an array of tuples.
        Index should be first element of tuples.
        Return False when index not found.'''
    try:
        res = False
        for dataele in searchList:
            if (dataele[(index)]) == value:
                res = dataele
    except IndexError:
        log(f'Index out of range while searching index:{value} in {searchList}', 'WARNING')
        return False
    print('getDataByIndex : ',res)
    return res

def getComplexPredicateGNP(term):
    print('Running getComplexPredicateGNP')
    CP_term = clean(term.split('+')[0])
    gender = 'm'
    number = 's'
    person = 'a'

    tags = find_tags_from_dix(CP_term)  # getting tags from morph analyzer to assign gender and number for agreement
    if '*' not in tags['form']:
        gender = tags['gen']
        number = tags['num']
    print('getComplexPredicateGNP : ',gender, number, person)
    return gender, number, person

def getGNP_using_k2(k2exists, searchList):
    print('Running getGNP_using_k2')
    casedata = getDataByIndex(k2exists, searchList)
    if (casedata == False):
        log('Something went wrong. Cannot determine GNP for verb.', 'ERROR')
        sys.exit()
    verb_gender, verb_number, verb_person = casedata[4], casedata[5], casedata[6]
    print('getGNP_using_k2 : ',verb_gender, verb_number, verb_person[0])
    return verb_gender, verb_number, verb_person[0]

def getGNP_using_k1(k1exists, searchList):
    print('Running getGNP_using_k1')
    casedata = getDataByIndex(k1exists, searchList)
    if (casedata == False):
        log('Something went wrong. Cannot determine GNP for verb k1 is missing.', 'ERROR')
        sys.exit()
    verb_gender, verb_number, verb_person = casedata[4], casedata[5], casedata[6]
    print('getGNP_using_k1 : ',verb_gender, verb_number, verb_person[0])
    return verb_gender, verb_number, verb_person












def getVerbGNP_new(concept_term, full_tam, is_cp, seman_data, depend_data, sentence_type, processed_nouns, processed_pronouns):
    print('Running getVerbGNP_new')
    '''
    '''
    if sentence_type in ('Imperative','imperative') or 'o' in full_tam:
        verb_gender = 'm'
        verb_number = 's'
        verb_person = 'm'
        print('getVerbGNP_new : ',verb_gender, verb_number, verb_person)
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
            verb_gender, verb_number, verb_person = getGNP_using_k1(k1exists, searchList)
        elif k1exists and k1_case == 'o' and k2exists and k2_case == 'o':
            verb_gender, verb_number, verb_person = getComplexPredicateGNP(cp_term)
        print('getVerbGNP_new : ',verb_gender, verb_number, verb_person[0])
        return verb_gender, verb_number, verb_person[0]

    if 'yA' in full_tam:
        if k1exists and k1_case == 'd':
            verb_gender, verb_number, verb_person = getGNP_using_k1(k1exists, searchList)
        elif k1exists and k1_case == 'o' and k2exists and k2_case == 'd':
            verb_gender, verb_number, verb_person = getGNP_using_k2(k2exists, searchList)
        print('getVerbGNP_new : ',verb_gender, verb_number, verb_person[0])
        return verb_gender, verb_number, verb_person[0]

    if full_tam in nA_list:
        print('getVerbGNP_new : ',verb_gender, verb_number, verb_person[0])
        return verb_gender, verb_number, verb_person[0]

    else:
        verb_gender, verb_number, verb_person = getGNP_using_k1(k1exists, searchList)
        print('getVerbGNP_new : ',verb_gender, verb_number, verb_person[0])
        return verb_gender, verb_number, verb_person[0]

def is_tam_ya(verbs_data):
    print('Running is_tam_ya')
    
    ya_tam = '-yA_'
    if len(verbs_data) > 0 and verbs_data != ()     :
        term = verbs_data[1]
        if ya_tam in term:
            return True
    return False

def is_kim(term):
    print('is_kim')
    if term == 'kim':
        return True
    
    return False

def is_complex_predicate(concept):
    print('is_complex_predicate')
    return "+" in concept

def is_CP(term):
    print('Running is_CP')
    """
    >>> is_CP('varRA+ho_1-gA_1')
    True
    >>> is_CP("kara_1-wA_hE_1")
    False
    """
    if "+" in term:
        print('is_CP     : True')
        return True
    else:
        print('is_CP     : False')
        return False

def is_update_index_NC(i, processed_words):
    print('Running is_update_index_NC')
    for data in processed_words:
        temp = tuple(data)
        if len(temp) > 7 and float(i) == temp[0] and temp[7] == 'NC':
            return True

    return False

def is_nonfinite_verb(concept):
    print('Running is_nonfinite_verb')
    return concept.type == 'nonfinite'

def has_tam_ya():
    '''Check if USR has verb with TAM "yA".
        It sets the global variable HAS_TAM to true
    '''
    print('Running has_tam_ya')
    global HAS_TAM
    if HAS_TAM == True:
        return True
    else:
        return False
    
def has_GNP(gnp_info):
    print('Running has_GNP')
    if len(gnp_info) and ('sg', 'pl') in gnp_info:
        return True
    return False

def has_ques_mark(POST_PROCESS_OUTPUT,sentence_type):
    print('Running has_ques_mark')

    if sentence_type[1:] in ("yn_interrogative", "yn_interrogative_negative", "pass-yn_interrogative", "interrogative",
                        "Interrogative", "pass-interrogative"):
        return 'kyA ' + POST_PROCESS_OUTPUT + ' ?'
    elif sentence_type[1:] in ('affirmative', 'Affirmative', 'negative', 'Negative', 'imperative', 'Imperative',"fragment","term","title","heading"):
        return POST_PROCESS_OUTPUT + ' |'

def identify_case(verb, dependency_data, processed_nouns, processed_pronouns):
    print('Running identify_case')
    return getVerbGNP_new(verb.term, verb.tam, dependency_data, processed_nouns, processed_pronouns)

def identify_main_verb(concept_term):
    print('Running identify_main_verb',concept_term)
    """
    >>> identify_main_verb("kara_1-wA_hE_1")
    'kara'
    >>> identify_main_verb("varRA+ho_1-gA_1")
    'ho'
    """
    if ("+" in concept_term):
        concept_term = concept_term.split("+")[1]
    con=clean(concept_term.split("-")[0])
    print('identify_main_verb : ',con)
    return con

def identify_default_tam_for_main_verb(concept_term):
    print('Running identify_default_tam_for_main_verb')
    """
    >>> identify_default_tam_for_main_verb("kara_1-wA_hE_1")
    'wA'
    >>> identify_default_tam_for_main_verb("kara_1-0_rahA_hE_1")
    '0'
    """
    con=concept_term.split("-")[1].split("_")[0]
    print('identify_default_tam_for_main_verb : ',con)
    return con


def identify_complete_tam_for_verb(concept_term):
    print('Running identify_complete_tam_for_verb')
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
    print('identify_complete_tam_for_verb : ',tam_v)
    return tam_v


def identify_auxillary_verb_terms(term):
    print('Running identify_auxillary_verb_terms')
    """
    >>> identify_auxillary_verb_terms("kara_1-wA_hE_1")
    ['hE']
    >>> identify_auxillary_verb_terms("kara_1-0_rahA_hE_1")
    ['rahA', 'hE']
    """
    aux_verb_terms = term.split("-")[1].split("_")[1:]
    cleaned_terms = map(clean, aux_verb_terms)
    el=list(filter(lambda x: x != '', cleaned_terms))
    print('identify_auxillary_verb_terms : ',el)
    return el            # Remove empty strings after cleaning


def identify_verb_type(verb_concept):
    print('Running identify_verb_type')
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
    print('identify_verb_type : ',v_type)
    return v_type

def findExactMatch(value: int, searchList: list, index=0):
    print('Running findExactMatch')
    '''search and return data by index in an array of tuples.
        Index should be first element of tuples.

        Return False when index not found.'''

    try:
        for dataele in searchList:
            if value == dataele[index].strip().split(':')[1]:
                return (True, dataele)
    except IndexError:
        log(f'Index out of range while searching index:{value} in {searchList}', 'WARNING')
        return (False, None)
    return (False, None)

def findValue(value: int, searchList: list, index=0):
    print('Running findValue')
    '''search and return data by index in an array of tuples.
        Index should be first element of tuples.

        Return False when index not found.'''

    try:
        for dataele in searchList:
            if value == dataele[index]:
                return (True, dataele)
    except IndexError:
        log(f'Index out of range while searching index:{value} in {searchList}', 'WARNING')
        return (False, None)
    return (False, None)

def find_tags_from_dix(word):
    print('Running find_tags_from_dix')
    """
    >>> find_tags_from_dix("mAz")
    {'cat': 'n', 'case': 'd', 'gen': 'f', 'num': 'p', 'form': 'mA'}
    """
    dix_command = "echo {} | apertium-destxt | lt-proc -ac hi.morfLC.bin | apertium-retxt".format(word)
    morph_forms = os.popen(dix_command).read()
    p_m=parse_morph_tags(morph_forms)
    print('find_tags_from_dix : ',p_m)
    return p_m

def find_tags_from_dix_as_list(word):
    print('Running find_tags_from_dix_as_list')
    """
    >>> find_tags_from_dix("mAz")
    {'cat': 'n', 'case': 'd', 'gen': 'f', 'num': 'p', 'form': 'mA'}
    """
    dix_command = "echo {} | apertium-destxt | lt-proc -ac hi.morfLC.bin | apertium-retxt".format(word)
    morph_forms = os.popen(dix_command).read()
    p_m=parse_morph_tags_as_list(morph_forms)
    print('find_tags_from_dix_as_list : ',p_m)
    return p_m

def find_exact_dep_info_exists(index, dep_rel, words_info):
    print('Running find_exact_dep_info_exists')
    for word in words_info:
        dep = word[4]
        dep_head = word[4].strip().split(':')[0]
        dep_val = word[4].strip().split(':')[1]
        if dep_val == dep_rel and int(dep_head) == index:
            return True
    
    return False

def find_match_with_same_head(data_head, term, words_info, index):
     print('Running find_match_with_same_head')
     for dataele in words_info:
        dataele_index = dataele[0]
        dep_head = dataele[index].strip().split(':')[0]
        dep_value = dataele[index].strip().split(':')[1]
        if str(data_head) == dep_head and term == dep_value:
            return True, dataele_index
     return False, -1


def parse_morph_tags(morph_form):
    print('Running parse_morph_tags')
    """
    >>> parse_morph_tags("mA<cat:n><case:d><gen:f><num:p>")
    {'cat': 'n', 'case': 'd', 'gen': 'f', 'num': 'p', 'form': 'mA'}
    """
    form = morph_form.split("<")[0]
    matches = re.findall("<(.*?):(.*?)>", morph_form)
    result = {match[0]: match[1] for match in matches}
    result["form"] = form
    print('parse_morph_tags : ',result)
    return result

def parse_morph_tags_as_list(morph_form):
    print('Running parse_morph_tags_as_list')
    """
    >>> parse_morph_tags("mA<cat:n><case:d><gen:f><num:p>")
    {'cat': 'n', 'case': 'd', 'gen': 'f', 'num': 'p', 'form': 'mA'}
    """
    form = morph_form.split("<")[0]
    matches = re.findall("<(.*?):(.*?)>", morph_form)
    result = [(match[0], match[1]) for match in matches]
    result.append(('form',form))
    print('parse_morph_tags_as_list : ',result)
    return result

def generate_input_for_morph_generator(input_data):
    print('Running generate_input_for_morph_generator')
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
    print('generate_input_for_morph_generator : ',morph_input_data)
    return morph_input_data


def write_data(writedata):
    print('Running write_data')
    """Write the Morph Input Data into a file"""
    final_input = " ".join(writedata)
    with open("morph_input.txt", 'w', encoding="utf-8") as file:
        file.write(final_input + "\n")
    return "morph_input.txt"


def run_morph_generator(input_file):
    print('Running run_morph_generator')
    """ Pass the morph generator through the input file"""
    fname = f'{input_file}-out.txt'
    f = open(fname, 'w')
    subprocess.run(f"sh ./run_morph-generator.sh {input_file}", stdout=f, shell=True)
    return "morph_input.txt-out.txt"


def generate_morph(processed_words):
    print('Running generate_morph')
    """Run Morph generator"""
    morph_input = generate_input_for_morph_generator(processed_words)
    MORPH_INPUT_FILE = write_data(morph_input)
    OUTPUT_FILE = run_morph_generator(MORPH_INPUT_FILE)
    return OUTPUT_FILE

def read_output_data(output_file):
    print('Running read_output_data')
    """Check the output file data for post processing"""

    with open(output_file, 'r') as file:
        data = file.read()
    print('read_output_data : ',data)
    return data


def analyse_output_data(output_data, morph_input):
    print('Running analyse_output_data')
    output_data = output_data.strip().split(" ")
    combine_data = []
    print('before combining : ',output_data, morph_input)
    for i in range(len(output_data)):
        morph_input_list = list(morph_input[i])
        morph_input_list[1] = output_data[i]
        combine_data.append(tuple(morph_input_list))
    print('analyse_output_data : ',combine_data)
    return combine_data

def handle_compound_nouns(noun, processed_nouns, category, case, gender, number, person, postposition):
    print('Running handle_compound_nouns')
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
    print('handle_compound_nouns : ',processed_nouns)
    return processed_nouns


def handle_unprocessed(outputData, processed_nouns):
    print('Running handle_unprocessed')
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
    print('handle_unprocessed : ',has_changes, processed_nouns)
    return has_changes, processed_nouns

def nextNounData_fromFullData(fromIndex, PP_FullData):
    print('Running nextNounData_fromFullData')
    index = fromIndex
    for data in PP_FullData:
        if data[0] > index:
            if data[2] == 'n':
                return data

    return ()
def nextNounData(fromIndex, word_info):
    print('Running nextNounData')
    index = fromIndex
    for i in range(len(word_info)):
        for data in word_info:
            if index == data[0]:
                if data[3] != '' and index != fromIndex:
                    return data
    return False

def fetchNextWord(index, words_info):
    print('Running fetchNextWord')
    next_word = ''
    for data in words_info:
        if index == data[0]:
            next_word = clean(data[1])
    print('fetchNextWord : ',next_word)
    return next_word

def change_gender(current_gender):
    print('Running change_gender')
    """
    >>> change_gender('m')
    'f'
    >>> change_gender('f')
    'm'
    """
    return 'f' if current_gender == 'm' else 'm'


def set_gender_make_plural(processed_words, g, num):
    print('Running set_gender_make_plural')
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
    print('set_gender_make_plural : ',process_data)
    return process_data


def set_main_verb_tam_zero(verb: Verb):
    print('Running set_main_verb_tam_zero')
    verb.tam = 0
    print('set_main_verb_tam_zero :',verb)
    return verb

def set_tam_for_nonfinite(dependency):
    print('Running set_tam_for_nonfinite')
    '''
    >>> set_tam_for_nonfinite('rvks')
    'adj_wA_huA'
    >>> set_tam_for_nonfinite('rbks')
    'yA_huA'
    >>> set_tam_for_nonfinite('rsk')
    'wA_huA'
    >>> set_tam_for_nonfinite('rpk')
    'kara'
    '''
    tam = 0
    if dependency == 'rvks':
        tam = 'adj_wA_huA'
    elif dependency == 'rpk':
        tam = 'kara'
    elif dependency == 'rsk':
        tam = 'adj_wA_huA'
    elif dependency == 'rbks':
        tam = 'adj_yA_huA'
    elif dependency == 'rblpk':
        tam = 'nA'
    elif dependency == 'rbk':
        tam = 'yA_gayA'
    print('set_tam_for_nonfinite : ',tam)
    return tam

def update_ppost_dict(data_index, param):
    print('Running update_ppost_dict')
    processed_postpositions_dict[data_index] = param

def extract_tamdict_hin():
    print('Running extract_tamdict_hin')
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

def extract_gnp_noun(noun_data):
    print('Running extract_gnp_noun')
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
    print('extract_gnp_noun : ',gender, number, person)
    return gender, number, person

def extract_gnp(data):
    print('Running extract_gnp')
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
    print('extract_gnp : ',gender, number, person)
    return gender, number, person

def add_postposition(transformed_fulldata, processed_postpositions):
    print('Running add_postposition')
    '''Adds postposition to words wherever applicable according to rules.'''
    PPFulldata = []

    for data in transformed_fulldata:
        index = data[0]
        if index in processed_postpositions:
            temp = list(data)
            ppost = processed_postpositions[index]
            if ppost != None and (temp[2] == 'n' or temp[2] == 'other'):
                temp[1] = temp[1] + ' ' + ppost
            data = tuple(temp)
        PPFulldata.append(data)
    print('add_postposition : ',PPFulldata)
    return PPFulldata

def add_discourse_elements(discourse_data, POST_PROCESS_OUTPUT):
    print('Running add_discourse_elements')
    if len(discourse_data) <= 0:
        return POST_PROCESS_OUTPUT
    coref_list=[]
    folder_path = sys.argv[1].split('/')[0]
    file_name_line = None  
    relation=['AvaSyakawApariNAma']  
    for i in range(len(discourse_data)):
        if '.' in discourse_data[i]:
            coref_list.append(i)
            file_name_line = discourse_data[i]
            file_name = file_name_line.split('.')[0]
            digit = file_name_line.split('.')[1].split(':')[0]
            discource_rel = file_name_line.split(':')[1]
            file_path = os.path.join(folder_path, f'{file_name}')
            print(file_path,'kl')
            if not os.path.exists(file_path):
                file_path += '.txt'
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"File '{file_path}' not found")
            with open(file_path, 'r', encoding='utf-8') as file:
                file_contents = file.readlines()
            
            if discource_rel in relation:
                print(file_contents[0],'file_contents',discource_rel)

            coref_word=file_contents[1].split(',')[int(digit)-1]
            coref_list.append(coref_word)
    
    for data_values in discourse_data:
        for element in discourse_dict:
            if element in data_values:
                if isinstance(discourse_dict[element], str):
                    POST_PROCESS_OUTPUT = discourse_dict[element] + " " + POST_PROCESS_OUTPUT
                elif isinstance(discourse_dict[element], list):
                    for i in range(len(discourse_dict[element])):
                        if i!=0:
                            POST_PROCESS_OUTPUT = discourse_dict[element][i]+ '/'+ POST_PROCESS_OUTPUT
                        else:
                            POST_PROCESS_OUTPUT = discourse_dict[element][i] + " " + POST_PROCESS_OUTPUT
    print('add_discourse_elements : ', POST_PROCESS_OUTPUT)
    return POST_PROCESS_OUTPUT


def add_adj_to_noun_attribute(key, value):
    print('Running add_adj_to_noun_attribute')
    if key is not None:
        if key in noun_attribute:
            noun_attribute[key][0].append(value)
            print('add_adj_to_noun_attribute : ',noun_attribute[key][0])
        else:
            noun_attribute[key] = [[],[]]
            print('add_adj_to_noun_attribute : ',noun_attribute[key])

def add_verb_to_noun_attribute(key, value):
    print('Running add_verb_to_noun_attribute')
    if key is not None:
        if key in noun_attribute:
            noun_attribute[key][1].append(value)
        else:
            noun_attribute[key] = [[], []]

def add_spkview(full_data, spkview_dict):
    print('Running add_spkview')
    transformed_data = []
    for data in full_data:
        index = data[0]
        if index in spkview_dict:
            temp = list(data)
            spkview_info = spkview_dict[index]
            for info in spkview_info:
                tag = info[0]
                val = info[1]
                if tag == 'before':
                    temp[1] = val + ' ' + temp[1]
                elif tag == 'after':
                    temp[1] = temp[1] + ' ' + val
                data = tuple(temp)
        transformed_data.append(data)
    print('add_spkview : ',transformed_data)
    return transformed_data

def add_MORPHO_SEMANTIC(full_data, MORPHO_SEMANTIC_DICT):
    print('Running add_MORPHO_SEMANTIC')
    transformed_data = []
    for data in full_data:
        index = data[0]
        if index in MORPHO_SEMANTIC_DICT:
            temp = list(data)
            term = MORPHO_SEMANTIC_DICT[index]
            for t in term:
                tag = t[0]
                val = t[1]
                if tag == 'before':
                    temp[1] = val + ' ' + temp[1]
                else:
                    temp[1] = temp[1] + ' ' + val
            data = tuple(temp)
        transformed_data.append(data)
    print('add_MORPHO_SEMANTIC : ',transformed_data)
    return transformed_data

def add_construction(transformed_data, construction_dict):
    print('Running add_construction')
    Constructdata = []
    dependency_check=['k7p','k7t']
    add_words_list=['meM','ko','ke','kI','kA']
    depend_data1=''
    for data in transformed_data:
        index = data[0]
        print(data)
        if len(data)==9:
            depend_data1=data[8]
        if index in construction_dict:
            temp = list(data)
            term = construction_dict[index]
            for t in term:
                tag = t[0]
                val = t[1]
                if tag == 'before':
                    temp[1] = val + ' ' + temp[1]
                else:
                    if val == ',':
                        temp[1] = temp[1] + val
                    else:
                        if depend_data1!='' and depend_data1 in add_words_list:
                            if depend_data1 in add_words_list and depend_data1 in temp[1]:
                                temp[1] = temp[1].split()[0] + ' ' +val
                        else:
                            temp[1] = temp[1] + ' ' +val
            data = tuple(temp)
        Constructdata.append(data)
    print('add_construction : ',Constructdata)
    return Constructdata

def add_additional_words(additional_words_dict, processed_data):
    print('Running add_additional_words')
    additionalData = []

    for data in processed_data:
        index = data[0]
        if index in additional_words_dict:
            temp = list(data)
            term = additional_words_dict[index]
            for t in term:
                tag = t[0]
                val = t[1]
                if tag == 'before':
                    temp[1] = val + ' ' + temp[1]
                else:
                    temp1=temp[1].split()
                    if len(temp1)>=2 and temp1[1]=='ko':
                        temp1[1] = val
                        temp[1] = ' '.join(temp1)
                    else:
                        temp[1] = temp[1] + ' ' + val
            data = tuple(temp)
        additionalData.append(data)
    print('add_additional_words : ',additionalData)
    return additionalData

def fetch_NC_head(i, processed_words):
    print('Running fetch_NC_head')
    for data in processed_words:
        temp = tuple(data)
        if int(temp[0]) == int(i) and temp[7] == 'NC_head':
            return temp[0]

def auxmap_hin(aux_verb):
    print('Running auxmap_hin')
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
    print('Running update_additional_words_dict')
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
    print('Running to_tuple')
    print('to_tuple : ',verb.index, verb.term, verb.category, verb.gender, verb.number, verb.person, verb.tam, verb.case, verb.type)
    return (verb.index, verb.term, verb.category, verb.gender, verb.number, verb.person, verb.tam, verb.case, verb.type)

def postposition_finalization(processed_nouns, processed_pronouns,processed_foreign_words, words_info):
    print('Running postposition_finalization')
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
    print('Running collect_processed_data')
    """collect sort and return processed data."""
    sorted_data=sorted(processed_foreign_words+processed_pronouns + processed_nouns + processed_adjectives + processed_verbs + processed_auxverbs + processed_indeclinables + processed_others)
    print('collect_processed_data combining all processed list in sorted order',sorted_data)
    return sorted_data

def join_compounds(transformed_data, construction_data):
    print('Running join_compounds')
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
    print('join_compounds : ',resultant_data)
    return resultant_data

def populate_morpho_semantic_dict(gnp_info, PPfull_data,words_info):
    print('Running populate_morpho_semantic_dict')
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
    print('populate_morpho_semantic_dict : ',populate_morpho_semantic_dict)
    return populate_morpho_semantic_dict,PPfull_data

def join_indeclinables(transformed_data, processed_indeclinables, processed_others):
    
    """Joins Indeclinable data with transformed data and sort it by index number."""
    return sorted(transformed_data + processed_indeclinables + processed_others)




def rearrange_sentence(fulldata):
    print('Running rearrange_sentence')
    '''Function comments'''
    finalData = sorted(fulldata)
    final_words = [x[1].strip() for x in finalData]
    r_s=" ".join(final_words)
    print('rearrange_sentence : ',r_s)
    return r_s

def collect_hindi_output(source_text):
    print('Running collect_hindi_output')
    """Take the output text and find the hindi text from it."""
    print(source_text)
    hindi_format = WXC(order="wx2utf", lang="hin")
    generate_hindi_text = hindi_format.convert(source_text)
    print('collect_hindi_output : ',generate_hindi_text)
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

if __name__ == '__main__':
    import doctest
    doctest.run_docstring_examples(identify_complete_tam_for_verb, globals())


==========================================================================================
# new 19-07-24
import os
import sys
import re
import subprocess
import constant
from wxconv import WXC
# from bulk_runner import output_list1
# from generate_input_modularize_new import additional_words_dict,spkview_dict
# from Table import store_data
from verb import Verb
from concept import Concept
additional_words_dict = {}
processed_postpositions_dict = {}
construction_dict = {}
spkview_dict = {}
MORPHO_SEMANTIC_DICT = {}

#pre processing

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

def log(mssg, logtype='OK'):
    '''Generates log message in predefined format.'''

    # Format for log message
    print(f'log : [{logtype}]:{mssg}')
    if logtype == 'ERROR':
        path = sys.argv[1]
        write_hindi_test(' ', 'Error', mssg, 'test.csv', path)

def write_hindi_text(hindi_output, POST_PROCESS_OUTPUT, OUTPUT_FILE):
#     print('Running write_hindi_text')
    """Append the hindi text into the file"""
    with open(OUTPUT_FILE, 'w') as file:
        file.write(POST_PROCESS_OUTPUT)
        file.write('\n')
        file.write(hindi_output)
        # log('Output data write successfully')
        print(hindi_output)
    return "Output data write successfully"

def write_hindi_test(hindi_output, POST_PROCESS_OUTPUT, src_sentence, OUTPUT_FILE, path):
#     print('Running write_hindi_test')
    """Append the hindi text into the file"""
    OUTPUT_FILE = 'TestResults.csv'# temporary for presenting
    str = path.strip('lion_story/')
    if str == '1':
        with open(OUTPUT_FILE, 'w') as file:
            file.write("")

    with open(OUTPUT_FILE, 'a') as file:
        file.write(path.strip('../hindi_gen/lion_story') + '\t')
        file.write(src_sentence.strip('"').strip('\n').strip('#') + '\t')
        file.write(POST_PROCESS_OUTPUT + '\t')
        file.write(hindi_output + '\t')
        file.write('\n')
        # log('Output data write successfully')
    return "Output data write successfully"

def write_masked_hindi_test(hindi_output, POST_PROCESS_OUTPUT, src_sentence, masked_data, OUTPUT_FILE, path):
#     print('Running write_masked_hindi_test')
    """Append the hindi text into the file"""
    OUTPUT_FILE = 'TestResults_masked.csv'  # temporary for presenting
    with open(OUTPUT_FILE, 'a') as file:
        file.write(path.strip('lion_story/') + ',')
        file.write(src_sentence.strip('#') + ',')
        file.write(POST_PROCESS_OUTPUT + ',')
        file.write(hindi_output + ',')
        file.write(masked_data)
        file.write('\n')
        # log('Output data write successfully')
    return "Output data write successfully"

def masked_postposition(processed_words, words_info, processed_verbs):
#     print('Running masked_postposition')
    '''Calculates masked postposition to words wherever applicable according to rules.'''
    masked_PPdata = {}

    for data in processed_words:
        if data[2] not in ('p', 'n', 'other'):
            continue
        data_info = getDataByIndex(data[0], words_info)
        try:
            data_case = False if data_info == False else data_info[4].split(':')[1].strip()
        except IndexError:
            data_case = False
        ppost = ''
        ppost_value = '<>'
        if data_case in ('k1', 'pk1'):
            if findValue('yA', processed_verbs, index=6)[0]:  # has TAM "yA"
                if findValue('k2', words_info, index=4)[0]: # or findExactMatch('k2p', words_info, index=4)[0]:
                    ppost = ppost_value
        elif data_case in ('r6', 'k3', 'k5', 'k5prk', 'k4', 'k4a', 'k7t', 'jk1','k7', 'k7p','k2g', 'k2','rsk', 'ru' ):
            ppost = ppost_value
        elif data_case == 'krvn' and data_info[2] == 'abs':  #abstract noun as adverb
            ppost = ppost_value
        elif data_case in ('k2g', 'k2') and data_info[2] in ("anim", "per"):
            ppost = ppost_value #'ko'
        elif data_case in ('rsm', 'rsma'):
            ppost = ppost_value+ ' ' + ppost_value #ke pAsa
        elif data_case == 'rt':
            ppost = ppost_value+ ' ' + ppost_value #'ke lie'
        elif data_case == 'rv':
            ppost = ppost_value+ ' ' + ppost_value + ' ' + ppost_value#'kI tulanA meM'
        elif data_case == 'r6':
            ppost = ppost_value # 'kI' if data[4] == 'f' else 'kA'
            nn_data = nextNounData(data[0], words_info)
            if nn_data != False:
                #print('Next Noun data:', nn_data)
                if nn_data[4].split(':')[1] in ('k3', 'k4', 'k5', 'k7', 'k7p', 'k7t', 'mk1', 'jk1', 'rt'):
                    ppost = ppost_value
                elif nn_data[3][1] != 'f' and nn_data[3][3] == 'p':
                    ppost = ppost_value#'ke'
                else:
                    pass
        else:
            pass
        if data[2] == 'p':
            temp = list(data)
            temp[7] = ppost if ppost != '' else 0
            data = tuple(temp)
        if data[2] == 'n' or data[2] == 'other':
            temp = list(data)
            temp[8] = ppost if ppost != '' else None
            data = tuple(temp)
            masked_PPdata[data[0]] = ppost
    return masked_PPdata

def clean(word, inplace=''):
    """
    Clean concept words by removing numbers and special characters from it using regex.
    >>> clean("kara_1-yA_1")
    'karayA'
    >>> clean("kara_1")
    'kara'
    >>> clean("padZa_1")
    'pada'
    >>> clean("caDZa_1")
    'caDa'
    """
    # Replace specific patterns
    word = word.replace('dZ', 'd').replace('jZ', 'j').replace('DZ', 'D')
    # Remove numbers and special characters
    return re.sub(r'[^a-zA-Z]+', inplace, word)

def generate_rulesinfo(file_data):
#     print('Running generate_rulesinfo')
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
    # print('generate_rulesinfo : ',[src_sentence, root_words, index_data, seman_data, gnp_data, depend_data, discourse_data, spkview_data,
            # scope_data, sentence_type, construction_data])
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
    # print('spkview_dict',spkview_dict)
    return populate_spk_dict

def generate_wordinfo(root_words, index_data, seman_data, gnp_data, depend_data, discourse_data, spkview_data,
                      scope_data):
#     print('Running generate_wordinfo')
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
    # print('generate_wordinfo : ',root_words, index_data, seman_data, gnp_data, depend_data, discourse_data, spkview_data, scope_data)
    return list(
        zip(index_data, root_words, seman_data, gnp_data, depend_data, discourse_data, spkview_data, scope_data))
    # return check_USR_format(root_words, index_data, seman_data, gnp_data, depend_data, discourse_data, spkview_data, scope_data)

# def check_USR_format(root_words, index_data, seman_data, gnp_data, depend_data, discourse_data, spkview_data,
#                       scope_data):
#     print('Running check_USR_format')
#     '''
#     Functionality:
#     1. To check if root words and their indices are in order
#     2. To ensure that all the tuples of the USR have same number of enteries

#     Returns:
#         Corrected USR as an array of tuples containing word and its USR info (corresponding value on same index in each row) i.e USR info word wise.
#     '''
#     data = [root_words, index_data, seman_data, gnp_data, depend_data, discourse_data, spkview_data, scope_data]
#     len_root = len(root_words)
#     len_index = len(index_data)

#     if len_root > len_index:
#         diff = len_root - len_index
#         while diff:
#             index_data.append(0)
#             diff = diff - 1
#             log(f'{constant.USR_row_info[1]} has lesser enteries as compared to {constant.USR_row_info[0]}')

#     elif len_root < len_index:
#         diff = len_index - len_root
#         while diff:
#             index_data.pop()
#             diff = diff - 1
#             log(f'{constant.USR_row_info[1]} has more enteries as compared to {constant.USR_row_info[0]}')

#     #once the lengths of root_words and index_data are equal check value of each index
#     len_root = len(root_words)
#     len_index = len(index_data)
#     if len_root == len_index:
#         for i in range(1, len_root + 1):
#             if index_data[i - 1] == i:
#                 continue
#             else:
#                 index_data[i - 1] = i
#                 log(f'{constant.USR_row_info[1]} has wrong entry at position {i}')

#     #Checking all tuples have same number of enteries
#     max_col = max(index_data)
#     i = 0
#     for ele in data:
#         length = len(ele)
#         if length < max_col:
#             diff = max_col - length
#             while diff:
#                 ele.append('')
#                 log(f'Added one entry at the end of {constant.USR_row_info[i]}')
#                 diff = diff - 1
#         elif length > max_col:
#             diff = length - max_col
#             while diff:
#                 ele.pop()
#                 log(f'Removed one entry from the end of {constant.USR_row_info[i]}')
#                 diff = diff - 1
#         i = i + 1

#     #Removing spaces if any,before/ after each ele for all rows in USR
#     for row in data:
#         for i in range(0, len(row)):
#             if type(row[i]) != int and row[i] != '':
#                 temp = row[i].strip()
#                 row[i] = temp
#     # print('check_USR_format : ',root_words,index_data, seman_data, gnp_data, depend_data, discourse_data, spkview_data, scope_data)

#     return list(
#         zip(index_data, root_words, seman_data, gnp_data, depend_data, discourse_data, spkview_data, scope_data))

def identify_cat(words_list):
#     print('Running identify_cat')
    '''
    Functionality: There are various categorizations of the concepts such as - nouns, pronouns etc. This function Checks word for its type to process
    accordingly and add that word to its corresponnding list.

    Parameters:
        1. words_list: It is an array of tuples. Each tuple consists of concept wise USR info.

    Returns:
        All the categorized lists of nouns, pronouns etc. with input concept tuple appended in it

    For eg.
        #jaMgala meM eka Sera WA.
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
            log(f'{word_data[1]} identified as foreign word.')
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
            log(f'{word_data[1]} identified as nominal verb form.')
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
#     print('identify_cat : ',foreign_words,indeclinables, pronouns, nouns, adjectives, verbs, adverbs, others, nominal_verb)
    return foreign_words,indeclinables, pronouns, nouns, adjectives, verbs, adverbs, others, nominal_verb

def check_named_entity(word_data):
#     print('Running check_named_entity')
    if word_data[2] == 'ne':
        return True
    # print('check_named_entity returns true or false')
    return False

def check_noun(word_data):
#     print('Running check_noun')
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
        #राम ने दो रोटी और दाल खायी।
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
        # identifying nouns from sem_cat
        if word_data[2] in ('place','Place','ne','NE') and '^' not in word_data[1]:
            return True
        # GNP present for a concept
#         print(word_data[3],'vss')

        if 'pl' == word_data[3]:
            return True
        return False
    except IndexError:
        log(f'Index Error for GNP Info. Checking noun for {word_data[1]}', 'ERROR')
        sys.exit()

def check_pronoun(word_data):
#     print('Running check_pronoun')
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
        #मैंने आज स्नान किया।
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
#     print('Running check_adjective')
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
        #राम ने दो रोटी और दाल खायी।
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

    # Convert the tuple to a list
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

    # Convert the list back to a tuple
    word_data = tuple(word_data_list)

    return False

def check_nonfinite_verb(word_data):
#     print('Running check_nonfinite_verb')
    '''Check if word is a non-fininte verb by the USR info'''

    if word_data[4] != '':
        rel = word_data[4].strip().split(':')[1]
        # if rel in ('rpk','rbk', 'rvks', 'rbks','rsk', 'rbplk'):
        if rel in ('rpk','rbk'):
            return True
    return False

def check_verb(word_data):
#     print('Running check_verb')
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
        #मैंने आज स्नान किया।
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
#     print('Running check_adverb')
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
#     print('Running check_indeclinable')
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
        #मैंने आज स्नान किया।
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
#     print('Running check_digit')
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
#     print('Running check_nominal_verb')
    '''
    Functionality: Check if dependency value belongs to NOMINAL_VERB_DEPENDENCY list and there is no GNP information

    Parameters:
        word_data: tuple of concept with all its information

    Returns:
        True - if any of the above condition is met
        False - otherwise
    '''
    # if word_data[4].strip() != '':
    #     relation = word_data[4].strip().split(':')[1]
    #     gnp_info = word_data[3]
    #     if relation in constant.NOMINAL_VERB_DEPENDENCY and gnp_info == '':
    #         return True
    # return False
    if word_data[4].strip() != '':
        relation = word_data[4].strip().split(':')[1]
        # gnp_info = word_data[3]
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

def check_is_digit(num):
#     print('Running check_is_digit')
    if num.isdigit():
        return True
    else:
        try:
            float_value = float(num)
            return True
        except ValueError:
            return False
    return False

def check_main_verb(depend_data):
    # for verb in verbs_data:
    #     if len(verb[4]) > 0 and verb[4].strip().split(':')[1] == 'main':
    #         main_verb = verb
    #         break
    # if not len(main_verb):
    #     log('USR error. Main verb not identified. Check the USR.')
    #     sys.exit()
    # print(depend_data,'dp')
    flag=False
    for dep in list(depend_data):
        dep1=dep.strip().split(':')[1]
        if  dep1== 'main' or dep1=='rcelab' or dep1=='rcdelim':
            flag=True
            break
    if flag==False:
        log('USR error. Main verb not identified. Check the USR.')
        sys.exit()
            
    

def process_foreign_word(foreign_words_data,words_info,verbs_data):
    print('Running process_foreign_word')
    for verb in verbs_data:
       if len(verb[4]) > 0 and verb[4].strip().split(':')[1] == 'main' or verb[4].strip().split(':')[1] == 'rcelab' or verb[4].strip().split(':')[1] == 'rcdelim':
            main_verb = verb
            break
    processed_foreign_words=[]
    for i in range(len(foreign_words_data)):
        index=foreign_words_data[i][0]
        gender, number, person, case = get_default_GNP()
        category='n'
        type=''
        foreign_list = list(foreign_words_data[i])
        
        foreign_list[1] = foreign_list[1].replace('^','')
        if '_' in foreign_list[1]:
            foreign_list[1]=clean(foreign_list[1])
        foreign_words_data[i] = tuple(foreign_list)
        case,postposition = preprocess_postposition_new('noun', foreign_words_data[i], words_info, main_verb)
        print(postposition,foreign_words_data[i],'ttt')

        processed_foreign_words.append((index,foreign_words_data[i][1],category,case,gender,number,person,type,postposition))
        
    print('process_foreign_word : ',processed_foreign_words)
    return processed_foreign_words


def preprocess_postposition_new(concept_type, np_data, words_info, verb_data):
    '''Calculates postposition to words wherever applicable according to rules.'''
    cp_verb_list = ['prayApreprsa+kara','sahAyawA+kara']
    if len(verb_data) > 0:
        verb_term = verb_data[1]
        print(verb_term,'vt')
        if len(verb_term) > 0:
            root_main = verb_term.strip().split('-')[0].split('_')[0]
    if np_data != ():
        # print('np_data',np_data)
        data_case = np_data[4].strip().split(':')[1]
        data_head = np_data[4].strip().split(':')[0]
        data_index = np_data[0]
        data_seman = np_data[2]
    ppost = ''
    new_case = 'o'
    if data_case in ('k1', 'pk1'):
        if is_tam_ya(verb_data): # has TAM "yA" or "yA_hE" or "yA_WA" marA WA
            k2exists, k2_index = find_match_with_same_head(data_head, 'k2', words_info, index=4) # or if CP_present, then also ne - add #get exact k2, not k2x
            vk2exists, vk2_index = find_match_with_same_head(data_head, 'vk2', words_info, index=4)
            if k2exists:
                ppost = 'ne'
                if is_CP(verb_term):
                    cp_parts = verb_term.strip().split('+')
                    clean_cp_term = ''
                    for part in cp_parts:
                        part = part.split("-")[0]
                        clean_cp_term = clean_cp_term + clean(part) + '+'
                    clean_cp_term = clean_cp_term[0:-1]
                    if clean_cp_term in cp_verb_list:
                        update_additional_words_dict(k2_index, 'after', 'kA')

            elif vk2exists:
                ppost = 'ne'
            else:
                ppost = ''
                log('Karma k2 not found. Output may be incorrect')

        elif identify_complete_tam_for_verb(verb_term) in constant.nA_list:
            ppost = 'ko'
        else:
            log('inside tam ya else')

    elif data_case == 'k2g':
        ppost = process_dep_k2g(data_case, verb_data)
    elif data_case == 'k2': #if CP present, and if concept is k2 for verb of CP, and the verb is not in specific list, then kA
        if data_seman and data_seman!=''and data_seman.split()[0] in ("anim", "per"):
            if clean(root_main) in constant.kisase_k2_verbs:
                ppost = 'se'
            else:
                ppost = 'ko'
        else:
            new_case = 'd'

    elif data_case == 'k2p':
        ppost = '' # modified from meM 22/06
    elif data_case in ('k3', 'k5', 'k5prk'):
        ppost = 'se'
    elif data_case in ('k4', 'k4a', 'k7t', 'jk1'):
        ppost = 'ko'
    elif data_case == 'k7p':
        ppost = 'meM'
    elif data_case =='k7':
        ppost = 'para'
    elif data_case == 'krvn' and data_seman == 'abs':
        ppost = 'se'
    elif data_case == 'rt':
        ppost = 'ke lie'
    elif data_case == 'rblak':
        ppost = 'ke bAxa'
    elif data_case == 'rblpk':
        ppost = 'se pahale'
    elif data_case in ('rsm', 'rsma'):
        ppost = 'ke pAsa'
    elif data_case == 'rhh':
        ppost = 'ke'
    elif data_case == 'rsk':
        ppost = 'hue'
    elif data_case == 'rn':
        ppost = 'meM'
    elif data_case == 'rib':
        ppost = 'se'
    elif data_case == 'ru':
        ppost = 'jEsI'
    elif data_case == 'rkl':
        next_word = fetchNextWord(data_index + 1, words_info)
        if next_word == 'bAxa':
            ppost = 'ke'
        elif next_word == 'pahale':
            ppost = 'se'

    elif data_case == 'rdl':
        next_word = fetchNextWord(data_index + 1, words_info)
        if next_word in ('anxara', 'bAhara', 'Age', 'sAmane', 'pICe', 'Upara', 'nIce', 'xAyeM',
                         'bAyeM', 'cAroM ora', 'bIca', 'pAsa'):
            ppost = 'ke'
        elif next_word == 'xUra':
            ppost = 'se'

    elif data_case == 'rv':
        ppost = 'se'
    elif data_case == 'rh':
        ppost = 'ke_kAraNa'
    elif data_case == 'rd':
        ppost = 'kI ora'
    elif 'rask' in data_case:
        ppost = 'ke sAWa'
    elif data_case == 'r6':
        ppost = 'kA' #if data[4] == 'f' else 'kA'
        nn_data = nextNounData(data_index, words_info)
        if nn_data != False:
            if nn_data[4].split(':')[1] in ('k3', 'k4', 'k5', 'k7', 'k7p', 'k7t', 'r6', 'mk1', 'jk1', 'rt'):
                ppost = 'ke'
                if nn_data[3][2] == 's':#agreement with gnp
                    if nn_data[3][1] == 'f':
                        ppost = 'kI'
                    else:
                        ppost = 'kA'
                else:
                    pass
    else:
        pass
    if ppost == '':
        new_case = 'd'

    if concept_type == 'noun':
        if ppost == '':
            ppost = None
        processed_postpositions_dict[data_index] = ppost

    if concept_type == 'pronoun':
        if ppost == '':
            ppost = 0
        processed_postpositions_dict[data_index] = ppost
    return new_case, ppost

def process_nominal_verb(nominal_verbs_data, processed_noun, words_info, verbs_data):

   nominal_verbs = []
   for verb in verbs_data:
       if len(verb[4]) > 0 and verb[4].strip().split(':')[1] == 'main' or verb[4].strip().split(':')[1] == 'rcelab' or verb[4].strip().split(':')[1] == 'rcdelim':
            main_verb = verb
            break

   for nominal_verb in nominal_verbs_data:
        index = nominal_verb[0]
        term = clean(nominal_verb[1])
        gender = 'm'
        number = 's'
        person = 'a'
        category = 'n'
        noun_type = 'common'
        case = 'o'
        postposition = ''
        log_msg = f'{term} identified as nominal, re-identified as other word and processed as common noun with index {index} gen:{gender} num:{number} person:{person} noun_type:{noun_type} case:{case} and postposition:{postposition}'

        relation = ''
        if nominal_verb[4] != '':
            relation = nominal_verb[4].strip().split(':')[1]
        # verb = Verb()

        # verb.type = 'nonfinite'
        # verb.tam = ''
        # tam=''
        # tam = set_tam_for_nonfinite(relation)

        case, postposition = preprocess_postposition_new('noun', nominal_verb, words_info, main_verb)
        tags = find_tags_from_dix_as_list(term)
        for tag in tags:
            if (tag[0] == 'cat' and tag[1] == 'v'):
                noun_type = 'vn'
                category='vn'
                # if relation =='rblak':
                #     term = term + 'ne_ke_bAxa'
                if relation in ('k2', 'rt', 'rh','rblpk','rblak','rblsk'):
                    term = term + 'nA'
                    log_msg = f'{term} processed as nominal verb with index {index} gen:{gender} num:{number} person:{person} noun_type:{noun_type} case:{case} and postposition:{postposition}'
                    break
                elif relation in ('k1'):
                    case='d'
                    term = term + 'nA'
                    log_msg = f'{term} processed as nominal verb with index {index} gen:{gender} num:{number} person:{person} noun_type:{noun_type} case:{case} and postposition:{postposition}'
                    break

        noun = (index, term, category, case, gender, number, person, noun_type, postposition)
        # processed_noun.append(noun)
        nominal_verbs.append(noun)
        log(log_msg)
   print(nominal_verbs,'nominal')
   return nominal_verbs

def process_adverb_as_noun(concept, processed_nouns):
    index, term, *_ = concept
    case = 'd' if ('+se_') not in term else 'o'
    term = clean(term.split('+')[0])
    category, gender, number, person, noun_type, postposition = 'n', 'm', 'p', 'a', 'abstract', 'se'
    processed_postpositions_dict[index] = postposition
    noun = (index, term, category, case, gender, number, person, noun_type, postposition)
    processed_nouns.append(noun)
    log(f' Adverb {term} processed as an abstract noun with index {index} gen:{gender} num:{number} case:{case},noun_type:{noun_type} and postposition:{postposition}')
    return

def process_adverb_as_verb(concept, processed_verbs):
    index, term, *_ = concept
    term = clean(term)
    gender, number, person, category, type, case = 'm', 's', 'a', 'v', 'adverb', 'd'
    tags = find_tags_from_dix_as_list(term)
    for tag in tags:
        if tag[0] == 'cat' and tag[1] == 'v':
            tam = 'kara'
            adverb = (index, term, category, gender, number, person, tam, case, type)
            processed_verbs.append(adverb)
            log(f'{term} adverb processed as a verb with index {index} gen:{gender} num:{number} person:{person}, and tam:{tam}')
            return

def process_adverbs(adverbs, processed_nouns, processed_verbs, processed_indeclinables, reprocessing):
    for adverb in adverbs:
        term = clean(adverb[1])
        if '+se_' in term or adverb[2] == 'abs':  # for adverbs like jora+se
            if not reprocessing:
                process_adverb_as_noun(adverb, processed_nouns)
        else:  # check morph tags
            tags = find_tags_from_dix_as_list(term)
            for tag in tags:
                if tag[0] == 'cat' and tag[1] == 'v':  # term type is verb in morph dix
                    return process_adverb_as_verb(adverb, processed_verbs)
                elif tag[0] == 'cat' and tag[1] == 'adj':  # term type is adjective in morph dix
                    term += 'rUpa se'
                    processed_indeclinables.append((adverb[0], term, 'indec'))
                    log(f'adverb {adverb[1]} processed indeclinable with form {term}')
                else:
                    for processed in processed_indeclinables:
                        if term == processed[1]:
                            log(f'adverb {adverb[1]} already processed indeclinable, no processing done')
                            return
                    processed_indeclinables.append((adverb[0], term, 'indec'))  # to be updated, when cases arise.
                    log(f'adverb {adverb[1]} processed indeclinable with form {term}, no processing done')
                    return

def process_indeclinables(indeclinables):
    '''
    Functionality:
        1. They do not require any furthur processing
        2. Make a tuple with - index, term, type(indec)

    Parameters:
        indeclinables: List of indeclinable data

    Returns:
        list of tuples.

    for eg.     :
        indeclinables: [(2, 'Aja_1', '', '', '3:k7t', '', '', '')]

    Result:
       processed_indeclinables: [(2, 'Aja', 'indec')]
    '''

    processed_indeclinables = []
    for indec in indeclinables:
        clean_indec = clean(indec[1])
        processed_indeclinables.append((indec[0], clean_indec, 'indec'))
    return processed_indeclinables

def process_nouns(nouns, words_info, verbs_data):
    '''
    Functionality:
        1. Make a noun tuple
        2. We update update_additional_words_dict(index, 'before', 'eka'), if number == 's' and noun[6] == 'some'

    Parameters:
        1. nouns - List of noun data
        2. words_info - List of USR info word wise
        3. verbs_data - List of verbs data

    Returns:
        processed_nouns = List of noun tuples where each tuple looks like - (index, word, category, case, gender, number, proper/noun type= proper, common, NC, nominal_verb, CP_noun or digit, postposition)

    For eg.:
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

        nouns     : [(1, 'rAma', 'male per', 'sg', '6:k1', '', '', ''), (3, 'rotI_1', '', 'sg', '6:k2', '', '', ''), (4, 'xAla_1', '', 'sg', '6:k2', '', '', '')]
        words_info     : [(1, 'rAma', 'male per', 'sg', '6:k1', '', '', ''), (2, 'xo_1', '', '', '3:card', '', '', ''), (3, 'rotI_1', '', 'sg', '6:k2', '', '', ''), (4, 'xAla_1', '', 'sg', '6:k2', '', '', ''), (5, 'KA_1-yA_1', '', '', '0:main', '', '', '')]
        verbs_data     : [(5, 'KA_1-yA_1', '', '', '0:main', '', '', '')]

    Result:
        processed_nouns     : [(1, 'rAma', 'n', 'o', 'm', 's', 'a', 'proper', 'ne'), (3, 'rotI', 'n', 'd', 'f', 's', 'a', 'common', None), (4, 'xAla', 'n', 'd', 'f', 's', 'a', 'common', None)]
    '''

    processed_nouns = []
    main_verb = ''
    for verb in verbs_data:
        if len(verb[4]) > 0 and verb[4].strip().split(':')[1] == 'main' or verb[4].strip().split(':')[1] == 'rcelab' or verb[4].strip().split(':')[1] == 'rcdelim':
            main_verb = verb
            break
    # if not len(main_verb):
    #     log('USR error. Main verb not identified. Check the USR.')
    #     sys.exit()
        # return None

    for noun in nouns:
        category = 'n'
        index = noun[0]
        dependency = noun[4].strip().split(':')[1]
        gender, number, person = extract_gnp_noun(noun)

        if noun[6] == 'respect': # respect for nouns
            number = 'p'
        noun_type = 'common' if '_' in noun[1] else 'proper'

        case, postposition = preprocess_postposition_new('noun', noun, words_info, main_verb)

        if '+' in noun[1]:
            processed_nouns = handle_compound_nouns(noun, processed_nouns, category, case, gender, number, person, postposition)
        else:
            term = noun[1]
            if check_is_digit(term):
                if '_' in term:
                    clean_noun = term.strip().split('_')[0]
                else:
                    clean_noun = term
                noun_type = 'digit'
            else:
                clean_noun = clean(noun[1])

            processed_nouns.append((noun[0], clean_noun, category, case, gender, number, person, noun_type, postposition))

            if number == 's' and noun[6] == 'some':
                update_additional_words_dict(index, 'before', 'eka')

        log(f'{noun[1]} processed as noun with case:{case} gen:{gender} num:{number} noun_type:{noun_type} postposition: {postposition}.')
        # print(processed_nouns,'pn')
    return processed_nouns

def process_pronouns(pronouns, processed_nouns, processed_indeclinables, words_info, verbs_data):
    '''
        Functionality:
            1. Make a pronoun tuple
            2. If the term is kim, there is separate handling
            3. If term is yahAz or vahAz along with discourse data as 'emphasis' we convert it to yahIM, vahIM and treat them as indeclinables which do not require furthur processing
            4. If dependency is r6, then use the dependency_head to fetch the related noun data, and pick fnum, gender and case of this pronoun term same as related noun.
            5. Except for r6 relation, fnum is by default None

        Parameters:
            1. pronouns - List of pronoun data
            2. processed_nouns - List of processed noun data
            3. processed_indeclinables - List of processed indeclinable data
            2. words_info - List of USR info word wise
            3. verbs_data - List of verbs data

        Returns:
            processed_pronouns = List of pronoun tuples where each tuple looks like - (index, word, category, case, gender, number, person, parsarg, fnum)

        For eg.:
            yaha_1,aBiprAya_8,yaha_1,hE_1-pres
            1,2,3,4
            ,,,
            ,,sg,
            2:r6,4:k1,4:k1s,0:main
            ,,Geo_ncert_6stnd_4ch_0031d:coref,
            ,,,
            ,,,
            affirmative

            pronouns     : [(1, 'yaha_1', '', '', '2:r6', '', '', ''), (3, 'yaha_1', '', 'sg', '4:k1s', 'Geo_ncert_6stnd_4ch_0031d:coref', '', '')]
            words_info     : [(1, 'yaha_1', '', '', '2:r6', '', '', ''), (2, 'aBiprAya_8', '', '', '4:k1', '', '', ''), (3, 'yaha_1', '', 'sg', '4:k1s', 'Geo_ncert_6stnd_4ch_0031d:coref', '', ''), (4, 'hE_1-pres', '', '', '0:main', '', '', '')]
            verbs_data     : [(4, 'hE_1-pres', '', '', '0:main', '', '', '')]

        Result:
            processed_nouns     : [(1, 'yaha', 'p', 'd', 'm', 's', 'a', 'kA', 's'), (3, 'yaha', 'p', 'd', 'm', 's', 'a', 0, None)]
        '''

    processed_pronouns = []
    for verb in verbs_data:
        if len(verb[4]) > 0 and verb[4].strip().split(':')[1] == 'main' or verb[4].strip().split(':')[1] == 'rcelab' or verb[4].strip().split(':')[1] == 'rcdelim':
            main_verb = verb
            break

    for pronoun in pronouns:
        index = pronoun[0]
        term = clean(pronoun[1])
        anim = pronoun[2]
        gnp = pronoun[3]
        relation_head = pronoun[4].strip().split(':')[0]
        relation = pronoun[4].strip().split(':')[1]
        spkview_data = pronoun[6]

        if is_kim(term):
            processed_pronouns, processed_indeclinables = process_kim(index, relation, anim, gnp, pronoun, words_info,
                                                                      main_verb, processed_pronouns, processed_indeclinables, processed_nouns)
        else:
            category = 'p'
            case = 'o'
            parsarg = 0

            if term in ['yahAz', 'vahAz'] and spkview_data == 'emphasis':
                term = term.replace('Az', 'IM')
                category = 'indec'
                processed_indeclinables.append((index, term, category))
                break

            case, postposition = preprocess_postposition_new('pronoun', pronoun, words_info, main_verb)
            if postposition != '':
                parsarg = postposition

            fnum = None
            gender, number, person = extract_gnp(pronoun)
            nn_data = is_next_word_noun(index+1, processed_nouns)
            if nn_data:
                number=nn_data[5]
                if number=='':
                    number='s'
                # print(nn_data,'nnnn')
            # print(nn_data,'nn_d')
            if term == 'addressee':
                addr_map = {'respect': 'Apa', 'informal': 'wU', '': 'wU'}
                pronoun_per = {'respect': 'm', 'informal': 'm', '': 'm_h1'}
                pronoun_number = {'respect': 'p', 'informal': 's', '': 'p'}
                word = addr_map.get(spkview_data.strip().lower(), 'wU')
                person = pronoun_per.get(spkview_data.strip().lower(), 'm_h1')
                number = pronoun_number.get(spkview_data.strip(), 'p')
            elif term == 'speaker':
                word = 'mEM'
            elif term == 'wyax':
                if spkview_data == "distal" and relation=='dem':
                    word = 'vaha'
                    case='o'
                elif nn_data and number=='p' and spkview_data == "proximal" and relation=='dem':
                    word = 'yaha'
                    case='o'
                elif nn_data and number=='s' and spkview_data == "proximal" and relation=='dem':
                    word = 'yaha'
                    case='o'
                    # number='p'
                    # print('klm')
                    # term=word
                    # tags = find_tags_from_dix_as_list(term)
                    # print(tags,'tg')
                    # for tag in tags:
                    #     if tag == ('cat', 'p') and tag == ('num','p'):
                    #         # noun_type = category = 'vn'
                    #         word='ina'
                    #         n="cat:p"/><s n="case:o"/><s n="parsarg:0"/><s n="gen:m"/><s n="num:p"/><s n="per:a"/></r></p></e>
                            
                elif spkview_data == "distal":
                    word = 'vaha'
                elif spkview_data == "proximal":
                    word = 'yaha'
                else:
                    word = term
            else:
                word = term

            if relation == "r6":
                fnoun = int(relation_head)
                fnoun_data = getDataByIndex(fnoun, processed_nouns, index=0)
                if fnoun_data:
                    gender = fnoun_data[4]  # To-ask
                    fnum = number = fnoun_data[5]
                    case = fnoun_data[3]
                if term == 'apanA':
                    parsarg = '0'

            processed_pronouns.append((index, word, category, case, gender, number, person, parsarg, fnum))
            log(f'{term} processed as pronoun with case:{case} par:{parsarg} gen:{gender} num:{number} per:{person} fnum:{fnum}')
    return processed_pronouns

def process_others(other_words):
    '''Process other words. Right now being processed as noun with default gnp'''
    processed_others = []
    for word in other_words:
        gender = 'm'
        number = 's'
        person = 'a'
        processed_others.append((word[0], clean(word[1]), 'other', gender, number, person))
    return processed_others

def process_verbs(verbs_data, seman_data, depend_data, sentence_type, spkview_data, processed_nouns, processed_pronouns, words_info,process_nominal_form, reprocess=False):
    '''
    Functionality:
        1. In the list of verbs data, identify
            a) if it is complex predicate - it is appended in processed_nouns
            b) if verb_type == 'nonfinite': - process the concept and append in processed_verbs
            c) otherwise process main verb and auxilliary verbs and append in respective lists
    Parameters:
         verbs_data: List of verbs data
         seman_data: Semantic data row of USR
         depend_data: Dependency data row of USR
         sentence_type: Sentence type
         spkview_data: Speaker's view data row of USR
         processed_nouns: List of processed_nouns
         processed_pronouns: List of processed_pronouns
         words_info: List of USR info word wise
         reprocess: for first time processing, it is False. In case of changes, it is made True and sent as parameter

        :Returns:
        List of processed_verbs and processed_auxverbs
    '''
    processed_verbs = []
    processed_auxverbs = []
    for concept in verbs_data:
        concept_dep_head = concept[4].strip().split(':')[0]
        concept_dep_val = concept[4].strip().split(':')[1]
        concept = Concept(index=concept[0], term=concept[1], dependency=concept[4])
        if(concept_dep_val == 'vk2'):
            update_additional_words_dict(int(concept_dep_head), 'after', 'ki')
        is_cp = is_CP(concept.term)
        print(concept.term)
        if is_cp:
            if not reprocess:
                CP = process_main_CP(concept.index, concept.term)
                if CP != [] and CP[2] == 'n':
                    log(f'{CP[1]} processed as noun with index {CP[0]} case:d gen:{CP[4]} num:{CP[5]} per:{CP[6]}, noun_type:{CP[7]}, default postposition:{CP[8]}.')
                    processed_nouns.append(tuple(CP))
        verb_type = identify_verb_type(concept)
        if verb_type == 'nonfinite':
            verb = process_nonfinite_verb(concept, seman_data, depend_data, sentence_type, processed_nouns, processed_pronouns,process_nominal_form, words_info)
            processed_verbs.append(to_tuple(verb))
        else:
            # if process_verb(concept, seman_data, depend_data, sentence_type, spkview_data, processed_nouns, processed_pronouns, reprocess):
            verb, aux_verbs = process_verb(concept, seman_data, depend_data, sentence_type, spkview_data, processed_nouns, processed_pronouns,process_nominal_form, reprocess)
            processed_verbs.append(to_tuple(verb))
            log(f'{verb.term} processed as main verb with index {verb.index} gen:{verb.gender} num:{verb.number} case:{verb.case}, and tam:{verb.tam}')
            processed_auxverbs.extend([to_tuple(aux_verb) for aux_verb in aux_verbs])
    return processed_verbs, processed_auxverbs

def process_adjectives(adjectives, processed_nouns, processed_verbs):
    '''Process adjectives as (index, word, category, case, gender, number)
        '''
    processed_adjectives = []
    gender, number, person, case = get_default_GNP()
    for adjective in adjectives:
        index = adjective[0]
        category = 'adj'
        adj = clean(adjective[1])

        relConcept = int(adjective[4].strip().split(':')[0]) # noun for regular adjcetives, and verb for k1s-samaadhikaran
        relation = adjective[4].strip().split(':')[1]
        if relation == 'k1s':
            if adj =='kim':
                adj = 'kEsA'
            relConcept_data = getDataByIndex(relConcept, processed_verbs)
        else:
            relConcept_data = getDataByIndex(relConcept, processed_nouns)

        if not relConcept_data:
            log(f'Associated noun/verb not found with the adjective {adjective[1]}. Using default m,s,a,o ')
        else:
            gender, number, person, case = get_gnpcase_from_concept(relConcept_data)
            if relation == 'k1s':
                case = 'd'

        if adj == 'kim' and relation == 'krvn':
            adj = 'kEsA'
        adjective = (index, adj, category, case, gender, number)
        processed_adjectives.append((index, adj, category, case, gender, number))
        log(f'{adjective[1]} processed as an adjective with case:{case} gen:{gender} num:{number}')
    return processed_adjectives

def process_kim(index, relation, anim, gnp, pronoun, words_info, main_verb, processed_pronouns, processed_indeclinables, processed_nouns):
    term = get_root_for_kim(relation, anim, gnp)
    if term == 'kyoM':
        processed_indeclinables.append((index, term, 'indec'))
    else:
        category = 'p'
        case = 'o'
        parsarg = 0
        case, postposition = preprocess_postposition_new('pronoun', pronoun, words_info, main_verb)
        if postposition != '':
            parsarg = postposition

        fnum = None
        gender, number, person = extract_gnp(pronoun[3])

        if "r6" in pronoun[4]:
            fnoun = int(pronoun[4][0])
            fnoun_data = getDataByIndex(fnoun, processed_nouns, index=0)
            gender = fnoun_data[4]  # To-ask
            fnum = number = fnoun_data[5]
            case = fnoun_data[3]
            if term == 'apanA':
                parsarg = '0'

        if term in ('kahAz'):
            parsarg = 0
        processed_pronouns.append((pronoun[0], term, category, case, gender, number, person, parsarg, fnum))
        log(f'kim processed as pronoun with term: {term} case:{case} par:{parsarg} gen:{gender} num:{number} per:{person} fnum:{fnum}')
    return processed_pronouns, processed_indeclinables

# def process_imp_sentence(words_info, processed_pronouns):
#     k1exists = findExactMatch('k1', words_info, index=4)[0]
#     if not k1exists:
#         temp = (0.9, 'wU', 'p', 'd', 'm', 's', 'm_h1', 0, None)
#         processed_pronouns.insert(0, temp)
#     return processed_pronouns

def process_main_CP(index, term):
    """
    >>> process_main_CP(2,'varRA+ho_1-gA_1')
    [1.9, 'varRA', 'n', 'd', 'm', 's', 'a', 'CP_noun', None]
    """
    CP_term = clean(term.split('+')[0])
    CP_index = index - 0.1
    gender = 'm'
    number = 's'
    person = 'a'
    postposition = None
    CP = []
    tags = find_tags_from_dix(CP_term)  # getting tags from morph analyzer to assign gender and number for agreement
    if '*' not in tags['form']:
        gender = tags['gen']
        number = tags['num']
        category = tags['cat']
    CP = [CP_index, CP_term, 'n','d', gender, number, person, 'CP_noun', postposition]
    return CP

def process_construction(processed_words, construction_data, depend_data, gnp_data, index_data):
    # Adding Ora or yA as a tuple to be sent to morph/ adding it at join_compounds only
    # if k1 in conj, all k1s and main verb g - m and n - pl
    # if all k1 male or mix - k1s g - male else g - f
    # cons list - can be more than one conj
    # k1 ka m/f/mix nikalkr k1s and verb ko g milega    index dep:gen
    # map to hold conj kaha aega
    # print('Running process_construction')
    construction_dict.clear()
    process_data = processed_words
    dep_gender_dict = {}
    a = 'after'
    b = 'before'
    if gnp_data != []:
        gender = []
        for i in range(len(gnp_data)):
            gnp_info = gnp_data[i]
            gnp_info = gnp_info.strip().strip('][')
            gnp = gnp_info.split(' ')
            gender.append(gnp[0])

    if depend_data != []:
        dependency = []
        for dep in depend_data:
            if dep != '':
                dep_val = dep.strip().split(':')[1]
                dependency.append(dep_val)

    for i, dep, g in zip(index_data, dependency, gender):
        dep_gender_dict[str(i)] = dep + ':' + g

    if construction_data != '*nil' and len(construction_data) > 0:
        construction = construction_data.strip().split(' ')
        for cons in construction:
            conj_type = cons.split(':')[0].strip().lower()
            # index = cons.split('@')[1].strip().strip('][').split(',') if '@' in cons else cons.strip().strip('][').split(',')
            # print(index,'vlllllllllllll')
            index = cons.split(':')[1].strip().strip('][').split(',')
            length_index = len(index)
            if conj_type == 'conj' or conj_type == 'disjunct':
                cnt_m = 0
                cnt_f = 0
                PROCESS = False
                for i in index:
                    print(index,'index',dep_gender_dict)
                    # print(dep_gender_dict[i],'llll')
                    relation = dep_gender_dict[i]
                    # print(dep_gender_dict[i],'llll')
                    dep = relation.split(':')[0]
                    gen = relation.split(':')[1]

                    if dep == 'k1':
                        PROCESS = True
                        if gen == 'm':
                            cnt_m = cnt_m + 1
                        elif gen == 'f':
                            cnt_f = cnt_f + 1

                if PROCESS:
                    if cnt_f == length_index:
                        g = 'f'
                        num = 'p'
                    else:
                        g = 'm'
                        num = 'p'
                    process_data = set_gender_make_plural(processed_words, g, num)

                update_index = index[length_index - 2]
                # check if update index is NC
                #if true then go till NC_head index update same index in construction dict and remove ppost if any from processed
                for i in index:
                    if i == update_index:
                        if is_update_index_NC(i, processed_words):
                            index_NC_head = fetch_NC_head(i, processed_words)
                            i = index_NC_head
                        if conj_type == 'conj':
                            temp = (a, 'Ora')
                        elif conj_type == 'disjunct':
                            temp = (a, 'yA')
                        break
                    else:
                        temp = (a, ',')
                        if float(i) in construction_dict:
                            construction_dict[float(i)].append(temp)
                        else:
                            construction_dict[float(i)] = [temp]

                        # if i in ppost_dict remove ppost rAma kA Ora SAma kA -> rAma Ora SAma kA
                        if float(i) in processed_postpositions_dict:
                            del processed_postpositions_dict[float(i)]

                if float(i) in construction_dict:
                    construction_dict[float(i)].append(temp)
                else:
                    construction_dict[float(i)] = [temp]

                if float(i) in processed_postpositions_dict:
                    del processed_postpositions_dict[float(i)]

            elif conj_type == 'list':
                length_list = len(index)
                for i in range(len(index)):
                    if i == length_list - 1:
                        break

                    if i == 0:
                        temp = (b, 'jEse')
                        if index[i] in construction_dict:
                            construction_dict[index[i]].append(temp)
                        else:
                            construction_dict[index[i]] = [temp]
                        temp = (a, ',')

                    elif i < length_list - 1:
                        temp = (a, ',')

                    if index[i] in construction_dict:
                        construction_dict[index[i]].append(temp)
                    else:
                        construction_dict[index[i]] = [temp]
    # print('process_construction : ',process_data)
    return process_data

def process_construction_span(processed_words, construction_data, depend_data, gnp_data, index_data):
    construction_dict.clear()
    process_data = processed_words
    dep_gender_dict = {}
    a = 'after'
    b = 'before'

    if construction_data != '*nil' and len(construction_data) > 0:
        construction = construction_data.strip().split(' ')
        for cons in construction:

            conj_type = cons.split(':')[0].strip().lower()
            index = cons.split(':')[1].strip(' ').strip().strip('][').split(',')
            length_index = len(index)
            if conj_type == '*span':
                cnt_m = 0
                cnt_f = 0
                PROCESS = False
                start_idx = index[0].split('@')[0]
                end_idx = index[1].split('@')[0]
                index=[start_idx,end_idx]
                update_index = index[length_index - 2]
                for i in range(len(index)):
                    if index[i] == update_index:
                        if start_idx=='':
                            temp= (a, 'waka')
                        elif end_idx == '':
                            temp = (a, 'se')
                        elif start_idx != '@'and end_idx != '@':
                            temp = (a, 'se')
                            temp1= (a, 'waka')
                        break
                    else:
                        temp = (a, ',')
                        if float(index[i]) in construction_dict:
                            construction_dict[float(index[i])].append(temp)
                        else:
                            construction_dict[float(index[i])] = [temp]

                        if float(index[i]) in processed_postpositions_dict:
                            del processed_postpositions_dict[float(i)]

                if index[i]!='' and float(index[i]) in construction_dict:
                    if index[i]!='':
                        construction_dict[float(index[i])].append(temp)
                    if index[i+1]!='':
                        construction_dict[float(index[i+1])].append(temp1)
                else:
                    if start_idx!='' and end_idx!='':
                        construction_dict[float(index[i])] = [temp]
                        construction_dict[float(index[i+1])]=[temp1]
                    elif start_idx!='':
                        construction_dict[float(index[i])] = [temp]
                    elif end_idx!='':
                        construction_dict[float(index[i+1])] = [temp]

                if index[i]!='' and float(index[i]) in processed_postpositions_dict:
                    del processed_postpositions_dict[float(i)]

    return process_data

def process_auxiliary_verbs(verb: Verb, concept, spkview_data) -> [Verb]:
    """
    >>> [to_tuple(aux) for aux in process_auxiliary_verbs(Verb(index=4, term = 'kara', gender='m', number='s', person='a', tam='hE', type= 'Auxillary'), concept_term='kara_17-0_sakawA_hE_1')]
    [(4.1, 'saka', 'v', 'm', 's', 'a', 'wA', 'Auxillary'), (4.2, 'hE', 'v', 'm', 's', 'a', 'hE',''Auxillary'')]
    """
    concept_term = concept.term
    concept_index = concept.index
    HAS_SHADE_DATA = False
    auxiliary_term_tam = []
    shade_index = 1
    for data in spkview_data:
        if data != '':
            data = data.strip().strip('][')
            if 'shade' in data and concept_index == shade_index:
                term = clean(data.split(':')[1])
                tam = identify_default_tam_for_main_verb(concept_term)
                HAS_SHADE_DATA = True
                break
        shade_index = shade_index + 1

    if HAS_SHADE_DATA:
        if term == 'jA' and tam == 'yA':
            tam = 'yA1'   # to generate gayA from jA-yA
        temp = (term, tam)
        auxiliary_term_tam.append(temp)
        verb = set_main_verb_tam_zero(verb)

    auxiliary_verb_terms = identify_auxillary_verb_terms(concept_term)
    for v in auxiliary_verb_terms:
        term, tam = auxmap_hin(v)
        temp = (term, tam)
        auxiliary_term_tam.append(temp)

    return [create_auxiliary_verb(index, pair[0], pair[1], verb) for index, pair in enumerate(auxiliary_term_tam)]

def process_dep_rbks(concept, words_info, processed_nouns, processed_pronouns):
    finalData = []
    k1_exists, k1_index = find_match_with_same_head(concept.index, 'k1', words_info, index=4)
    k3_exists, k3_index = find_match_with_same_head(concept.index, 'k3', words_info, index=4)
    if k1_exists:
        case = 'o'
        ppost = 'ke xvArA'

        for i in range(len(processed_nouns)):
            data = processed_nouns[i]
            data_index = data[0]
            if data_index == k1_index:
                temp = list(data)
                temp[3] = case
                temp[8] = ppost
                processed_nouns[i] = tuple(temp)
                update_ppost_dict(data_index, ppost)

    elif k3_exists:
        case = 'o'
        ppost = 'ke xvArA'

        for i in range(len(processed_nouns)):
            data = processed_nouns[i]
            data_index = data[0]
            if data_index == k3_index:
                temp = list(data)
                temp[3] = case
                temp[8] = ppost
                processed_nouns[i] = tuple(temp)
                update_ppost_dict(data_index, ppost)

def process_verb(concept: Concept, seman_data, dependency_data, sentence_type, spkview_data, processed_nouns, processed_pronouns,process_nominal_form, reprocessing):
    """
    concept pattern: 'main_verb' - 'TAM for main verb' _Aux_verb+tam...
    Example 1:
    kara_1-wA_hE_1
    main verb - kara,  main verb tam: wA, Aux -hE with TAM hE (identified from tam mapping file)

    Example 2:
    kara_1-yA_1
    main verb - kara,  main verb tam: yA,

    Example 3:
    kara_1-0_rahA_hE_1
    main verb - kara,  main verb tam: 0, Aux verb -rahA with TAM hE, Aux -hE with TAM hE (identified from tam mapping file)

    Example 4:
    kara_1-0_sakawA_hE_1
    main verb - kara,  main verb tam: 0, Aux verb -saka with TAM wA, Aux -hE with TAM hE (identified from tam mapping file)

    *Aux root and Aux TAM identified from auxillary mapping File
    """
    # if process_main_verb(concept, seman_data, dependency_data, sentence_type, processed_nouns, processed_pronouns, reprocessing):
    verb = process_main_verb(concept, seman_data, dependency_data, sentence_type, processed_nouns, processed_pronouns,process_nominal_form, reprocessing)
    auxiliary_verbs = process_auxiliary_verbs(verb, concept, spkview_data)
    return verb, auxiliary_verbs
    # else:
    #     return None

def process_nonfinite_verb(concept, seman_data, depend_data, sentence_type, processed_nouns, processed_pronouns,process_nominal_form, words_info):
    '''
    >>process_nonfinite_verb([], [()],[()])
    '''
    gender = 'm'
    number = 's'
    person = 'a'
    verb = Verb()
    verb.index = concept.index
    is_cp = is_CP(concept.term)
    if is_cp: #only CP_head as nonfinite verb
        draft_concept = concept.term.split('+')[1]
        verb.term  = clean(draft_concept)
    else:
        verb.term = clean(concept.term)

    verb.type = 'nonfinite'
    verb.tam = ''
    relation = concept.dependency.strip().split(':')[1]
    if relation == 'rbks':
        process_dep_rbks(concept, words_info, processed_nouns, processed_pronouns)

    verb.tam = set_tam_for_nonfinite(relation)
    full_tam = verb.tam
    # if getVerbGNP_new(verb.term, full_tam, is_cp, seman_data, depend_data, sentence_type, processed_nouns, processed_pronouns):
    gender, number, person = getVerbGNP_new(verb.term, full_tam, is_cp, seman_data, depend_data, sentence_type, processed_nouns, processed_pronouns,process_nominal_form)
    verb.gender = gender
    verb.number = number
    verb.person = person
    verb.case = 'o' # to be updated - agreement with following noun
    log(f'{verb.term} processed as nonfinite verb with index {verb.index} gen:{verb.gender} num:{verb.number} case:{verb.case}, and tam:{verb.tam}')
    return verb
    # else:
    #     return None

def process_dep_k2g(data_case, main_verb):
    verb = identify_main_verb(main_verb[1])
    if verb in constant.kisase_k2g_verbs:
        ppost = 'se'
    else:
        ppost = 'ko'
    return ppost

def process_main_verb(concept: Concept, seman_data, dependency_data, sentence_type, processed_nouns, processed_pronouns,process_nominal_form, reprocessing):
    """
    >>> to_tuple(process_main_verb(Concept(index=2, term='varRA+ho_1-gA_1', dependency='0:main'), ['2:k7t', '0:main'], [(1, 'kala', 'n', 'o', 'm', 's', 'a', 'common', None)], [], False))
    [OK]     : varRA processed as noun with index 1.9 case:d gen:f num:s per:a, noun_type:CP_noun, default postposition:None.
    (2, 'ho', 'v', 'f', 's', 'a', 'gA')
    >>> to_tuple(process_main_verb(Concept(index=2, term='varRA+ho_1-gA_1', dependency='0:main'), ['2:k7t', '0:main'], [(1, 'kala', 'n', 'o', 'm', 's', 'a', 'common', None)], [], True))
    [OK]     : ho reprocessed as verb with index 2 gen:f num:s per:a in agreement with CP
    (2, 'ho', 'v', 'f', 's', 'a', 'gA')
    >>>
    """
    verb = Verb()
    verb.type = "main"
    verb.index = concept.index
    verb.term = identify_main_verb(concept.term)
    full_tam = identify_complete_tam_for_verb(concept.term)
    verb.tam = identify_default_tam_for_main_verb(concept.term)
    if verb.term == 'hE' and verb.tam in ('pres', 'past'):  # process TAM
        alt_tam = {'pres': 'hE', 'past': 'WA'}
        alt_root = {'pres': 'hE', 'past': 'WA'}
        verb.term = alt_root[verb.tam]  # handling past tense by passing correct root WA
        verb.tam = alt_tam[verb.tam]
    if verb.term == 'jA' and verb.tam == 'yA':
        verb.tam = 'yA1'

    is_cp = is_CP(concept.term)
    # if getVerbGNP_new(concept.term, full_tam, is_cp, seman_data, dependency_data, sentence_type, processed_nouns, processed_pronouns):
    verb.gender, verb.number, verb.person = getVerbGNP_new(concept.term, full_tam, is_cp, seman_data, dependency_data, sentence_type, processed_nouns, processed_pronouns,process_nominal_form)
    return verb
    # else:
    #     return None


def create_auxiliary_verb(index, term, tam, main_verb: Verb):
#     print('Running create_auxiliary_verb')
    verb = Verb()
    verb.index = main_verb.index + (index + 1)/10
    verb.gender, verb.number, verb.person = main_verb.gender, main_verb.number, main_verb.person
    verb.term = term
    verb.tam = tam
    if verb.term == 'cAha':
            verb.person = 'm_h'
    verb.type = 'auxillary'
    log(f'{verb.term} processed as auxillary verb with index {verb.index} gen:{verb.gender} num:{verb.number} and tam:{verb.tam}')
#     print('create_auxiliary_verb : ',verb)
    return verb
def get_all_form(morph_forms):
#     print('Running get_all_form')
    """
    >>> get_first_form("^mAz/mA<cat:n><case:d><gen:f><num:p>/mAz<cat:n><case:d><gen:f><num:s>/mAz<cat:n><case:o><gen:f><num:s>$")
    'mA<cat:n><case:d><gen:f><num:p>/mAz<cat:n><case:d><gen:f><num:s>/mAz<cat:n><case:o><gen:f><num:s>'
    """
    morph=morph_forms.split("$")[1]
#     print('get_all_form : ',morph)
    return morph

def get_first_form(morph_forms):
#     print('Running get_first_form')
    """
    >>> get_first_form("^mAz/mA<cat:n><case:d><gen:f><num:p>/mAz<cat:n><case:d><gen:f><num:s>/mAz<cat:n><case:o><gen:f><num:s>$")
    'mA<cat:n><case:d><gen:f><num:p>'
    """
    morph=morph_forms.split("/")[1]
    # print(morph_forms.split("$")[1],'get_first_form')
#     print('get_first_form : ',morph)
    return morph

def get_root_for_kim(relation, anim, gnp):
#     print('Running get_root_for_kim')
    # kOna is root for - kisakA, kisakI, kisake, kinakA, kinake, kinakI, kOna, kisa, kisane, kise, kisako,
    # kisase, kisake, kisameM, kisameM_se, isapara, kina, inhoMne, kinheM, kinako, kinase, kinpara, kinake, kinameM, kinameM_se, kisI, kisa

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
    elif relation =='k1' or relation =='k2':
        return 'kyA'
    else:
        return 'kim'

def get_default_GNP():
#     print('Running get_default_GNP')
    gender,number,person,case = 'm','s','a','o'
    
#     print('get_default_GNP : ',gender, number, person, case)
    return gender, number, person, case

def get_gnpcase_from_concept(concept): #computes GNP values from noun or
#     print('Running get_gnpcase_from_concept')

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
#     print('get_gnpcase_from_concept : ',gender, number, person, case)
    return gender, number, person, case

def get_TAM(term, tam):
#     print('Running get_TAM')
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
#     print('get_TAM : ',tam)
    return tam

def get_main_verb(term):
#     print('Running get_main_verb')
    ''' return main verb from a term'''

    pass

def getDataByIndex(value, searchList: list, index=0):
#     print('Running getDataByIndex')
    '''search and return data by index in an array of tuples.
        Index should be first element of tuples.
        Return False when index not found.'''
    try:
        res = False
        for dataele in searchList:
            # print(dataele[(index)])
            # dataele=list(dataele)
            # if (dataele[(index)]) == value and dataele[7]=='vn':
            #     dataele[3]='d'
            #     res = tuple(dataele)
            if (dataele[(index)]) == value:
                # res = tuple(dataele)
                res = dataele
        return res
    except IndexError:
        log(f'Index out of range while searching index:{value} in {searchList}', 'WARNING')
        return False
    # try:
    #     results = []
    #     for value in value_list:
    #         res = False
    #         for dataele in searchList:
    #             if dataele[index] == value:
    #                 res = dataele
    #                 break  # Assuming each value matches at most one data element
    #         if res:
    #             results.append(res)
    #     if not results:
    #         return False
    #     return results
    # except IndexError:
    #     log(f'Index out of range while searching index:{value_list} in {searchList}', 'WARNING')
    #     return False
#     print('getDataByIndex : ',res)
    

def getComplexPredicateGNP(term):
#     print('Running getComplexPredicateGNP')
    CP_term = clean(term.split('+')[0])
    gender = 'm'
    number = 's'
    person = 'a'

    tags = find_tags_from_dix(CP_term)  # getting tags from morph analyzer to assign gender and number for agreement
    if '*' not in tags['form']:
        gender = tags['gen']
        number = tags['num']
#     print('getComplexPredicateGNP : ',gender, number, person)
    return gender, number, person

def getGNP_using_k2(k2exists, searchList):
#     print('Running getGNP_using_k2')
    casedata = getDataByIndex(k2exists, searchList)
    if (casedata == False):
        log('Something went wrong. Cannot determine GNP for verb.', 'ERROR')
        sys.exit()
    verb_gender, verb_number, verb_person = casedata[4], casedata[5], casedata[6]
#     print('getGNP_using_k2 : ',verb_gender, verb_number, verb_person[0])
    return verb_gender, verb_number, verb_person[0]
        
def getGNP_using_k1(k1exists, searchList):
#     print('Running getGNP_using_k1')
    # for k1 in k1exists:
    casedata = getDataByIndex(k1exists, searchList)
    if (casedata == False):
        log('Something went wrong. Cannot determine GNP for verb k1 is missing.', 'ERROR')
        sys.exit()
    verb_gender, verb_number, verb_person = casedata[4], casedata[5], casedata[6]
#     print('getGNP_using_k1 : ',verb_gender, verb_number, verb_person[0])
    return verb_gender, verb_number, verb_person

def getVerbGNP_new(concept_term, full_tam, is_cp, seman_data, depend_data, sentence_type, processed_nouns, processed_pronouns,process_nominal_form):
#     print('Running getVerbGNP_new')
    '''
    '''
    #for imperative sentences
    if sentence_type in ('Imperative','imperative') or 'o' in full_tam:
        verb_gender = 'm'
        verb_number = 's'
        verb_person = 'm'
#         print('getVerbGNP_new : ',verb_gender, verb_number, verb_person)
        return verb_gender, verb_number, verb_person

    #for non-imperative sentences
    # For non-imperative sentences
    k1exists = False
    k2exists = False
    k1_case = ''
    k2_case = ''
    verb_gender, verb_number, verb_person, case = get_default_GNP()
    searchList = processed_nouns + processed_pronouns + process_nominal_form
    print('searchlist',searchList)

    for cases in depend_data:
        if cases == '':
            continue
        k1exists = (depend_data.index(cases) + 1) if 'k1' == cases[-2:] else k1exists
        k2exists = (depend_data.index(cases) + 1) if 'k2' == cases[-2:] else k2exists
    # if k1exists:
    #     for k1 in k1exists:
    #         casedata = getDataByIndex(k1[0], searchList)
    #         if not casedata:
    #             log('Something went wrong. Cannot determine case for k1.', 'ERROR')
    #         else:
    #             k1_case = casedata[3]
    #             # Assuming you need to handle multiple cases, modify as necessary

    # if k2exists:
    #     for k2 in k2exists:
    #         casedata = getDataByIndex(k2[0], searchList)
    #         if not casedata:
    #             log('Something went wrong. Cannot determine case for k2.', 'ERROR')
    #         else:
    #             k2_case = casedata[3]
                # Assuming you need to handle multiple cases, modify as necessary

        # k1exists = (match.group(1)) if 'k1' == cases[-2:] else k1exists
        # k2exists = (match.group(1)) if 'k2' == cases[-2:] else k2exists


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
            verb_gender, verb_number, verb_person = getGNP_using_k1(k1exists, searchList)
        elif k1exists and k1_case == 'o' and k2exists and k2_case == 'o':
            verb_gender, verb_number, verb_person = getComplexPredicateGNP(cp_term)
#         print('getVerbGNP_new : ',verb_gender, verb_number, verb_person[0])
        return verb_gender, verb_number, verb_person[0]

    if 'yA' in full_tam:
        if k1exists and k1_case == 'd':
            verb_gender, verb_number, verb_person = getGNP_using_k1(k1exists, searchList)
        elif k1exists and k1_case == 'o' and k2exists and k2_case == 'd':
            verb_gender, verb_number, verb_person = getGNP_using_k2(k2exists, searchList)
#         print('getVerbGNP_new : ',verb_gender, verb_number, verb_person[0])
        return verb_gender, verb_number, verb_person[0]

    if full_tam in constant.nA_list:
#         print('getVerbGNP_new : ',verb_gender, verb_number, verb_person[0])
        return verb_gender, verb_number, verb_person[0]

    #tam - gA
    else:
        verb_gender, verb_number, verb_person = getGNP_using_k1(k1exists, searchList)
#         print('getVerbGNP_new : ',verb_gender, verb_number, verb_person[0])
        return verb_gender, verb_number, verb_person[0]

def is_tam_ya(verbs_data):
#     print('Running is_tam_ya')

    ya_tam = '-yA_'
    if len(verbs_data) > 0 and verbs_data != ()     :
        term = verbs_data[1]
        if ya_tam in term:
            return True
    # print('is_tam_ya')
    return False

def is_kim(term):
#     print('is_kim')
    if term == 'kim':
        return True

    return False

def is_complex_predicate(concept):
#     print('is_complex_predicate')
    return "+" in concept

def is_CP(term):
#     print('Running is_CP')
    """
    >>> is_CP('varRA+ho_1-gA_1')
    True
    >>> is_CP("kara_1-wA_hE_1")
    False
    """
    if "+" in term:
#         print('is_CP     : True')
        return True
    else:
#         print('is_CP     : False')
        return False

def is_update_index_NC(i, processed_words):
#     print('Running is_update_index_NC')
    for data in processed_words:
        temp = tuple(data)
        if len(temp) > 7 and float(i) == temp[0] and temp[7] == 'NC':
            return True

    return False

def is_nonfinite_verb(concept):
#     print('Running is_nonfinite_verb')
    return concept.type == 'nonfinite'

def has_tam_ya():
    '''Check if USR has verb with TAM "yA".
        It sets the global variable HAS_TAM to true
    '''
#     print('Running has_tam_ya')
    global HAS_TAM
    if HAS_TAM == True:
        return True
    else:
        return False

def has_GNP(gnp_info):
#     print('Running has_GNP')
    if len(gnp_info) and ('sg', 'pl') in gnp_info:
        return True
    return False

def has_ques_mark(POST_PROCESS_OUTPUT,sentence_type):
#     print('Running has_ques_mark')
    # interrogative_lst = ["yn_interrogative", "yn_interrogative_negative", "pass-yn_interrogative", "interrogative",
    #                      "Interrogative", "pass-interrogative"]

    if sentence_type[1:] in ("yn_interrogative", "yn_interrogative_negative", "pass-yn_interrogative", "interrogative",
                        "Interrogative", "pass-interrogative"):
        return 'kyA ' + POST_PROCESS_OUTPUT + ' ?'
    elif sentence_type[1:] in ('pass_affirmative','affirmative', 'Affirmative', 'negative', 'Negative', 'imperative', 'Imperative',"fragment","term","title","heading"):
        return POST_PROCESS_OUTPUT + ' |'

def identify_case(verb, dependency_data, processed_nouns, processed_pronouns):
#     print('Running identify_case')
    return getVerbGNP_new(verb.term, verb.tam, dependency_data, processed_nouns, processed_pronouns)

def identify_main_verb(concept_term):
#     print('Running identify_main_verb',concept_term)
    """
    >>> identify_main_verb("kara_1-wA_hE_1")
    'kara'
    >>> identify_main_verb("varRA+ho_1-gA_1")
    'ho'
    """
    if ("+" in concept_term):
        concept_term = concept_term.split("+")[1]
    # print(clean(concept_term.split("-")[0]))
    con=clean(concept_term.split("-")[0])
#     print('identify_main_verb : ',con)
    return con

def identify_default_tam_for_main_verb(concept_term):
#     print('Running identify_default_tam_for_main_verb')
    """
    >>> identify_default_tam_for_main_verb("kara_1-wA_hE_1")
    'wA'
    >>> identify_default_tam_for_main_verb("kara_1-0_rahA_hE_1")
    '0'
    """
    # print(concept_term.split("-")[1].split("_")[0],'identify_default_tam_for_main_verb')
    # print(concept_term.split("-")[1])
    # con=concept_term.split("-")[1].split("_")[0]
    if '-' in concept_term:
        con=concept_term.split("-")[1]
        if '_' in con:
            con=con.split("_")[0]
            return con
        else:
            return con
    else:
        return concept_term
#     print('identify_default_tam_for_main_verb : ',con)
    return con

def identify_complete_tam_for_verb(concept_term):
#     print('Running identify_complete_tam_for_verb')
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
#     print('identify_complete_tam_for_verb : ',tam_v)
    return tam_v

def identify_auxillary_verb_terms(term):
#     print('Running identify_auxillary_verb_terms')
    """
    >>> identify_auxillary_verb_terms("kara_1-wA_hE_1")
    ['hE']
    >>> identify_auxillary_verb_terms("kara_1-0_rahA_hE_1")
    ['rahA', 'hE']
    """
    aux_verb_terms = term.split("-")[1].split("_")[1:]
    cleaned_terms = map(clean, aux_verb_terms)
    # print('identify_auxillary_verb_terms')
    # print(cleaned_terms)
    el=list(filter(lambda x: x != '', cleaned_terms))
#     print('identify_auxillary_verb_terms : ',el)
    return el            # Remove empty strings after cleaning

def identify_verb_type(verb_concept):
#     print('Running identify_verb_type')
    '''
    >>identify_verb_type([])
    '''
    #dep_rel = verb_concept[4].strip().split(':')[1] #if using with non-OO program
    dependency = verb_concept.dependency
    dep_rel = dependency.strip().split(':')[1]
    v_type = ''
    if dep_rel == 'main':
        v_type = "main"
    # elif dep_rel in ('rpk', 'rbk', 'rvks', 'rbks', 'rsk', 'rblpk','rblak','rblsk'):
    #     v_type = "nonfinite"
    elif dep_rel in ('rpk', 'rbk','rvks'):
        v_type = "nonfinite"
    # elif dep_rel in ('rblpk','rblak','rblsk'):
    #     v_type = "nominal_verb"
    else:
        v_type = "main"
#     print('identify_verb_type : ',v_type)
    return v_type

def findExactMatch(value: int, searchList: list, index=0):
#     print('Running findExactMatch')
    '''search and return data by index in an array of tuples.
        Index should be first element of tuples.

        Return False when index not found.'''

    try:
        for dataele in searchList:
            if value == dataele[index].strip().split(':')[1]:
                return (True, dataele)
    except IndexError:
        log(f'Index out of range while searching index:{value} in {searchList}', 'WARNING')
        return (False, None)
    return (False, None)

def findValue(value: int, searchList: list, index=0):
#     print('Running findValue')
    '''search and return data by index in an array of tuples.
        Index should be first element of tuples.

        Return False when index not found.'''

    try:
        for dataele in searchList:
            if value == dataele[index]:
                return (True, dataele)
    except IndexError:
        log(f'Index out of range while searching index:{value} in {searchList}', 'WARNING')
        return (False, None)
    return (False, None)

def find_tags_from_dix(word):
#     print('Running find_tags_from_dix')
    """
    >>> find_tags_from_dix("mAz")
    {'cat': 'n', 'case': 'd', 'gen': 'f', 'num': 'p', 'form': 'mA'}
    """
    dix_command = "echo {} | apertium-destxt | lt-proc -ac hi.morfLC.bin | apertium-retxt".format(word)
    morph_forms = os.popen(dix_command).read()
    p_m=parse_morph_tags(morph_forms)
#     print('find_tags_from_dix : ',p_m)
    return p_m

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

def find_exact_dep_info_exists(index, dep_rel, words_info):
#     print('Running find_exact_dep_info_exists')
    for word in words_info:
        dep = word[4]
        dep_head = word[4].strip().split(':')[0]
        dep_val = word[4].strip().split(':')[1]
        if dep_val == dep_rel and int(dep_head) == index:
            return True

    return False

def find_match_with_same_head(data_head, term, words_info, index):
#      print('Running find_match_with_same_head')
    #  k2exists, k2_index = find_match_with_same_head(data_head, 'k2', words_info, index=4)
     for dataele in words_info:
        dataele_index = dataele[0]
        dep_head = dataele[index].strip().split(':')[0]
        dep_value = dataele[index].strip().split(':')[1]
        if str(data_head) == dep_head and term == dep_value:
            return True, dataele_index
     return False, -1

def parse_morph_tags(morph_form):
#     print('Running parse_morph_tags')
    """
    >>> parse_morph_tags("mA<cat:n><case:d><gen:f><num:p>")
    {'cat': 'n', 'case': 'd', 'gen': 'f', 'num': 'p', 'form': 'mA'}
    """
    form = morph_form.split("<")[0]
    matches = re.findall("<(.*?):(.*?)>", morph_form)
    result = {match[0]: match[1] for match in matches}
    result["form"] = form
#     print('parse_morph_tags : ',result)
    return result

def parse_morph_tags_as_list(morph_form):
#     print('Running parse_morph_tags_as_list')
    """
    >>> parse_morph_tags("mA<cat:n><case:d><gen:f><num:p>")
    {'cat': 'n', 'case': 'd', 'gen': 'f', 'num': 'p', 'form': 'mA'}
    """
    form = morph_form.split("<")[0]
    matches = re.findall("<(.*?):(.*?)>", morph_form)
    result = [(match[0], match[1]) for match in matches]
    result.append(('form',form))
#     print('parse_morph_tags_as_list : ',result)
    return result

def generate_input_for_morph_generator(input_data):
#     print('Running generate_input_for_morph_generator')
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
        # elif data[2] == 'n' and data[7] == 'vn':
        #     morph_data = f'^{data[1]}<cat:{data[7]}><case:{data[3]}>$'
        elif data[2] == 'vn':
            morph_data = f'^{data[1]}<cat:{data[2]}><case:{data[3]}>$'
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
#     print('generate_input_for_morph_generator : ',morph_input_data)
    return morph_input_data

def write_data(writedata):
#     print('Running write_data')
    """Write the Morph Input Data into a file"""
    final_input = " ".join(writedata)
    with open("morph_input.txt", 'w', encoding="utf-8") as file:
        file.write(final_input + "\n")
    return "morph_input.txt"

def run_morph_generator(input_file):
#     print('Running run_morph_generator')
    """ Pass the morph generator through the input file"""
    fname = f'{input_file}-out.txt'
    f = open(fname, 'w')
    subprocess.run(f"sh ./run_morph-generator.sh {input_file}", stdout=f, shell=True)
    return "morph_input.txt-out.txt"

def generate_morph(processed_words):
#     print('Running generate_morph')
    """Run Morph generator"""
    morph_input = generate_input_for_morph_generator(processed_words)
    MORPH_INPUT_FILE = write_data(morph_input)
    OUTPUT_FILE = run_morph_generator(MORPH_INPUT_FILE)
    return OUTPUT_FILE

def read_output_data(output_file):
#     print('Running read_output_data')
    """Check the output file data for post processing"""

    with open(output_file, 'r') as file:
        data = file.read()
#     print('read_output_data : ',data)
    return data

def analyse_output_data(output_data, morph_input):
#     print('Running analyse_output_data')
    output_data = output_data.strip().split(" ")
    combine_data = []
    print('before combining : ',output_data, morph_input)
    for i in range(len(output_data)):
        morph_input_list = list(morph_input[i])
        morph_input_list[1] = output_data[i]
        combine_data.append(tuple(morph_input_list))
#     print('analyse_output_data : ',combine_data)
    return combine_data

def handle_compound_nouns(noun, processed_nouns, category, case, gender, number, person, postposition):
#     print('Running handle_compound_nouns')
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
#     print('handle_compound_nouns : ',processed_nouns)
    return processed_nouns

# def handle_unprocessed_all(outputData, processed_nouns):
#     print('Running handle_unprocessed_all')
#     """swapping gender info that does not exist in dictionary."""
#     output_data = outputData.strip().split(" ")
#     has_changes = False
#     reprocess_list = []
#     dataIndex = 0  # temporary [to know index value of generated word from sentence]
#     for data in output_data:
#         dataIndex = dataIndex + 1
#         if data[0] == '#':
#             for i in range(len(processed_nouns)):
#                 if round(processed_nouns[i][0]) == dataIndex:
#                         if processed_nouns[i][7] != 'proper':
#                             temp = list(processed_nouns[i])
#                             temp[4] = change_gender(processed_nouns[i][4])
#                             #temp[4] = 'f' if processed_nouns[i][4] == 'm' else 'm'
#                             reprocess_list.append(['n', i, processed_nouns[i][0],temp[4], temp[7]])
#                             processed_nouns[i] = tuple(temp)
#                             has_changes = True
#                             log(f'{temp[1]} reprocessed as noun with new gen:{temp[4]}.')
#     print('handle_unprocessed_all : ',has_changes, reprocess_list, processed_nouns)
#     return has_changes, reprocess_list, processed_nouns

def handle_unprocessed(outputData, processed_nouns):
#     print('Running handle_unprocessed')
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
                    #if not processed_nouns[i][7] == 'proper' and not processed_nouns[i][7] == 'NC' and not processed_nouns[i][7] == 'CP_noun':
                        has_changes = True
                        temp = list(processed_nouns[i])
                        temp[4] = 'f' if processed_nouns[i][4] == 'm' else 'm'
                        processed_nouns[i] = tuple(temp)
                        log(f'{temp[1]} reprocessed as noun with gen:{temp[4]}.')
                    else:
                        break
#     print('handle_unprocessed : ',has_changes, processed_nouns)
    return has_changes, processed_nouns

def nextNounData_fromFullData(fromIndex, PP_FullData):
#     print('Running nextNounData_fromFullData')
    index = fromIndex
    for data in PP_FullData:
        if data[0] > index:
            if data[2] == 'n':
                return data

    return ()
def is_next_word_noun(index,processed_nouns):
    # print("klm")
    for data in processed_nouns:
        if data[0]==index and data[2]=='n':
            # print(data[0],'data1')
            return data
            # return data
    else:
        return False

def nextNounData(fromIndex, word_info):
#     print('Running nextNounData')
    #for NC go till NC_head and return that tuple
    # index = fromIndex
    # for i in range(len(word_info)):
    #     for data in word_info:
    #         if index == data[0]:
    #             if data[3] != '' and index != fromIndex:
    #                 return data
    index = fromIndex
    for data in word_info:
        if index == data[0] and data[3] != '' and index != fromIndex:
            return data
                # if ':' in data[4]:
                #     index = int(data[4][0])
    return False

def fetchNextWord(index, words_info):
#     print('Running fetchNextWord')
    next_word = ''
    for data in words_info:
        if index == data[0]:
            next_word = clean(data[1])
#     print('fetchNextWord : ',next_word)
    return next_word

def change_gender(current_gender):
#     print('Running change_gender')
    """
    >>> change_gender('m')
    'f'
    >>> change_gender('f')
    'm'
    """
    return 'f' if current_gender == 'm' else 'm'

def set_gender_make_plural(processed_words, g, num):
#     print('Running set_gender_make_plural')
    process_data = []
    # for all k1s and main verb change gender to female and number to plural
    for i in range(len(processed_words)):
        word_list = list(processed_words[i])
        if word_list[2] == 'adj':
            # 4th index - gender, 5th index - number
            word_list[4] = g
            word_list[5] = num
        elif word_list[2] == 'v':
            # 3rd index - gender, 4th index - number
            word_list[3] = g
            word_list[4] = num
        process_data.append(tuple(word_list))
#     print('set_gender_make_plural : ',process_data)
    return process_data

def set_main_verb_tam_zero(verb: Verb):
#     print('Running set_main_verb_tam_zero')
    verb.tam = 0
#     print('set_main_verb_tam_zero :',verb)
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
        # 'rvks': 'adj_wA_huA',
        'rpk': 'kara',
        'rsk': 'adj_wA_huA',
        # 'rbks': 'adj_yA_huA',
        # 'rblpk': 'nA',
        # 'rbk': 'yA_gayA',
    }.get(dependency, '')
    return tam

def update_ppost_dict(data_index, param):
#     print('Running update_ppost_dict')
    # whether entry exists or not, param is updated in ppost_dict
    processed_postpositions_dict[data_index] = param

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

def extract_gnp_noun(noun_data):
#     print('Running extract_gnp_noun')
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

        #Setting gender
        seman_data = noun_data[2].strip()
        #seman_info_lst = seman_data.split()
        if len(seman_data) > 0:
            if 'male' in seman_data:
                gender = 'm'
            elif 'female' in seman_data:
                gender = 'f'
        else:
            tags = find_tags_from_dix(noun_term)
            if '*' not in tags['form']:
                gender = tags['gen']

        #Setting number
        if len(noun_data[3]):
            # print(noun_data[3],'noun data')
            number = noun_data[3].strip()[0]
            # number = noun_data[3].strip()[3]

        #Setting person
        if noun_term == 'speaker':
            person = 'u'
        elif noun_term == 'addressee':
            person = 'm'
        else:
            person = 'a'
#     print('extract_gnp_noun : ',gender, number, person)
    return gender, number, person

def extract_gnp(data):
#     print('Running extract_gnp')
    gender = 'm'
    number = 's'
    person = 'a'

    if len(data):
        term = clean(data[1])

        # Setting gender
        seman_data = data[2].strip()
        # seman_info_lst = seman_data.split()
        if len(seman_data) > 0:
            if 'male' in seman_data:
                gender = 'm'
            elif 'female' in seman_data:
                gender = 'f'

        # Setting number
        if len(data[3]):
            number = data[3].strip()[0]

        # Setting person
        if term == 'speaker':
            person = 'u'
        elif term == 'addressee':
            person = 'm'
        else:
            person = 'a'
#     print('extract_gnp : ',gender, number, person)
    return gender, number, person

def add_postposition(transformed_fulldata, processed_postpositions):
#     print('Running add_postposition')
    '''Adds postposition to words wherever applicable according to rules.'''
    PPFulldata = []

    for data in transformed_fulldata:
        index = data[0]
        if index in processed_postpositions:
            temp = list(data)
            ppost = processed_postpositions[index]
            if ppost != None and (temp[2] == 'n'or temp[2] == 'vn' or temp[2] == 'other'):
                temp[1] = temp[1] + ' ' + ppost
            data = tuple(temp)
        PPFulldata.append(data)
#     print('add_postposition : ',PPFulldata)
    return PPFulldata

def add_discourse_elements(discourse_data,spkview_data, POST_PROCESS_OUTPUT):
#     print('Running add_discourse_elements')
    if len(discourse_data) <= 0:
        return POST_PROCESS_OUTPUT
    # coref_list=[]
    # folder_path = sys.argv[1].split('/')[0]
    # file_name_line = None  
    # relation=['AvaSyakawApariNAma']  
    # print(discourse_data,'kl')
    # for i in range(len(discourse_data)):
    #     if '.' in discourse_data[i]:
    #         coref_list.append(i)
    #         file_name_line = discourse_data[i]
    #         file_name = file_name_line.split('.')[0]
    #         digit = file_name_line.split('.')[1].split(':')[0]
    #         discource_rel = file_name_line.split(':')[1]
    #         file_path = os.path.join(folder_path, f'{file_name}')
    #         print(file_path,'kl')
    #         # Add .txt to file name if file not found
    #         if not os.path.exists(file_path):
    #             file_path += '.txt'
    #         if not os.path.exists(file_path):
    #             raise FileNotFoundError(f"File '{file_path}' not found")
    #         with open(file_path, 'r', encoding='utf-8') as file:
    #             file_contents = file.readlines()

    #         if discource_rel in relation:
    #             print(file_contents[0],'file_contents',discource_rel)

    #         coref_word=file_contents[1].split(',')[int(digit)-1]
    #         coref_list.append(coref_word)
            # return coref_list
    if isinstance(discourse_data, list):
#         print("The variable 'numbers' is a list.")
        for data_values in discourse_data:
            if data_values!='' and 'coref' not in data_values:
                    
                data_values=data_values.split(':')[1]
                    # print(data_values,'kk')
                for element in constant.discourse_dict:
                    # print('ele1',element,discourse_data)
                    if element == data_values:
                        # print('ele2',element)
                        if isinstance(constant.discourse_dict[element], str):
                            POST_PROCESS_OUTPUT = constant.discourse_dict[element] + " " + POST_PROCESS_OUTPUT
                        # elif isinstance(constant.discourse_dict[element], list):
                        #     for i in range(len(constant.discourse_dict[element])):
                                
                        #         if data_values=='samuccaya':
                        #             if 'BI_1' in spkview_data :
                        #                 # print(output_list1[0],'outpput_list')
                        #                 POST_PROCESS_OUTPUT = 'balki '+ POST_PROCESS_OUTPUT
                        #                 # output_list1[-1]='ना केवल '+ output_list1[-1]
                        #                 # print(output_list1[1],'outpput_list')
                        #                 break
                        #             elif i!=0:
                        #                 POST_PROCESS_OUTPUT = constant.discourse_dict[element][i]+ '/'+ POST_PROCESS_OUTPUT
                        #             else:
                        #                 POST_PROCESS_OUTPUT = constant.discourse_dict[element][i] + " " + POST_PROCESS_OUTPUT
                                        
                        #         elif i!=0:
                        #             POST_PROCESS_OUTPUT = constant.discourse_dict[element][i]+ '/'+ POST_PROCESS_OUTPUT
                        #         else:
                        #             POST_PROCESS_OUTPUT = constant.discourse_dict[element][i] + " " + POST_PROCESS_OUTPUT
                        elif isinstance(constant.discourse_dict[element], list):
                            for i, value in enumerate(constant.discourse_dict[element]):
                                if data_values == 'samuccaya':
                                    if 'BI_1' in spkview_data:
                                        POST_PROCESS_OUTPUT = 'balki ' + POST_PROCESS_OUTPUT
                                        break
                                    else:
                                        separator = '/' if i != 0 else ' '
                                        POST_PROCESS_OUTPUT = value + separator + POST_PROCESS_OUTPUT
                                else:
                                    separator = '/' if i != 0 else ' '
                                    POST_PROCESS_OUTPUT = value + separator + POST_PROCESS_OUTPUT
                if 'nA kevala/' in POST_PROCESS_OUTPUT:
                    POST_PROCESS_OUTPUT = POST_PROCESS_OUTPUT.replace('nA kevala/', '')

    else:
#         print("The variable 'numbers' is not a list.")
        # for data_values in discourse_data:
        if discourse_data:
#                     print(discourse_data,'kk')
                    discourse_data=discourse_data.split(':')[1]
        for element in constant.discourse_dict:
            # print('ele1',element,discourse_data)
            if element == discourse_data:
                # print('ele2',element)
                if isinstance(constant.discourse_dict[element], str):
                    POST_PROCESS_OUTPUT = constant.discourse_dict[element] + " " + POST_PROCESS_OUTPUT
                elif isinstance(constant.discourse_dict[element], list):
                    for i in range(len(constant.discourse_dict[element])):
                        if i!=0:
                            POST_PROCESS_OUTPUT = constant.discourse_dict[element][i]+ '/'+ POST_PROCESS_OUTPUT
                        else:
                            POST_PROCESS_OUTPUT = constant.discourse_dict[element][i] + " " + POST_PROCESS_OUTPUT
#     print('add_discourse_elements : ', POST_PROCESS_OUTPUT)
    return POST_PROCESS_OUTPUT

# def nakeval_balki(output_list):
#     if 'BI_1' in spkview_dict


def add_adj_to_noun_attribute(key, value):
#     print('Running add_adj_to_noun_attribute')
    if key is not None:
        if key in constant.noun_attribute:
            constant.noun_attribute[key][0].append(value)
#             print('add_adj_to_noun_attribute : ',constant.noun_attribute[key][0])
        else:
            constant.noun_attribute[key] = [[],[]]
#             print('add_adj_to_noun_attribute : ',constant.noun_attribute[key])

def add_verb_to_noun_attribute(key, value):
#     print('Running add_verb_to_noun_attribute')
    if key is not None:
        if key in constant.noun_attribute:
            constant.noun_attribute[key][1].append(value)
        else:
            constant.noun_attribute[key] = [[], []]

def add_spkview(full_data, spkview_dict):
#     print('Running add_spkview')
    transformed_data = []
    for data in full_data:
        index = data[0]
        if index in spkview_dict:
            temp = list(data)
            spkview_info = spkview_dict[index]
            for info in spkview_info:
                tag = info[0]
                val = info[1]
                if tag == 'before':
                    temp[1] = val + ' ' + temp[1]
                elif tag == 'after':
                    temp[1] = temp[1] + ' ' + val
                data = tuple(temp)
        transformed_data.append(data)
#     print('add_spkview : ',transformed_data)
    return transformed_data

def add_MORPHO_SEMANTIC(full_data, MORPHO_SEMANTIC_DICT):
#     print('Running add_MORPHO_SEMANTIC')
    transformed_data = []
    for data in full_data:
        index = data[0]
        if index in MORPHO_SEMANTIC_DICT:
            temp = list(data)
            term = MORPHO_SEMANTIC_DICT[index]
            for t in term:
                tag = t[0]
                val = t[1]
                if tag == 'before':
                    temp[1] = val + ' ' + temp[1]
                else:
                    temp[1] = temp[1] + ' ' + val
            data = tuple(temp)
        transformed_data.append(data)
#     print('add_MORPHO_SEMANTIC : ',transformed_data)
    return transformed_data

def add_construction(transformed_data, construction_dict):
#     print('Running add_construction')
    Constructdata = []
    dependency_check=['k7p','k7t']
    add_words_list=['meM','ko','ke','kI','kA']
    depend_data1=''
    for data in transformed_data:
        index = data[0]
#         print(data)
        if len(data)==9:
            depend_data1=data[8]
        if index in construction_dict:
            temp = list(data)
            term = construction_dict[index]
            for t in term:
                tag = t[0]
                val = t[1]
                if tag == 'before':
                    temp[1] = val + ' ' + temp[1]
                else:
                    if val == ',':
                        temp[1] = temp[1] + val
                    else:
                        if depend_data1!='' and depend_data1 in add_words_list:
                            if depend_data1 in add_words_list and depend_data1 in temp[1]:
                                temp[1] = temp[1].split()[0] + ' ' +val
                        else:
                            temp[1] = temp[1] + ' ' +val
            data = tuple(temp)
        Constructdata.append(data)
#     print('add_construction : ',Constructdata)
    return Constructdata

def add_additional_words(additional_words_dict, processed_data):
    print('Running add_additional_words')
    additionalData = []
    print('additional_words_dict',additional_words_dict)
    for data in processed_data:
        index = data[0]
        if index in additional_words_dict:
            temp = list(data)
            print('temp:',temp)
            term = additional_words_dict[index]
            print('term:',term)
            for t in term:
                tag = t[0]
                val = t[1]
                print('val',val)
                if tag == 'before':
                    temp[1] = val + ' ' + temp[1]
                else:
                    temp1=temp[1].split()
                    if len(temp1)>=2 and temp1[1]=='ko':
                        temp1[1] = val
                        temp[1] = ' '.join(temp1)
                    else:
                        temp[1] = temp[1] + ' ' + val
            data = tuple(temp)
        additionalData.append(data)
    print('add_additional_words : ',additionalData)
    return additionalData

def fetch_NC_head(i, processed_words):
#     print('Running fetch_NC_head')
    for data in processed_words:
        temp = tuple(data)
        if int(temp[0]) == int(i) and temp[7] == 'NC_head':
            return temp[0]

def auxmap_hin(aux_verb):
#     print('Running auxmap_hin')
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
#     print('Running update_additional_words_dict')
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
#     print('Running to_tuple')
#     print('to_tuple : ',verb.index, verb.term, verb.category, verb.gender, verb.number, verb.person, verb.tam, verb.case, verb.type)
    return (verb.index, verb.term, verb.category, verb.gender, verb.number, verb.person, verb.tam, verb.case, verb.type)

def postposition_finalization(processed_nouns, processed_pronouns,processed_foreign_words,process_nominal_form, words_info):
#     print('Running postposition_finalization')
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

            for nominal_v in process_nominal_form:
                index = nominal_v[0]
                case = nominal_v[3]
                if head == str(index) and case == 'o':
                    update_ppost_dict(data_index, 'ke')
            # for f_word in processed_foreign_words:
            #     index = f_word[0]
            #     case = f_word[3]
            #     if head == str(index) and case == 'o':
            #         update_ppost_dict(data_index, 'ke')

def collect_processed_data(processed_foreign_words,processed_pronouns, processed_nouns,process_nominal_form, processed_adjectives, processed_verbs,
                           processed_auxverbs, processed_indeclinables, processed_others):
#     print('Running collect_processed_data')
    """collect sort and return processed data."""
    sorted_data=sorted(processed_foreign_words+processed_pronouns + processed_nouns + process_nominal_form + processed_adjectives + processed_verbs + processed_auxverbs + processed_indeclinables + processed_others)
#     print('collect_processed_data combining all processed list in sorted order',sorted_data)
    return sorted_data

def join_compounds(transformed_data, construction_data):
#     print('Running join_compounds')
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
#     print('join_compounds : ',resultant_data)
    return resultant_data

def populate_morpho_semantic_dict(gnp_info, PPfull_data,words_info):
#     print('Running populate_morpho_semantic_dict')
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
                        # Convert the specific element to a list
                        PPfull_data[i] = list(PPfull_data[i])
                        # Make the modification
                        PPfull_data[i][1] = PPfull_data[i][1].replace(dup_word, dup_word1)
                        # Convert back to a tuple
                        PPfull_data[i] = tuple(PPfull_data[i])

                        temp = (b, dup_word)

                else:
                    # fetch GNP of next noun
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
#     print('populate_morpho_semantic_dict : ',populate_morpho_semantic_dict)
    return populate_morpho_semantic_dict,PPfull_data

def join_indeclinables(transformed_data, processed_indeclinables, processed_others):

    """Joins Indeclinable data with transformed data and sort it by index number."""
    return sorted(transformed_data + processed_indeclinables + processed_others)

# def create_agreement_map(index_row, dependency_data):
#     print('Running create_agreement_map')
#     """
#     >>> create_agreement_map()

#     """

def rearrange_sentence(fulldata):
#     print('Running rearrange_sentence')
    '''Function comments'''
    finalData = sorted(fulldata)
    final_words = [x[1].strip() for x in finalData]
    r_s=" ".join(final_words)
#     print('rearrange_sentence : ',r_s)
    return r_s

def collect_hindi_output(source_text):
#     print('Running collect_hindi_output')
    """Take the output text and find the hindi text from it."""
#     print(source_text)
    hindi_format = WXC(order="wx2utf", lang="hin")
    generate_hindi_text = hindi_format.convert(source_text)
#     print('collect_hindi_output : ',generate_hindi_text)
    return generate_hindi_text
#         previndex = data[0]
#         prevword = data[1]
#
#     return resultant_data

# def verb_agreement_with_CP(verb, CP):
#     print('Running verb_agreement_with_CP')
#     """
#     >>> verb_agreement_with_CP(Verb(index=2, gender='m', number='s', person='a'), [1.9, 'varRA', 'n', 'd', 'f', 's', 'a', 'CP_noun', ''])
#     ('f', 's', 'a')
#     >>> verb_agreement_with_CP(Verb(index=2, gender='m', number='s', person='a'), [1.9, 'pAnI', 'n', 'd', 'm', 's', 'a', 'CP_noun', ''])
#     ('m', 's', 'a')
#     """

#     if CP != [] and (verb.index - 0.1 == CP[0]) and CP[7] == "CP_noun":  # setting correspondence between CP noun and verb
#         print('verb_agreement_with_CP : ',CP[4], CP[5], CP[6])
#         return CP[4], CP[5], CP[6]
#     else:
#         print('verb_agreement_with_CP : ',verb.gender, verb.number, verb.person)
#         return verb.gender, verb.number, verb.person

# def update_case_and_ppost(data, case, ppost):
#     print('Running update_case_and_ppost')
#     temp = list(data)
#     index = temp[0]

#     pass

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
            # Add .txt to file name if file not found
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