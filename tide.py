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


def get_current_tide_status(tides: List[Dict]) -> Optional[Dict]:
    """Calculate the current tide status based on surrounding tides."""
    if len(tides) < 2:
        return None
    
    now = datetime.now()
    
    # Find the two tides we're between (previous and next)
    prev_tide = None
    next_tide = None
    
    for i, tide in enumerate(tides):
        if tide["time"] is None:
            continue
        
        if tide["time"] <= now:
            prev_tide = tide
        elif tide["time"] > now and next_tide is None:
            next_tide = tide
            break
    
    # If we don't have both surrounding tides, we can't calculate
    if prev_tide is None or next_tide is None:
        return None
    
    # Calculate progress between the two tides
    total_duration = (next_tide["time"] - prev_tide["time"]).total_seconds()
    elapsed = (now - prev_tide["time"]).total_seconds()
    progress = elapsed / total_duration if total_duration > 0 else 0
    
    # Parse heights as floats
    try:
        prev_height = float(prev_tide["height"].replace("m", ""))
        next_height = float(next_tide["height"].replace("m", ""))
    except (ValueError, AttributeError):
        return None
    
    # Calculate current estimated height (simple linear interpolation)
    current_height = prev_height + (next_height - prev_height) * progress
    
    # Determine if rising or falling
    is_rising = next_tide["type"] == "HIGH"
    direction = "Rising" if is_rising else "Falling"
    
    # Calculate time until next tide
    time_remaining = next_tide["time"] - now
    hours_remaining = time_remaining.total_seconds() / 3600
    
    return {
        "current_height": current_height,
        "direction": direction,
        "is_rising": is_rising,
        "progress": progress,
        "prev_tide": prev_tide,
        "next_tide": next_tide,
        "hours_remaining": hours_remaining
    }


def display_current_tide(tides: List[Dict]):
    """Display the current tide status."""
    status = get_current_tide_status(tides)
    
    if status is None:
        return
    
    # Build a visual tide indicator
    progress = status["progress"]
    bar_width = 20
    filled = int(progress * bar_width)
    
    if status["is_rising"]:
        # Rising tide: low → high
        bar = "░" * filled + "▓" + "░" * (bar_width - filled - 1)
        direction_arrow = "↑"
        direction_color = "green"
    else:
        # Falling tide: high → low  
        bar = "░" * filled + "▓" + "░" * (bar_width - filled - 1)
        direction_arrow = "↓"
        direction_color = "blue"
    
    # Format time remaining
    hours = status["hours_remaining"]
    if hours >= 1:
        time_str = f"{int(hours)}h {int((hours % 1) * 60)}m"
    else:
        time_str = f"{int(hours * 60)}m"
    
    # Create the current tide display
    current_text = Text()
    current_text.append("  Current: ", style="bold")
    current_text.append(f"{status['current_height']:.2f}m ", style="bold cyan")
    current_text.append(f"{direction_arrow} {status['direction']} ", style=f"bold {direction_color}")
    
    progress_text = Text()
    progress_text.append("  ", style="")
    progress_text.append(f"{status['prev_tide']['type'].lower()} ", style="dim")
    progress_text.append(f"[{bar}]", style="cyan")
    progress_text.append(f" {status['next_tide']['type'].lower()}", style="dim")
    progress_text.append(f"  ({time_str} to {status['next_tide']['type'].lower()})", style="dim")
    
    console.print()
    console.print(Panel(
        Text.assemble(current_text, "\n", progress_text),
        title=Text("🌊 Right Now", style="bold yellow"),
        border_style="yellow",
        padding=(0, 1)
    ))


def display_tides(tides: List[Dict]):
    """Display tide information with the next high tide highlighted."""
    if not tides:
        console.print("[yellow]No tide data available.[/yellow]")
        return
    
    # Get current date
    now = datetime.now()
    date_str = now.strftime("%A, %b %d %Y")
    
    # Display current tide status first
    display_current_tide(tides)
    
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
