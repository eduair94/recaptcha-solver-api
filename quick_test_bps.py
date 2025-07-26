#!/usr/bin/env python3
"""
Quick test script for BPS Uruguay website
Usage: python quick_test_bps.py
"""

import requests
import json
import sys

def test_bps_simple():
    """Simple test for BPS website."""
    
    url = "http://localhost:5000/solve-captcha"
    payload = {
        "url": "https://app2.bps.gub.uy/blanqueocontrasena-frontend/blanqueo"
    }
    
    print("🇺🇾 Testing BPS Uruguay website...")
    print(f"Target: {payload['url']}")
    
    try:
        # Check if API is running
        health_response = requests.get("http://localhost:5000/health", timeout=5)
        if health_response.status_code != 200:
            print("❌ API server is not running. Start it with: python start_api.py")
            return False
        
        print("✅ API server is running")
        print("📡 Sending request...")
        
        # Send the actual request
        response = requests.post(url, json=payload, timeout=180)
        result = response.json()
        
        print(f"📊 Status: {response.status_code}")
        print(f"⏱️  Time: {result.get('total_time', 'N/A')}s")
        
        if result.get('success'):
            print("✅ SUCCESS!")
            
            if result.get('captcha_found'):
                print(f"🎫 Token: {result.get('token', 'N/A')}")
                print(f"⏱️  Solve Time: {result.get('captcha_solve_time', 'N/A')}s")
            else:
                print("ℹ️  No reCAPTCHA found")
            
            # Show cookies
            cookies = result.get('cookies', [])
            print(f"🍪 Cookies: {len(cookies)} found")
            
            if cookies:
                print("\nCookie Details:")
                for cookie in cookies[:5]:  # Show first 5 cookies
                    name = cookie.get('name', 'unnamed')
                    value = cookie.get('value', '')
                    domain = cookie.get('domain', 'N/A')
                    print(f"  • {name} = {value[:20]}{'...' if len(value) > 20 else ''} ({domain})")
                
                if len(cookies) > 5:
                    print(f"  ... and {len(cookies) - 5} more cookies")
            
            return True
            
        else:
            print("❌ FAILED")
            print(f"Error: {result.get('error', 'Unknown')}")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ Request timed out")
        return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API. Make sure it's running: python start_api.py")
        return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

if __name__ == "__main__":
    print("🚀 BPS Uruguay Quick Test")
    print("=" * 40)
    
    success = test_bps_simple()
    
    print("\n" + "=" * 40)
    if success:
        print("🎉 Test completed successfully!")
        print("\n💡 You can now use the API with:")
        print("   - The reCAPTCHA token (if found)")
        print("   - The extracted cookies for session management")
    else:
        print("😞 Test failed")
        print("\n🔧 Troubleshooting:")
        print("   1. Make sure API is running: python start_api.py")
        print("   2. Check your internet connection")
        print("   3. Verify the BPS website is accessible")
    
    sys.exit(0 if success else 1)
