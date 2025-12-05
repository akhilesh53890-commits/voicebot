from flask import Flask, render_template, request, jsonify
import medical_ner as ner
import symptom_checker as sc

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/process', methods=['POST'])
def process_input():
    data = request.json
    user_text = data.get('text', '')
    
    if not user_text:
        return jsonify({'response_text': "I didn't hear anything. Please try again."})

    # 1. Extract entities
    symptoms = ner.extract_symptoms(user_text)
    
    # 2. Get Medical Advice (Strict Format)
    response_text = sc.get_medical_advice(symptoms)
    
    # Check if we should prompt for booking (only if not emergency and symptoms found)
    booking_prompt = False
    if symptoms and "EMERGENCY DETECTED" not in response_text:
         booking_prompt = True

    return jsonify({
        'response_text': response_text,
        'symptoms': symptoms,
        'booking_prompt': booking_prompt
    })

@app.route('/api/book', methods=['POST'])
def book_appointment():
    data = request.json
    condition = data.get('condition')
    
    if condition:
        booking_info = sc.book_appointment(condition)
        return jsonify({'response_text': booking_info})
    else:
        return jsonify({'response_text': "I couldn't book an appointment as the condition is unclear."})

if __name__ == '__main__':
    app.run(debug=True)
