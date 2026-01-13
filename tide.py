#!/usr/bin/env python3
"""
Moonee Beach Tide CLI
Fetches and displays tide information from WillyWeather
"""

import sys
from datetime import datetime
from typing import List, Dict, Optional
import requests
from bs4 import BeautifulSoup
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text

# Constants
TIDE_URL = "https://tides.willyweather.com.au/nsw/mid-north-coast/moonee-beach.html"
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"

console = Console()


def fetch_tide_data() -> Optional[str]:
    """Fetch the HTML content from WillyWeather."""
    try:
        headers = {"User-Agent": USER_AGENT}
        response = requests.get(TIDE_URL, headers=headers, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        console.print(f"[red]Error fetching tide data: {e}[/red]")
        return None


def parse_tide_data(html: str) -> List[Dict]:
    """Parse tide information from HTML."""
    soup = BeautifulSoup(html, "lxml")
    tides = []
    
    try:
        # Find today's tide section (first li with class="day")
        today_section = soup.find("li", class_="day")
        
        if not today_section:
            console.print("[red]Could not find tide data on the page.[/red]")
            return []
        
        # Find all tide points within today
        tide_points = today_section.find_all("li", class_=lambda x: x and ("point-high" in x or "point-low" in x))
        
        for point in tide_points:
            # Determine if high or low tide
            point_classes = point.get("class", [])
            tide_type = "HIGH" if "point-high" in point_classes else "LOW"
            
            # Extract time from h3 tag
            time_elem = point.find("h3")
            if not time_elem:
                continue
            
            time_str = time_elem.get_text(strip=True)
            
            # Extract height from span tag
            height_elem = point.find("span")
            if not height_elem:
                continue
            
            height_str = height_elem.get_text(strip=True)
            
            # Parse time to compare with current time
            try:
                tide_time = datetime.strptime(time_str, "%I:%M %p")
                # Set to today's date
                now = datetime.now()
                tide_time = tide_time.replace(year=now.year, month=now.month, day=now.day)
            except ValueError:
                # If parsing fails, try alternative format without space
                try:
                    tide_time = datetime.strptime(time_str, "%I:%M%p")
                    now = datetime.now()
                    tide_time = tide_time.replace(year=now.year, month=now.month, day=now.day)
                except ValueError:
                    tide_time = None
            
            tides.append({
                "time_str": time_str,
                "time": tide_time,
                "height": height_str,
                "type": tide_type
            })
    
    except Exception as e:
        console.print(f"[red]Error parsing tide data: {e}[/red]")
        return []
    
    return tides


def find_next_high_tide(tides: List[Dict]) -> Optional[int]:
    """Find the index of the next high tide."""
    now = datetime.now()
    
    for i, tide in enumerate(tides):
        if tide["type"] == "HIGH" and tide["time"] and tide["time"] > now:
            return i
    
    # If no future high tide today, return None
    return None


def display_tides(tides: List[Dict]):
    """Display tide information with the next high tide highlighted."""
    if not tides:
        console.print("[yellow]No tide data available.[/yellow]")
        return
    
    # Get current date
    now = datetime.now()
    date_str = now.strftime("%A, %b %d %Y")
    
    # Find next high tide
    next_high_idx = find_next_high_tide(tides)
    
    # Create title
    title = Text(f"Moonee Beach Tides - {date_str}", style="bold cyan")
    
    # Create table
    table = Table(show_header=False, box=None, padding=(0, 1))
    table.add_column("Indicator", style="yellow", width=3)
    table.add_column("Time", style="white", width=10)
    table.add_column("Type", width=6)
    table.add_column("Height", style="cyan", width=8)
    table.add_column("Marker", style="bold green", width=15)
    
    for i, tide in enumerate(tides):
        indicator = "→" if i == next_high_idx else " "
        
        # Style based on tide type
        if tide["type"] == "HIGH":
            type_style = "bold white"
            type_text = "HIGH"
        else:
            type_style = "dim white"
            type_text = "low"
        
        marker = "← NEXT HIGH" if i == next_high_idx else ""
        
        table.add_row(
            indicator,
            tide["time_str"],
            Text(type_text, style=type_style),
            tide["height"],
            marker
        )
    
    # Display in a panel
    console.print()
    console.print(Panel(table, title=title, border_style="blue"))
    console.print()
    
    # Show next high tide summary
    if next_high_idx is not None:
        next_high = tides[next_high_idx]
        summary = Text()
        summary.append("Next High Tide: ", style="bold")
        summary.append(f"{next_high['time_str']}", style="bold green")
        summary.append(f" ({next_high['height']})", style="cyan")
        console.print(summary)
        console.print()
    else:
        console.print("[yellow]No more high tides today. Check tomorrow![/yellow]")
        console.print()


def main():
    """Main entry point."""
    console.print("[dim]Fetching tide data for Moonee Beach...[/dim]")
    
    # Fetch data
    html = fetch_tide_data()
    if not html:
        sys.exit(1)
    
    # Parse data
    tides = parse_tide_data(html)
    if not tides:
        console.print("[red]Failed to parse tide data. The website structure may have changed.[/red]")
        sys.exit(1)
    
    # Display
    display_tides(tides)


if __name__ == "__main__":
    main()
