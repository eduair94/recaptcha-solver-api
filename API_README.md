# reCAPTCHA Solver API

A Flask-based REST API that solves Google reCAPTCHA challenges using audio recognition. The API accepts cookies, URLs, and optional proxy configurations to solve reCAPTCHA on web pages.

## Features

- 🤖 Automated reCAPTCHA solving using audio recognition
- 🍪 Support for custom cookies
- 🌐 Optional proxy support
- 🔧 Configurable user agents
- 📊 Detailed response with timing information
- 🚀 RESTful API interface

## Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Ensure you have Chrome/Chromium installed on your system.

## Usage

### Starting the API Server

Run the Flask application:
```bash
python api.py
```

The API will start on `http://localhost:5000`

### API Endpoints

#### POST /solve-captcha

Solves reCAPTCHA on a given webpage.

**Request Body:**
```json
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
  "proxy": "ip:port",
  "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}
```

**Parameters:**
- `url` (required): Target URL containing reCAPTCHA
- `cookies` (optional): Array of cookie objects to set before solving
- `proxy` (optional): Proxy configuration in format `ip:port` or `username:password@ip:port`
- `user_agent` (optional): Custom user agent string

**Response:**
```json
{
  "success": true,
  "token": "03AGdBq25...",
  "captcha_solve_time": 15.32,
  "total_time": 18.45,
  "url": "https://example.com/page-with-captcha",
  "message": "reCAPTCHA solved successfully"
}
```

#### GET /health

Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "service": "reCAPTCHA Solver API",
  "timestamp": 1640995200.0
}
```

#### GET /

API information endpoint with usage examples.

### Cookie Format

Cookies should be provided as an array of objects with the following structure:

```json
{
  "name": "cookie_name",        // Required
  "value": "cookie_value",      // Required
  "domain": "example.com",      // Optional, defaults to URL domain
  "path": "/",                  // Optional, defaults to "/"
  "secure": false,              // Optional, defaults to false
  "httpOnly": false,            // Optional, defaults to false
  "expires": 1640995200,        // Optional, Unix timestamp
  "sameSite": "Lax"            // Optional, "Strict", "Lax", or "None"
}
```

### Proxy Configuration

The API supports two proxy formats:

1. **Simple proxy**: `ip:port`
   ```json
   {
     "proxy": "127.0.0.1:8080"
   }
   ```

2. **Authenticated proxy**: `username:password@ip:port`
   ```json
   {
     "proxy": "user:pass@127.0.0.1:8080"
   }
   ```

## Testing

Use the provided test script to verify the API functionality:

```bash
python test_api.py
```

This will run several test cases including:
- Basic reCAPTCHA solving
- Solving with cookies
- Solving with custom user agent
- Health check verification

## Examples

### Python Client Example

```python
import requests

# Basic usage
response = requests.post('http://localhost:5000/solve-captcha', json={
    'url': 'https://www.google.com/recaptcha/api2/demo'
})

result = response.json()
if result['success']:
    print(f"reCAPTCHA solved! Token: {result['token']}")
else:
    print(f"Failed: {result['error']}")
```

### cURL Example

```bash
curl -X POST http://localhost:5000/solve-captcha \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://www.google.com/recaptcha/api2/demo",
    "cookies": [
      {
        "name": "session",
        "value": "abc123",
        "domain": "google.com"
      }
    ]
  }'
```

### JavaScript Example

```javascript
const response = await fetch('http://localhost:5000/solve-captcha', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    url: 'https://www.google.com/recaptcha/api2/demo',
    cookies: [
      {
        name: 'session_id',
        value: 'abc123',
        domain: 'google.com'
      }
    ]
  })
});

const result = await response.json();
console.log(result);
```

## How It Works

1. **Browser Setup**: Creates a headless Chrome browser with specified options
2. **Cookie Setting**: Applies provided cookies to the browser session
3. **Navigation**: Navigates to the target URL
4. **reCAPTCHA Detection**: Locates and interacts with the reCAPTCHA iframe
5. **Audio Challenge**: Clicks the audio challenge button
6. **Audio Processing**: Downloads and processes the audio file using speech recognition
7. **Solution Submission**: Submits the recognized text as the solution
8. **Token Extraction**: Retrieves the reCAPTCHA token upon successful completion

## Dependencies

- **DrissionPage**: Browser automation
- **Flask**: Web framework for API
- **pydub**: Audio processing
- **SpeechRecognition**: Google speech-to-text
- **requests**: HTTP client for testing

## Important Notes

- The API runs headless Chrome, which requires Chrome/Chromium to be installed
- Audio processing requires an internet connection for Google Speech Recognition
- Some websites may detect automated behavior - use appropriate delays and user agents
- Respect website terms of service and rate limits
- This tool is for educational and testing purposes

## Troubleshooting

### Common Issues

1. **Chrome not found**: Ensure Chrome/Chromium is installed and accessible
2. **Audio processing fails**: Check internet connection for Google Speech API
3. **reCAPTCHA not detected**: Verify the target page actually contains reCAPTCHA
4. **Bot detection**: Try different user agents or add delays

### Error Responses

The API returns detailed error messages:

```json
{
  "success": false,
  "error": "Error description",
  "total_time": 5.23,
  "url": "https://example.com"
}
```

## License

This project is for educational purposes. Please respect website terms of service and use responsibly.
