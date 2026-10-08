import filecmp
import os
import csv

def compare_folders(dir1, dir2, csv_writer):
    """
    Compares two directories and writes differences to a CSV file.

    Args:
        dir1 (str): The path to the first directory.
        dir2 (str): The path to the second directory.
        csv_writer (csv.writer): CSV writer object to write results.
    """
    if not os.path.isdir(dir1):
        print(f"Error: Directory '{dir1}' does not exist.")
        return
    if not os.path.isdir(dir2):
        print(f"Error: Directory '{dir2}' does not exist.")
        return

    dcmp = filecmp.dircmp(dir1, dir2)

    csv_writer.writerow([f"Comparing '{dir1}' and '{dir2}'"])

    if dcmp.left_only:
        csv_writer.writerow(["Only in first directory"])
        for item in dcmp.left_only:
            csv_writer.writerow(["", item])

    if dcmp.right_only:
        csv_writer.writerow(["Only in second directory"])
        for item in dcmp.right_only:
            csv_writer.writerow(["", item])

    if dcmp.diff_files:
        csv_writer.writerow(["Different content"])
        for item in dcmp.diff_files:
            csv_writer.writerow(["", item])

    if dcmp.common_funny:
        csv_writer.writerow(["Uncomparable items"])
        for item in dcmp.common_funny:
            csv_writer.writerow(["", item])

    if dcmp.same_files:
        csv_writer.writerow(["Identical files"])
        for item in dcmp.same_files:
            csv_writer.writerow(["", item])

    if dcmp.common_dirs:
        for sdcmp in dcmp.subdirs.values():
            compare_folders(sdcmp.left, sdcmp.right, csv_writer)

if __name__ == "__main__":
    folder_a = "../pictures"  # Replace with your first folder path
    folder_b = "../CrossDevice/20250908"  # Replace with your second folder path
    output_csv = "comparison_results.csv"

    with open(output_csv, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Category", "Item"])
        compare_folders(folder_a, folder_b, writer)

    print(f"\nComparison results saved to '{output_csv}'")
