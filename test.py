from DrissionPage import ChromiumPage, ChromiumOptions
from RecaptchaSolver import RecaptchaSolver
import time

CHROME_ARGUMENTS = [
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
    "--disable-gpu",
    "--accept-lang=en-US",
    "--disable-usage-stats",
    "--disable-crash-reporter",
    "--no-sandbox",
    "--headless=1"
]
 
options = ChromiumOptions()
for argument in CHROME_ARGUMENTS:
    options.set_argument(argument)
    
# Set a port for remote debugging (DrissionPage will handle this automatically)
options.set_argument("--remote-debugging-port=0")  # Use 0 to let DrissionPage pick an available port

try:
    driver = ChromiumPage(addr_or_opts=options)
    recaptchaSolver = RecaptchaSolver(driver)


    driver.get("https://app2.bps.gub.uy/blanqueocontrasena-frontend/blanqueo")
    # Wait for the reCAPTCHA iframe to be displayed
    driver.wait.ele_displayed("@title=reCAPTCHA", timeout=10)
    time.sleep(1)  # Give the page a moment to stabilize

    try:
        # Look for reCAPTCHA iframe or elements
        iframe_selectors = [
            "@title=reCAPTCHA",
            "iframe[src*='recaptcha']",
            ".g-recaptcha",
            "#recaptcha"
        ]
        captcha_found = False
        for selector in iframe_selectors:
            try:
                element = driver.ele(selector, timeout=2)
                if element:
                    captcha_found = True
                    print(f"Found reCAPTCHA using selector: {selector}")
                    break
            except:
                continue
        if not captcha_found:
            print("No reCAPTCHA found on the page")
    except Exception as e:
        print(f"Error checking for reCAPTCHA: {str(e)}")

    # Wait again to ensure iframe is stable before solving
    driver.wait.ele_displayed("@title=reCAPTCHA", timeout=10)
    time.sleep(0.5)
    t0 = time.time()
    recaptchaSolver.solveCaptcha()
    token = recaptchaSolver.get_token()
    print(f"Time to solve the captcha: {time.time()-t0:.2f} seconds - {token}")

finally:
    try:
        driver.close()
    except:
        pass
