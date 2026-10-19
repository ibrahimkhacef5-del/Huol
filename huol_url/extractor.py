# huol_url/extractor.py
import os
import re

# البروتوكولات المدعومة (يمكنك التوسيع)
PROTOCOLS = (
    "http://", "https://",
    "ssh://", "sftp://", "ftp://", "ftps://",
    "git://", "ws://", "wss://",
)

# تعبير منتظم يلتقط الروابط مهما كانت اللغة
# يتوقف عند علامات الاقتباس أو المسافة أو نهاية السطر
LINK_REGEX = re.compile(
    r"""(?:%s)[^\s"'<>\)\]\}]+""" % "|".join(re.escape(p) for p in PROTOCOLS),
    re.IGNORECASE,
)

# امتدادات الملفات النصية المدعومة (يعمل فعلياً على أي ملف نصي)
TEXT_EXTENSIONS = {
    ".py", ".js", ".ts", ".jsx", ".tsx", ".html", ".htm", ".css",
    ".sh", ".bash", ".zsh", ".fish", ".php", ".rb", ".go", ".rs",
    ".java", ".kt", ".c", ".cpp", ".h", ".hpp", ".cs", ".swift",
    ".json", ".yaml", ".yml", ".toml", ".xml", ".md", ".txt",
    ".env", ".ini", ".cfg", ".conf", ".sql", ".lua", ".pl",
}


def extract_links_from_text(text):
    """استخراج الروابط من نص خام"""
    return sorted(set(LINK_REGEX.findall(text)))


def extract_links_from_file(filepath):
    """استخراج الروابط من ملف واحد (أي لغة)"""
    if not os.path.isfile(filepath):
        raise FileNotFoundError(f"الملف غير موجود: {filepath}")

    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        text = f.read()

    return extract_links_from_text(text)


def extract_links_from_path(path):
    """
    استخراج الروابط من:
    - ملف واحد (أي امتداد)
    - أو مجلد (يمر على كل الملفات النصية داخله)

    Returns:
        dict: {اسم_الملف_أو_المسار: [قائمة_الروابط]}
    """
    results = {}

    if os.path.isfile(path):
        results[path] = extract_links_from_file(path)
        return results

    if os.path.isdir(path):
        for root, _, files in os.walk(path):
            for fname in files:
                ext = os.path.splitext(fname)[1].lower()
                # معالجة الملفات النصية المعروفة أو التي بدون امتداد
                if ext in TEXT_EXTENSIONS or ext == "":
                    fpath = os.path.join(root, fname)
                    try:
                        links = extract_links_from_file(fpath)
                        if links:
                            results[fpath] = links
                    except Exception:
                        continue
        return results

    raise FileNotFoundError(f"المسار غير موجود: {path}")
