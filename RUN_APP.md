# How to Run the App

## Quick Start (No Debug Mode - Recommended)

```bash
cd /Users/admin/Projects/krazio-email
source venv/bin/activate
python app.py
```

The app will run on **http://localhost:5001** without debug mode (no auto-reload, no warnings).

## With Debug Mode (Development)

If you want debug mode with auto-reload:

```bash
export FLASK_ENV=development
cd /Users/admin/Projects/krazio-email
source venv/bin/activate
python app.py
```

**Note:** Debug mode may show harmless warnings about semaphore cleanup - this is normal and doesn't affect functionality.

## Stop the App

Press `Ctrl+C` in the terminal, or:

```bash
pkill -f "python.*app.py"
```

## Production Mode

For production, use Gunicorn:

```bash
source venv/bin/activate
gunicorn app:app --bind 0.0.0.0:5001 --workers 2
```

Or use the gunicorn config:

```bash
gunicorn --config gunicorn_config.py app:app
```

## Troubleshooting

### Port Already in Use

If port 5001 is busy:

```bash
# Find what's using the port
lsof -i :5001

# Kill the process
kill -9 <PID>

# Or use a different port
export PORT=5002
python app.py
```

### Multiple Processes Running

Clean up all Flask processes:

```bash
pkill -f "python.*app.py"
sleep 1
# Then start fresh
```

