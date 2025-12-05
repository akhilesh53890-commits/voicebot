import voice_interface as vi
import medical_ner as ner
import symptom_checker as sc
import time

def main():
    vi.speak("Hello! I am your healthcare assistant. Please describe your symptoms.")
    
    # 1. Listen to user
    user_input = vi.listen()
    
    if not user_input:
        vi.speak("I didn't hear anything. Please try again.")
        return

    # 2. Extract entities
    symptoms = ner.extract_symptoms(user_input)
    
    if not symptoms:
        vi.speak("I couldn't detect any specific symptoms. Could you please describe them differently?")
        return
    
    vi.speak(f"I understood that you are experiencing: {', '.join(symptoms)}.")
    
    # 3. Check symptoms
    condition, first_aid = sc.check_symptoms(symptoms)
    
    if condition:
        vi.speak(f"Based on your symptoms, it looks like you might have: {condition}.")
        vi.speak(f"Here is some first aid advice: {first_aid}")
        
        # 4. Book appointment
        vi.speak("Would you like me to book an appointment with a doctor? Say yes or no.")
        response = vi.listen()
        
        if response and "yes" in response.lower():
            booking_info = sc.book_appointment(condition)
            vi.speak(booking_info)
        else:
            vi.speak("Okay, take care and get well soon!")
            
    else:
        vi.speak("I'm not sure what condition that might be. Please consult a doctor.")

if __name__ == "__main__":
    main()
