# huol_url/core.py
import os
import json
from pathlib import Path
from datetime import datetime

# ============ إعدادات ============
FOLDER_NAME = "Huol Url"
JSON_FILENAME = "links.json"

# ============ واجهة البداية ============
BANNER = r"""
    ██╗  ██╗██╗   ██╗ ██████╗ ██╗
    ██║  ██║██║   ██║██╔═══██╗██║
    ███████║██║   ██║██║   ██║██║
    ██╔══██║██║   ██║██║   ██║██║
    ██║  ██║╚██████╔╝╚██████╔╝███████╗
    ╚═╝  ╚═╝ ╚═════╝  ╚═════╝ ╚══════╝
        🔗  Huol Url  •  Link Manager
"""

def _c(text, color_code):
    """تلوين نص في الطرفية"""
    return f"\033[{color_code}m{text}\033[0m"

def _cyan(t):   return _c(t, "96")
def _green(t):  return _c(t, "92")
def _yellow(t): return _c(t, "93")
def _red(t):    return _c(t, "91")
def _dim(t):    return _c(t, "90")
def _bold(t):   return _c(t, "1")

def print_banner():
    """طباعة الواجهة الجمالية"""
    print(_cyan(BANNER))
    print(_dim("─" * 55))
    print(f"  {_green('✓')} الإصدار    : {_bold('0.2.0')}")
    print(f"  {_green('✓')} الحالة     : {_bold('جاهز للعمل')}")
    print(_dim("─" * 55))

def print_status():
    """طباعة حالة المكتبة (المجلد + عدد الروابط)"""
    folder, json_file = get_folder_path(), get_json_path()
    exists_folder = folder.exists()
    exists_json = json_file.exists()
    count = len(load_links()) if exists_json else 0

    print(f"  {_green('📁')} المجلد     : {_bold(str(folder))}  {_green('موجود') if exists_folder else _red('غير موجود')}")
    print(f"  {_green('📄')} الملف      : {_bold(str(json_file))}  {_green('موجود') if exists_json else _red('غير موجود')}")
    print(f"  {_green('🔗')} الروابط    : {_yellow(str(count))} رابط محفوظ")
    print(_dim("─" * 55))
    print(f"  {_dim('للاستخدام: huol_url.add_links([...])  أو  huol_url.extract_and_store(path)')}")
    print(_dim("─" * 55))
    print()

# ============ تحديد مسار التخزين ============
def get_storage_path():
    """
    مسار التخزين المناسب:
    - Termux/Android: /sdcard أو /storage/emulated/0
    - غير ذلك: مجلد المستخدم الرئيسي
    """
    android_paths = [
        "/sdcard",
        "/storage/emulated/0",
        os.path.expanduser("~/storage/shared"),
    ]
    for p in android_paths:
        if os.path.isdir(p) and os.access(p, os.W_OK):
            return Path(p)
    return Path.home()

def get_folder_path():
    return get_storage_path() / FOLDER_NAME

def get_json_path():
    return get_folder_path() / JSON_FILENAME

# ============ إعداد المجلد والملف ============
def ensure_setup():
    """إنشاء المجلد وملف JSON إن لم يكونا موجودين"""
    folder = get_folder_path()
    folder.mkdir(parents=True, exist_ok=True)

    json_file = get_json_path()
    if not json_file.exists():
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(
                {"links": [], "created_at": datetime.now().isoformat()},
                f,
                ensure_ascii=False,
                indent=2,
            )
    return folder, json_file

# ============ عمليات JSON ============
def _read_json():
    ensure_setup()
    with open(get_json_path(), "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {"links": []}

def _write_json(data):
    ensure_setup()
    with open(get_json_path(), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load_links():
    """قراءة قائمة الروابط المحفوظة"""
    return _read_json().get("links", [])

def save_links(links):
    """حفظ قائمة الروابط"""
    data = _read_json()
    data["links"] = sorted(set(links))
    data["updated_at"] = datetime.now().isoformat()
    _write_json(data)

def add_links(new_links):
    """
    إضافة روابط جديدة مع منع التكرار.
    Returns: عدد الروابط المضافة فعلياً
    """
    existing = set(load_links())
    added = 0
    for link in new_links:
        link = link.strip()
        if link and link not in existing:
            existing.add(link)
            added += 1
    save_links(sorted(existing))
    return added

def remove_link(url):
    """حذف رابط واحد. Returns: True إذا حُذف، False إذا لم يوجد."""
    links = load_links()
    if url in links:
        links.remove(url)
        save_links(links)
        return True
    return False

def clear_links():
    """مسح كل الروابط مع الاحتفاظ بالملف"""
    save_links([])

def stats():
    """إحصائيات سريعة عن الروابط"""
    links = load_links()
    by_proto = {}
    for l in links:
        proto = l.split("://", 1)[0] + "://" if "://" in l else "other"
        by_proto[proto] = by_proto.get(proto, 0) + 1
    return {
        "total": len(links),
        "by_protocol": by_proto,
    }

# ============ استخراج الروابط من أي سكربت ============
def extract_and_store(path):
    """
    يقرأ ملف سكربت (أي لغة) أو مجلداً،
    يستخرج كل الروابط، ويضيفها إلى links.json.
    """
    from .extractor import extract_links_from_path

    found = extract_links_from_path(path)
    all_links = sorted({link for links in found.values() for link in links})
    added = add_links(all_links)

    return {
        "files_processed": len(found),
        "links_found": len(all_links),
        "links_added": added,
        "details": found,
    }

# ============ واجهة الطرفية (اختياري) ============
def show():
    """طباعة الواجهة الكاملة والحالة الحالية"""
    print_banner()
    print_status()
