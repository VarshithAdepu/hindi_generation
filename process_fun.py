from bulk_common_v3 import*
import constant
from utils import*

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
    '''Calculates postposition to words wherever applicable according to rules.'''
    cp_verb_list = ['prayApreprsa+kara','sahAyawA+kara']
    if len(verb_data) > 0:
        verb_term = verb_data[1]
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
                if relation in ('k2', 'rt', 'rh'):
                    term = term + 'nA'
                log_msg = f'{term} processed as nominal verb with index {index} gen:{gender} num:{number} person:{person} noun_type:{noun_type} case:{case} and postposition:{postposition}'
                break

        noun = (index, term, category, case, gender, number, person, noun_type, postposition)
        processed_noun.append(noun)
        log(log_msg)

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
        if len(verb[4]) > 0 and verb[4].strip().split(':')[1] == 'main':
            main_verb = verb
            break
    if not len(main_verb):
        log('USR error. Main verb not identified. Check the USR.')
        sys.exit()
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
                if spkview_data == "distal" and relation=='dem':
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

def process_verbs(verbs_data, seman_data, depend_data, sentence_type, spkview_data, processed_nouns, processed_pronouns, words_info, reprocess=False):
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
            verb = process_nonfinite_verb(concept, seman_data, depend_data, sentence_type, processed_nouns, processed_pronouns, words_info)
            processed_verbs.append(to_tuple(verb))
        else:
            if process_verb(concept, seman_data, depend_data, sentence_type, spkview_data, processed_nouns, processed_pronouns, reprocess):
                verb, aux_verbs = process_verb(concept, seman_data, depend_data, sentence_type, spkview_data, processed_nouns, processed_pronouns, reprocess)
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
                    print(dep_gender_dict[i],'llll')
                    relation = dep_gender_dict[i]
                    print(dep_gender_dict[i],'llll')
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

def process_verb(concept: Concept, seman_data, dependency_data, sentence_type, spkview_data, processed_nouns, processed_pronouns, reprocessing):
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
    verb = process_main_verb(concept, seman_data, dependency_data, sentence_type, processed_nouns, processed_pronouns, reprocessing)
    auxiliary_verbs = process_auxiliary_verbs(verb, concept, spkview_data)
    return verb, auxiliary_verbs
    # else:
    #     return None

def process_nonfinite_verb(concept, seman_data, depend_data, sentence_type, processed_nouns, processed_pronouns, words_info):
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
    if getVerbGNP_new(verb.term, full_tam, is_cp, seman_data, depend_data, sentence_type, processed_nouns, processed_pronouns):
        gender, number, person = getVerbGNP_new(verb.term, full_tam, is_cp, seman_data, depend_data, sentence_type, processed_nouns, processed_pronouns)
        verb.gender = gender
        verb.number = number
        verb.person = person
        verb.case = 'o' # to be updated - agreement with following noun
        log(f'{verb.term} processed as nonfinite verb with index {verb.index} gen:{verb.gender} num:{verb.number} case:{verb.case}, and tam:{verb.tam}')
        return verb
    else:
        return None

def process_dep_k2g(data_case, main_verb):
    verb = identify_main_verb(main_verb[1])
    if verb in constant.kisase_k2g_verbs:
        ppost = 'se'
    else:
        ppost = 'ko'
    return ppost

def process_main_verb(concept: Concept, seman_data, dependency_data, sentence_type, processed_nouns, processed_pronouns, reprocessing):
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
    verb.gender, verb.number, verb.person = getVerbGNP_new(concept.term, full_tam, is_cp, seman_data, dependency_data, sentence_type, processed_nouns, processed_pronouns)
    return verb
    # else:
    #     return None
