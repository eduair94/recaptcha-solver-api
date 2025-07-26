// Node.js script to perform the BPS Uruguay registrar request
// Usage: node bps_request.js
// Make sure to replace the gRecaptchaResponse value with your actual token

const axios = require("axios");

async function sendBpsRequest() {
  const url = "https://app2.bps.gub.uy/blanqueocontrasena-backend/api/v1/registrar";

  const data = {
    codPais: "1",
    nroDocumento: "47073450",
    tipoDocumento: "DO",
    gRecaptchaResponse: "YOUR_RECAPTCHA_TOKEN_HERE", // <-- Replace with your token
  };

  const headers = {
    Accept: "application/json, text/plain, */*",
    "Accept-Language": "es-ES,es;q=0.9",
    Connection: "keep-alive",
    "Content-Type": "application/json",
    Origin: "https://app2.bps.gub.uy",
    Referer: "https://app2.bps.gub.uy/blanqueocontrasena-frontend/blanqueo",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
    "sec-ch-ua": '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
  };

  try {
    const response = await axios.post(url, data, { headers });
    console.log("Status:", response.status);
    console.log("Response:", response.data);
  } catch (error) {
    if (error.response) {
      console.error("Error status:", error.response.status);
      console.error("Error data:", error.response.data);
    } else {
      console.error("Request error:", error.message);
    }
  }
}

sendBpsRequest();
