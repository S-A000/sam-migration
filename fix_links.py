import os

dir_path = r"d:\python projects\data_migration_saas\frontend\public"
files_to_fix = [
    "ConnectionManager.html",
    "LiveMigrationManager.html",
    "LogsAndHealth.html",
    "Billing&Health.html",
    "index.html",
]

for filename in files_to_fix:
    filepath = os.path.join(dir_path, filename)
    if not os.path.exists(filepath):
        continue
    
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    # We will just find 'href="#"' and the text after it to see which link it belongs to.
    
    # We can split the content by '<a ' and then reassemble
    parts = content.split('<a ')
    new_parts = [parts[0]]
    
    for part in parts[1:]:
        if 'href="#"' in part:
            if 'Connection Manager' in part:
                part = part.replace('href="#"', 'href="/manager"')
            elif 'Migration Monitor' in part:
                part = part.replace('href="#"', 'href="/monitor"')
            elif 'Logs &amp; Health' in part or 'Logs & Health' in part:
                part = part.replace('href="#"', 'href="/logs"')
            elif 'Billing &amp; Analytics' in part or 'Billing & Analytics' in part:
                part = part.replace('href="#"', 'href="/billing"')
            elif 'Pricing' in part: # keep as '#'? 
                pass
        
        new_parts.append(part)
        
    new_content = '<a '.join(new_parts)
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(new_content)
        
print("Replacement done.")
