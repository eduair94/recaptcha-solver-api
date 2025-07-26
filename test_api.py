import requests
import json
import time

# API endpoint URL
API_URL = "http://localhost:5000/solve-captcha"

def test_api_basic():
    """Test the API with basic Google reCAPTCHA demo."""
    
    payload = {
        "url": "https://www.google.com/recaptcha/api2/demo"
    }
    
    print("Testing reCAPTCHA API...")
    print(f"URL: {payload['url']}")
    
    try:
        response = requests.post(API_URL, json=payload, timeout=60)
        result = response.json()
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(result, indent=2)}")
        
        if result.get('success'):
            print("✅ reCAPTCHA solved successfully!")
            print(f"⏱️  Solve time: {result.get('captcha_solve_time', 'N/A')} seconds")
            print(f"🎫 Token: {result.get('token', 'N/A')}")
        else:
            print("❌ Failed to solve reCAPTCHA")
            print(f"Error: {result.get('error', 'Unknown error')}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {str(e)}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

def test_api_with_cookies():
    """Test the API with cookies."""
    
    payload = {
        "url": "https://www.google.com/recaptcha/api2/demo",
        "cookies": [
            {
                "name": "test_cookie",
                "value": "test_value",
                "domain": "google.com",
                "path": "/",
                "secure": True,
                "httpOnly": False
            }
        ]
    }
    
    print("\nTesting reCAPTCHA API with cookies...")
    print(f"URL: {payload['url']}")
    print(f"Cookies: {len(payload['cookies'])} cookie(s)")
    
    try:
        response = requests.post(API_URL, json=payload, timeout=60)
        result = response.json()
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(result, indent=2)}")
        
        if result.get('success'):
            print("✅ reCAPTCHA solved successfully with cookies!")
            print(f"⏱️  Solve time: {result.get('captcha_solve_time', 'N/A')} seconds")
        else:
            print("❌ Failed to solve reCAPTCHA with cookies")
            print(f"Error: {result.get('error', 'Unknown error')}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {str(e)}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

def test_api_with_proxy():
    """Test the API with proxy (commented out since most users won't have a proxy)."""
    
    payload = {
        "url": "https://www.google.com/recaptcha/api2/demo",
        # "proxy": "127.0.0.1:8080",  # Uncomment and modify if you have a proxy
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    print("\nTesting reCAPTCHA API with custom user agent...")
    print(f"URL: {payload['url']}")
    print(f"User Agent: {payload.get('user_agent', 'Default')}")
    
    try:
        response = requests.post(API_URL, json=payload, timeout=60)
        result = response.json()
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(result, indent=2)}")
        
        if result.get('success'):
            print("✅ reCAPTCHA solved successfully with custom user agent!")
            print(f"⏱️  Solve time: {result.get('captcha_solve_time', 'N/A')} seconds")
        else:
            print("❌ Failed to solve reCAPTCHA with custom user agent")
            print(f"Error: {result.get('error', 'Unknown error')}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {str(e)}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

def test_health_endpoint():
    """Test the health check endpoint."""
    
    try:
        response = requests.get("http://localhost:5000/health")
        result = response.json()
        
        print(f"\nHealth Check - Status Code: {response.status_code}")
        print(f"Response: {json.dumps(result, indent=2)}")
        
    except Exception as e:
        print(f"❌ Health check failed: {str(e)}")

if __name__ == "__main__":
    print("🚀 Starting reCAPTCHA API Tests")
    print("Make sure the API server is running on http://localhost:5000")
    print("=" * 60)
    
    # Test health endpoint first
    test_health_endpoint()
    
    # Test basic functionality
    test_api_basic()
    
    # Test with cookies
    test_api_with_cookies()
    
    # Test with custom user agent
    test_api_with_proxy()
    
    print("\n" + "=" * 60)
    print("🏁 Tests completed!")
