import spacy
from spacy.pipeline import EntityRuler

# Load the small English model
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print("Downloading 'en_core_web_sm' model...")
    from spacy.cli import download
    download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

# Add a custom entity ruler for symptoms
# This ensures we catch specific medical terms even if the general model misses them
ruler = nlp.add_pipe("entity_ruler", before="ner")
patterns = [
    {"label": "SYMPTOM", "pattern": "headache"},
    {"label": "SYMPTOM", "pattern": "fever"},
    {"label": "SYMPTOM", "pattern": "cough"},
    {"label": "SYMPTOM", "pattern": "cold"},
    {"label": "SYMPTOM", "pattern": "sore throat"},
    {"label": "SYMPTOM", "pattern": "stomach ache"},
    {"label": "SYMPTOM", "pattern": "nausea"},
    {"label": "SYMPTOM", "pattern": "dizzy"},
    {"label": "SYMPTOM", "pattern": "fatigue"},
    {"label": "SYMPTOM", "pattern": "rash"},
    {"label": "SYMPTOM", "pattern": "chest pain"},
    {"label": "SYMPTOM", "pattern": "shortness of breath"},
    {"label": "SYMPTOM", "pattern": "vomiting"},
    {"label": "SYMPTOM", "pattern": "diarrhea"}
]
ruler.add_patterns(patterns)

def extract_symptoms(text):
    """Extracts symptom entities from the given text."""
    doc = nlp(text.lower())
    symptoms = []
    for ent in doc.ents:
        if ent.label_ == "SYMPTOM":
            symptoms.append(ent.text)
    
    # Fallback: check for keywords if no entities found (simple matching)
    if not symptoms:
        for pattern in patterns:
            if pattern["pattern"] in text.lower():
                symptoms.append(pattern["pattern"])
                
    return list(set(symptoms)) # Return unique symptoms
