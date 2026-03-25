"""Merge all contribution files into master_templates.json."""
import json
import os
import glob

MASTER = 'templates/master_templates.json'
CONTRIB_DIR = 'contributions'

# Load master
if os.path.isfile(MASTER):
    with open(MASTER, 'r') as f:
        master = json.load(f)
else:
    master = {'version': 1, 'total_items': 0, 'templates': {}}

templates = master.get('templates', {})
before = len(templates)

# Process all contribution files
contrib_files = glob.glob(os.path.join(CONTRIB_DIR, '*.json'))
processed = 0

for fpath in contrib_files:
    if fpath.endswith('.gitkeep'):
        continue
    try:
        with open(fpath, 'r') as f:
            contrib = json.load(f)

        new_items = contrib.get('templates', {})
        for key, template in new_items.items():
            # Validate: must have hex, mask, size
            if not all(k in template for k in ('hex', 'mask', 'size')):
                continue
            # Dedup: keep smallest size (simplest template)
            if key in templates:
                if template['size'] >= templates[key]['size']:
                    continue
            templates[key] = template

        # Delete processed file
        os.remove(fpath)
        processed += 1
    except Exception as e:
        print(f'Error processing {fpath}: {e}')

after = len(templates)
master['templates'] = templates
master['total_items'] = after
master['version'] = master.get('version', 1)

with open(MASTER, 'w') as f:
    json.dump(master, f, separators=(',', ':'))

print(f'Merged {processed} files: {before} -> {after} templates (+{after - before})')
