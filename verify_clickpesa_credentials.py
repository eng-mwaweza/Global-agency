"""
ClickPesa Credentials Verification Script

This script helps you verify your ClickPesa API credentials are valid.
Run this before trying to process payments.

Usage:
    python verify_clickpesa_credentials.py
"""

import os
import sys
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_credentials():
    """Test ClickPesa API credentials"""
    
    print("=" * 60)
    print("ClickPesa Credentials Verification")
    print("=" * 60)
    
    # Get credentials from environment
    client_id = os.getenv('CLICKPESA_CLIENT_ID')
    api_key = os.getenv('CLICKPESA_API_KEY')
    base_url = os.getenv('CLICKPESA_BASE_URL', 'https://api.clickpesa.com/third-parties')
    
    # Check if credentials exist
    print("\n1. Checking credentials configuration...")
    if not client_id:
        print("   ❌ CLICKPESA_CLIENT_ID not found in .env file")
        return False
    if not api_key:
        print("   ❌ CLICKPESA_API_KEY not found in .env file")
        return False
    
    # Check for placeholder values
    placeholders = ['your_client_id_here', 'your_api_key_here', 'your_actual_client_id_from_dashboard', 'your_actual_api_key_from_dashboard']
    if client_id in placeholders:
        print(f"   ❌ CLICKPESA_CLIENT_ID contains placeholder value: {client_id}")
        print("   Please replace it with your actual Client ID from ClickPesa dashboard")
        return False
    if api_key in placeholders:
        print(f"   ❌ CLICKPESA_API_KEY contains placeholder value")
        print("   Please replace it with your actual API Key from ClickPesa dashboard")
        return False
    
    print(f"   ✓ Client ID found: {client_id[:10]}...{client_id[-4:]}")
    print(f"   ✓ API Key found: {api_key[:10]}...{api_key[-4:]}")
    print(f"   ✓ Base URL: {base_url}")
    
    # Test API connection
    print("\n2. Testing API connection...")
    test_url = f"{base_url}/payments/preview-ussd-push-request"
    
    # Test different authentication methods
    auth_methods = [
        ("X-API-Key + X-Client-Id", {
            'X-API-Key': api_key,
            'X-Client-Id': client_id,
            'Content-Type': 'application/json'
        }),
        ("Bearer Token", {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }),
        ("Api-Key + Client-Id", {
            'Api-Key': api_key,
            'Client-Id': client_id,
            'Content-Type': 'application/json'
        }),
    ]
    
    test_payload = {
        "amount": "1000",
        "currency": "TZS",
        "orderReference": "VERIFY_TEST_001",
        "phoneNumber": "255712345678",
        "fetchSenderDetails": False
    }
    
    success = False
    for method_name, headers in auth_methods:
        print(f"\n   Testing {method_name}...")
        try:
            response = requests.post(test_url, json=test_payload, headers=headers, timeout=10)
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    # Check if it's just a health check
                    if 'name' in data and data.get('name') == 'clickpesa-core':
                        print(f"   ⚠️  Got health check response, not actual API response")
                        continue
                    print(f"   ✅ SUCCESS! Authentication method works: {method_name}")
                    print(f"   Response: {data}")
                    success = True
                    break
                except:
                    print(f"   Response: {response.text[:200]}")
            elif response.status_code == 401:
                print(f"   ❌ Authentication failed (401 Unauthorized)")
                print(f"   Response: {response.text[:200]}")
            else:
                print(f"   Response: {response.text[:200]}")
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
    
    if not success:
        print("\n" + "=" * 60)
        print("❌ CREDENTIAL VERIFICATION FAILED")
        print("=" * 60)
        print("\nYour ClickPesa credentials are INVALID or EXPIRED.")
        print("\nTo fix this:")
        print("1. Go to: https://dashboard.clickpesa.com")
        print("2. Log in to your ClickPesa account")
        print("3. Navigate to: Settings → API Credentials")
        print("4. Generate new credentials or copy existing valid ones")
        print("5. Update your .env file with:")
        print(f"   CLICKPESA_CLIENT_ID=<your_new_client_id>")
        print(f"   CLICKPESA_API_KEY=<your_new_api_key>")
        print("\n6. Make sure you're using the correct environment:")
        print("   - Production: https://api.clickpesa.com/third-parties")
        print("   - Sandbox: Check ClickPesa documentation for sandbox URL")
        print("\n7. Verify your account is active and has API access enabled")
        print("\nIf you continue to have issues, contact ClickPesa support.")
        return False
    
    print("\n" + "=" * 60)
    print("✅ CREDENTIAL VERIFICATION SUCCESSFUL")
    print("=" * 60)
    print("\nYour ClickPesa credentials are valid and working!")
    print("You can now process payments through the student portal.")
    return True

if __name__ == "__main__":
    success = test_credentials()
    sys.exit(0 if success else 1)
