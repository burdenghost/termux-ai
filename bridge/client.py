import json,sys,urllib.request,urllib.error
from common import load_token
A={"health":{"action":"health"},"list":{"action":"list_files","path":"."},"git-status":{"action":"git_status"},"tests":{"action":"run_tests"}}
def main():
 if len(sys.argv)<2: print("Usage: client.py health|list|git-status|tests|read RELATIVE_PATH"); return 2
 c=sys.argv[1]
 if c=="read" and len(sys.argv)==3: p={"action":"read_file","path":sys.argv[2]}
 elif c in A and len(sys.argv)==2: p=A[c]
 else: print("Unsupported action/arguments"); return 2
 req=urllib.request.Request("http://127.0.0.1:8765/v1/action",data=json.dumps(p).encode(),headers={"Content-Type":"application/json","Authorization":"Bearer "+load_token()},method="POST")
 try:
  with urllib.request.urlopen(req,timeout=65) as r: print(json.dumps(json.loads(r.read()),indent=2))
 except urllib.error.HTTPError as e: print("HTTP",e.code,e.read().decode(errors="replace")); return 1
 except Exception as e: print("Connection failed:",type(e).__name__,str(e)); return 1
 return 0
if __name__=="__main__": raise SystemExit(main())
