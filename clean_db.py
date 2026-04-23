import sqlite3
import json

db_path = r'e:\T\hardsecnet\hardsecnet-pyside\runtime\hardsecnet.db'

# The 8 missing script IDs
missing_ids = {
    'CIS-Windows-Demo-ScreenSaverActive',
    'CIS-Windows-Demo-Autorun',
    'CIS-Windows-Demo-ZoneInformation',
    'CIS-Windows-Demo-FileExtensions',
    'CIS-Windows-Demo-ScreenSaverTimeout',
    'CIS-Windows-Workstation-FirewallPolicy',
    'CIS-Windows-Workstation-PasswordPolicy',
    'CIS-Windows-11-1.4.1'
}

target_profiles = [
    'Password And Locking', 
    'Password Expiry And Public Firewall', 
    'USB And Attachment Safety', 
    'Windows Workstation Hardening'
]

db = sqlite3.connect(db_path)
c = db.cursor()

c.execute('SELECT id, name, payload FROM profiles')
rows = c.fetchall()

updated_count = 0

for row in rows:
    profile_id = row[0]
    payload = json.loads(row[2])
    name = payload.get('name', '')
    
    if name in target_profiles:
        original_bids = payload.get('benchmark_ids', [])
        
        # Filter out the missing ones
        cleaned_bids = [b for b in original_bids if b not in missing_ids]
        
        if len(cleaned_bids) != len(original_bids):
            payload['benchmark_ids'] = cleaned_bids
            new_payload = json.dumps(payload)
            c.execute('UPDATE profiles SET payload = ? WHERE id = ?', (new_payload, profile_id))
            print(f"Cleaned profile '{name}': Removed {len(original_bids) - len(cleaned_bids)} missing benchmarks.")
            updated_count += 1

db.commit()
db.close()
print(f"Database cleanup complete. Updated {updated_count} profiles.")
