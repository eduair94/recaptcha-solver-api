module.exports = {
  apps: [
    {
      name: "recaptcha-api",
      script: "start_api.py", // or "api.py" if you run that directly
      interpreter: "python", // or "python" if that's your command
      args: "",
      watch: false,
      autorestart: true,
      max_restarts: 10,
      env: {
        // You can set environment variables here if needed
        // "PORT": 5000
      },
    },
  ],
};
