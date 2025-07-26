from DrissionPage import ChromiumPage, ChromiumOptions
from RecaptchaSolver import RecaptchaSolver
import time


# Use minimal Chrome arguments for best compatibility
CHROME_ARGUMENTS = [
    "--no-first-run",
    #"--headless",
    "--disable-gpu",
    "--no-sandbox"
]

options = ChromiumOptions()
for argument in CHROME_ARGUMENTS:
    options.set_argument(argument)

try:
    driver = ChromiumPage(addr_or_opts=options)
    recaptchaSolver = RecaptchaSolver(driver)



    driver.get("https://app2.bps.gub.uy/blanqueocontrasena-frontend/blanqueo")
    # Robustly wait for the reCAPTCHA iframe to be available
    import datetime
    start = datetime.datetime.now()
    timeout = 30  # seconds
    found_iframe = False
    while (datetime.datetime.now() - start).total_seconds() < timeout:
        try:
            if driver.ele("@title=reCAPTCHA", timeout=2):
                found_iframe = True
                print("Found reCAPTCHA iframe!")
                break
        except Exception:
            pass
        time.sleep(1)
    if not found_iframe:
        print("No reCAPTCHA iframe found on the page after waiting.")
        raise RuntimeError("No reCAPTCHA iframe found")

    time.sleep(1)  # Give the page a moment to stabilize
    t0 = time.time()
    recaptchaSolver.solveCaptcha()
    token = recaptchaSolver.get_token()
    print(f"Time to solve the captcha: {time.time()-t0:.2f} seconds - {token}")

finally:
    try:
        driver.close()
    except:
        pass
