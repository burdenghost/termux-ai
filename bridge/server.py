import json, subprocess, sys
from http.server import BaseHTTPRequestHandler, HTTPServer
from common import load_config, load_token, safe_path
HOST,PORT="127.0.0.1",8765
def fixed(argv,root,timeout=20):
 p=subprocess.run(argv,cwd=str(root),capture_output=True,text=True,timeout=timeout,shell=False)
 return {"exit_code":p.returncode,"output":(p.stdout+"\n"+p.stderr).strip()[:12000]}
class H(BaseHTTPRequestHandler):
 def log_message(self,fmt,*args): print("bridge:",fmt%args)
 def reply(self,status,obj):
  b=json.dumps(obj).encode(); self.send_response(status); self.send_header("Content-Type","application/json"); self.send_header("Cache-Control","no-store"); self.send_header("X-Content-Type-Options","nosniff"); self.send_header("Content-Length",str(len(b))); self.end_headers(); self.wfile.write(b)
 def do_POST(self):
  try:
   if self.client_address[0]!="127.0.0.1": return self.reply(403,{"error":"localhost only"})
   if self.headers.get("Authorization","")!="Bearer "+load_token(): return self.reply(401,{"error":"unauthorized"})
   if self.path!="/v1/action": return self.reply(404,{"error":"not found"})
   n=int(self.headers.get("Content-Length","0"))
   if n<1 or n>4096: return self.reply(413,{"error":"invalid request size"})
   q=json.loads(self.rfile.read(n)); a=q.get("action"); root=load_config()
   if a=="health": r={"ok":True,"project_root":str(root),"actions":["health","list_files","read_file","git_status","run_tests"]}
   elif a=="list_files":
    rel=q.get("path","."); p=safe_path(root,rel)
    if not p.is_dir(): return self.reply(400,{"error":"not a directory"})
    r={"path":rel,"entries":[{"name":x.name,"type":"directory" if x.is_dir() else "file"} for x in sorted(p.iterdir(),key=lambda x:x.name.lower()) if not x.is_symlink()][:200]}
   elif a=="read_file":
    rel=q.get("path",""); p=safe_path(root,rel)
    if not p.is_file(): return self.reply(400,{"error":"not a regular file"})
    if p.stat().st_size>200000: return self.reply(413,{"error":"file exceeds 200 KB"})
    b=p.read_bytes()
    if b"\x00" in b[:8192]: return self.reply(415,{"error":"binary file"})
    r={"path":rel,"content":b.decode("utf-8",errors="replace")}
   elif a=="git_status": r=fixed(["git","status","--short","--branch"],root)
   elif a=="run_tests":
    if not safe_path(root,"tests").is_dir(): return self.reply(400,{"error":"No tests/ directory"})
    r=fixed([sys.executable,"-m","unittest","discover","-s","tests","-v"],root,60)
   else: return self.reply(400,{"error":"action not allowlisted"})
   self.reply(200,r)
  except subprocess.TimeoutExpired: self.reply(408,{"error":"action timed out"})
  except (ValueError,KeyError,json.JSONDecodeError) as e: self.reply(400,{"error":str(e)})
  except Exception as e: self.reply(500,{"error":type(e).__name__})
if __name__=="__main__":
 print("Localhost-only bridge at http://127.0.0.1:8765; Ctrl+C to stop")
 HTTPServer((HOST,PORT),H).serve_forever()
