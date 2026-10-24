"""CSG-Branding für RustDesk: Server, Schlüssel, Programmname, Symbole und Logo.

Aufruf im Quellcode-Ordner von RustDesk (vom Workflow csg-build.yml):  python3 csg-kit/csg/apply.py .
Die Werte stehen in csg/settings.json (von der Serviceplattform beim Herunterladen des Baukastens eingetragen).
"""
import json
import re
import shutil
import sys
from pathlib import Path

KIT = Path(__file__).resolve().parent
SRC = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
cfg = json.loads((KIT / "settings.json").read_text(encoding="utf-8"))
app, product, server, key = cfg["app_name"], cfg["product_name"], cfg["server"], cfg["key"]
if not re.fullmatch(r"[A-Za-z0-9]{2,40}", app):
    sys.exit("app_name darf nur Buchstaben und Ziffern enthalten")
if "{{" in server or "{{" in key or not server or not key:
    sys.exit("settings.json: Server und Schlüssel fehlen – Baukasten aus der Serviceplattform verwenden")


def patch(rel: str, pairs: list[tuple[str, str]], regex: bool = False) -> None:
    path = SRC / rel
    text = path.read_text(encoding="utf-8")
    for old, new in pairs:
        if regex:
            text, n = re.subn(old, new, text)
        else:
            n = text.count(old)
            text = text.replace(old, new)
        if n == 0:
            sys.exit(f"{rel}: Stelle nicht gefunden: {old}")
    path.write_text(text, encoding="utf-8")
    print(f"angepasst: {rel}")


# 1. Server, Schlüssel und Name fest einbauen (libs/hbb_common/src/config.rs)
patch("libs/hbb_common/src/config.rs", [
    (r'pub const RENDEZVOUS_SERVERS: &\[&str\] = &\[[^\]]*\];', f'pub const RENDEZVOUS_SERVERS: &[&str] = &["{server}"];'),
    (r'pub const RS_PUB_KEY: &str = "[^"]*";', f'pub const RS_PUB_KEY: &str = "{key}";'),
    (r'pub static ref APP_NAME: RwLock<String> = RwLock::new\("RustDesk"\.to_owned\(\)\);',
     f'pub static ref APP_NAME: RwLock<String> = RwLock::new("{app}".to_owned());'),
    # eigener Server gilt nicht als „öffentlicher Server“ (sonst Hinweis „richten Sie Ihren eigenen Server ein“)
    (r'pub static ref PROD_RENDEZVOUS_SERVER: RwLock<String> = RwLock::new\("".to_owned\(\)\);',
     f'pub static ref PROD_RENDEZVOUS_SERVER: RwLock<String> = RwLock::new("{server}".to_owned());'),
], regex=True)

# 1b. QuickSupport: Heißt die Programmdatei „…QuickSupport…“, startet das Programm im kompakten Modus
#     „nur eingehend“ (wie TeamViewer QuickSupport). Installiertes Programm und Techniker bleiben unverändert.
patch("src/common.rs", [(
    "pub fn load_custom_client() {\n",
    "pub fn load_custom_client() {\n"
    "    #[cfg(windows)]\n"
    "    {\n"
    "        let csg_name = std::env::var(PORTABLE_APPNAME_RUNTIME_ENV_KEY)\n"
    "            .ok()\n"
    "            .or_else(|| std::env::current_exe().ok().map(|p| p.to_string_lossy().to_string()))\n"
    "            .unwrap_or_default()\n"
    "            .to_lowercase();\n"
    "        if csg_name.contains(\"quicksupport\") {\n"
    "            config::HARD_SETTINGS\n"
    "                .write()\n"
    "                .unwrap()\n"
    "                .insert(\"conn-type\".to_owned(), \"incoming\".to_owned());\n"
    "        }\n"
    "    }\n",
)])

# 2. Windows-Programm: Name in Fenster und Dateiinfo
patch("flutter/windows/runner/main.cpp", [('std::wstring app_name = L"RustDesk";', f'std::wstring app_name = L"{app}";')])
patch("flutter/windows/runner/Runner.rc", [
    ('VALUE "FileDescription", "RustDesk Remote Desktop" "\\0"', f'VALUE "FileDescription", "{product}" "\\0"'),
    ('VALUE "ProductName", "RustDesk" "\\0"', f'VALUE "ProductName", "{product}" "\\0"'),
])

# 3. Symbole und Logo
copies = {
    "icon.ico": ["res/icon.ico", "flutter/windows/runner/resources/app_icon.ico"],
    "tray-icon.ico": ["res/tray-icon.ico"],
    "icon.png": ["res/icon.png", "flutter/assets/icon.png"],
    "32x32.png": ["res/32x32.png"],
    "64x64.png": ["res/64x64.png"],
    "128x128.png": ["res/128x128.png"],
    "icon-512.png": ["res/128x128@2x.png"],
    "logo.png": ["flutter/assets/logo.png"],
    "logo_light.png": ["flutter/assets/logo_light.png"],
    "logo_dark.png": ["flutter/assets/logo_dark.png"],
}
for source, targets in copies.items():
    for target in targets:
        dest = SRC / target
        if dest.parent.is_dir():
            shutil.copyfile(KIT / source, dest)
            print(f"kopiert: {source} -> {target}")
print(f"Fertig: {product} ({app}), Server {server}")
