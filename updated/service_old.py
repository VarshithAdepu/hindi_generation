# from flask import Flask, request, jsonify
import sys
from repository.common_v3 import *
#from common_v2 import *
# from json import Json_format
from extract_json import *

HAS_CONSTRUCTION_DATA = False
HAS_SPKVIEW_DATA = False
ADD_MORPHO_SEMANTIC_DATA = False
HAS_DISCOURSE_DATA = False
HAS_ADDITIONAL_WORDS = False
HAS_COREF = False
flag_conj=False
flag_disjunct=False
flag_span=False
flag_cp=False
flag_meas=False
flag_rate=False
flag_spatial=False
flag_waw=False
flag_cal=False
flag_xvanxva=False
# Import all the required functions from your other modules
# Example:
# from common_v3 import (read_file, generate_rulesinfo, process_verbs, etc.)
# from Json_format import Json_format
# from extract_json_data import *

# Global flags
HAS_CONSTRUCTION_DATA = False
HAS_SPKVIEW_DATA = False
ADD_MORPHO_SEMANTIC_DATA = False
HAS_DISCOURSE_DATA = False
HAS_ADDITIONAL_WORDS = False
HAS_COREF = False

flag_conj = False
flag_disjunct = False
flag_span = False
flag_cp = False
flag_meas = False
flag_rate = False
flag_spatial = False
flag_waw = False
flag_cal = False
flag_xvanxva = False

# Main function that handles the core processing logic
def process_file_data(input_data):
    global HAS_CONSTRUCTION_DATA, HAS_SPKVIEW_DATA, ADD_MORPHO_SEMANTIC_DATA, HAS_DISCOURSE_DATA, HAS_ADDITIONAL_WORDS, HAS_COREF
    global flag_conj, flag_disjunct, flag_span, flag_cp, flag_meas, flag_rate, flag_spatial, flag_waw, flag_cal, flag_xvanxva

    # Initialize flags and output data list
    output_data_list = []
    # output_text,sentence_id=convert_vert_to_csv(input_data)
    # Read the input file
    # file_data= read_file(output_text)
    # print(output_text,'hhh')
    # Extract rules info
    rules_info = generate_rulesinfo(input_data)
    
    # Extract individual components from rules_info
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
    sentence_type = rules_info[10]
    
    # Initialize construction-related data
    conj_concept = root_words
    span_concept = root_words
    
    # Process each root word
    for i, concept in enumerate(root_words):
        if 'conj' in concept:
            flag_conj = True
            HAS_CONSTRUCTION_DATA = True
            depend_data = construction_row(i, construction_data, depend_data, index_data)
        elif 'disjunct' in concept:
            flag_disjunct = True
            HAS_CONSTRUCTION_DATA = True
            depend_data = construction_row(i, construction_data, depend_data, index_data)
        elif 'span' in concept:
            flag_span = True
            HAS_CONSTRUCTION_DATA = True
            depend_data = construction_row_span(i, construction_data, depend_data, index_data)
        elif 'cp' in concept:
            flag_cp = True
            HAS_CONSTRUCTION_DATA = True
            depend_data = construction_row_cp(i, construction_data, depend_data, index_data)
        elif 'meas' in concept:
            flag_meas = True
            HAS_CONSTRUCTION_DATA = True
            depend_data = construction_row_meas(i, construction_data, depend_data, index_data)
        elif 'rate' in concept:
            flag_rate = True
            HAS_CONSTRUCTION_DATA = True
            depend_data = construction_row_meas(i, construction_data, depend_data, index_data)
        elif 'waw' in concept:
            flag_waw = True
            HAS_CONSTRUCTION_DATA = True
            depend_data = construction_row_waw(i, construction_data, depend_data, index_data)
        elif clean(concept) in ('compound', 'waw'):
            flag_waw = True
            HAS_CONSTRUCTION_DATA = True
            depend_data = construction_row_waw(i, construction_data, depend_data, index_data)
        elif 'calender' in concept:
            flag_cal = True
            HAS_CONSTRUCTION_DATA = True
            depend_data = construction_row_calender(i, construction_data, depend_data, index_data)
        elif 'spatial' in concept:
            flag_spatial = True
            HAS_CONSTRUCTION_DATA = True
            depend_data = construction_row_spatial(i, construction_data, depend_data, index_data)
        elif 'xvanxva' in concept:
            flag_xvanxva = True
            HAS_CONSTRUCTION_DATA = True
            depend_data = construction_row(i, construction_data, depend_data, index_data)

    check_main_verb(depend_data)
    
    # Speaker view data processing
    if spkview_data:
        HAS_SPKVIEW_DATA = populate_spkview_dict(spkview_data, index_data)
    
    # Discourse data processing
    if discourse_data:
        HAS_DISCOURSE_DATA = True
        if 'coref' in discourse_data:
            HAS_COREF = True

    # Generate word info
    words_info = generate_wordinfo(root_words, index_data, seman_data, gnp_data, depend_data, discourse_data, spkview_data, scope_data, construction_data)
    
    # Identify word categories
    foreign_words_data, indeclinables_data, pronouns_data, nouns_data, verbal_adjectives, adjectives_data, verbs_data, adverbs_data, others_data, nominal_forms_data = identify_cat(words_info)
    
    # Process individual word categories
    processed_foreign_words = process_foreign_word(index_data, foreign_words_data, words_info, verbs_data)
    processed_indeclinables = process_indeclinables(indeclinables_data)
    processed_nouns = process_nouns(index_data, seman_data, nouns_data, words_info, verbs_data)
    processed_pronouns = process_pronouns(index_data, pronouns_data, processed_nouns, processed_indeclinables, words_info, verbs_data)
    processed_others = process_others(others_data)
    process_nominal_form = process_nominal_verb(index_data, nominal_forms_data, processed_nouns, words_info, verbs_data)
    processed_verbs, processed_auxverbs = process_verbs(verbs_data, seman_data, gnp_data, depend_data, sentence_type, spkview_data, processed_nouns, processed_pronouns, index_data, words_info, False)
    
    # Further processing of adjectives, adverbs, etc.
    processed_adjectives = process_adjectives(adjectives_data, processed_nouns, processed_verbs)
    process_adverbs(adverbs_data, processed_nouns, processed_verbs, processed_others, reprocessing=False)
    
    # Finalize postposition processing
    postposition_finalization(processed_nouns, processed_pronouns, processed_foreign_words, words_info)
    
    if len(additional_words_dict) > 0:
        HAS_ADDITIONAL_WORDS = True
    
    # Collect all processed data
    processed_words = collect_processed_data(index_data, processed_foreign_words, processed_pronouns, processed_nouns, processed_adjectives, processed_verbs, processed_auxverbs, processed_indeclinables, processed_others)
    
    # Construction data processing
    if HAS_CONSTRUCTION_DATA:
        if flag_conj or flag_disjunct:
            processed_words = process_construction(processed_words, root_words, construction_data, depend_data, gnp_data, index_data, conj_concept)
            flag_conj, flag_disjunct = False, False
        if flag_span:
            processed_words = process_construction_span(processed_words, construction_data, index_data)
            flag_span = False
        if flag_rate:
            processed_words = process_construction_rate(processed_words, construction_data, index_data)
            flag_rate = False
        if flag_spatial:
            processed_words = process_construction_spatial(processed_words, construction_data, index_data)
            flag_spatial = False
        if flag_xvanxva:
            processed_words = process_construction_xvanxva(processed_words, construction_data, index_data)
            flag_xvanxva = False
    
    # Generate morph and output file
    outputData = generate_morph(processed_words)
    # outputData = read_output_data(OUTPUT_FILE)
    
    # Handle unprocessed data and apply changes
    has_changes, processed_nouns = handle_unprocessed(index_data, depend_data, outputData, processed_nouns)
    
    if has_changes:
        processed_verbs, processed_auxverbs = process_verbs(verbs_data, seman_data, gnp_data, depend_data, sentence_type, spkview_data, processed_nouns, processed_pronouns, index_data, words_info, True)
        processed_adjectives = process_adjectives(adjectives_data, processed_nouns, processed_verbs)
        process_adverbs(adverbs_data, processed_nouns, processed_verbs, processed_others, reprocessing=True)
        processed_words = collect_processed_data(index_data, processed_foreign_words, processed_pronouns, processed_nouns, processed_adjectives, processed_verbs, processed_auxverbs, processed_indeclinables, processed_others)

        # Sentence is generated again
        processed_words = collect_processed_data(index_data,processed_foreign_words,processed_pronouns, processed_nouns,  processed_adjectives, processed_verbs,processed_auxverbs,processed_indeclinables,processed_others)
        if HAS_CONSTRUCTION_DATA:
            if flag_conj or flag_disjunct:
                processed_words = process_construction(processed_words, construction_data, depend_data, gnp_data,index_data,conj_concept)
            if flag_span:
                processed_words = process_construction_span(processed_words, construction_data, index_data)
            if flag_rate:
                processed_words = process_construction_rate(processed_words, construction_data,index_data)
            if flag_spatial:
                processed_words = process_construction_spatial(processed_words, construction_data,index_data)
    
        outputData = generate_morph(processed_words)

    # Post-Processing Stage
    # outputData = read_output_data(OUTPUT_FILE)
    # generated words and word-info data is combined #pp data not yet added
    transformed_data = analyse_output_data(outputData, processed_words)

    # compound words and post-positions are joined.
    transformed_data = join_compounds(transformed_data, construction_data)
    #post-positions are joined.
    PP_fulldata = add_postposition(transformed_data,index_data,depend_data, processed_postpositions_dict)
    #construction data is joined
    if HAS_CONSTRUCTION_DATA:
        PP_fulldata = add_construction(PP_fulldata, construction_dict)

    if HAS_SPKVIEW_DATA:
        PP_fulldata = add_spkview(PP_fulldata, spkview_dict)

    ADD_MORPHO_SEMANTIC_DATA,PP_fulldata = populate_morpho_semantic_dict(index_data,gnp_data, PP_fulldata,words_info)
    if ADD_MORPHO_SEMANTIC_DATA:
        PP_fulldata = add_MORPHO_SEMANTIC(PP_fulldata, MORPHO_SEMANTIC_DICT)

    if HAS_ADDITIONAL_WORDS:
        PP_fulldata = add_additional_words(additional_words_dict, PP_fulldata)
    # Finalize post-processing
    # coref_list=process_coref(index_data,PP_fulldata,discourse_data,path)
    # output_sentence = rearrange_sentence(processed_words, coref_list)
    POST_PROCESS_OUTPUT = rearrange_sentence(PP_fulldata)  # reaarange by index number
    
    # if HAS_COREF:
    #     POST_PROCESS_OUTPUT = rearrange_sentence(PP_fulldata)  # reaarange by index number
    # if clean(temp[1]) not in ('cp','conj','disjunct','span','widthmeas','depthmeas','distmeas','rate','timemeas','waw','calender','massmeas','heightmeas','spatial'):
    #     POST_PROCESS_OUTPUT = POST_PROCESS_OUTPUT[0]
    POST_PROCESS_OUTPUT=POST_PROCESS_OUTPUT.split()
    allowed_values = ('cp', 'conj', 'disjunct', 'span', 'widthmeas', 'depthmeas', 'distmeas', 'rate', 'timemeas', 'waw', 'calender', 'massmeas', 'heightmeas', 'spatial')
    POST_PROCESS_OUTPUT = [word for word in POST_PROCESS_OUTPUT if clean(word) not in allowed_values]

    for i in range(len(processed_foreign_words)):
        n=processed_foreign_words[i][0]
        POST_PROCESS_OUTPUT[n-1] = processed_foreign_words[i][1].replace('+',' ')

    POST_PROCESS_OUTPUT=' '.join(POST_PROCESS_OUTPUT)

    # path=path.split('/')[1]
    if HAS_DISCOURSE_DATA:
        
        # POST_PROCESS_OUTPUT = add_discourse_elements(discourse_data,spkview_data, POST_PROCESS_OUTPUT)
        # fp = 'output.json'
        # discourse,sp_data = extract_discourse_values(input_data)
        discourse=''
        sp_data = ''
        # print(sp_data)
        relation = ['AvaSyakawApariNAma','vyaBicAra']
        if discourse and discourse in relation:
            POST_PROCESS_OUTPUT = add_discourse_elements(discourse,spkview_data,sp_data, POST_PROCESS_OUTPUT)
        else:
            for i in discourse_data:
                if i and i.split(':')[1] not in relation and 'coref' not in i:
                    POST_PROCESS_OUTPUT = add_discourse_elements(discourse_data,spkview_data,sp_data, POST_PROCESS_OUTPUT)
            
    
    POST_PROCESS_OUTPUT = has_ques_mark(POST_PROCESS_OUTPUT,sentence_type)
    # if 'BI_1' in spkview_data:
    # POST_PROCESS_OUTPUT=extract_spkview_values('output.json',path,POST_PROCESS_OUTPUT)
    for i in discourse_data:
        if 'AvaSyakawApariNAma' in i and 'nahIM' not in spkview_data:
            POST_PROCESS_OUTPUT = 'yaxi ' + POST_PROCESS_OUTPUT
            # break
        elif 'vyaBicAra' in i:
            POST_PROCESS_OUTPUT = 'yaxyapi ' + POST_PROCESS_OUTPUT
    print(POST_PROCESS_OUTPUT)
    hindi_output = collect_hindi_output(POST_PROCESS_OUTPUT)
    # output_data_list.append(hindi_output)
    # if '/' in hindi_output:
    #     write_hindi_text_list(hindi_output, POST_PROCESS_OUTPUT, OUTPUT_FILE)
    # else:
    #     write_hindi_text(hindi_output, POST_PROCESS_OUTPUT, OUTPUT_FILE)
    
    print(hindi_output)
    return hindi_output

def convert_vert_to_csv(input_text):
    sentences=[]
    # Split the input text into segments based on the closing </segment_id> tag
    segments = input_text.strip().split('</segment_id>')
    
    # Initialize lists to store segment outputs and segment IDs
    all_output = []
    segment_ids = []
    
    # Process each segment individually
    for segment in segments:
        # Skip empty segments
        if not segment.strip():
            continue
        
        # Split each segment into lines and remove any empty lines
        lines = segment.strip().splitlines()
        
        # Extract the first line (segment_id)
        segment_id = lines[0].strip()
        if "<segment_id=" in segment_id:  # Extract sentence id
            segment_id = segment_id.split('=')[1].strip('>')  # Extract everything after '=' and remove '>'
            segment_ids.append(segment_id)  # Store the segment ID
        
        # Extract the second line (sentence)
        sentence = lines[1].strip()
        
        # Initialize lists to store the columns
        words, indices, entities, extra_column1, extra_column2, extra_column3, extra_column4, extra_column5, extra_column6 = ([] for _ in range(9))
        
        # Process each line of the table data (ignore the first two and last lines)
        for line in lines[2:-1]:
            columns = line.split()
            words.append(columns[0])  # word
            # print(columns[1])
            indices.append(columns[1])  # index
            entities.append(columns[2] if columns[2] != '-' else '')  # entity
            
            # Check each extra column and replace '-' with an empty string
            extra_column1.append(columns[3] if columns[3] != '-' else '')
            extra_column2.append(columns[4] if columns[4] != '-' else '')
            extra_column3.append(columns[5] if columns[5] != '-' else '')
            extra_column4.append(columns[6] if columns[6] != '-' else '')
            extra_column5.append(columns[7] if columns[7] != '-' else '')
            extra_column6.append(columns[8] if len(columns) > 8 and columns[8] != '-' else '')

        # Extract the last line (marker)
        last_line_marker = lines[-1].strip()
        
        # Create the output for this segment
        output = [
            sentence,
            ','.join(words),
            ','.join(indices),
            ','.join(entities),
            ','.join(extra_column1),
            ','.join(extra_column2),
            ','.join(extra_column3),
            ','.join(extra_column4),
            ','.join(extra_column5),
            ','.join(extra_column6),
            last_line_marker,
        ]
        
        # Add the result to the final output
        print(output,'oppp')
        output1=process_file_data(output)
        all_output.append(output1)

    # print(segment_ids)    # Return both the segment outputs and the segment IDs as separate lists
    # for segment_id, output in zip(segment_ids, all_output):
    last_output=process_sentence(segment_ids,sentences,all_output)
    print(last_output)
    return last_output


if __name__=='__main__':
    input_data="""<segment_id= test_Geo_nios_10ch_0003>
#हमें	अपने	आप	को	गर्म	रखने	तथा	बढने	के	लिए	अनुकूल	तापमान	भी	चाहिये	।
$speaker	1	anim	pl	8:k1	-	-	-	-
Kuxa 	2	-	-	9:k2	1:coref	-	-	-
garma_1	11	-	-	-	-	-	-	10:kriyAmUla
raKa_3	4	-	-	-	-	-	-	10:verbalizer
[cp_1]	10	-	-	-	-	-	-	9:op1
baDa_1	5	-	-	-	-	-	-	9:op2
anukUla_1	6	-	-	7:mod	-	-	-	-
wApamAna_1	7	-	-	8:k2	-	BI_1	-	-
cAha_1-e_1	8	-	-	0:main	-	-	-	-
[conj_1]	9	-	-	8:rt	-	-	-	-
%affirmative
</segment_id>"""

    convert_vert_to_csv(input_data)
