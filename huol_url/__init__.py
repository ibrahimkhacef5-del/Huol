# huol_url/__init__.py
from .core import (
    ensure_setup,
    load_links,
    save_links,
    add_links,
    clear_links,
    get_folder_path,
    get_json_path,
)

# إنشاء المجلد وملف JSON تلقائياً عند أول استيراد
ensure_setup()

__version__ = "0.1.0"
__all__ = [
    "ensure_setup",
    "load_links",
    "save_links",
    "add_links",
    "clear_links",
    "get_folder_path",
    "get_json_path",
]
