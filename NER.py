import spacy

# Load the spaCy English NER model
nlp = spacy.load("en_core_web_sm")

# Function to extract a specified number of entities (3: person, org, others)
def extract_entities_3(text):
    doc = nlp(text)
    entities = {
        "PERSON": [],
        "ORG": [],
        "OTHERS": []
    }
    for ent in doc.ents:
        label = ent.label_
        entity = ent.text
        if label == "PERSON":
            entities["PERSON"].append(entity)
        elif label == "ORG":
            entities["ORG"].append(entity)
        else:
            entities["OTHERS"].append(entity)
    return entities

# Function to extract a specified number of entities (4: person, org, loc, others)
def extract_entities_4(text):
    doc = nlp(text)
    entities = {
        "PERSON": [],
        "ORG": [],
        "LOC": [],
        "OTHERS": []
    }
    for ent in doc.ents:
        label = ent.label_
        entity = ent.text
        if label == "PERSON":
            entities["PERSON"].append(entity)
        elif label == "ORG":
            entities["ORG"].append(entity)
        elif label == "GPE":
            entities["LOC"].append(entity)
        else:
            entities["OTHERS"].append(entity)
    return entities

# Function to extract a specified number of entities (7: person, org, loc, date, time, money, others)
def extract_entities_7(text):
    doc = nlp(text)
    entities = {
        "PERSON": [],
        "ORG": [],
        "LOC": [],
        "DATE": [],
        "TIME": [],
        "MONEY": [],
        "OTHERS": []
    }
    for ent in doc.ents:
        label = ent.label_
        entity = ent.text
        if label == "PERSON":
            entities["PERSON"].append(entity)
        elif label == "ORG":
            entities["ORG"].append(entity)
        elif label == "GPE":
            entities["LOC"].append(entity)
        elif label == "DATE":
            entities["DATE"].append(entity)
        elif label == "TIME":
            entities["TIME"].append(entity)
        elif label == "MONEY":
            entities["MONEY"].append(entity)
        else:
            entities["OTHERS"].append(entity)
    return entities

# Example text
text = '''Anser worked at Princeton University. 
       Apple Inc. is headquartered in Cupertino, California. 
       The Eiffel Tower is located in Paris, France.  
       The meeting is scheduled for 2:30 PM on May 15, 2023. 
       The cost of the ticket is $50.'''


#create input function asking for how mnay entities required
input = int(input("How many entities do you want to extract?\nType:\n1 for 3 entities\n2 for 4 entities\n3 for 7 entities\n"
"Enter your choice: "))

if input == 1:
    entities = extract_entities_3(text)
    # Print lists in dict one by one
    for key, value in entities.items():
        print()
        print(f"{key}:")
        for item in value:
            print(item)
        print()

elif input == 2:
    entities = extract_entities_4(text)
    for key, value in entities.items():
        print()
        print(f"{key}:")
        for item in value:
            print(item)
        print()
elif input == 3:
    entities = extract_entities_7(text)
    for key, value in entities.items():
        print()
        print(f"{key}:")
        for item in value:
            print(item)
        print()


