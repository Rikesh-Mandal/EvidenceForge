
from pathlib import Path
import csv
import re
import shutil

csv_path = Path("data/router_samples.csv")
backup_path = Path("data/router_samples_backup.csv")

# Read the original file
lines = csv_path.read_text(encoding="utf-8-sig").splitlines()

fixed_lines = []
invalid_rows = []

for line_number, line in enumerate(lines, start=1):
    # Remove all double quotes
    line = line.replace('"', '').strip()

    # Add comma after ? if followed by a valid label
    line = re.sub(
        r'\?\s*,?\s*(?=(deployment|model|policy)\s*$)',
        '?,',
        line,
        flags=re.IGNORECASE
    )

    # Check CSV structure
    columns = next(csv.reader([line]))

    if len(columns) != 2:
        invalid_rows.append((line_number, line))

    fixed_lines.append(line)

# Avoid overwriting the file if CSV structure is invalid
if invalid_rows:
    print("Some rows cannot be safely converted:")
    for number, content in invalid_rows[:15]:
        print(f"Line {number}: {content}")

    print(f"\nTotal invalid rows: {len(invalid_rows)}")
    print("Original CSV unchanged.")
else:
    shutil.copy2(csv_path, backup_path)

    csv_path.write_text(
        "\n".join(fixed_lines) + "\n",
        encoding="utf-8"
    )

    print("CSV fixed successfully!")
    print(f"Rows processed: {len(fixed_lines) - 1}")
    print(f"Backup: {backup_path}")
