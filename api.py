from flask import Flask, request, jsonify
from DrissionPage import ChromiumPage, ChromiumOptions
from RecaptchaSolver import RecaptchaSolver
import time
import logging
from typing import Dict, List, Optional, Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

class CaptchaAPI:
    """API class for solving reCAPTCHA challenges."""
    
    # Default Chrome arguments for browser operation
    DEFAULT_CHROME_ARGUMENTS = [
        "--no-first-run",
        "--force-color-profile=srgb",
        "--metrics-recording-only",
        "--password-store=basic",
        "--use-mock-keychain",
        "--export-tagged-pdf",
        "--no-default-browser-check",
        "--disable-background-mode",
        "--enable-features=NetworkService,NetworkServiceInProcess",
        "--disable-features=FlashDeprecationWarning",
        "--deny-permission-prompts",
        "--accept-lang=en-US",
        "--disable-usage-stats",
        "--disable-crash-reporter",
        "--no-sandbox"
        "--headless=1"
    ]

    @staticmethod
    def create_driver(proxy: Optional[str] = None, user_agent: Optional[str] = None, 
                     headless: bool = False) -> ChromiumPage:
        """Create a ChromiumPage driver with specified options.
        
        Args:
            proxy: Optional proxy string in format 'ip:port' or 'username:password@ip:port'
            user_agent: Optional custom user agent string
            headless: Whether to run browser in headless mode (default: False for visible mode)
            
        Returns:
            ChromiumPage: Configured browser driver
        """
        options = ChromiumOptions()
        
        # Add default arguments
        for argument in CaptchaAPI.DEFAULT_CHROME_ARGUMENTS:
            options.set_argument(argument)
        
        # Add headless mode if requested
        if headless:
            options.set_argument("--headless=new")
            options.set_argument("--disable-gpu")
            logger.info("Running browser in headless mode")
        else:
            logger.info("Running browser in visible mode")
        
        # Configure proxy if provided
        if proxy:
            if '@' in proxy:
                # Format: username:password@ip:port
                auth_part, proxy_part = proxy.split('@')
                username, password = auth_part.split(':')
                options.set_argument(f"--proxy-server={proxy_part}")
                options.set_argument(f"--proxy-auth={username}:{password}")
            else:
                # Format: ip:port
                options.set_argument(f"--proxy-server={proxy}")
        
        # Set custom user agent if provided
        if user_agent:
            options.set_argument(f"--user-agent={user_agent}")
        
        return ChromiumPage(addr_or_opts=options)

    @staticmethod
    def set_cookies(driver: ChromiumPage, cookies: List[Dict[str, Any]], domain: str) -> None:
        """Set cookies for the browser session.
        
        Args:
            driver: ChromiumPage driver instance
            cookies: List of cookie dictionaries
            domain: Domain to set cookies for
        """
        # Navigate to domain first to set cookies
        driver.get(f"https://{domain}")
        
        for cookie in cookies:
            try:
                # Ensure required cookie fields
                cookie_data = {
                    'name': cookie.get('name', ''),
                    'value': cookie.get('value', ''),
                    'domain': cookie.get('domain', domain),
                    'path': cookie.get('path', '/'),
                    'secure': cookie.get('secure', False),
                    'httpOnly': cookie.get('httpOnly', False)
                }
                
                # Add optional fields if present
                if 'expires' in cookie:
                    cookie_data['expires'] = cookie['expires']
                if 'sameSite' in cookie:
                    cookie_data['sameSite'] = cookie['sameSite']
                
                # Use the correct DrissionPage method to set cookies
                driver.set.cookies(cookie_data)
                logger.info(f"Set cookie: {cookie_data['name']}")
                
            except Exception as e:
                logger.warning(f"Failed to set cookie {cookie.get('name', 'unknown')}: {str(e)}")
                # Try alternative method if the first one fails
                try:
                    driver.set.cookie(
                        name=cookie.get('name', ''),
                        value=cookie.get('value', ''),
                        domain=cookie.get('domain', domain),
                        path=cookie.get('path', '/'),
                        secure=cookie.get('secure', False),
                        http_only=cookie.get('httpOnly', False)
                    )
                    logger.info(f"Set cookie (alternative method): {cookie.get('name', '')}")
                except Exception as e2:
                    logger.error(f"Failed to set cookie with both methods {cookie.get('name', 'unknown')}: {str(e2)}")

    @staticmethod
    def get_all_cookies(driver: ChromiumPage) -> List[Dict[str, Any]]:
        """Extract all cookies from the current browser session.
        
        Args:
            driver: ChromiumPage driver instance
            
        Returns:
            List of cookie dictionaries
        """
        try:
            all_cookies = []
            # Use the correct DrissionPage method to get cookies
            cookies = driver.cookies()
            
            for cookie in cookies:
                cookie_data = {
                    'name': cookie.get('name', ''),
                    'value': cookie.get('value', ''),
                    'domain': cookie.get('domain', ''),
                    'path': cookie.get('path', '/'),
                    'secure': cookie.get('secure', False),
                    'httpOnly': cookie.get('httpOnly', False)
                }
                
                # Add optional fields if present
                if 'expires' in cookie:
                    cookie_data['expires'] = cookie['expires']
                if 'sameSite' in cookie:
                    cookie_data['sameSite'] = cookie['sameSite']
                
                all_cookies.append(cookie_data)
            
            return all_cookies
        except Exception as e:
            logger.warning(f"Failed to extract cookies: {str(e)}")
            return []

    @staticmethod
    def solve_captcha_on_page(url: str, cookies: Optional[List[Dict[str, Any]]] = None, 
                             proxy: Optional[str] = None, user_agent: Optional[str] = None,
                             headless: bool = False) -> Dict[str, Any]:
        """Solve reCAPTCHA on a given page.
        
        Args:
            url: Target URL containing reCAPTCHA
            cookies: Optional list of cookies to set
            proxy: Optional proxy configuration
            user_agent: Optional custom user agent
            headless: Whether to run browser in headless mode (default: False for visible mode)
            
        Returns:
            Dict containing success status, token, cookies, and timing information
        """
        driver = None
        start_time = time.time()
        
        try:
            # Create driver with specified options
            driver = CaptchaAPI.create_driver(proxy=proxy, user_agent=user_agent, headless=headless)
            
            # Set cookies if provided
            if cookies:
                from urllib.parse import urlparse
                domain = urlparse(url).netloc
                CaptchaAPI.set_cookies(driver, cookies, domain)
            
            # Navigate to target URL
            logger.info(f"Navigating to: {url}")
            driver.get(url)
            
            # Wait for page to load completely
            time.sleep(3)
            
            # Check if reCAPTCHA is present on the page
            captcha_found = False
            try:
                # Look for reCAPTCHA iframe or elements
                iframe_selectors = [
                    "@title=reCAPTCHA",
                    "iframe[src*='recaptcha']",
                    ".g-recaptcha",
                    "#recaptcha"
                ]
                
                for selector in iframe_selectors:
                    try:
                        element = driver.ele(selector, timeout=2)
                        if element:
                            captcha_found = True
                            logger.info(f"Found reCAPTCHA using selector: {selector}")
                            break
                    except:
                        continue
                        
                if not captcha_found:
                    logger.warning("No reCAPTCHA found on the page")
                    
            except Exception as e:
                logger.warning(f"Error checking for reCAPTCHA: {str(e)}")
            
            # Initialize reCAPTCHA solver
            recaptcha_solver = RecaptchaSolver(driver)
            
            # Solve the captcha if found
            token = None
            is_solved = False
            captcha_solve_time = 0
            
            if captcha_found:
                logger.info("Attempting to solve reCAPTCHA...")
                captcha_start_time = time.time()
                try:
                    recaptcha_solver.solveCaptcha()
                    logger.info("Captcha solved");
                    captcha_solve_time = time.time() - captcha_start_time
                    
                    logger.info("Get Captcha Token");
                    # Get the token
                    token = recaptcha_solver.get_token()
                    
                    # Check if solved
                    is_solved = recaptcha_solver.is_solved()
                    
                except Exception as e:
                    logger.error(f"Error solving reCAPTCHA: {str(e)}")
                    captcha_solve_time = time.time() - captcha_start_time
            
            # Extract all cookies from the current session
            extracted_cookies = CaptchaAPI.get_all_cookies(driver)
            
            total_time = time.time() - start_time
            
            result = {
                'success': is_solved if captcha_found else True,  # True if no captcha found
                'captcha_found': captcha_found,
                'token': token,
                'cookies': extracted_cookies,
                'captcha_solve_time': round(captcha_solve_time, 2),
                'total_time': round(total_time, 2),
                'url': url,
                'message': ('reCAPTCHA solved successfully' if is_solved 
                           else 'No reCAPTCHA found on page' if not captcha_found 
                           else 'Failed to solve reCAPTCHA')
            }
            
            logger.info(f"Result: {result}")
            return result
            
        except Exception as e:
            error_message = f"Error solving reCAPTCHA: {str(e)}"
            logger.error(error_message)
            
            # Try to extract cookies even on error
            extracted_cookies = []
            if driver:
                try:
                    extracted_cookies = CaptchaAPI.get_all_cookies(driver)
                except:
                    pass
            
            return {
                'success': False,
                'captcha_found': False,
                'error': error_message,
                'cookies': extracted_cookies,
                'total_time': round(time.time() - start_time, 2),
                'url': url
            }
        
        finally:
            if driver:
                try:
                    driver.close()
                except Exception as e:
                    logger.warning(f"Error closing driver: {str(e)}")


@app.route('/solve-captcha', methods=['POST'])
def solve_captcha_endpoint():
    """API endpoint to solve reCAPTCHA on a given page.
    
    Expected JSON payload:
    {
        "url": "https://example.com/page-with-captcha",
        "cookies": [
            {
                "name": "session_id",
                "value": "abc123",
                "domain": "example.com",
                "path": "/",
                "secure": true,
                "httpOnly": false
            }
        ],
        "proxy": "ip:port" or "username:password@ip:port",
        "user_agent": "Mozilla/5.0 ..."
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'No JSON data provided'
            }), 400
        
        # Validate required fields
        url = data.get('url')
        if not url:
            return jsonify({
                'success': False,
                'error': 'URL is required'
            }), 400
        
        # Extract optional parameters
        cookies = data.get('cookies', [])
        proxy = data.get('proxy')
        user_agent = data.get('user_agent')
        headless = data.get('headless', False)  # Default to visible mode
        
        # Validate cookies format if provided
        if cookies and not isinstance(cookies, list):
            return jsonify({
                'success': False,
                'error': 'Cookies must be a list of objects'
            }), 400
        
        # Solve the captcha
        result = CaptchaAPI.solve_captcha_on_page(
            url=url,
            cookies=cookies,
            proxy=proxy,
            user_agent=user_agent,
            headless=headless
        )
        
        # Return appropriate HTTP status code
        status_code = 200 if result.get('success') else 500
        return jsonify(result), status_code
        
    except Exception as e:
        logger.error(f"Endpoint error: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Internal server error: {str(e)}'
        }), 500


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'service': 'reCAPTCHA Solver API',
        'timestamp': time.time()
    })


@app.route('/', methods=['GET'])
def api_info():
    """API information endpoint."""
    return jsonify({
        'name': 'reCAPTCHA Solver API',
        'version': '1.0.0',
        'description': 'API for solving reCAPTCHA challenges using audio recognition',
        'endpoints': {
            'POST /solve-captcha': 'Solve reCAPTCHA on a given page',
            'GET /health': 'Health check',
            'GET /': 'API information'
        },
        'example_request': {
            'url': 'https://app2.bps.gub.uy/blanqueocontrasena-frontend/blanqueo',
            'cookies': [
                {
                    'name': 'JSESSIONID',
                    'value': 'abc123',
                    'domain': 'app2.bps.gub.uy'
                }
            ],
            'proxy': 'ip:port',
            'user_agent': 'Mozilla/5.0...'
        },
        'example_response': {
            'success': True,
            'captcha_found': True,
            'token': '03AGdBq25...',
            'cookies': [
                {
                    'name': 'JSESSIONID',
                    'value': 'new-session-value',
                    'domain': 'app2.bps.gub.uy',
                    'path': '/',
                    'secure': True,
                    'httpOnly': True
                }
            ],
            'captcha_solve_time': 15.32,
            'total_time': 18.45,
            'url': 'https://app2.bps.gub.uy/blanqueocontrasena-frontend/blanqueo',
            'message': 'reCAPTCHA solved successfully'
        }
    })


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
