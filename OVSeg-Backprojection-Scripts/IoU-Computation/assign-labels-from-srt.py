import csv
from collections import Counter

# Read CSV file to get frame numbers and labels
csv_file = 'frame_label_map_updated.csv'  # Replace with your CSV file path
csv_data = {}
with open(csv_file, 'r') as file:
    reader = csv.reader(file)
    next(reader)  # Skip header row
    for row in reader:
        frame_num = int(row[0])
        labels = row[2].split(',')
        csv_data[frame_num] = labels

# Read text file and combine labels for each line
text_file = 'points3D_backprojection_labelled.txt'  # Replace with your text file path
lines = []
with open(text_file, 'r') as file:
    lines = file.readlines()

output_lines = []
for line_num, line in enumerate(lines[3:], start=4):  # Read lines 4-13
    values = line.strip().split()

    if len(values) > 6 and not values[6].replace(".", "").isdigit():
        final_labels = [values[6]]
        frame_ids = values[7:]
    else:
        frame_ids = values[6:] if len(values) > 6 else []
        final_labels = []

    combined_labels = []
    for frame_id in frame_ids:
        frame_num = None
        if frame_id.isnumeric():
            frame_num = int(frame_id.split('_')[-1])
        if frame_num is not None and frame_num in csv_data:
            combined_labels.extend(csv_data[frame_num])

    label_counts = Counter(combined_labels)
    label_counts.pop('[]', None)  # Exclude empty labels from count

    most_common = label_counts.most_common()
    if most_common:
        max_count = most_common[0][1]
        final_labels.extend([label for label, count in most_common if count == max_count])

    final_label_string = ' '.join(final_labels)
    output_lines.append(' '.join(values[:6]) + ' ' + final_label_string + '\n')

# Save the modified lines to a new file
output_file = 'points3D_backprojection_clean_srt_labelling.txt'  # Replace with desired output file path
with open(output_file, 'w') as file:
    file.writelines(output_lines)

print(f"Modified lines saved to {output_file}")