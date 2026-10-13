import json, os, pathlib, secrets
d=pathlib.Path.home()/".config"/"termux-ai-bridge"; d.mkdir(parents=True,exist_ok=True); os.chmod(d,0o700)
default=str(pathlib.Path.home()/"projects")
root=pathlib.Path(input(f"Project root [{default}]: ").strip() or default).expanduser()
root.mkdir(parents=True,exist_ok=True); root=root.resolve()
(d/"token").write_text(secrets.token_urlsafe(36)+"\n"); os.chmod(d/"token",0o600)
(d/"config.json").write_text(json.dumps({"project_root":str(root)},indent=2)+"\n"); os.chmod(d/"config.json",0o600)
print("Setup complete. Token stored privately; it was not printed. Root:",root)
