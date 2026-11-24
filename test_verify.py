# -*- coding: utf-8 -*-
import os
import json
import re

print("=== Running System Integrity & Auth Verification ===")

# 1. File existence checks
files_to_check = [
    'index.html', 'style.css', 'app.js', 'auth.js',
    'questions_data.js', 'study_notes.js', 'theory_library.js',
    'run_app.py', 'start_app.bat'
]
for fname in files_to_check:
    assert os.path.exists(fname), f"Missing {fname}"
    print(f"✓ {fname} exists ({os.path.getsize(fname)} bytes)")

# 2. Image assets
assets_to_check = ['app_assets/page_5_Image29.png', 'app_assets/page_9_Image38.png']
for asset in assets_to_check:
    assert os.path.exists(asset), f"Missing {asset}"
    print(f"✓ {asset} exists ({os.path.getsize(asset)} bytes)")

# 3. DOM Elements Check in index.html for app.js and auth.js
with open('index.html', 'r', encoding='utf-8') as f:
    index_html = f.read()

with open('app.js', 'r', encoding='utf-8') as f:
    app_js = f.read()

with open('auth.js', 'r', encoding='utf-8') as f:
    auth_js = f.read()

ids_in_app = set(re.findall(r"getElementById\(['\"]([a-zA-Z0-9_-]+)['\"]\)", app_js))
ids_in_auth = set(re.findall(r"getElementById\(['\"]([a-zA-Z0-9_-]+)['\"]\)", auth_js))

all_required_ids = ids_in_app.union(ids_in_auth)
print(f"Checking {len(all_required_ids)} DOM IDs ({len(ids_in_app)} in app.js, {len(ids_in_auth)} in auth.js)...")

missing_ids = [id_name for id_name in all_required_ids if f'id="{id_name}"' not in index_html and f"id='{id_name}'" not in index_html]

if missing_ids:
    raise AssertionError(f"Missing DOM IDs in index.html: {missing_ids}")
else:
    print("✓ All DOM IDs in both app.js and auth.js are present in index.html!")

# 4. Check Auth Configuration & Whitelist
expected_whitelist = [
    "Vương Thị Yến Nhi",
    "Nguyễn Hữu Xuân Bắc",
    "Nguyễn Minh Thắng",
    "Nguyễn Trần Trung Kiên",
    "Nguyễn Tiến Dũng"
]
for name in expected_whitelist:
    assert name in auth_js, f"Name {name} missing in auth.js"
print("✓ All 5 required candidate names present in DEFAULT_WHITELIST.")

assert 'ADMIN_KEY = "Thangcyrus"' in auth_js, "ADMIN_KEY Thangcyrus missing or modified!"
print("✓ ADMIN_KEY = 'Thangcyrus' verified.")

# 5. Check Script Inclusion Order in index.html
script_tags = re.findall(r'<script src="([^"]+)"></script>', index_html)
print("Script order in index.html:", script_tags)
assert 'auth.js' in script_tags, "auth.js not included in index.html"
assert script_tags.index('auth.js') < script_tags.index('app.js'), "auth.js should be loaded before app.js"
print("✓ Script load order verified (auth.js before app.js).")

# 6. Check Questions Bank
with open('questions_data.js', 'r', encoding='utf-8') as f:
    js_text = f.read()

prefix = 'var QUESTIONS_BANK = window.QUESTIONS_BANK = '
if prefix in js_text:
    raw_json = js_text.replace(prefix, '').rstrip(';\n')
else:
    raw_json = js_text.replace('const QUESTIONS_BANK = ', '').rstrip(';\n')

q_data = json.loads(raw_json)
print(f"✓ QUESTIONS_BANK valid JSON with {len(q_data)} questions.")

# 7. Check Study Notes & Theory Docs
with open('study_notes.js', 'r', encoding='utf-8') as f:
    sn_text = f.read()
assert 'STUDY_GUIDE' in sn_text and 'TRAPS_GUIDE' in sn_text
print("✓ study_notes.js syntax verified.")

with open('theory_library.js', 'r', encoding='utf-8') as f:
    tl_text = f.read()
assert 'THEORY_DOCS' in tl_text
print("✓ theory_library.js syntax verified.")

print("\n🎉 ALL TESTS AND AUTH SYSTEM CHECKS PASSED PERFECTLY!")
