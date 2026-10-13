import json, pathlib
APP_DIR=pathlib.Path.home()/".config"/"termux-ai-bridge"
CONFIG_PATH=APP_DIR/"config.json"
TOKEN_PATH=APP_DIR/"token"
def load_config():
    return pathlib.Path(json.loads(CONFIG_PATH.read_text())["project_root"]).expanduser().resolve()
def load_token():
    t=TOKEN_PATH.read_text().strip()
    if len(t)<32: raise RuntimeError("Bridge token missing; run bridge/setup.py")
    return t
def safe_path(root, relative):
    if not isinstance(relative,str) or not relative or "\x00" in relative: raise ValueError("relative path required")
    p=(root/relative).resolve()
    if p!=root and root not in p.parents: raise ValueError("path escapes project root")
    if p.is_symlink(): raise ValueError("symlinks not allowed")
    return p
