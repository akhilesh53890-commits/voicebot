import random

# Emergency Symptoms (Red Flags)
EMERGENCY_SYMPTOMS = [
    "chest pain", "shortness of breath", "difficulty breathing", "severe bleeding", 
    "unconscious", "fainting", "severe head injury", "stroke symptoms", "heart attack",
    "severe allergic reaction", "anaphylaxis", "coughing blood", "severe burns"
]

# Knowledge Base
KNOWLEDGE_BASE = {
    "headache": {
        "conditions": ["Tension Headache", "Migraine", "Dehydration", "Sinusitis"],
        "otc_meds": ["Paracetamol (Acetaminophen) - 500mg as per label", "Ibuprofen - 400mg with food (if not allergic)"],
        "first_aid": "Rest in a dark, quiet room. Drink plenty of water. Apply a cold or warm compress to the forehead.",
        "doctor_advice": "If headache is sudden, severe ('thunderclap'), or accompanied by stiff neck, fever, or vision changes."
    },
    "fever": {
        "conditions": ["Viral Infection (Flu/Cold)", "Bacterial Infection", "Heat Exhaustion"],
        "otc_meds": ["Paracetamol - 500mg every 4-6 hours (max 4g/day)", "Ibuprofen - as per label instructions"],
        "first_aid": "Stay hydrated with water or ORS. Rest. Wear light clothing. Use tepid sponging if fever is high.",
        "doctor_advice": "If temperature > 103°F (39.4°C), lasts more than 3 days, or accompanied by rash, stiff neck, or difficulty breathing."
    },
    "cough": {
        "conditions": ["Common Cold", "Bronchitis", "Allergies", "Post-nasal Drip"],
        "otc_meds": ["Cough Syrup (Dextromethorphan for dry cough, Guaifenesin for wet cough)", "Honey and warm water (natural remedy)"],
        "first_aid": "Drink warm fluids. Inhale steam. Gargle with warm salt water. Avoid smoke and irritants.",
        "doctor_advice": "If cough lasts > 3 weeks, produces blood, or causes difficulty breathing."
    },
    "sore throat": {
        "conditions": ["Pharyngitis (Viral)", "Strep Throat", "Tonsillitis"],
        "otc_meds": ["Throat Lozenges", "Paracetamol for pain relief", "Saline gargle"],
        "first_aid": "Gargle with warm salt water. Drink warm liquids (tea with honey). Stay hydrated.",
        "doctor_advice": "If severe pain, difficulty swallowing, high fever, or white patches on tonsils."
    },
    "stomach ache": {
        "conditions": ["Indigestion", "Gastritis", "Food Poisoning", "IBS"],
        "otc_meds": ["Antacids (e.g., Tums, Rolaids) for heartburn", "Simethicone for gas"],
        "first_aid": "Avoid solid food for a few hours. Sip clear fluids or water. Avoid dairy, spicy, or fatty foods.",
        "doctor_advice": "If pain is severe, localized to lower right abdomen (appendicitis risk), or accompanied by vomiting blood or bloody stool."
    },
    "nausea": {
        "conditions": ["Food Poisoning", "Viral Gastroenteritis", "Motion Sickness", "Indigestion"],
        "otc_meds": ["ORS (Oral Rehydration Solution) to prevent dehydration", "Bismuth Subsalicylate (Pepto-Bismol)"],
        "first_aid": "Drink small sips of clear fluids (water, ginger ale). Eat bland foods (crackers, toast) when ready.",
        "doctor_advice": "If unable to keep fluids down for 24 hours, signs of dehydration, or severe abdominal pain."
    },
     "cold": {
        "conditions": ["Common Cold", "Seasonal Allergies", "Sinusitis"],
        "otc_meds": ["Antihistamines (e.g., Cetirizine, Loratadine) for runny nose", "Decongestants (e.g., Pseudoephedrine) - use with caution"],
        "first_aid": "Rest. Drink plenty of fluids. Use a humidifier. Saline nasal spray.",
        "doctor_advice": "If symptoms last > 10 days or worsen, or if high fever develops."
    },
    "rash": {
        "conditions": ["Contact Dermatitis", "Allergic Reaction", "Eczema", "Insect Bite"],
        "otc_meds": ["Antihistamines (Oral)", "Calamine Lotion", "Hydrocortisone Cream (1%)"],
        "first_aid": "Wash area with mild soap and water. Avoid scratching. Apply cool compress.",
        "doctor_advice": "If rash spreads rapidly, is painful, infected, or accompanied by fever/swelling (signs of anaphylaxis)."
    }
}

SAFETY_WARNING = "\n\n⚠️ **This is an AI-generated medical suggestion. Please consult a certified doctor for accurate diagnosis.**"

def get_medical_advice(symptoms):
    """
    Generates a strictly formatted medical advice string based on symptoms.
    """
    if not symptoms:
        return "I couldn't detect any specific symptoms. Please describe how you are feeling."

    # 1. Check for Emergency Symptoms
    urgent_symptoms = [s for s in symptoms if s in EMERGENCY_SYMPTOMS]
    if urgent_symptoms:
        return (
            f"🚨 **EMERGENCY DETECTED** 🚨\n\n"
            f"You mentioned: **{', '.join(urgent_symptoms)}**.\n"
            f"These are signs of a potential medical emergency.\n\n"
            f"**Action Required:**\n"
            f"1. Call emergency services immediately (911 or local equivalent).\n"
            f"2. Go to the nearest Emergency Room.\n"
            f"3. Do not drive yourself if possible.\n"
            f"{SAFETY_WARNING}"
        )

    # 2. Analyze Symptoms (Take the primary/first one for simplicity in this demo)
    # In a real app, we would aggregate advice for all symptoms.
    primary_symptom = None
    for s in symptoms:
        if s in KNOWLEDGE_BASE:
            primary_symptom = s
            break
    
    if not primary_symptom:
        return (
            f"**1. Detected Symptoms**\n{', '.join(symptoms)}\n\n"
            f"**2. Possible Conditions**\nUnclear based on my current knowledge.\n\n"
            f"**3. Safe OTC Medicines**\nNone recommended without clearer symptoms.\n\n"
            f"**4. First-Aid Advice**\nMonitor your symptoms. Stay hydrated and rest.\n\n"
            f"**5. When to See a Real Doctor**\nIf you feel unwell or symptoms persist.\n"
            f"{SAFETY_WARNING}"
        )

    data = KNOWLEDGE_BASE[primary_symptom]
    
    response = (
        f"**1. Detected Symptoms**\n{', '.join(symptoms)}\n\n"
        f"**2. Possible Conditions (not a diagnosis)**\n{', '.join(data['conditions'])}\n\n"
        f"**3. Safe OTC Medicines**\n" + "\n".join([f"• {med}" for med in data['otc_meds']]) + "\n\n"
        f"**4. First-Aid Advice**\n{data['first_aid']}\n\n"
        f"**5. When to See a Real Doctor**\n{data['doctor_advice']}\n"
        f"{SAFETY_WARNING}"
    )
    
    return response

def book_appointment(condition):
    """
    Simulates booking an appointment.
    """
    doctors = ["Dr. Smith", "Dr. Jones", "Dr. Emily"]
    times = ["10:00 AM", "2:00 PM", "4:30 PM"]
    
    doctor = random.choice(doctors)
    time = random.choice(times)
    
    return f"I have booked an appointment for {condition} with {doctor} at {time} tomorrow."
