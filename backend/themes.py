"""
Theme management for NoteDiscovery
"""

from pathlib import Path
from typing import List, Dict
import re


def get_available_themes(themes_dir: str) -> List[Dict[str, str]]:
    """Get all available themes from the themes directory"""
    themes_path = Path(themes_dir)
    themes = []
    
    # Theme icons/emojis mapping
    theme_icons = {
        "light": "🌞",
        "dark": "🌙",
        "dracula": "🧛",
        "nord": "❄️",
        "monokai": "🎞️",
        "vue-high-contrast": "💚",
        "cobalt2": "🌊",
        "vs-blue": "🔷",
        "retro-dark": "🚀"
    }
    
    # Load all themes from themes folder
    if themes_path.exists():
        for theme_file in themes_path.glob("*.css"):
            theme_name = theme_file.stem.replace("-", " ").replace("_", " ").title()
            icon = theme_icons.get(theme_file.stem, "🎨")
            
            themes.append({
                "id": theme_file.stem,
                "name": f"{icon} {theme_name}",
                "builtin": False
            })
    
    return themes


def get_theme_css(themes_dir: str, theme_id: str) -> str:
    """Get the CSS content for a specific theme"""
    theme_path = Path(themes_dir) / f"{theme_id}.css"
    
    if not theme_path.exists():
        return ""
    
    with open(theme_path, 'r', encoding='utf-8') as f:
        return f.read()

