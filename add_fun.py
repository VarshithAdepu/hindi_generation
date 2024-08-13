import sys
import re
import constant

def add_postposition(transformed_fulldata, processed_postpositions):
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
                        elif isinstance(constant.discourse_dict[element], list):
                            for i in range(len(constant.discourse_dict[element])):
                                
                                if data_values=='samuccaya':
                                    if 'BI_1' in spkview_data :
                                        # print(output_list1[0],'outpput_list')
                                        POST_PROCESS_OUTPUT = 'balki '+ POST_PROCESS_OUTPUT
                                        # output_list1[-1]='ना केवल '+ output_list1[-1]
                                        # print(output_list1[1],'outpput_list')
                                        break
                                    else:
                                        POST_PROCESS_OUTPUT = constant.discourse_dict[element][i]+ '/'+ POST_PROCESS_OUTPUT
                                        
                                elif i!=0:
                                    POST_PROCESS_OUTPUT = constant.discourse_dict[element][i]+ '/'+ POST_PROCESS_OUTPUT
                                else:
                                    POST_PROCESS_OUTPUT = constant.discourse_dict[element][i] + " " + POST_PROCESS_OUTPUT
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

def add_adj_to_noun_attribute(key, value):
    if key is not None:
        if key in constant.noun_attribute:
            constant.noun_attribute[key][0].append(value)
        else:
            constant.noun_attribute[key] = [[],[]]

def add_verb_to_noun_attribute(key, value):
    if key is not None:
        if key in constant.noun_attribute:
            constant.noun_attribute[key][1].append(value)
        else:
            constant.noun_attribute[key] = [[], []]

def add_spkview(full_data, spkview_dict):
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
    return transformed_data

def add_MORPHO_SEMANTIC(full_data, MORPHO_SEMANTIC_DICT):
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
    return transformed_data

def add_construction(transformed_data, construction_dict):
    Constructdata = []
    dependency_check=['k7p','k7t']
    add_words_list=['meM','ko','ke','kI','kA']
    depend_data1=''
    for data in transformed_data:
        index = data[0]
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