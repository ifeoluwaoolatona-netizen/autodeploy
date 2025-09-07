import re, json
from pathlib import Path

def improved_sniff(repo_dir):
    p = Path(repo_dir)
    info = {"app_type":"unknown","start_cmd":None,"port":None,"container":False,"detected_files":[]}
    
    for f in p.rglob('*'):
        if f.is_file() and f.name.lower() in ("package.json","requirements.txt","dockerfile","procfile"):
            info["detected_files"].append(str(f.relative_to(p)))
    
    if (p/"Dockerfile").exists():
        info["container"] = True
    
    pkg = p/"package.json"
    if pkg.exists():
        d = json.loads(pkg.read_text())
        scripts = d.get("scripts",{})
        if "start" in scripts: info["start_cmd"]=scripts["start"]
        info["app_type"]="node"
    
    req = p/"requirements.txt"
    if req.exists():
        txt = req.read_text().lower()
        if "flask" in txt: 
            info["app_type"]="flask"; info["port"]=5000
        if "django" in txt:
            info["app_type"]="django"; info["port"]=8000
    
    proc = p/"Procfile"
    if proc.exists():
        m = re.search(r'web:\s*(.+)', proc.read_text())
        if m: info["start_cmd"]=m.group(1).strip()
    
    return info
