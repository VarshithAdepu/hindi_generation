# from common_v3 import *
# #from common_v2 import *
# HAS_CONSTRUCTION_DATA = False
# HAS_SPKVIEW_DATA = False
# ADD_MORPHO_SEMANTIC_DATA = False
# HAS_DISCOURSE_DATA = False
# HAS_ADDITIONAL_WORDS = False


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
#     file_names = os.listdir(path)
#     file_names.sort()
#     for file_name in file_names:
#         # Construct the full path to each file
#         # file_path = os.path.join(path, file_name)
#         print("fnames: ",file_name)
#     output_data_list = []
#     for file_name in file_names:
#         # Construct the full path to each file
#         file_path = os.path.join(path, file_name)
#         print("fn: ",file_name)
        
#         # Process each file as needed
#         file_data = read_file(file_path)
#     # file_data = read_file(path) #Reading USR
    
#         rules_info = generate_rulesinfo(file_data) #Extracting Rules from each row of USR

#         # Extracting Information
#         src_sentence = rules_info[0]
#         root_words = rules_info[1]
#         index_data = [int(x) for x in rules_info[2]]
#         seman_data = rules_info[3]
#         gnp_data = rules_info[4]
#         depend_data = rules_info[5]
#         discourse_data = rules_info[6]
#         spkview_data = rules_info[7]
#         scope_data = rules_info[8]
#         sentence_type = rules_info[9]
#         construction_data = ''
#         # if len(rules_info) > 10 and rules_info[10] != '':
#         #     if 'speaker not found in dictionary' in rules_info[10]:
#         #         construction_data = ''
#         #     else:
#         #         HAS_CONSTRUCTION_DATA = True
#         #only when construction data is not nil
#         if len(rules_info) > 10 and rules_info[10]!='*nil':
#             construction_data = rules_info[10]
#             HAS_CONSTRUCTION_DATA = True

#         if spkview_data != [] or len(spkview_data) > 0:
#             HAS_SPKVIEW_DATA = populate_spkview_dict(spkview_data)
#             #returns true or false
#         if discourse_data != [] or len(discourse_data) > 0:
#             HAS_DISCOURSE_DATA = True

        
#         # Making a collection of words and its rules as a list of tuples.
#         words_info = generate_wordinfo(root_words, index_data, seman_data,
#                                     gnp_data, depend_data, discourse_data, spkview_data, scope_data)

#         # Categorising words as Nouns/Pronouns/Adjectives/..etc.
#         foreign_words_data,indeclinables_data, pronouns_data, nouns_data, adjectives_data, verbs_data, adverbs_data, others_data, nominal_forms_data = identify_cat(
#             words_info)

#         #  Processing Stage
#         processed_foreign_words = process_foreign_word(foreign_words_data,words_info,verbs_data)
#         processed_indeclinables = process_indeclinables(indeclinables_data)
#         processed_nouns = process_nouns(nouns_data, words_info, verbs_data)
#         processed_pronouns = process_pronouns(pronouns_data, processed_nouns, processed_indeclinables, words_info, verbs_data)
#         processed_others = process_others(others_data)
#         processed_verbs, processed_auxverbs = process_verbs(verbs_data, seman_data, depend_data, sentence_type, spkview_data,processed_nouns, processed_pronouns, words_info, False)
#         processed_adjectives = process_adjectives(adjectives_data, processed_nouns, processed_verbs)
#         process_adverbs(adverbs_data, processed_nouns, processed_verbs, processed_others, reprocessing=False)
#         process_nominal_form = process_nominal_verb(nominal_forms_data, processed_nouns, words_info, verbs_data)
#         postposition_finalization(processed_nouns, processed_pronouns,processed_foreign_words, words_info)
#         print('additional_words_dict:::',additional_words_dict)
#         if len(additional_words_dict) > 0:
#             # print(additional_words_dict,'jjjjjjjjjjj')
#             HAS_ADDITIONAL_WORDS = True

#         # Every word is collected into one and sorted by index number.
#         processed_words = collect_processed_data(processed_foreign_words,processed_pronouns,processed_nouns,processed_adjectives,
#                                                 processed_verbs, processed_auxverbs,processed_indeclinables, processed_others)


#         # calculating postpositions for words if applicable.
#         # processed_words, processed_postpositions = preprocess_postposition_new(processed_words, words_info,processed_verbs)
#         if HAS_CONSTRUCTION_DATA:
#             processed_words = process_construction(processed_words, construction_data, depend_data, gnp_data, index_data)
#             processed_words = process_construction_span(processed_words, construction_data, depend_data, gnp_data, index_data)

#         # Input for morph generator is generated and fed into it.
#         # Generator outputs the result in a file named morph_input.txt-out.txt
#         OUTPUT_FILE = generate_morph(processed_words)
#         # Create a new list to store the data from the output file
        

#         # # Append the data from the output file to the new list
#         # with open(OUTPUT_FILE, "r") as file:
#         #     for line in file:
#         #         output_data_list.append(line.strip())

#         # # Print the new list
#         # print(output_data_list,"o/p")

#         # Re-processing Stage
#         # Output from morph generator is read.
#         outputData = read_output_data(OUTPUT_FILE)
#         # Check for any non-generated words (mainly noun) & change the gender for non-generated words
#         #has_changes, reprocess_list, processed_nouns = handle_unprocessed_all(outputData, processed_nouns)
#         #print(reprocess_list)
#         has_changes, processed_nouns = handle_unprocessed(outputData, processed_nouns)

#         # handle unprocessed_verbs also with verb agreement
#         # If any changes is done in gender for any word.
#         # Adjectives and verbs are re-processed as they might be dependent on it.
#         if has_changes:
#             # Reprocessing adjectives and verbs based on new noun info
#             processed_verbs, processed_auxverbs = process_verbs(verbs_data, seman_data, depend_data, sentence_type, spkview_data, processed_nouns, processed_pronouns, words_info, True)
#             processed_adjectives = process_adjectives(adjectives_data, processed_nouns, processed_verbs)
#             process_adverbs(adverbs_data, processed_nouns, processed_verbs, processed_others, reprocessing=True)

#             # Sentence is generated again
#             processed_words = collect_processed_data(processed_foreign_words,processed_pronouns, processed_nouns,  processed_adjectives, processed_verbs,processed_auxverbs,processed_indeclinables,processed_others)
#             if HAS_CONSTRUCTION_DATA:
#                 processed_words = process_construction(processed_words, construction_data, depend_data, gnp_data,index_data)
#                 processed_words = process_construction_span(processed_words, construction_data, depend_data, gnp_data, index_data)

#             OUTPUT_FILE = generate_morph(processed_words)

#         # Post-Processing Stage
#         outputData = read_output_data(OUTPUT_FILE)
#         # generated words and word-info data is combined #pp data not yet added
#         transformed_data = analyse_output_data(outputData, processed_words)

#         # compound words and post-positions are joined.
#         transformed_data = join_compounds(transformed_data, construction_data)

#         #post-positions are joined.
#         PP_fulldata = add_postposition(transformed_data, processed_postpositions_dict)
#         #construction data is joined
#         if HAS_CONSTRUCTION_DATA:
#             PP_fulldata = add_construction(PP_fulldata, construction_dict)

#         if HAS_SPKVIEW_DATA:
#             PP_fulldata = add_spkview(PP_fulldata, spkview_dict)

#         ADD_MORPHO_SEMANTIC_DATA,PP_fulldata = populate_morpho_semantic_dict(gnp_data, PP_fulldata,words_info)
#         if ADD_MORPHO_SEMANTIC_DATA:
#             PP_fulldata = add_MORPHO_SEMANTIC(PP_fulldata, MORPHO_SEMANTIC_DICT)

#         if HAS_ADDITIONAL_WORDS:
#             PP_fulldata = add_additional_words(additional_words_dict, PP_fulldata)

#         POST_PROCESS_OUTPUT = rearrange_sentence(PP_fulldata)  # reaarange by index number
        
#         POST_PROCESS_OUTPUT=POST_PROCESS_OUTPUT.split()

#         for i in range(len(processed_foreign_words)):
#             n=processed_foreign_words[i][0]
#             POST_PROCESS_OUTPUT[n-1] = processed_foreign_words[i][1].replace('+',' ')

#         POST_PROCESS_OUTPUT=' '.join(POST_PROCESS_OUTPUT)
        
#         coref_list=process_coref(discourse_data)
#         if coref_list and len(coref_list)==2:
#             adding_coref = POST_PROCESS_OUTPUT.split()
#             coref_word = '(' + clean(coref_list[1]) + ')'
#             adding_coref.insert(int(coref_list[0])+1, coref_word)
#             POST_PROCESS_OUTPUT = ' '.join(adding_coref)

#         # hindi_output = collect_hindi_output(POST_PROCESS_OUTPUT)


#         # if has_ques_mark(POST_PROCESS_OUTPUT,sentence_type):
#         #     POST_PROCESS_OUTPUT = POST_PROCESS_OUTPUT + ' ?'

#         if HAS_DISCOURSE_DATA:
#             POST_PROCESS_OUTPUT = add_discourse_elements(discourse_data, POST_PROCESS_OUTPUT)
        
#         POST_PROCESS_OUTPUT = has_ques_mark(POST_PROCESS_OUTPUT,sentence_type)
#         # if has_ques_mark(POST_PROCESS_OUTPUT,sentence_type):
#         #     POST_PROCESS_OUTPUT = POST_PROCESS_OUTPUT + ' ?'

#         # # for yn_interrogative add kya in the beginning
#         # if sentence_type in ("yn_interrogative","yn_interrogative_negative", "pass-yn_interrogative"):
#         #     POST_PROCESS_OUTPUT = 'kyA ' + POST_PROCESS_OUTPUT

#         # if sentence_type in ('affirmative', 'Affirmative', 'negative', 'Negative', 'imperative', 'Imperative'):
#         #     POST_PROCESS_OUTPUT = POST_PROCESS_OUTPUT + ' |'

#         hindi_output = collect_hindi_output(POST_PROCESS_OUTPUT)
#         output_data_list.append(hindi_output)
#         print("h/p: ",output_data_list)
#         print(file_name,'fn/')
#         # #next line for single line input
#         write_hindi_text(hindi_output, POST_PROCESS_OUTPUT, OUTPUT_FILE)
#     additional_words_dict={}
#     with open('output_file.txt', 'w') as file:
#         for item in output_data_list:
#             file.write(str(item) + '\n')  # Write each item to a new line
#         print('written successfully')
        

#     # next line code for bulk generation of results. All results are collated in test.csv. Run sh test.sh
#     # write_hindi_test(hindi_output, POST_PROCESS_OUTPUT, src_sentence, OUTPUT_FILE, path)

#     # # #for masked input -uncomment the following:
#     # masked_pup_list = masked_postposition(processed_words, words_info, processed_verbs)
#     # masked_pp_fulldata = add_postposition(transformed_data, masked_pup_list)
#     # arranged_masked_output = rearrange_sentence(masked_pp_fulldata)
#     # masked_hindi_data = collect_hindi_output(arranged_masked_output)
#     # write_masked_hindi_t
# =====================================================================================================================

from bulk_common_v3 import *
from Json_format import *
from extract_json_data import *
import sys
import os
from check_fun import *
from process_fun import *
from add_fun import *

HAS_CONSTRUCTION_DATA = False
HAS_SPKVIEW_DATA = False
ADD_MORPHO_SEMANTIC_DATA = False
HAS_DISCOURSE_DATA = False
HAS_ADDITIONAL_WORDS = False
# additional_words_dict = {}


def process_file(file_path):
    global HAS_CONSTRUCTION_DATA, HAS_SPKVIEW_DATA, HAS_DISCOURSE_DATA, HAS_ADDITIONAL_WORDS
    # Process each file as needed
    file_data = read_file(file_path)
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
    sentence_type = rules_info[9]
    construction_data = ''
    # src_sentence, root_words, index_data, seman_data, gnp_data, depend_data, discourse_data, spkview_data, scope_data, sentence_type, *rest = rules_info

    if len(rules_info) > 10 and rules_info[10]!='*nil':
        construction_data = rules_info[10]
        HAS_CONSTRUCTION_DATA = True

    if spkview_data:
        HAS_SPKVIEW_DATA = populate_spkview_dict(spkview_data)

    if discourse_data:
        HAS_DISCOURSE_DATA = True

    # Making a collection of words and its rules as a list of tuples.
    words_info = generate_wordinfo(root_words, index_data, seman_data,
                                gnp_data, depend_data, discourse_data, spkview_data, scope_data)
    # Categorising words as Nouns/Pronouns/Adjectives/..etc.
    # if categorize_words(words_info):
    categorized_data = categorize_words(words_info)
    # else:
    #     return None,None,False
    #  Processing Stage
    processed_data = process_words(categorized_data, words_info, seman_data, depend_data, sentence_type, spkview_data)

    processed_foreign_words, processed_pronouns, processed_nouns, processed_adjectives, processed_verbs, processed_auxverbs, processed_indeclinables, processed_others = processed_data
    # if processed_verbs == None and processed_auxverbs== None:
    #     return None,None,False

    if len(additional_words_dict) > 0: 
        HAS_ADDITIONAL_WORDS = True

    # Every word is collected into one and sorted by index number.
    processed_words = collect_processed_data(*processed_data)

    # calculating postpositions for words if applicable.
    # processed_words, processed_postpositions = preprocess_postposition_new(processed_words, words_info,processed_verbs)
    if HAS_CONSTRUCTION_DATA:
        processed_words = process_construction(processed_words, construction_data, depend_data, gnp_data, index_data)
        processed_words = process_construction_span(processed_words, construction_data, depend_data, gnp_data, index_data)

    # Input for morph generator is generated and fed into it.
    # Generator outputs the result in a file named morph_input.txt-out.txt
    OUTPUT_FILE = generate_morph(processed_words)
    # Output from morph generator is read.
    outputData = read_output_data(OUTPUT_FILE)

    # Check for any non-generated words (mainly noun) & change the gender for non-generated words
    has_changes, processed_nouns = handle_unprocessed(outputData, processed_data[2])

    # handle unprocessed_verbs also with verb agreement
    if has_changes:
        # Reprocessing adjectives and verbs based on new noun info
        reprocessed_data = reprocess_words(categorized_data,processed_data, processed_nouns, words_info, seman_data, depend_data, sentence_type, spkview_data)
        # Sentence is generated again
        processed_words = collect_processed_data(*reprocessed_data)

        if HAS_CONSTRUCTION_DATA:
            processed_words = process_construction(processed_words, construction_data, depend_data, gnp_data, index_data)
            processed_words = process_construction_span(processed_words, construction_data, depend_data, gnp_data, index_data)

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

    ADD_MORPHO_SEMANTIC_DATA, PP_fulldata = populate_morpho_semantic_dict(gnp_data, PP_fulldata, words_info)
    if ADD_MORPHO_SEMANTIC_DATA:
        PP_fulldata = add_MORPHO_SEMANTIC(PP_fulldata, MORPHO_SEMANTIC_DICT)
    if HAS_ADDITIONAL_WORDS:
        PP_fulldata = add_additional_words(additional_words_dict, PP_fulldata)

    POST_PROCESS_OUTPUT = rearrange_sentence(PP_fulldata)
    POST_PROCESS_OUTPUT = handle_foreign_words(POST_PROCESS_OUTPUT, processed_foreign_words)

    coref_list = process_coref(discourse_data)
    if coref_list and len(coref_list) == 2:
        POST_PROCESS_OUTPUT = add_coref(POST_PROCESS_OUTPUT, coref_list)

    if HAS_DISCOURSE_DATA:
        POST_PROCESS_OUTPUT = process_discourse_data(POST_PROCESS_OUTPUT,spkview_data, discourse_data, file_name)

    POST_PROCESS_OUTPUT = has_ques_mark(POST_PROCESS_OUTPUT, sentence_type)
    hindi_output = collect_hindi_output(POST_PROCESS_OUTPUT)
    write_hindi_text(hindi_output, POST_PROCESS_OUTPUT, OUTPUT_FILE)

    # next line code for bulk generation of results. All results are collated in test.csv. Run sh test.sh
    # write_hindi_test(hindi_output, POST_PROCESS_OUTPUT, src_sentence, OUTPUT_FILE, path)

    # # #for masked input -uncomment the following:
    # masked_pup_list = masked_postposition(processed_words, words_info, processed_verbs)
    # masked_pp_fulldata = add_postposition(transformed_data, masked_pup_list)
    # arranged_masked_output = rearrange_sentence(masked_pp_fulldata)
    # masked_hindi_data = collect_hindi_output(arranged_masked_output)
    # write_masked_hindi_test(hindi_output, POST_PROCESS_OUTPUT, src_sentence, masked_hindi_data, OUTPUT_FILE, path)
    return hindi_output,POST_PROCESS_OUTPUT

def categorize_words(words_info):
    # foreign_words,indeclinables, pronouns, nouns, adjectives, verbs, adverbs, others, nominal_verb=identify_cat(words_info)
    # if nouns:
    return identify_cat(words_info)
    # else:
    #     return None

def process_words(categorized_data, words_info, seman_data, depend_data, sentence_type, spkview_data):
    foreign_words_data, indeclinables_data, pronouns_data, nouns_data, adjectives_data, verbs_data, adverbs_data, others_data, nominal_forms_data = categorized_data

    processed_foreign_words = process_foreign_word(foreign_words_data, words_info, verbs_data)
    processed_indeclinables = process_indeclinables(indeclinables_data)
    # if process_nouns(nouns_data, words_info, verbs_data):
    processed_nouns = process_nouns(nouns_data, words_info, verbs_data)
    # else:
    #     return None,None
    processed_pronouns = process_pronouns(pronouns_data, processed_nouns, processed_indeclinables, words_info, verbs_data)
    processed_others = process_others(others_data)
    # if process_verbs(verbs_data, seman_data, depend_data, sentence_type, spkview_data, processed_nouns, processed_pronouns, words_info, False):
    processed_verbs, processed_auxverbs = process_verbs(verbs_data, seman_data, depend_data, sentence_type, spkview_data, processed_nouns, processed_pronouns, words_info, False)
    # else:
    #     return None,None

    processed_adjectives = process_adjectives(adjectives_data, processed_nouns, processed_verbs)
    process_adverbs(adverbs_data, processed_nouns, processed_verbs, processed_others, reprocessing=False)
    process_nominal_form = process_nominal_verb(nominal_forms_data, processed_nouns, words_info, verbs_data)
    postposition_finalization(processed_nouns, processed_pronouns, processed_foreign_words, words_info)

    return (processed_foreign_words, processed_pronouns, processed_nouns, processed_adjectives, processed_verbs, processed_auxverbs, processed_indeclinables, processed_others)

def reprocess_words(categorized_data,processed_data, processed_nouns, words_info, seman_data, depend_data, sentence_type, spkview_data):
    processed_foreign_words, processed_pronouns, processed_nouns, processed_adjectives, processed_verbs, processed_auxverbs, processed_indeclinables, processed_others = processed_data
    foreign_words_data, indeclinables_data, pronouns_data, nouns_data, adjectives_data, verbs_data, adverbs_data, others_data, nominal_forms_data = categorized_data
    processed_verbs, processed_auxverbs = process_verbs(verbs_data, seman_data, depend_data, sentence_type, spkview_data, processed_nouns, processed_pronouns, words_info, True)
    processed_adjectives = process_adjectives(adjectives_data, processed_nouns, processed_verbs)
    process_adverbs(adverbs_data, processed_nouns, processed_verbs, processed_others, reprocessing=True)

    return (processed_foreign_words, processed_pronouns, processed_nouns, processed_adjectives, processed_verbs, processed_auxverbs, processed_indeclinables, processed_others)

def handle_foreign_words(POST_PROCESS_OUTPUT, processed_foreign_words):
    POST_PROCESS_OUTPUT = POST_PROCESS_OUTPUT.split()
    for i in range(len(processed_foreign_words)):
        n = processed_foreign_words[i][0]
        POST_PROCESS_OUTPUT[n-1] = processed_foreign_words[i][1].replace('+', ' ')
    return ' '.join(POST_PROCESS_OUTPUT)

def add_coref(POST_PROCESS_OUTPUT, coref_list):
    adding_coref = POST_PROCESS_OUTPUT.split()
    coref_word = '(' + clean(coref_list[1]) + ')'
    adding_coref.insert(int(coref_list[0]) + 1, coref_word)
    return ' '.join(adding_coref)

def process_discourse_data(POST_PROCESS_OUTPUT,spkview_data, discourse_data, file_name):
    fp = 'output.json'
    file_name=file_name.split('/')[1]
    discourse = extract_discourse_values(fp, file_name)
    relation = 'AvaSyakawApariNAma'
    if discourse and relation in discourse:
        POST_PROCESS_OUTPUT = add_discourse_elements(discourse,spkview_data, POST_PROCESS_OUTPUT)
    elif not any(relation in item for item in discourse_data):
        POST_PROCESS_OUTPUT = add_discourse_elements(discourse_data,spkview_data, POST_PROCESS_OUTPUT)
    return POST_PROCESS_OUTPUT

if __name__ == "__main__":

    log("Program Started", "START")
    # Reading filename as command-line argument
    try:
        file_name = sys.argv[1]
    except IndexError:
        log("No argument given. Please provide path for input file as an argument.", "ERROR")
        sys.exit()

    Json_format(file_name.split('/')[0])
    

    output_data_list = []
    # for file_name in file_names:
    #     print(file_name)
    #     file_path = os.path.join(path, file_name)
    hindi_output,Wxconv_data = process_file(file_name)
    reset_global_dicts()
    # combined_output = f"{Wxconv_data}\n{hindi_output}\n"
    # output_data_list.append(combined_output)
    # if success:
    output_data_list.append(hindi_output)
    # else:
    #     str1=file_names + " Something went wrong"
    #     output_data_list.append(str1)
    print(hindi_output)
    
# ==========================================================================================================
