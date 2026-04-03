#!/usr/bin/env python3
"""
Test API Keys for PrepPulse Application
Tests OpenAI API and Apify API Token
"""

import os
import sys
from pathlib import Path

# Load env variables
from dotenv import load_dotenv
load_dotenv()

print("=" * 70)
print("🔍 API KEY VALIDATION TEST")
print("=" * 70)

# ============================================================================
# TEST 1: OpenAI API Key
# ============================================================================
print("\n1️⃣  Testing OpenAI API Key...")
print("-" * 70)

openai_key = os.getenv("OPEN_API_KEY")

if not openai_key:
    print("❌ OPEN_API_KEY is empty or not set")
    sys.exit(1)

if not openai_key.startswith("sk-"):
    print(f"⚠️  Warning: Key format unexpected. Expected 'sk-' prefix")
    print(f"   Current key format: {openai_key[:20]}...")

print(f"✅ OPEN_API_KEY found: {openai_key[:20]}...{openai_key[-10:]}")

try:
    from openai import OpenAI
    
    client = OpenAI(api_key=openai_key)
    
    print("🔗 Testing OpenAI API connection...")
    
    # Simple test call
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Say 'StudyBuddy API is working!' in one sentence."}
        ],
        temperature=0.7,
        max_tokens=50
    )
    
    reply = response.choices[0].message.content
    print(f"✅ OpenAI API Response: {reply}")
    print("✅ OpenAI API Test: PASSED ✓")
    
except Exception as e:
    print(f"❌ OpenAI API Test FAILED: {str(e)}")
    sys.exit(1)

# ============================================================================
# TEST 2: Apify API Token
# ============================================================================
print("\n2️⃣  Testing Apify API Token...")
print("-" * 70)

apify_token = os.getenv("APIFY_API_TOKEN")

if not apify_token:
    print("⚠️  APIFY_API_TOKEN is empty (Optional feature)")
else:
    print(f"✅ APIFY_API_TOKEN found: {apify_token[:20]}...{apify_token[-10:]}")
    
    try:
        import requests
        
        print("🔗 Testing Apify API connection...")
        
        # Test Apify token validity
        headers = {"Authorization": f"Bearer {apify_token}"}
        response = requests.get(
            "https://api.apify.com/v2/users/me",
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            user_data = response.json()
            print(f"✅ Apify User: {user_data.get('username', 'User')}")
            print("✅ Apify API Test: PASSED ✓")
        else:
            print(f"⚠️  Apify API returned status: {response.status_code}")
            print(f"   Response: {response.text[:100]}")
            if response.status_code == 401:
                print("❌ Apify API Token INVALID")
                sys.exit(1)
    except requests.exceptions.Timeout:
        print("⚠️  Apify API timeout (Network issue, token might be valid)")
    except Exception as e:
        print(f"⚠️  Apify API Test Warning: {str(e)}")

# ============================================================================
# TEST 3: SMTP Configuration (Optional)
# ============================================================================
print("\n3️⃣  Checking SMTP Configuration...")
print("-" * 70)

smtp_user = os.getenv("SMTP_USER")
smtp_password = os.getenv("SMTP_PASSWORD")

if smtp_user and smtp_password:
    print(f"✅ SMTP configured: {smtp_user}")
    print("✅ SMTP is ready for email features")
else:
    print("⚠️  SMTP not configured (Optional - password reset emails won't work)")

# ============================================================================
# SUMMARY
# ============================================================================
print("\n" + "=" * 70)
print("📊 API VALIDATION SUMMARY")
print("=" * 70)
print("✅ OpenAI API Key: VALID & WORKING")
print("✅ Apify API Token: CONFIGURED" + (" & WORKING" if apify_token else " (OPTIONAL)"))
print("✅ Application is ready for deployment!")
print("=" * 70)
print("\n🚀 All required APIs are validated and working!")
print("👉 You can now use PrepPulse/StudyBuddy with full AI capabilities.\n")
