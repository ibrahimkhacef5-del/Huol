# huol_url/__init__.py
import os

from .core import (
    ensure_setup,
    load_links,
    save_links,
    add_links,
    remove_link,
    clear_links,
    stats,
    get_folder_path,
    get_json_path,
    get_storage_path,
    extract_and_store,
    print_banner,
    print_status,
    show,
)
from .extractor import (
    extract_links_from_text,
    extract_links_from_file,
    extract_links_from_path,
)

# إنشاء المجلد والملف تلقائياً
ensure_setup()

# عرض الواجهة مرة واحدة فقط عند أول استيراد
if os.environ.get("HUOL_URL_SILENT") != "1":
    show()
    os.environ["HUOL_URL_SILENT"] = "1"

__version__ = "0.2.0"
__all__ = [
    "ensure_setup", "load_links", "save_links", "add_links",
    "remove_link", "clear_links", "stats",
    "get_folder_path", "get_json_path", "get_storage_path",
    "extract_and_store",
    "extract_links_from_text", "extract_links_from_file", "extract_links_from_path",
    "print_banner", "print_status", "show",
]
