#!/usr/bin/env python3
"""Bounded GET probes; 403s are recorded once, never bypassed."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import urllib.error
import urllib.request

p=argparse.ArgumentParser()
p.add_argument("ledger")
p.add_argument("--out",required=True)
p.add_argument("--cache")
a=p.parse_args()
records=[]
for entry in json.loads(Path(a.ledger).read_text()):
    url=entry["url"]
    record={**entry,"checked_at":datetime.now(timezone.utc).isoformat(),"route":"executor HTTP proxy","visually_inspected":False}
    if not url.startswith(("https://","http://")):
        record.update(status="invalid_scheme"); records.append(record); continue
    try:
        req=urllib.request.Request(url,headers={"User-Agent":"ResearchDesignStudio/1.0"})
        with urllib.request.urlopen(req,timeout=15) as response:
            mime=response.headers.get("Content-Type","")
            body=response.read(8_000_001)
            record.update(http=response.status,mime=mime,bytes=len(body),sha256=hashlib.sha256(body).hexdigest(),final_url=response.url)
            if len(body)>8_000_000: record["status"]="too_large"
            elif mime.startswith("image/"):
                record["status"]="image_accessed"
                if a.cache:
                    d=Path(a.cache);d.mkdir(parents=True,exist_ok=True)
                    f=d/(record["sha256"]+".img");f.write_bytes(body);record["cache_path"]=str(f)
            else: record["status"]="text_accessed"
    except (urllib.error.URLError,TimeoutError,OSError) as e:
        record.update(status="blocked_or_unavailable",error=str(e)[:250])
    records.append(record)
Path(a.out).parent.mkdir(parents=True,exist_ok=True)
Path(a.out).write_text(json.dumps(records,ensure_ascii=False,indent=2))
print(json.dumps({"checked":len(records),"accessible":sum(x["status"] in ("text_accessed","image_accessed") for x in records),"out":a.out}))
