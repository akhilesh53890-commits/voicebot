import medical_ner as ner
import symptom_checker as sc

def test_logic():
    print("--- Testing Logic ---")
    
    # Test Case 1: Headache
    text1 = "I have a severe headache and I feel dizzy."
    print(f"\nInput: {text1}")
    symptoms1 = ner.extract_symptoms(text1)
    print(f"Extracted Symptoms: {symptoms1}")
    condition1, first_aid1 = sc.check_symptoms(symptoms1)
    print(f"Condition: {condition1}")
    print(f"First Aid: {first_aid1}")
    
    # Test Case 2: Fever and Cough
    text2 = "My daughter has a high fever and a bad cough."
    print(f"\nInput: {text2}")
    symptoms2 = ner.extract_symptoms(text2)
    print(f"Extracted Symptoms: {symptoms2}")
    condition2, first_aid2 = sc.check_symptoms(symptoms2)
    print(f"Condition: {condition2}")
    print(f"First Aid: {first_aid2}")
    
    # Test Case 3: Unknown
    text3 = "I feel weird."
    print(f"\nInput: {text3}")
    symptoms3 = ner.extract_symptoms(text3)
    print(f"Extracted Symptoms: {symptoms3}")
    condition3, first_aid3 = sc.check_symptoms(symptoms3)
    print(f"Condition: {condition3}")
    print(f"First Aid: {first_aid3}")

    # Test Case 4: Booking
    print(f"\nBooking Appointment for {condition1}...")
    booking = sc.book_appointment(condition1)
    print(booking)

if __name__ == "__main__":
    test_logic()
