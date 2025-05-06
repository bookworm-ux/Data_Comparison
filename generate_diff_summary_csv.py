import os
import json
import csv

DIFF_FOLDER = "diff_output"
CSV_OUTPUT = "diff_summary.csv"

rows = []

for filename in sorted(os.listdir(DIFF_FOLDER)):
    if not filename.endswith(".json"):
        continue

    path = os.path.join(DIFF_FOLDER, filename)
    with open(path, 'r', encoding='utf-8') as f:
        diff = json.load(f)

    if diff:
        fields_changed = []
        for key in ["values_changed", "dictionary_item_added", "dictionary_item_removed",
                    "iterable_item_added", "iterable_item_removed"]:
            if key in diff:
                fields_changed += list(diff[key].keys())

        rows.append([filename, "❌", len(fields_changed), "; ".join(fields_changed)])
    else:
        rows.append([filename, "✅", 0, ""])

with open(CSV_OUTPUT, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(["File", "Diff Exists?", "# Fields Changed", "Changed Fields"])
    writer.writerows(rows)

print(f"✅ CSV summary saved to: {CSV_OUTPUT}")
