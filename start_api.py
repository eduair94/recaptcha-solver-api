#!/usr/bin/env python3
"""
reCAPTCHA Solver API Startup Script

This script starts the reCAPTCHA solver API server with proper configuration.
"""

import os
import sys
import subprocess
import argparse

def check_dependencies():
    """Check if all required dependencies are installed."""
    required_packages = [
        'flask',
        'DrissionPage', 
        'pydub',
        'SpeechRecognition',
        'requests'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            package_name = package.lower().replace('-', '_')
            if package_name == 'drissionpage':
                __import__('DrissionPage')
            elif package_name == 'speechrecognition':
                __import__('speech_recognition')
            else:
                __import__(package_name)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ Missing required packages:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\n💡 Install missing packages with:")
        print("   pip install -r requirements.txt")
        return False
    
    print("✅ All dependencies are installed!")
    return True

def start_api_server(host='0.0.0.0', port=5000, debug=False):
    """Start the API server."""
    print(f"🚀 Starting reCAPTCHA Solver API...")
    print(f"   Host: {host}")
    print(f"   Port: {port}")
    print(f"   Debug: {debug}")
    print(f"   URL: http://{host}:{port}")
    print("\n" + "="*50)
    
    try:
        # Import and run the Flask app
        from api import app
        app.run(debug=debug, host=host, port=port)
    except KeyboardInterrupt:
        print("\n\n🛑 Server stopped by user")
    except Exception as e:
        print(f"\n❌ Error starting server: {str(e)}")
        return False
    
    return True

def main():
    """Main function to parse arguments and start the server."""
    parser = argparse.ArgumentParser(
        description='reCAPTCHA Solver API Server',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python start_api.py                    # Start with default settings
  python start_api.py --port 8080        # Start on port 8080
  python start_api.py --debug             # Start in debug mode
  python start_api.py --host 127.0.0.1   # Start on localhost only
        """
    )
    
    parser.add_argument(
        '--host',
        default='0.0.0.0',
        help='Host to bind the server to (default: 0.0.0.0)'
    )
    
    parser.add_argument(
        '--port',
        type=int,
        default=5000,
        help='Port to bind the server to (default: 5000)'
    )
    
    parser.add_argument(
        '--debug',
        action='store_true',
        help='Run in debug mode'
    )
    
    parser.add_argument(
        '--check-deps',
        action='store_true',
        help='Only check dependencies and exit'
    )
    
    args = parser.parse_args()
    
    print("🤖 reCAPTCHA Solver API")
    print("=" * 30)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    if args.check_deps:
        print("✅ Dependency check completed successfully!")
        sys.exit(0)
    
    # Start the server
    success = start_api_server(
        host=args.host,
        port=args.port,
        debug=args.debug
    )
    
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()
