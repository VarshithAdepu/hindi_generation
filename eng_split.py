import re

# Sample text
text = """
Ram has gone to the school.
Radha is going to market but Mohan is sleeping.
He saw the movie and Mohan went to market.
Aakash is going to home today but I will stay.
Having gone to the school Ram and Sita saw a bus.
Ravi and Rohan are best friends but they don't live together.
If she will go then I will not come.
She and her sister had fever yesterday.
He will have lunch but Sita will not eat.
"""

# Function to split text into sentences
def split_into_sentences(text):
    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', text.strip())
    return [sentence.strip() for sentence in sentences if sentence]

# Function to determine TAM characteristics
def determine_tam(sentence):
    words = sentence.lower().split()
    tense = "Present"
    aspect = "Simple"
    mood = "Indicative"
    
    # Check for tense indicators
    if any(word in words for word in ["was", "were", "did", "had"]):
        tense = "Past"
    elif any(word in words for word in ["will", "shall"]):
        tense = "Future"
    
    # Check for aspect indicators
    if any(word in words for word in ["being"]):
        aspect = "Progressive"
    elif any(word in words for word in ["have", "has", "had"]):
        aspect = "Perfect"
        if any(word in words for word in ["being"]):
            aspect = "Perfect Progressive"
    
    # Check for mood indicators
    if sentence.lower().startswith("please") or sentence.endswith("!"):
        mood = "Imperative"
    elif "if" in words:
        mood = "Conditional"
    elif any(word in words for word in ["would", "could"]):
        mood = "Conditional"
    
    return tense, aspect, mood

# Function to split sentences into clauses based on TAM and connectives
def split_based_on_tam_and_connectives(sentence):
    connectives = ["but", "and", "or", "if", "then"]
    clauses = []
    
    # Find all positions of connectives in the sentence
    split_positions = [m.start() for m in re.finditer(r'\b(' + '|'.join(connectives) + r')\b', sentence)]
    
    # Add end of the sentence as a split position
    split_positions.append(len(sentence))
    
    # Avoid splitting if the connective is part of the clause
    prev_pos = 0
    for pos in split_positions:
        clause = sentence[prev_pos:pos].strip()
        if clause:
            tense, aspect, mood = determine_tam(clause)
            clauses.append({
                "text": clause,
                "tense": tense,
                "aspect": aspect,
                "mood": mood
            })
        prev_pos = pos + 1
    
    # Handle cases where conjunctions may not indicate a split
    refined_clauses = []
    for clause in clauses:
        # Combine clauses that should be together
        if refined_clauses and clause['text'].lower().startswith("and "):
            refined_clauses[-1]['text'] += " " + clause['text']
            refined_clauses[-1]['tense'] = determine_tam(refined_clauses[-1]['text'])[0]
            refined_clauses[-1]['aspect'] = determine_tam(refined_clauses[-1]['text'])[1]
            refined_clauses[-1]['mood'] = determine_tam(refined_clauses[-1]['text'])[2]
        else:
            refined_clauses.append(clause)
    
    return refined_clauses

# Process each sentence and split based on TAM and connectives
sentences = split_into_sentences(text)
for sentence in sentences:
    print(f"Sentence: '{sentence}'")
    clauses = split_based_on_tam_and_connectives(sentence)
    for i, clause in enumerate(clauses, start=1):
        print(f"Clause {i}: '{clause['text']}'")
        print(f"  Tense: {clause['tense']}, Aspect: {clause['aspect']}, Mood: {clause['mood']}")
    print()
