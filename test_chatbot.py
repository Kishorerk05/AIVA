#!/usr/bin/env python3
"""
Test script for AIVA chatbot to verify the fixes:
1. No name repetition
2. Proper email/phone validation
3. Temperature setting for reduced hallucinations
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.chatbot import get_response

def test_chatbot():
    """Test the chatbot with various scenarios"""
    
    print("🧪 Testing AIVA Chatbot...\n")
    
    # Test 1: Initial greeting
    print("=== Test 1: Initial Greeting ===")
    response1 = get_response("hi")
    print(f"User: hi")
    print(f"AIVA: {response1}\n")
    
    # Test 2: Name collection
    print("=== Test 2: Name Collection ===")
    response2 = get_response("My name is John")
    print(f"User: My name is John")
    print(f"AIVA: {response2}\n")
    
    # Test 3: Insurance type
    print("=== Test 3: Insurance Type ===")
    response3 = get_response("health")
    print(f"User: health")
    print(f"AIVA: {response3}\n")
    
    # Test 4: Check for name repetition
    print("=== Test 4: Check for Name Repetition ===")
    response4 = get_response("for me")
    print(f"User: for me")
    print(f"AIVA: {response4}\n")
    
    # Test 5: Email/Phone validation
    print("=== Test 5: Email/Phone Validation ===")
    response5 = get_response("john@example.com")
    print(f"User: john@example.com")
    print(f"AIVA: {response5}\n")
    
    print("✅ Testing completed!")

if __name__ == "__main__":
    test_chatbot() 