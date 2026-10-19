# huol_url/core.py
import os
import json
from pathlib import Path

# اسم المجلد وملف JSON
FOLDER_NAME = "Huol Url"
JSON_FILENAME = "links.json"

def get_storage_path():
    """
    تحديد مسار التخزين المناسب:
    - على Termux/Android: /sdcard أو /storage/emulated/0
    - على الحاسوب: مجلد المستخدم الرئيسي
    """
    # مسارات Android الشائعة
    android_paths = [
        "/sdcard",
        "/storage/emulated/0",
        os.path.expanduser("~/storage/shared"),  # Termux بعد termux-setup-storage
    ]
    for p in android_paths:
        if os.path.isdir(p) and os.access(p, os.W_OK):
            return Path(p)
    
    # fallback: المجلد الرئيسي للمستخدم
    return Path.home()

def get_folder_path():
    """إرجاع مسار مجلد Huol Url"""
    return get_storage_path() / FOLDER_NAME

def get_json_path():
    """إرجاع مسار ملف links.json"""
    return get_folder_path() / JSON_FILENAME

def ensure_setup():
    """
    إنشاء المجلد وملف JSON إن لم يكونا موجودين.
    يُستدعى تلقائياً عند الاستيراد أو عند كل عملية.
    """
    folder = get_folder_path()
    folder.mkdir(parents=True, exist_ok=True)
    
    json_file = get_json_path()
    if not json_file.exists():
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump({"links": []}, f, ensure_ascii=False, indent=2)
    
    return folder, json_file

def load_links():
    """قراءة الروابط المخزنة من ملف JSON"""
    ensure_setup()
    with open(get_json_path(), "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("links", [])

def save_links(links):
    """حفظ قائمة الروابط في ملف JSON"""
    ensure_setup()
    with open(get_json_path(), "w", encoding="utf-8") as f:
        json.dump({"links": links}, f, ensure_ascii=False, indent=2)

def add_links(new_links):
    """
    إضافة روابط جديدة مع إزالة التكرار.
    Returns: عدد الروابط المضافة فعلياً
    """
    existing = set(load_links())
    added = 0
    for link in new_links:
        if link not in existing:
            existing.add(link)
            added += 1
    save_links(sorted(existing))
    return added

def clear_links():
    """مسح كل الروابط"""
    save_links([])
