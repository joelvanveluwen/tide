# Moonee Beach Tide CLI - Setup Complete! 🌊

Your tide CLI has been successfully installed and configured!

## What Was Created

1. **tide.py** - Main Python script that fetches and displays tide data
2. **requirements.txt** - Python dependencies
3. **README.md** - Complete documentation
4. **venv/** - Python virtual environment with all dependencies installed
5. **.gitignore** - Git ignore file to keep your repo clean

## Quick Start

### Option 1: Use the `tide` alias (Recommended)

The alias has been added to your `~/.zshrc`. To activate it:

```bash
source ~/.zshrc
```

Then simply run:
```bash
tide
```

### Option 2: Run directly

```bash
/Users/jvanvelu/Projects/tide/venv/bin/python /Users/jvanvelu/Projects/tide/tide.py
```

## Example Output

```
Fetching tide data for Moonee Beach...

╭───────────────── Moonee Beach Tides - Tuesday, Jan 13 2026 ──────────────────╮
│       5:16 am     HIGH    1.36m                                              │
│       11:47 am    low     0.64m                                              │
│  →    5:02 pm     HIGH    1.01m     ← NEXT HIGH                              │
│       11:01 pm    low     0.44m                                              │
╰──────────────────────────────────────────────────────────────────────────────╯

Next High Tide: 5:02 pm (1.01m)
```

## Features

✅ Shows all of today's tides (high and low)
✅ Highlights the next upcoming high tide
✅ Beautiful, colorful terminal output
✅ Real-time data from WillyWeather
✅ Fast and lightweight

## Need Help?

Check the README.md for more details, troubleshooting, and configuration options.

Enjoy your tide tracking! 🏄‍♂️
