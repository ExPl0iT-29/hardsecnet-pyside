import sqlite3, json

db = sqlite3.connect(r'e:\T\hardsecnet\hardsecnet-pyside\runtime\hardsecnet.db')
c = db.cursor()
c.execute('SELECT name, payload FROM profiles')
profiles = []
for row in c.fetchall():
    p = json.loads(row[1])
    name = p.get('name', '').lower()
    if any(k in name for k in ['password', 'usb', 'workstation', 'attachment']):
        profiles.append(p)

for p in profiles:
    print(f"Profile: {p['name']}")
    print(f"Benchmarks: {', '.join(p['benchmark_ids'])}\n")
