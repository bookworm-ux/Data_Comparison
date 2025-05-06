import os
import json
from deepdiff import DeepDiff

FOLDER_1 = "output_jsons_invoice"
FOLDER_2 = "output_jsons_groundtruth_invoice"
OUTPUT_FOLDER = "diff_output"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

# Helper to make anything JSON-serializable
def make_serializable(obj):
    try:
        json.dumps(obj)
        return obj
    except TypeError:
        return str(obj)  # or return None if you prefer to skip

def clean_diff(diff):
    if isinstance(diff, dict):
        return {k: clean_diff(v) for k, v in diff.items()}
    elif isinstance(diff, list):
        return [clean_diff(i) for i in diff]
    else:
        return make_serializable(diff)

files1 = sorted([f for f in os.listdir(FOLDER_1) if f.endswith(".json")])
files2 = sorted([f for f in os.listdir(FOLDER_2) if f.endswith(".json")])

if len(files1) != len(files2):
    print("⚠️ Warning: Folder file counts don't match.")
    print(f"{FOLDER_1} has {len(files1)} files")
    print(f"{FOLDER_2} has {len(files2)} files")
    print("Comparing up to the shortest length.\n")

for i, (f1, f2) in enumerate(zip(files1, files2)):
    path1 = os.path.join(FOLDER_1, f1)
    path2 = os.path.join(FOLDER_2, f2)

    json1 = load_json(path1)
    json2 = load_json(path2)

    diff = DeepDiff(
        json1,
        json2,
        ignore_order=True,
        report_repetition=True,
        exclude_types={type}
    )

    safe_diff = clean_diff(diff.to_dict())

    output_name = f"diff_{i+1}_{os.path.splitext(f1)[0]}_vs_{os.path.splitext(f2)[0]}.json"
    output_path = os.path.join(OUTPUT_FOLDER, output_name)

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(safe_diff, f, indent=2)

print(f"✅ Compared {f1} vs {f2} → saved: {output_name}")
