import json
import sys
from deepdiff import DeepDiff

def load_json(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def compare_json_files(file1, file2, output_diff_path=None):
    json1 = load_json(file1)
    json2 = load_json(file2)
    
    diff = DeepDiff(json1, json2, ignore_order=True)
    
    if output_diff_path:
        with open(output_diff_path, 'w', encoding='utf-8') as f:
            json.dump(diff, f, indent=2)
        print(f"✅ Differences written to: {output_diff_path}")
    else:
        print("🔍 Differences:\n", json.dumps(diff, indent=2))

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python compare_json.py file1.json file2.json [output_diff.json]")
    else:
        file1 = sys.argv[1]
        file2 = sys.argv[2]
        output = sys.argv[3] if len(sys.argv) > 3 else None
        compare_json_files(file1, file2, output)
