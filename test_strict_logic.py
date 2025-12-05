import symptom_checker as sc

def test_strict_logic():
    print("--- Testing Strict Logic ---")
    
    # Test Case 1: Emergency
    print("\n[Test 1: Emergency]")
    symptoms1 = ["chest pain", "headache"]
    response1 = sc.get_medical_advice(symptoms1)
    try:
        print(response1.encode('utf-8', errors='ignore').decode('utf-8'))
    except:
        print("Response contains emojis (skipped printing for console safety)")
    assert "🚨" in response1
    assert "EMERGENCY DETECTED" in response1
    
    # Test Case 2: Common Symptom (Fever)
    print("\n[Test 2: Fever]")
    symptoms2 = ["fever"]
    response2 = sc.get_medical_advice(symptoms2)
    try:
        print(response2.encode('utf-8', errors='ignore').decode('utf-8'))
    except:
        print("Response contains emojis (skipped printing for console safety)")
    assert "**1. Detected Symptoms**" in response2
    assert "**6. Safety Warning**" in response2 or "⚠️" in response2
    assert "Paracetamol" in response2
    
    # Test Case 3: Unknown
    print("\n[Test 3: Unknown]")
    symptoms3 = ["feeling weird"]
    response3 = sc.get_medical_advice(symptoms3)
    try:
        print(response3.encode('utf-8', errors='ignore').decode('utf-8'))
    except:
        print("Response contains emojis (skipped printing for console safety)")
    assert "Safe OTC Medicines" in response3

if __name__ == "__main__":
    test_strict_logic()
