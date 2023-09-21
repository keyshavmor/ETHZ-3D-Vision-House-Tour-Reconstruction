filename = 'points3D_backprojection_clean.txt'  # Replace 'your_file.txt' with the actual file name

labels = {
    (255, 0, 0): "Table",
    (0, 0, 255): "Chair",
    (0, 255, 0): "Lamp",
    (255, 255, 0): "Screen",
    (0, 255, 255): "Cloth",
    (255, 0, 255): "Cabinet",
    (173, 0, 255): "Bed",
    (255, 176, 0): "Painting",
    (255, 93, 0): "Shelf",
    (138, 64, 191): "Rug",
    (239, 174, 31): "Clock"
}

with open(filename, 'r') as file:
    lines = file.readlines()

counts = {label: 0 for label in labels.values()}
processed_lines = []

for line in lines[3:]:  # Ignore the first three lines
    values = line.strip().split()
    rgb_values = tuple(map(int, values[3:6]))

    label = labels.get(rgb_values)
    if label:
        counts[label] += 1
        values = values[:6] + [label] + values[6:]

    processed_lines.append(' '.join(values))

# Save the processed lines to a new file
output_filename = 'points3D_backprojection_labelled.txt'  # Replace 'processed_file.txt' with the desired output file name
with open(output_filename, 'w') as output_file:
    output_file.writelines('\n'.join(processed_lines))

# Print the counts for each label
for label, count in counts.items():
    print(f"Number of points with label '{label}': {count}")
