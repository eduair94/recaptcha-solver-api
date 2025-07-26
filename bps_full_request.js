// Node.js script to solve reCAPTCHA and submit the BPS registrar request
// Usage: node bps_full_request.js
// Requires: npm install axios

const axios = require("axios");

const CAPTCHA_API_URL = "http://localhost:5000/solve-captcha";
const CAPTCHA_SITE_URL = "https://app2.bps.gub.uy/blanqueocontrasena-frontend/blanqueo";
const REGISTRAR_URL = "https://app2.bps.gub.uy/blanqueocontrasena-backend/api/v1/registrar";

async function getRecaptchaToken() {
  try {
    const response = await axios.post(CAPTCHA_API_URL, { url: CAPTCHA_SITE_URL }, { timeout: 180000 });
    if (response.data && response.data.success && response.data.token) {
      console.log("✅ Captcha solved! Token:", response.data.token);
      const fs = require("fs");
      fs.writeFileSync("captcha_response.json", JSON.stringify(response.data, null, 2));
      return response.data.token;
    } else {
      throw new Error("Failed to solve captcha: " + (response.data.error || "Unknown error"));
    }
  } catch (error) {
    console.error("Error solving captcha:", error.message);
    process.exit(1);
  }
}

async function sendBpsRequest(token) {
  const data = {
    codPais: "1",
    nroDocumento: "47073451",
    tipoDocumento: "DO",
    gRecaptchaResponse: token,
  };

  const headers = {
    Accept: "application/json, text/plain, */*",
    "Accept-Language": "es-ES,es;q=0.9",
    Connection: "keep-alive",
    "Content-Type": "application/json",
    Origin: "https://app2.bps.gub.uy",
    Referer: CAPTCHA_SITE_URL,
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
    "sec-ch-ua": '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
  };

  try {
    const response = await axios.post(REGISTRAR_URL, data, { headers });
    console.log("Status:", response.status);
    console.log("Response:", response.data);
    const fs = require("fs");
    fs.writeFileSync("bps_response.json", JSON.stringify(response.data, null, 2));
  } catch (error) {
    if (error.response) {
      console.error("Error status:", error.response.status);
      console.error("Error data:", error.response.data);
    } else {
      console.error("Request error:", error.message);
    }
  }
}

(async () => {
  const token = await getRecaptchaToken();
  await sendBpsRequest(token);
})();
