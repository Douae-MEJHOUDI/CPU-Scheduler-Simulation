#!/usr/bin/env python3
"""
Run script for CPU Scheduler Simulation Web Interface.
This script sets up environment variables and launches the Flask application.
"""

import os
import sys
import argparse
from app import create_app

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="CPU Scheduler Simulation Web Interface")
    parser.add_argument("--host", default="127.0.0.1", help="Host to run the server on")
    parser.add_argument("--port", type=int, default=5000, help="Port to run the server on")
    parser.add_argument("--debug", action="store_true", help="Run in debug mode")
    return parser.parse_args()

def setup_environment():
    """Set up environment variables."""
    if 'SECRET_KEY' not in os.environ:
        import secrets
        os.environ['SECRET_KEY'] = secrets.token_hex(16)

    if len(sys.argv) > 1 and '--debug' in sys.argv:
        os.environ['FLASK_ENV'] = 'development'
    else:
        os.environ['FLASK_ENV'] = 'production'

def main():
    """Main function to run the Flask application."""
    args = parse_arguments()
    setup_environment()
    
    app = create_app()

    print(f"\n{'='*50}")
    print(f" CPU Scheduler Simulation Web Interface")
    print(f"{'='*50}")
    print(f" Server running at http://{args.host}:{args.port}")
    print(f" Press Ctrl+C to quit")
    print(f"{'='*50}\n")
    
    app.run(host=args.host, port=args.port, debug=args.debug)

if __name__ == "__main__":
    main()