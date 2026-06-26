#!/usr/bin/env python3
import os
import sys
import re

link_regex = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')

# Dynamically resolve root relative to this script
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, ".."))
docs_dir = os.path.join(project_root, "docs")

# Check if submodules are empty
stmlib_path = os.path.join(project_root, "stmlib")
bootloader_path = os.path.join(project_root, "stm_audio_bootloader")

stmlib_empty = not os.path.exists(stmlib_path) or len(os.listdir(stmlib_path)) == 0
bootloader_empty = not os.path.exists(bootloader_path) or len(os.listdir(bootloader_path)) == 0

broken_links = []
total_links = 0

if not os.path.exists(docs_dir):
    print("No docs/ directory found.")
    sys.exit(0)

for root, dirs, files in os.walk(docs_dir):
    for file in files:
        if file.endswith(".md"):
            filepath = os.path.join(root, file)
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
            
            matches = link_regex.findall(content)
            for text, url in matches:
                # Skip external web URLs
                if url.startswith("http://") or url.startswith("https://"):
                    continue
                
                total_links += 1
                
                # Strip the URL fragment/hash
                url_clean = url.split("#")[0]
                
                if url_clean.startswith("file:///"):
                    target_path = url_clean.replace("file://", "")
                elif url_clean.startswith("file://"):
                    target_path = url_clean.replace("file://", "")
                else:
                    target_path = os.path.normpath(os.path.join(root, url_clean))
                
                # Check if we should skip due to empty submodules
                if stmlib_empty and target_path.startswith(stmlib_path):
                    continue
                if bootloader_empty and target_path.startswith(bootloader_path):
                    continue
                
                # Verify existence on filesystem
                if not os.path.exists(target_path):
                    broken_links.append((filepath, text, url, target_path))

print(f"Checked {total_links} links total.")
if broken_links:
    print(f"Found {len(broken_links)} broken links:")
    for file, text, url, target in broken_links:
        rel_file = os.path.relpath(file, project_root)
        print(f"  {rel_file}: broken link [{text}]({url}) -> target not found: {target}")
    sys.exit(1)
else:
    print("All links verified successfully!")
    sys.exit(0)
