import re

lines = [
    "Failed password for invalid user admin from 192.168.1.15 port 22 ssh2",
    "Accepted password for root from 10.0.0.8 port 22 ssh2",
]

pattern = re.compile(r'(\w+) from ([\d\.]+)')

for line in lines:
    match = pattern.search(line)
    if match:
        print(match.groups())