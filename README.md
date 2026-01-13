# Moonee Beach Tide CLI 🌊

A simple Python CLI tool to check tide times for Moonee Beach, NSW, Australia.

## Features

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

╭─ Moonee Beach Tides - Monday, Jan 13 2026 ─╮
│                                             │
│     5:16 AM   HIGH   1.36m                  │
│    11:47 AM   low    0.64m                  │
│  →  5:02 PM   HIGH   1.01m   ← NEXT HIGH   │
│    11:01 PM   low    0.44m                  │
│                                             │
╰─────────────────────────────────────────────╯

Next High Tide: 5:02 PM (1.01m)
```

## Data Source

Tide data is scraped from [WillyWeather](https://tides.willyweather.com.au/nsw/mid-north-coast/moonee-beach.html).

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
