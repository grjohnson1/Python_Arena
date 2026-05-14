import os
import csv

REQUIRED_HEADERS = ["Name", "Date", "Result", "Low", "High", "Description"]


def get_folder_path():
    while True:
        folder = input("\nEnter the folder path (e.g. C:/Users/MyFolder): ").strip()
        if os.path.isdir(folder):
            return folder
        print(f"  [!] Path not found: '{folder}'. Please try again.")


def find_csv_files(folder):
    return [
        os.path.join(folder, f)
        for f in os.listdir(folder)
        if f.lower().endswith(".csv") and os.path.isfile(os.path.join(folder, f))
    ]


def get_csv_headers(filepath):
    try:
        with open(filepath, newline="", encoding="utf-8-sig") as f:
            reader = csv.reader(f)
            headers = next(reader, None)
            return [h.strip() for h in headers] if headers else []
    except Exception as e:
        print(f"  [!] Could not read '{os.path.basename(filepath)}': {e}")
        return []


def has_required_headers(headers):
    return all(col in headers for col in REQUIRED_HEADERS)


def get_output_filename(folder):
    while True:
        name = input("\nEnter the output filename (without extension): ").strip()
        if not name:
            print("  [!] Filename cannot be empty.")
            continue
        filename = name if name.lower().endswith(".csv") else name + ".csv"
        full_path = os.path.join(folder, filename)
        if os.path.exists(full_path):
            overwrite = input(f"  [!] '{filename}' already exists. Overwrite? (y/n): ").strip().lower()
            if overwrite != "y":
                continue
        return full_path, filename


def collect_all_fieldnames(matching_files):
    seen = []
    for filepath in matching_files:
        headers = get_csv_headers(filepath)
        for h in headers:
            if h and h not in seen:  # skip None/empty column names
                seen.append(h)
    return seen


def combine_csv_files(matching_files, output_path):
    fieldnames = collect_all_fieldnames(matching_files)
    with open(output_path, "w", newline="", encoding="utf-8-sig") as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for filepath in matching_files:
            with open(filepath, newline="", encoding="utf-8-sig") as infile:
                reader = csv.DictReader(infile)
                for row in reader:
                    # Strip None keys (unnamed trailing columns) from each row
                    clean_row = {k: v for k, v in row.items() if k is not None and k != ""}
                    writer.writerow(clean_row)


def main():
    print("=" * 55)
    print("         CSV File Combiner")
    print("=" * 55)
    print(f"Looking for files with headers: {', '.join(REQUIRED_HEADERS)}")

    folder = get_folder_path()

    all_csv = find_csv_files(folder)
    if not all_csv:
        print("\n  No CSV files found in that folder. Exiting.")
        return

    print(f"\n  Found {len(all_csv)} CSV file(s) in folder. Scanning headers...")

    matching = []
    skipped = []
    for filepath in all_csv:
        headers = get_csv_headers(filepath)
        if has_required_headers(headers):
            matching.append(filepath)
        else:
            skipped.append(os.path.basename(filepath))

    print(f"\n  {len(matching)} file(s) have all required headers.")
    if skipped:
        print(f"  {len(skipped)} file(s) skipped (missing headers): {', '.join(skipped)}")

    if not matching:
        print("\n  No matching files to combine. Exiting.")
        return

    output_path, filename = get_output_filename(folder)

    print(f"\n  {len(matching)} file(s) will be combined into '{filename}'.")
    confirm = input("  Proceed? (y/n): ").strip().lower()
    if confirm != "y":
        print("  Cancelled. No file was created.")
        return

    try:
        combine_csv_files(matching, output_path)
        print(f"\n  Done! Combined file saved to:\n  {output_path}")
    except Exception as e:
        print(f"\n  [!] Error writing output file: {e}")


if __name__ == "__main__":
    main()