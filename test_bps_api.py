import requests
import json
import time

# API endpoint URL
API_URL = "http://localhost:5000/solve-captcha"
BPS_URL = "https://app2.bps.gub.uy/blanqueocontrasena-frontend/blanqueo"

def test_bps_website():
    """Test the API with the BPS Uruguay website."""
    
    payload = {
        "url": BPS_URL,
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
    }
    
    print("🇺🇾 Testing BPS Uruguay reCAPTCHA API...")
    print(f"URL: {payload['url']}")
    print(f"User Agent: {payload['user_agent']}")
    print("=" * 60)
    
    try:
        print("📡 Sending request to API...")
        response = requests.post(API_URL, json=payload, timeout=120)  # Increased timeout
        result = response.json()
        
        print(f"📊 Status Code: {response.status_code}")
        print(f"⏱️  Total Time: {result.get('total_time', 'N/A')} seconds")
        print(f"🔍 reCAPTCHA Found: {result.get('captcha_found', 'Unknown')}")
        
        if result.get('success'):
            print("✅ SUCCESS!")
            if result.get('captcha_found'):
                print(f"🎫 reCAPTCHA Token: {result.get('token', 'N/A')}")
                print(f"⏱️  Captcha Solve Time: {result.get('captcha_solve_time', 'N/A')} seconds")
            else:
                print("ℹ️  No reCAPTCHA found on the page")
        else:
            print("❌ FAILED")
            print(f"Error: {result.get('error', 'Unknown error')}")
        
        # Display cookies
        cookies = result.get('cookies', [])
        print(f"\n🍪 Extracted Cookies ({len(cookies)} found):")
        if cookies:
            for i, cookie in enumerate(cookies, 1):
                print(f"  {i}. {cookie.get('name', 'unnamed')}")
                print(f"     Value: {cookie.get('value', '')[:50]}{'...' if len(cookie.get('value', '')) > 50 else ''}")
                print(f"     Domain: {cookie.get('domain', 'N/A')}")
                print(f"     Path: {cookie.get('path', 'N/A')}")
                print(f"     Secure: {cookie.get('secure', False)}")
                print(f"     HttpOnly: {cookie.get('httpOnly', False)}")
                if i < len(cookies):
                    print()
        else:
            print("  No cookies found")
        
        print("\n" + "=" * 60)
        print("📋 Full Response:")
        print(json.dumps(result, indent=2, ensure_ascii=False))
        
        return result
        
    except requests.exceptions.Timeout:
        print("❌ Request timed out - the website might be slow to respond")
        return None
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {str(e)}")
        return None
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None

def test_bps_with_cookies():
    """Test the API with some sample cookies for the BPS website."""
    
    payload = {
        "url": BPS_URL,
        "cookies": [
            {
                "name": "JSESSIONID",
                "value": "test-session-id",
                "domain": "app2.bps.gub.uy",
                "path": "/",
                "secure": True,
                "httpOnly": True
            },
            {
                "name": "language",
                "value": "es",
                "domain": "app2.bps.gub.uy",
                "path": "/",
                "secure": False,
                "httpOnly": False
            }
        ],
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
    }
    
    print("\n🇺🇾 Testing BPS Uruguay with Sample Cookies...")
    print(f"URL: {payload['url']}")
    print(f"Input Cookies: {len(payload['cookies'])} cookie(s)")
    print("=" * 60)
    
    try:
        print("📡 Sending request to API...")
        response = requests.post(API_URL, json=payload, timeout=120)
        result = response.json()
        
        print(f"📊 Status Code: {response.status_code}")
        print(f"⏱️  Total Time: {result.get('total_time', 'N/A')} seconds")
        print(f"🔍 reCAPTCHA Found: {result.get('captcha_found', 'Unknown')}")
        
        if result.get('success'):
            print("✅ SUCCESS!")
            if result.get('captcha_found'):
                print(f"🎫 reCAPTCHA Token: {result.get('token', 'N/A')}")
                print(f"⏱️  Captcha Solve Time: {result.get('captcha_solve_time', 'N/A')} seconds")
        else:
            print("❌ FAILED")
            print(f"Error: {result.get('error', 'Unknown error')}")
        
        # Display cookies
        cookies = result.get('cookies', [])
        print(f"\n🍪 Final Cookies ({len(cookies)} found):")
        if cookies:
            for i, cookie in enumerate(cookies, 1):
                cookie_value = cookie.get('value', '')
                display_value = cookie_value[:30] + '...' if len(cookie_value) > 30 else cookie_value
                print(f"  {i}. {cookie.get('name', 'unnamed')} = {display_value}")
                print(f"     Domain: {cookie.get('domain', 'N/A')} | Path: {cookie.get('path', 'N/A')}")
        
        return result
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None

def check_api_health():
    """Check if the API server is running."""
    try:
        response = requests.get("http://localhost:5000/health", timeout=5)
        if response.status_code == 200:
            print("✅ API server is running")
            return True
        else:
            print(f"⚠️  API server responded with status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ API server is not accessible: {str(e)}")
        print("💡 Make sure to start the API server with: python start_api.py")
        return False

if __name__ == "__main__":
    print("🤖 BPS Uruguay reCAPTCHA API Test")
    print("=" * 60)
    
    # Check if API is running
    if not check_api_health():
        exit(1)
    
    print("\n🚀 Starting tests...")
    
    # Test 1: Basic BPS website test
    result1 = test_bps_website()
    
    # Test 2: BPS website with sample cookies
    result2 = test_bps_with_cookies()
    
    print("\n" + "=" * 60)
    print("🏁 Test Summary:")
    print(f"Test 1 (Basic): {'✅ PASSED' if result1 and result1.get('success') else '❌ FAILED'}")
    print(f"Test 2 (With Cookies): {'✅ PASSED' if result2 and result2.get('success') else '❌ FAILED'}")
    
    if result1 or result2:
        print("\n💡 Tips:")
        print("- The API now extracts and returns all cookies from the session")
        print("- Use the returned cookies for subsequent requests to maintain session state")
        print("- The API automatically detects if reCAPTCHA is present on the page")
        print("- If no reCAPTCHA is found, the request is still considered successful")
