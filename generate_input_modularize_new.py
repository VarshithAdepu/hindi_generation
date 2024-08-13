from common_v3 import *
#from common_v2 import *
from Json_format import Json_format
from extract_json_data import extract_discourse_values

HAS_CONSTRUCTION_DATA = False
HAS_SPKVIEW_DATA = False
ADD_MORPHO_SEMANTIC_DATA = False
HAS_DISCOURSE_DATA = False
HAS_ADDITIONAL_WORDS = False
HAS_COREF = False
flag_conj=False
flag_span=False

if __name__ == "__main__":
    log("Program Started", "START")

    # Reading filename as command-line argument
    try:
        path = sys.argv[1]
    except IndexError:
        log("No argument given. Please provide path for input file as an argument.", "ERROR")
        sys.exit()
    print(path,'llll')
    # List all files in the directory
    # file_names = os.listdir(path)
    # file_names.sort()
    output_data_list = []
    # for file_name in file_names:
    #     # Construct the full path to each file
    #     file_path = os.path.join(path, file_name)
    #     print("fn: ",file_name)
    
    # Call Json_format function to process the directory
    Json_format(path)
        # Process each file as needed
    file_data = read_file(path)
# file_data = read_file(path) #Reading USR

    rules_info = generate_rulesinfo(file_data) #Extracting Rules from each row of USR

    # Extracting Information
    src_sentence = rules_info[0]
    root_words = rules_info[1]
    index_data = [int(x) for x in rules_info[2]]
    seman_data = rules_info[3]
    gnp_data = rules_info[4]
    depend_data = rules_info[5]
    discourse_data = rules_info[6]
    spkview_data = rules_info[7]
    scope_data = rules_info[8]
    construction_data = rules_info[9]
    # print(construction_data,'cd')
    sentence_type = rules_info[10]
    
    print(depend_data,'dp')
    # print(depend_data,'dp')
    construction=['conj','span']
    conj_concept=[]
    span_concept=[]
    conj_concept=root_words
    span_concept=root_words

    print(span_concept,'cc')

    for i, concept in enumerate(root_words):
        if 'conj' in concept :
            flag_conj=True
            depend_data=construction_row(i,construction_data,depend_data)
            # del(gnp_data[i])
            print(depend_data,'pend')
            print(root_words,'rttt')
        elif 'disjunct' in concept :
            flag_conj=True
            depend_data=construction_row(i,construction_data,depend_data)
            del(gnp_data[i])
        elif 'span' in concept :
            flag_span=True
            depend_data=construction_row(i,construction_data,depend_data)
            del(gnp_data[i])
            print(root_words,'rttt')
        elif 'cp' in concept:
            flag_cp=True
            depend_data=construction_row_cp(i,construction_data,depend_data)
            # del(gnp_data[i])


    print(construction_data,'dp')
    check_main_verb(depend_data)
    # if len(rules_info) > 10 and rules_info[10] != '':
    #     if 'speaker not found in dictionary' in rules_info[10]:
    #         construction_data = ''
    #     else:
    #         HAS_CONSTRUCTION_DATA = True
    #only when construction data is not nil
    if flag_conj or flag_span:
        # construction_data = rules_info[10]
        HAS_CONSTRUCTION_DATA = True

    # if len(rules_info) > 10 and rules_info[10]!='*nil':
    #     construction_data = rules_info[10]
    #     HAS_CONSTRUCTION_DATA = True

    if spkview_data != [] or len(spkview_data) > 0:
        HAS_SPKVIEW_DATA = populate_spkview_dict(spkview_data)
        #returns true or false
    if discourse_data != [] or len(discourse_data) > 0:
        HAS_DISCOURSE_DATA = True

    if 'coref' in discourse_data:
        HAS_COREF = True

    
    # Making a collection of words and its rules as a list of tuples.
    words_info = generate_wordinfo(root_words, index_data, seman_data,
                                gnp_data, depend_data, discourse_data, spkview_data,scope_data,construction_data)
    print(words_info,'wordinfo')
    # Categorising words as Nouns/Pronouns/Adjectives/..etc.
    foreign_words_data,indeclinables_data, pronouns_data, nouns_data,verbal_adjectives, adjectives_data, verbs_data, adverbs_data, others_data, nominal_forms_data = identify_cat(
        words_info)
    print(words_info,'wordinfo')
    
    # print(verbs_data,'vd')

    #  Processing Stage
    processed_foreign_words = process_foreign_word(foreign_words_data,words_info,verbs_data)
    processed_indeclinables = process_indeclinables(indeclinables_data)
    processed_nouns = process_nouns(nouns_data, words_info, verbs_data)
    # print(processed_nouns)
    processed_pronouns = process_pronouns(pronouns_data, processed_nouns, processed_indeclinables, words_info, verbs_data)
    processed_others = process_others(others_data)
    process_nominal_form = process_nominal_verb(nominal_forms_data, processed_nouns, words_info, verbs_data)
    processed_verbs, processed_auxverbs = process_verbs(verbs_data, seman_data, depend_data, sentence_type, spkview_data,processed_nouns, processed_pronouns,index_data, words_info, False)
    # processed_adjectives = process_verbal_adjective(verbal_adjectives,processed_nouns, words_info, verbs_data)
    processed_adjectives = process_adjectives(adjectives_data, processed_nouns, processed_verbs)
    process_adverbs(adverbs_data, processed_nouns, processed_verbs, processed_others, reprocessing=False)
    postposition_finalization(processed_nouns, processed_pronouns,processed_foreign_words, words_info)
    if len(additional_words_dict) > 0:
        # print(additional_words_dict,'jjjjjjjjjjj')
        HAS_ADDITIONAL_WORDS = True
    print(processed_foreign_words,processed_pronouns,processed_nouns,processed_adjectives,
                                            processed_verbs, processed_auxverbs,processed_indeclinables, processed_others)

    # Every word is collected into one and sorted by index number.
    processed_words = collect_processed_data(index_data,processed_foreign_words,processed_pronouns,processed_nouns,processed_adjectives,
                                            processed_verbs, processed_auxverbs,processed_indeclinables, processed_others)


    # calculating postpositions for words if applicable.
    # processed_words, processed_postpositions = preprocess_postposition_new(processed_words, words_info,processed_verbs)
    if HAS_CONSTRUCTION_DATA:
        if flag_conj:
            processed_words = process_construction(processed_words, construction_data, depend_data, gnp_data, index_data,conj_concept)
        elif flag_span:
            processed_words = process_construction_span(processed_words, construction_data, depend_data, gnp_data, index_data,span_concept)

    # Input for morph generator is generated and fed into it.
    # Generator outputs the result in a file named morph_input.txt-out.txt
    OUTPUT_FILE = generate_morph(processed_words)
    # Create a new list to store the data from the output file
    

    # # Append the data from the output file to the new list
    # with open(OUTPUT_FILE, "r") as file:
    #     for line in file:
    #         output_data_list.append(line.strip())

    # # Print the new list
    # print(output_data_list,"o/p")

    # Re-processing Stage
    # Output from morph generator is read.
    outputData = read_output_data(OUTPUT_FILE)
    # Check for any non-generated words (mainly noun) & change the gender for non-generated words
    #has_changes, reprocess_list, processed_nouns = handle_unprocessed_all(outputData, processed_nouns)
    #print(reprocess_list)
    has_changes, processed_nouns = handle_unprocessed(outputData, processed_nouns)

    # handle unprocessed_verbs also with verb agreement
    # If any changes is done in gender for any word.
    # Adjectives and verbs are re-processed as they might be dependent on it.
    if has_changes:
        # Reprocessing adjectives and verbs based on new noun info
        processed_verbs, processed_auxverbs = process_verbs(verbs_data, seman_data, depend_data, sentence_type, spkview_data, processed_nouns, processed_pronouns,index_data, words_info, True)
        processed_adjectives = process_adjectives(adjectives_data, processed_nouns, processed_verbs)
        process_adverbs(adverbs_data, processed_nouns, processed_verbs, processed_others, reprocessing=True)

        # Sentence is generated again
        processed_words = collect_processed_data(index_data,processed_foreign_words,processed_pronouns, processed_nouns,  processed_adjectives, processed_verbs,processed_auxverbs,processed_indeclinables,processed_others)
        if HAS_CONSTRUCTION_DATA:
            if flag_conj:
                processed_words = process_construction(processed_words, construction_data, depend_data, gnp_data,index_data,conj_concept)
            elif flag_span:
                processed_words = process_construction_span(processed_words, construction_data, depend_data, gnp_data, index_data,span_concept)

        OUTPUT_FILE = generate_morph(processed_words)

    # Post-Processing Stage
    outputData = read_output_data(OUTPUT_FILE)
    # generated words and word-info data is combined #pp data not yet added
    transformed_data = analyse_output_data(outputData, processed_words)

    # compound words and post-positions are joined.
    transformed_data = join_compounds(transformed_data, construction_data)

    #post-positions are joined.
    PP_fulldata = add_postposition(transformed_data, processed_postpositions_dict)
    #construction data is joined
    if HAS_CONSTRUCTION_DATA:
        PP_fulldata = add_construction(PP_fulldata, construction_dict)

    if HAS_SPKVIEW_DATA:
        PP_fulldata = add_spkview(PP_fulldata, spkview_dict)

    ADD_MORPHO_SEMANTIC_DATA,PP_fulldata = populate_morpho_semantic_dict(gnp_data, PP_fulldata,words_info)
    if ADD_MORPHO_SEMANTIC_DATA:
        PP_fulldata = add_MORPHO_SEMANTIC(PP_fulldata, MORPHO_SEMANTIC_DICT)

    if HAS_ADDITIONAL_WORDS:
        PP_fulldata = add_additional_words(additional_words_dict, PP_fulldata)

    coref_list=process_coref(index_data,PP_fulldata,discourse_data)
    print(coref_list,'lstt')
    POST_PROCESS_OUTPUT = rearrange_sentence(PP_fulldata,coref_list)  # reaarange by index number
    
    # if HAS_COREF:
    #     POST_PROCESS_OUTPUT = rearrange_sentence(PP_fulldata)  # reaarange by index number
    
    POST_PROCESS_OUTPUT=POST_PROCESS_OUTPUT.split()

    for i in range(len(processed_foreign_words)):
        n=processed_foreign_words[i][0]
        POST_PROCESS_OUTPUT[n-1] = processed_foreign_words[i][1].replace('+',' ')

    POST_PROCESS_OUTPUT=' '.join(POST_PROCESS_OUTPUT)
    
    # coref_list=process_coref(processed_words,discourse_data)
    # print(coref_list,'lstt')
    # for list in coref_list:
    #     if list and len(list)==2:
    #         adding_coref = POST_PROCESS_OUTPUT.split()
    #         coref_word = '(' + clean(list[1]) + ')'
    #         adding_coref.insert(int(list[0])+1, coref_word)
    #         POST_PROCESS_OUTPUT = ' '.join(adding_coref)

    # hindi_output = collect_hindi_output(POST_PROCESS_OUTPUT)


    # if has_ques_mark(POST_PROCESS_OUTPUT,sentence_type):
    #     POST_PROCESS_OUTPUT = POST_PROCESS_OUTPUT + ' ?'

    if HAS_DISCOURSE_DATA:
        
        # POST_PROCESS_OUTPUT = add_discourse_elements(discourse_data,spkview_data, POST_PROCESS_OUTPUT)
        fp = 'output.json'
        path=path.split('/')[1]
        discourse = extract_discourse_values(fp, path)
        relation = 'AvaSyakawApariNAma'
        if discourse and relation in discourse:
            POST_PROCESS_OUTPUT = add_discourse_elements(discourse,spkview_data, POST_PROCESS_OUTPUT)
        
        elif not any(relation in item for item in discourse_data):
            POST_PROCESS_OUTPUT = add_discourse_elements(discourse_data,spkview_data, POST_PROCESS_OUTPUT)
    
    POST_PROCESS_OUTPUT = has_ques_mark(POST_PROCESS_OUTPUT,sentence_type)
    # if has_ques_mark(POST_PROCESS_OUTPUT,sentence_type):
    #     POST_PROCESS_OUTPUT = POST_PROCESS_OUTPUT + ' ?'

    # # for yn_interrogative add kya in the beginning
    # if sentence_type in ("yn_interrogative","yn_interrogative_negative", "pass-yn_interrogative"):
    #     POST_PROCESS_OUTPUT = 'kyA ' + POST_PROCESS_OUTPUT

    # if sentence_type in ('affirmative', 'Affirmative', 'negative', 'Negative', 'imperative', 'Imperative'):
    #     POST_PROCESS_OUTPUT = POST_PROCESS_OUTPUT + ' |'
    
    print(POST_PROCESS_OUTPUT,'ppo')
    hindi_output = collect_hindi_output(POST_PROCESS_OUTPUT)
    # output_data_list.append(hindi_output)
    write_hindi_text(hindi_output, POST_PROCESS_OUTPUT, OUTPUT_FILE)
    print(hindi_output)
    # print("h/p: ",output_data_list)
    # print(file_name,'fn/')
    # #next line for single line input
    
# with open('output_file_lion.txt', 'w') as file:
#     for item in output_data_list:
#         file.write(str(item) + '\n')  # Write each item to a new line
#     print('written successfully')
    

# next line code for bulk generation of results. All results are collated in test.csv. Run sh test.sh
# write_hindi_test(hindi_output, POST_PROCESS_OUTPUT, src_sentence, OUTPUT_FILE, path)

# # #for masked input -uncomment the following:
# masked_pup_list = masked_postposition(processed_words, words_info, processed_verbs)
# masked_pp_fulldata = add_postposition(transformed_data, masked_pup_list)
# arranged_masked_output = rearrange_sentence(masked_pp_fulldata)
# masked_hindi_data = collect_hindi_output(arranged_masked_output)
# write_masked_hindi_test(hindi_output, POST_PROCESS_OUTPUT, src_sentence, masked_hindi_data, OUTPUT_FILE, path)



# from common_v3 import *
# #from common_v2 import *
# from Json_format import Json_format
# from extract import extract_discourse_values

# HAS_CONSTRUCTION_DATA = False
# HAS_SPKVIEW_DATA = False
# ADD_MORPHO_SEMANTIC_DATA = False
# HAS_DISCOURSE_DATA = False
# HAS_ADDITIONAL_WORDS = False
# flag_conj=False
# flag_span=False

# if __name__ == "__main__":
#     log("Program Started", "START")

#     # Reading filename as command-line argument
#     try:
#         path = sys.argv[1]
#     except IndexError:
#         log("No argument given. Please provide path for input file as an argument.", "ERROR")
#         sys.exit()
#     print(path,'llll')
#     # List all files in the directory
#     # file_names = os.listdir(path)
#     # file_names.sort()
#     output_data_list = []
#     # for file_name in file_names:
#     #     # Construct the full path to each file
#     #     file_path = os.path.join(path, file_name)
#     #     print("fn: ",file_name)
    
#     # Call Json_format function to process the directory
#     Json_format(path.split('/')[0])
#         # Process each file as needed
#     file_data = read_file(path)
# # file_data = read_file(path) #Reading USR

#     rules_info = generate_rulesinfo(file_data) #Extracting Rules from each row of USR
#     print(rules_info,'rules info')
#     # Extracting Information
#     src_sentence = rules_info[0]
#     root_words = rules_info[1]
#     index_data = [int(x) for x in rules_info[2]]
#     seman_data = rules_info[3]
#     gnp_data = rules_info[4]
#     depend_data = rules_info[5]
#     discourse_data = rules_info[6]
#     spkview_data = rules_info[7]
#     scope_data = rules_info[8]
#     sentence_type = rules_info[9]
#     construction_data = ''
#     # print(depend_data,'dp')

#     check_main_verb(depend_data)
#     # if len(rules_info) > 10 and rules_info[10] != '':
#     #     if 'speaker not found in dictionary' in rules_info[10]:
#     #         construction_data = ''
#     #     else:
#     #         HAS_CONSTRUCTION_DATA = True
#     #only when construction data is not nil
#     if len(rules_info) > 10 and rules_info[10]!='*nil':
#         construction_data = rules_info[10]
#         if 'conj' in construction_data:
#             flag_conj=True
#         elif 'span' in construction_data:
#             flag_span=True
#         HAS_CONSTRUCTION_DATA = True

#     if spkview_data != [] or len(spkview_data) > 0:
#         HAS_SPKVIEW_DATA = populate_spkview_dict(spkview_data)
#         #returns true or false
#     if discourse_data != [] or len(discourse_data) > 0:
#         HAS_DISCOURSE_DATA = True

    
#     # Making a collection of words and its rules as a list of tuples.
#     words_info = generate_wordinfo(root_words, index_data, seman_data,
#                                 gnp_data, depend_data, discourse_data, spkview_data, scope_data)

#     # Categorising words as Nouns/Pronouns/Adjectives/..etc.
#     foreign_words_data,indeclinables_data, pronouns_data, nouns_data,verbal_adjectives, adjectives_data, verbs_data, adverbs_data, others_data, nominal_forms_data = identify_cat(
#         words_info)
#     print(words_info,'wordinfo')
    
#     # print(verbs_data,'vd')

#     #  Processing Stage
#     processed_foreign_words = process_foreign_word(foreign_words_data,words_info,verbs_data)
#     processed_indeclinables = process_indeclinables(indeclinables_data)
#     processed_nouns = process_nouns(nouns_data, words_info, verbs_data)
#     # print(processed_nouns)
#     processed_pronouns = process_pronouns(pronouns_data, processed_nouns, processed_indeclinables, words_info, verbs_data)
#     processed_others = process_others(others_data)
#     process_nominal_form = process_nominal_verb(nominal_forms_data, processed_nouns, words_info, verbs_data)
#     processed_verbs, processed_auxverbs = process_verbs(verbs_data, seman_data, depend_data, sentence_type, spkview_data,processed_nouns, processed_pronouns,index_data, words_info, False)
#     # processed_adjectives = process_verbal_adjective(verbal_adjectives,processed_nouns, words_info, verbs_data)
#     processed_adjectives = process_adjectives(adjectives_data, processed_nouns, processed_verbs)
#     process_adverbs(adverbs_data, processed_nouns, processed_verbs, processed_others, reprocessing=False)
#     postposition_finalization(processed_nouns, processed_pronouns,processed_foreign_words, words_info)
#     if len(additional_words_dict) > 0:
#         # print(additional_words_dict,'jjjjjjjjjjj')
#         HAS_ADDITIONAL_WORDS = True
#     print(processed_foreign_words,processed_pronouns,processed_nouns,processed_adjectives,
#                                             processed_verbs, processed_auxverbs,processed_indeclinables, processed_others)

#     # Every word is collected into one and sorted by index data.
#     processed_words = collect_processed_data(index_data,processed_foreign_words,processed_pronouns,processed_nouns,processed_adjectives,
#                                             processed_verbs, processed_auxverbs,processed_indeclinables, processed_others)


#     # calculating postpositions for words if applicable.
#     # processed_words, processed_postpositions = preprocess_postposition_new(processed_words, words_info,processed_verbs)
#     if HAS_CONSTRUCTION_DATA:
#         if flag_conj:
#             processed_words = process_construction(processed_words, construction_data, depend_data, gnp_data, index_data)
#         elif flag_span:
#             processed_words = process_construction_span(processed_words, construction_data, depend_data, gnp_data, index_data)

#     # Input for morph generator is generated and fed into it.
#     # Generator outputs the result in a file named morph_input.txt-out.txt
#     OUTPUT_FILE = generate_morph(processed_words)
#     # Create a new list to store the data from the output file
    

#     # # Append the data from the output file to the new list
#     # with open(OUTPUT_FILE, "r") as file:
#     #     for line in file:
#     #         output_data_list.append(line.strip())

#     # # Print the new list
#     # print(output_data_list,"o/p")

#     # Re-processing Stage
#     # Output from morph generator is read.
#     outputData = read_output_data(OUTPUT_FILE)
#     # Check for any non-generated words (mainly noun) & change the gender for non-generated words
#     #has_changes, reprocess_list, processed_nouns = handle_unprocessed_all(outputData, processed_nouns)
#     #print(reprocess_list)
#     has_changes, processed_nouns = handle_unprocessed(index_data,outputData, processed_nouns)

#     # handle unprocessed_verbs also with verb agreement
#     # If any changes is done in gender for any word.
#     # Adjectives and verbs are re-processed as they might be dependent on it.
#     if has_changes:
#         # Reprocessing adjectives and verbs based on new noun info
#         processed_verbs, processed_auxverbs = process_verbs(verbs_data, seman_data, depend_data, sentence_type, spkview_data, processed_nouns, processed_pronouns,index_data, words_info, True)
#         processed_adjectives = process_adjectives(adjectives_data, processed_nouns, processed_verbs)
#         process_adverbs(adverbs_data, processed_nouns, processed_verbs, processed_others, reprocessing=True)

#         # Sentence is generated again
#         processed_words = collect_processed_data(index_data,processed_foreign_words,processed_pronouns, processed_nouns,  processed_adjectives, processed_verbs,processed_auxverbs,processed_indeclinables,processed_others)
#         if HAS_CONSTRUCTION_DATA:
#             processed_words = process_construction(processed_words, construction_data, depend_data, gnp_data,index_data)
#             processed_words = process_construction_span(processed_words, construction_data, depend_data, gnp_data, index_data)

#         OUTPUT_FILE = generate_morph(processed_words)

#     # Post-Processing Stage
#     outputData = read_output_data(OUTPUT_FILE)
#     # generated words and word-info data is combined #pp data not yet added
#     transformed_data = analyse_output_data(outputData, processed_words)

#     # compound words and post-positions are joined.
#     transformed_data = join_compounds(transformed_data, construction_data)

#     #post-positions are joined.
#     PP_fulldata = add_postposition(transformed_data, processed_postpositions_dict)
#     #construction data is joined
#     if HAS_CONSTRUCTION_DATA:
#         PP_fulldata = add_construction(PP_fulldata, construction_dict)

#     if HAS_SPKVIEW_DATA:
#         PP_fulldata = add_spkview(PP_fulldata, spkview_dict)

#     ADD_MORPHO_SEMANTIC_DATA,PP_fulldata = populate_morpho_semantic_dict(gnp_data, PP_fulldata,words_info)
#     if ADD_MORPHO_SEMANTIC_DATA:
#         PP_fulldata = add_MORPHO_SEMANTIC(PP_fulldata, MORPHO_SEMANTIC_DICT)

#     if HAS_ADDITIONAL_WORDS:
#         PP_fulldata = add_additional_words(additional_words_dict, PP_fulldata)

#     POST_PROCESS_OUTPUT = rearrange_sentence(PP_fulldata)  # reaarange by index number
    
#     POST_PROCESS_OUTPUT=POST_PROCESS_OUTPUT.split()

#     for i in range(len(processed_foreign_words)):
#         n=processed_foreign_words[i][0]
#         POST_PROCESS_OUTPUT[n-1] = processed_foreign_words[i][1].replace('+',' ')

#     POST_PROCESS_OUTPUT=' '.join(POST_PROCESS_OUTPUT)
    
#     coref_list=process_coref(discourse_data)
#     if coref_list:
#         for i,coref_ele in enumerate(coref_list):
#             if coref_ele and len(coref_ele)==2:
#                 adding_coref = POST_PROCESS_OUTPUT.split()
#                 coref_word = '(' + clean(coref_ele[1]) + ')'
#                 adding_coref.insert(int(coref_ele[0])+(i+1), coref_word)
#                 POST_PROCESS_OUTPUT = ' '.join(adding_coref)

#     # coref_list = process_coref(discourse_data)
#     # if coref_list:
#     #     adding_coref = POST_PROCESS_OUTPUT.split()
#     #     for i in range(0, len(coref_list), 2):
#     #         index = coref_list[i]
#     #         coref_word = '(' + clean(coref_list[i + 1]) + ')'
#     #         adding_coref.insert(int(index) + 1, coref_word)
#     #     POST_PROCESS_OUTPUT = ' '.join(adding_coref)

#     # hindi_output = collect_hindi_output(POST_PROCESS_OUTPUT)


#     # if has_ques_mark(POST_PROCESS_OUTPUT,sentence_type):
#     #     POST_PROCESS_OUTPUT = POST_PROCESS_OUTPUT + ' ?'

#     if HAS_DISCOURSE_DATA:
        
#         # POST_PROCESS_OUTPUT = add_discourse_elements(discourse_data,spkview_data, POST_PROCESS_OUTPUT)
#         fp = 'output.json'
#         path=path.split('/')[1]
#         discourse = extract_discourse_values(fp, path)
#         relation = 'AvaSyakawApariNAma'
#         if discourse and relation in discourse:
#             POST_PROCESS_OUTPUT = add_discourse_elements(discourse,spkview_data, POST_PROCESS_OUTPUT)
        
#         elif not any(relation in item for item in discourse_data):
#             POST_PROCESS_OUTPUT = add_discourse_elements(discourse_data,spkview_data, POST_PROCESS_OUTPUT)
    
#     POST_PROCESS_OUTPUT = has_ques_mark(POST_PROCESS_OUTPUT,sentence_type)
#     # if has_ques_mark(POST_PROCESS_OUTPUT,sentence_type):
#     #     POST_PROCESS_OUTPUT = POST_PROCESS_OUTPUT + ' ?'

#     # # for yn_interrogative add kya in the beginning
#     # if sentence_type in ("yn_interrogative","yn_interrogative_negative", "pass-yn_interrogative"):
#     #     POST_PROCESS_OUTPUT = 'kyA ' + POST_PROCESS_OUTPUT

#     # if sentence_type in ('affirmative', 'Affirmative', 'negative', 'Negative', 'imperative', 'Imperative'):
#     #     POST_PROCESS_OUTPUT = POST_PROCESS_OUTPUT + ' |'
    

#     hindi_output = collect_hindi_output(POST_PROCESS_OUTPUT)
#     # output_data_list.append(hindi_output)
#     write_hindi_text(hindi_output, POST_PROCESS_OUTPUT, OUTPUT_FILE)
#     print(hindi_output)
#     # print("h/p: ",output_data_list)
#     # print(file_name,'fn/')
#     # #next line for single line input
    
# # with open('output_file_lion.txt', 'w') as file:
# #     for item in output_data_list:
# #         file.write(str(item) + '\n')  # Write each item to a new line
# #     print('written successfully')
    

# # next line code for bulk generation of results. All results are collated in test.csv. Run sh test.sh
# # write_hindi_test(hindi_output, POST_PROCESS_OUTPUT, src_sentence, OUTPUT_FILE, path)

# # # #for masked input -uncomment the following:
# # masked_pup_list = masked_postposition(processed_words, words_info, processed_verbs)
# # masked_pp_fulldata = add_postposition(transformed_data, masked_pup_list)
# # arranged_masked_output = rearrange_sentence(masked_pp_fulldata)
# # masked_hindi_data = collect_hindi_output(arranged_masked_output)
# # write_masked_hindi_test(hindi_output, POST_PROCESS_OUTPUT, src_sentence, masked_hindi_data, OUTPUT_FILE, path)
