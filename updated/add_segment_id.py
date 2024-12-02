# def wrap_segments(input_data):
#     segment_id = 1
#     output_data = ""
#     segment_lines = []

#     # Split the input data by line
#     lines = input_data.splitlines()

#     for line in lines:
#         # Check if the line starts with '#' which indicates a new segment
#         if line.startswith('#'):
#             # If there are existing lines for the previous segment, wrap them with segment tags
#             if segment_lines:
#                 output_data += f"<segment_id= {segment_id:03}>\n"
#                 output_data += "\n".join(segment_lines) + "\n"
#                 output_data += f"</segment_id>\n"
#                 segment_id += 1
#                 segment_lines = []

#         # Add current line to the segment
#         segment_lines.append(line)

#     # Add the last segment if any
#     if segment_lines:
#         output_data += f"<segment_id= {segment_id:03}>\n"
#         output_data += "\n".join(segment_lines) + "\n"
#         output_data += f"</segment_id>\n"

#     return output_data


# Input data
input_data =[{"segment_id": "Geo_nios_2ch_0034", "text": "यह *घनट्त 11.0 से अधिक भी है।"}, 
             {"segment_id": "Geo_nios_2ch_0027b", "text": "वह *वेधन में #प्रयोग #कर #कोई #प्रकार का #यंत्र पिघला सकता है।"}, 
             {"segment_id": "Geo_nios_2ch_0010", "text": "यह #दोनों #प्रक्रिया ही #शैल के #टूट फुट और #नई *स्थलाकृति के निर्माण के लिये जिम्मेदार है।"}, 
             {"segment_id": "Geo_nios_2ch_0038", "text": "इसकी भीतरी परत ठोस है जो (ठोस) चित्र #सी से दिखाई गई है।"}, 
             {"segment_id": "Geo_nios_2ch_0023", "text": "इस पाठ के #अध्ययन #कर आप #मृदा #निर्माण के लिये #सहायक #विभिन्न कारक व्याख्या कर सकोगे *चोम्पोउन्ड् के लिये।"}, 
             {"segment_id": "Geo_nios_2ch_0024c", "text": "तथा/एवं/और #यह *भूगर्भीय पदार्थों का #बनावट गहराई #बढ बदलती जाती है।"}, 
             {"segment_id": "Geo_nios_2ch_0016", "text": "इस #पाठ के अध्ययन #कर आप #शैल और खनिज में *अन्तर कर सकोगे।"}, 
             {"segment_id": "Geo_nios_2ch_0018", "text": "इस पाठ के #अध्ययन करने के बाद आप #शैल का आर्थिक *महत्व बता सकोगे।"}, 
             {"segment_id": "Geo_nios_2ch_0001", "text": "संभवतः पृथ्वी ही पूरे ब्रह्मांड का एक इस प्रकार का ज्ञात ग्रह है *जहाँ (पृथ्वी) विकसित जीवन पाया जाता है।"}, 
             {"segment_id": "Geo_nios_2ch_0013", "text": "हम अपक्षय, #यह (अपक्षय) #प्रकार, #तल के संतुलन के प्रक्रिया, मृदा के निर्माण और #यह (निर्माण) *महत्व के विषय में अध्ययन करेंगे *चोम्पोउन्ड् के के।"}, 
             {"segment_id": "Geo_nios_2ch_0048", "text": "*स्थलमण्डल का #ऊपरी #भागना *भूपर्पटी कहता है।"}, 
             {"segment_id": "Geo_nios_2ch_0008c", "text": "जो #शैल #विखंडित करता है।"}, 
             {"segment_id": "Geo_nios_2ch_0006b", "text": "*स्थलाकृति का *स्वरूप सदैव नहीं रहता है।"}, 
             {"segment_id": "Geo_nios_2ch_0020", "text": "इस पाठ के #अध्ययन #कर आप #धरातल का *स्वऊप #बदल #तल *स्Mतुलन का #विभिन्न #प्रक्रिया *व्याख्य कर सकोगे *चोम्पोउन्ड् का।"}, 
             {"segment_id": "Geo_nios_2ch_0019b", "text": "तथा/एवं/और आप उपयुक्त उदाहरण से इनके प्रकार वर्णन कर सकोगे।"}, 
             {"segment_id": "Geo_nios_2ch_0008b", "text": "invalid literal for int() with base 10: ''"}, 
             {"segment_id": "Geo_nios_2ch_0022", "text": "invalid literal for int() with base 10: ''"}, 
             {"segment_id": "Geo_nios_2ch_0042", "text": "बल्कि यह #परत #सीमा भी *सिलीका *मैगनीशियम कहता है।"}, 
             {"segment_id": "Geo_nios_2ch_0028", "text": "इस कारण/इसी कारण/इसके परिणामस्वरूप/अतः/इसलिए/इसीलिए *वेधन कार्य कम गहराई पर ही #सीमित है *चोम्पोउन्ड्।"}, 
             {"segment_id": "Geo_nios_2ch_0051", "text": "यह पृथ्वी का सबसे #अधिक घनत्व वाली परत है।"}, 
             {"segment_id": "Geo_nios_2ch_0012", "text": "इस पाठ में हम #पृथ्वी का #भूगर्भ और #यह (भूगर्भ) *उपरी #भाग भू *पर्पटी का पदार्थ अध्ययन करेंगे *चोम्पोउन्ड्।"}, 
             {"segment_id": "Geo_nios_2ch_0049", "text": "पृथ्वी के *आन्तरिक #भाग का 3 #प्रमुख *संकेन्द्रीय परत है #क्रोड, *मैंटल और *स्थलमंडल।"}, 
             {"segment_id": "Geo_nios_2ch_0004a", "text": "इस कारण/इसी कारण/इसके परिणामस्वरूप/अतः/इसलिए/इसीलिए यह स्पष्ट होता है।"}, {"segment_id": "Geo_nios_2ch_0037", "text": "हम क्रोड पुनः 2 परतों में बाँट सकते हैं।"}, {"segment_id": "Geo_nios_2ch_0047", "text": "बल्कि यह #परत *स्याल भी *सिलैका *एल्यूमैनियम कहता है।"}, {"segment_id": "Geo_nios_2ch_0050", "text": "क्रोड सबसे *आन्तरिक परत है।"}, {"segment_id": "Geo_nios_2ch_0033", "text": "यह सबसे अधिक #घनत्व वाली परत है।"}, {"segment_id": "Geo_nios_2ch_0045", "text": "यह *स्थलमण्डल कहता है जिसका (स्थलमण्डल) घनत्व 2.75 2.90 है।"}, {"segment_id": "Geo_nios_2ch_0046", "text": "*स्थलमण्डल का #प्रमुख *निर्माणकारी *तत्व *सिलीका चि *एल्यूमीनियम एल है।"}, {"segment_id": "Geo_nios_2ch_0006a", "text": "local variable 'verb' referenced before assignment"}, {"segment_id": "Geo_nios_2ch_0003a", "text": "local variable 'verb' referenced before assignment"}, {"segment_id": "Geo_nios_2ch_0009", "text": "दूसरी #प्रकार का शक्ति *टूटाफूटा #शैल ऊँचे भू हटाकर #नीचे के #भू #जमा करतीं रहतीं हैं *चोम्पोउन्ड् से *चोम्पोउन्ड् पर।"}, {"segment_id": "Geo_nios_2ch_0015", "text": "इस #पाठ के अध्ययन #कर आप #भूगर्भ का #विभिन्न परतें #यह (परत) मोटाई, #तापमान, घनत्व और दबाव के संदर्भ में #तुलना कर सकोगे के।"}, {"segment_id": "Geo_nios_2ch_0040", "text": "#जिस परत क्रोड है यह (है) *मैंटल कहती है।"}, {"segment_id": "Geo_nios_2ch_0043", "text": "इसका घनत्व 3.1 5.1 है।"}, {"segment_id": "Geo_nios_2ch_0036", "text": "invalid literal for int() with base 10: ''"}, {"segment_id": "Geo_nios_2ch_0035", "text": "यह *लोहा धातुओं और *निकिल धातुओं से बना है।"}, {"segment_id": "Geo_nios_2ch_0044", "text": "*मैंटल पृथ्वी के सबसे ऊपरी परत से घिरा है।"}, {"segment_id": "Geo_nios_2ch_0005", "text": "संसार में खनन कार्य 5 किलोमीटर कम गहराई पर ही #सीमित है *मेअस् से कम भी।"}, {"segment_id": "Geo_nios_2ch_0024a", "text": "#पृथ्वी का *आन्तरिक #भागना प्रत्यक्ष रूप #देख नहीं *सम्भव है।"}, {"segment_id": "Geo_nios_2ch_0002", "text": "अन्य आकाशीय *पिण्ड जैसी पृथ्वी का आकृति भी है गोलाकार।"}, {"segment_id": "Geo_nios_2ch_0011", "text": "#मैं *अत्यंत महत्वपूर्ण मृदा भी एकसीमातक इस प्रक्रियाओं से निर्माण होता है।"}, {"segment_id": "Geo_nios_2ch_0025", "text": "invalid literal for int() with base 10: ''"}, {"segment_id": "Geo_nios_2ch_0026", "text": "invalid literal for int() with base 10: ''"}, {"segment_id": "Geo_nios_2ch_0007", "text": "उसका रूप लगातर बदलता रहता है।"}, {"segment_id": "Geo_nios_2ch_0017", "text": "इस #पाठ के *अद्ययन #कर आप #रचना के आधार में #शैल *वर्गीकरण् कर सकोगे।"}, {"segment_id": "Geo_nios_2ch_0024b", "text": "चूंकि/चूँकि/क्योंकि यह बहुत बडा गोला है।"}, {"segment_id": "Geo_nios_2ch_0014", "text": "इस #पाठ के अध्ययन कर का आप #पृथ्वी के *आन्तरिक भाग या #भूगर्भ के संबंध में प्रत्यक्षरूप से प्रेक्षण #कर का सीमाएँ समझा सकोगे के।"}, {"segment_id": "Geo_nios_2ch_0004b", "text": "धरातल #नीचे पर तापमान बहुत ऊँचा है।"}, {"segment_id": "Geo_nios_2ch_0030", "text": "पृथ्वी के विशाल #आकार और *गइराई के साथ #बढ तापमान ने भूगर्भ के प्रत्यक्ष जानकारी का सीमाएँ निश्चित कीं हैं।"}, {"segment_id": "Geo_nios_2ch_0029", "text": "पृथ्वी के गर्भ के विषय में प्रत्यक्ष जानकारी मिल में कई कठिनाइयाँ आतीं हैं।"}, {"segment_id": "Geo_nios_2ch_0003b", "text": "*स्त्रोत्र से गर्म #जल और ज्वालामुखियों से *अत्यंत गर्म लावी पृथ्वी के #भीतरी भागों से निकलकर धरातल पर *पहुंच है।"}, {"segment_id": "Geo_nios_2ch_0032", "text": "#पृथ्वी का सबसे अधिक #गहराई वाली परत क्रोड कहता है।"}, {"segment_id": "Geo_nios_2ch_0031", "text": "invalid literal for int() with base 10: ''"}, {"segment_id": "Geo_nios_2ch_0021", "text": "इस #पाठ के अध्ययन #कर आप *निम्नीकरण और *अधिवृद्धि में *अन्तर कर सकोगे।"}, {"segment_id": "Geo_nios_2ch_0008b", "text": "invalid literal for int() with base 10: ''"}, {"segment_id": "Geo_nios_2ch_0027a", "text": "भूगर्भ पर अधिक ऊँचा तापमान है।"}, {"segment_id": "Geo_nios_2ch_0008a", "text": "बाह्य शक्ति के एक समूह में वह शक्ति *सम्मलित हैं।"}, {"segment_id": "Geo_nios_2ch_0019a", "text": "इस पाठ के अध्ययन #कर आप #अपक्षय शब्द व्याख्या कर सकोगे।"}, {"segment_id": "Geo_nios_2ch_0039", "text": "दूसरा #परत अर्द्ध #तरल है जो (है) चित्र #सी से दिखाया गया है।"}, {"segment_id": "Geo_nios_2ch_0041", "text": "यह #परत मुख्यतः *सिलीक और *मैगनीशियम से बना है।"}
             ]
             
# Loop through the list and print each dictionary in the desired format
for item in input_data:
    # print(f'segment_id: "{item["segment_id"]}", text: "{item["text"]}"')
    print(f'text: "{item["text"]}"')

# output_data = wrap_segments(input_data)

# Output the result
# print(output_data)
