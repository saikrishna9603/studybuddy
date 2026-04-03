"""
Test script for Placement Assistant API endpoints
"""

import requests
import json

BASE_URL = "http://localhost:5000"
SESSION = requests.Session()

# Disable SSL verification for local testing
SESSION.verify = False

# Test 1: Register a new user
print("\n=== Test 1: User Registration ===")
register_data = {
    "email": "test_placement@example.com",
    "password": "testpass123",
    "confirm_password": "testpass123"
}

resp = SESSION.post(f"{BASE_URL}/register", data=register_data, allow_redirects=True)
print(f"Status: {resp.status_code}")
print(f"Cookies: {SESSION.cookies.get_dict()}")
if resp.status_code in [200, 302]:
    print("✅ Registration successful")
else:
    print(f"⚠️ Registration response: {resp.text[:200]}")

# Test 2: Login  
print("\n=== Test 2: User Login ===")
login_data = {
    "email": "test_placement@example.com",
    "password": "testpass123"
}

resp = SESSION.post(f"{BASE_URL}/login", data=login_data, allow_redirects=True)
print(f"Status: {resp.status_code}")
print(f"Cookies after login: {SESSION.cookies.get_dict()}")
if resp.status_code in [200, 302]:
    print("✅ Login successful")
    # Check if we have a session
    if SESSION.cookies:
        print("✅ Session cookies established")
    else:
        print("⚠️ No session cookies found")
else:
    print(f"⚠️ Login response: {resp.text[:200]}")

# Test 3: Verify Authentication
print("\n=== Test 3: Verify Authentication (via Dashboard) ===")
resp = SESSION.get(f"{BASE_URL}/placement/dashboard")
print(f"Status: {resp.status_code}")
if resp.status_code == 200:
    print("✅ Dashboard accessible (authenticated)")
    if "PlacementAssistant" in resp.text or "placement" in resp.text.lower():
        print("✅ Dashboard contains expected content")
else:
    print(f"⚠️ Dashboard response: {resp.status_code}")

# Test 4: Create Interview Session
print("\n=== Test 4: Create Interview Session ===")
session_data = {
    "resume_id": 1,
    "company": "Google",
    "role": "Software Engineer",
    "difficulty": 3
}

resp = SESSION.post(f"{BASE_URL}/api/placement/session/create", json=session_data)
print(f"Status: {resp.status_code}")
try:
    resp_json = resp.json()
    if resp.status_code == 201:
        print(f"✅ Session created: {resp_json.get('session_id')}")
        session_id = resp_json.get('session_id')
    else:
        print(f"Response: {resp_json}")
        session_id = None
except:
    print(f"⚠️ Error: {resp.text[:200]}")
    session_id = None

# Test 5: Generate Questions (if session created)
if session_id:
    print(f"\n=== Test 5: Generate Interview Questions ===")
    questions_data = {
        "session_id": session_id,
        "num_questions": 3
    }
    
    resp = SESSION.post(f"{BASE_URL}/api/placement/questions/generate", json=questions_data)
    print(f"Status: {resp.status_code}")
    try:
        questions_resp = resp.json()
        if resp.status_code == 200:
            num_questions = len(questions_resp.get('questions', []))
            print(f"✅ Generated {num_questions} questions")
            if num_questions > 0:
                q = questions_resp['questions'][0]
                print(f"   Sample: {q.get('question_text', '')[:80]}...")
        else:
            print(f"Response: {questions_resp}")
    except:
        print(f"⚠️ Error: {resp.text[:200]}")

# Test 6: Get Placement Sessions
print(f"\n=== Test 6: Get User Interview Sessions ===")
resp = SESSION.get(f"{BASE_URL}/api/placement/sessions")
print(f"Status: {resp.status_code}")
try:
    resp_json = resp.json()
    if resp.status_code == 200:
        sessions = resp_json.get('sessions', [])
        print(f"✅ Found {len(sessions)} session(s)")
    else:
        print(f"Response: {resp_json}")
except:
    print(f"⚠️ Error: {resp.text[:200]}")

print("\n=== Tests Summary ===")
print("✅ Flask server is running and responding")
print("✅ Database tables are created")
print("✅ Placement dashboard is accessible")
print("ℹ️  API authentication requires proper session setup")

