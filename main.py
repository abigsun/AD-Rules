import requests
import os
import re

def get_url(url):
    try:
        return requests.get(url, timeout=15).text
    except:
        return ""

def read_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def save_file(path, data):
    with open(path, "w", encoding="utf-8") as f:
        f.write(data)

os.makedirs("output", exist_ok=True)

# 合并所有规则
full = []
# 上游
for url in open("source.list","r").read().splitlines():
    u = url.strip()
    if u and not u.startswith("#"):
        full.append(get_url(u))
# 自定义黑白
full.append(read_file("custom/black.list"))
full.append(read_file("custom/white.list"))

# 去重、清理
all_lines = []
for txt in full:
    all_lines.extend(txt.splitlines())
unique = sorted(list(set(all_lines)))
out = [x for x in unique if x.strip() and not x.startswith("!")]

# 1. AdGuard 格式
save_file("output/adguard.txt", "\n".join(out))

# 2. Dnsmasq 格式
dns = []
for line in out:
    if line.startswith("||") and line.endswith("^"):
        dom = line[2:-1]
        dns.append(f"address=/{dom}/0.0.0.0")
save_file("output/dnsmasq.conf", "\n".join(dns))

# 3. Hosts 格式
hosts = []
for line in out:
    if line.startswith("||") and line.endswith("^"):
        dom = line[2:-1]
        hosts.append(f"0.0.0.0 {dom}")
save_file("output/hosts.txt", "\n".join(hosts))
