"""Read HUD/USDA .xlsx files after stripping broken core.xml timestamps."""
import re, zipfile
from pathlib import Path

def sanitized_xlsx(src, dest):
    src = Path(src)
    dest = Path(dest)
    dest.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(src) as zin, zipfile.ZipFile(dest, "w") as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            if item.filename == "docProps/core.xml":
                text = data.decode("utf-8", "replace")
                text = re.sub(r"<dcterms:modified[^>]*>[^<]*</dcterms:modified>", "", text)
                text = re.sub(r"<dcterms:created[^>]*>[^<]*</dcterms:created>", "", text)
                data = text.encode("utf-8")
            zout.writestr(item, data)
    return dest
