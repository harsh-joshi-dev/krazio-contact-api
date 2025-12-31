#!/bin/bash
# Simple startup script for Render
echo "Starting Krazio Email API..."
gunicorn app:app --bind 0.0.0.0:${PORT:-5000} --workers 1 --timeout 120 --graceful-timeout 30 --log-level info

