# Moonee Beach Tide CLI 🌊

A simple Python CLI tool to check tide times for Moonee Beach, NSW, Australia.

## Features

- **Current tide status** - shows estimated height, rising/falling direction, and time to next tide
- Displays all of today's tide times and heights
- Highlights the next upcoming high tide
- Clean, colorful terminal output
- Fast and lightweight

## Installation

1. **Clone or navigate to the project directory:**
   ```bash
   cd /Users/jvanvelu/Projects/tide
   ```

2. **Create a virtual environment:**
   ```bash
   python3 -m venv venv
   ```

3. **Activate the virtual environment and install dependencies:**
   ```bash
   source venv/bin/activate
   pip install -r requirements.txt
   ```

4. **Make the script executable:**
   ```bash
   chmod +x tide.py
   ```

## Usage

### Run directly (with venv activated):
```bash
cd /Users/jvanvelu/Projects/tide
source venv/bin/activate
python tide.py
```

### Or run without activating venv:
```bash
/Users/jvanvelu/Projects/tide/venv/bin/python /Users/jvanvelu/Projects/tide/tide.py
```

### Set up the `tide` alias for easy access:

The alias has been automatically added to your `~/.zshrc`. Just reload your shell:

```bash
source ~/.zshrc  # or source ~/.bashrc
```

Now you can run from anywhere:
```bash
tide
```

(If you prefer a different alias name, you can edit `~/.zshrc` and change the alias)

## Example Output

```
Fetching tide data for Moonee Beach...

╭──────────────────── 🌊 Right Now ────────────────────╮
│   Current: 1.11m ↓ Falling                           │
│   high [░░░░░░░▓░░░░░░░░░░░░] low  (4h 9m to low)    │
╰──────────────────────────────────────────────────────╯

╭───────── Moonee Beach Tides - Thursday, Jan 15 2026 ─────────╮
│       6:54 am     HIGH    1.52m                               │
│       1:42 pm     low     0.46m                               │
│  →    7:07 pm     HIGH    1.03m     ← NEXT HIGH               │
╰───────────────────────────────────────────────────────────────╯

Next High Tide: 7:07 pm (1.03m)
```

## Data Source

Tide data is scraped from [WillyWeather](https://tides.willyweather.com.au/nsw/mid-north-coast/moonee-beach.html). But to be fair they just take the data from gov funded BoM.

## Requirements

- Python 3.7+
- Internet connection
- Dependencies listed in `requirements.txt`

## Troubleshooting

**"Error fetching tide data"**
- Check your internet connection
- Ensure WillyWeather website is accessible

**"Failed to parse tide data"**
- The website structure may have changed
- Try updating the script or report an issue

## License

Free to use and modify as needed.
