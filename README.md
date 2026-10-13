# Termux AI Core & Bridge

A cloud-first AI CLI plus a deliberately restricted local Termux bridge.

## Status
Prototype v0.1.0. Tests run in the development environment; Android-device installation and live API calls must still be verified on-device.

## Components
- `core/`: cloud AI CLI starter
- `bridge/`: localhost-only authenticated file/status/test interface
- `tests/`: safety tests
- `termux-ai-bridge-v0.1.0.zip`: downloadable starter package is available in the ChatGPT conversation where this repo was initiated.

## Bridge install (Termux)
```bash
pkg update
pkg install python git
git clone https://github.com/burdenghost/termux-ai.git
cd termux-ai
python -m unittest discover -s tests -v
python bridge/setup.py
python bridge/server.py
```

The bridge binds only to 127.0.0.1:8765. In another Termux session:
```bash
python bridge/client.py health
python bridge/client.py list
python bridge/client.py git-status
python bridge/client.py tests
```

Set a project root when setup asks. The root must be a Git repository for `git-status` to return a repository status; otherwise it returns Git's normal “not a repository” error.

## Security
- No arbitrary shell command endpoint.
- Only fixed actions: health, list files, read a UTF-8 file, git status, and Python unittest discovery.
- Random bearer token stored under `~/.config/termux-ai-bridge/token` with owner-only permissions.
- Files are confined to the selected project root; read size capped at 200 KB.
- Never expose the service to LAN/public internet or share the token.
- File reads may expose private source code. Review output before pasting it into a chat.
- This local service does NOT automatically connect ChatGPT to your phone. Remote access requires a separately designed, authenticated relay.

## License
MIT
