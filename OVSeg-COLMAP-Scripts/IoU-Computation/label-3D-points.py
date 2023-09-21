import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import random

filename = 'points3D_colmap_ovseg.txt'  # Replace 'your_file.txt' with the actual file name

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
    (239, 174, 31): "Clock",
    (64, 128, 99): "Bag",
    (150, 60, 99): "Shoes"
}

# Print RGB values for cosine similarity
for rgb in labels.keys():
    print(f"Checking cosine similarity for RGB value: {rgb}")

with open(filename, 'r') as file:
    lines = file.readlines()

counts = {label: 0 for label in labels.values()}
processed_lines = []

total_points = len(lines) - 3  # Exclude the first three lines
progress_interval = 20000
processed_count = 0

for line in lines[3:]:  # Ignore the first three lines
    values = line.strip().split()

    if len(values) >= 8 and values[7] in labels.values():
        processed_lines.append(' '.join(values))  # Line already has a label, skip cosine similarity
    else:
        point_rgb = np.array(list(map(int, values[4:7])))
        best_label = None
        best_similarity = -1

        for rgb, label in labels.items():
            label_rgb = np.array(rgb)
            similarity = cosine_similarity([point_rgb], [label_rgb])[0][0]

            if similarity > best_similarity:
                best_label = label
                best_similarity = similarity
            elif similarity == best_similarity:
                # Random tie-breaker
                if random.randint(0, 1):
                    best_label = label

        if len(values) >= 8:
            values[7] = best_label if best_similarity > 0.75 else "None"  # Assign label if similarity is above threshold
        else:
            values.append(best_label if best_similarity > 0.75 else "None")

        if best_similarity > 0.75:
            counts[best_label] += 1

        processed_lines.append(' '.join(values))
        processed_count += 1

        if processed_count % progress_interval == 0 or processed_count == total_points:
            print(f"Processed {processed_count}/{total_points} points.")


# Save the processed lines to a new file
output_filename = 'points3D_colmap_ovseg_labelled.txt'  # Replace 'processed_file.txt' with the desired output file name
with open(output_filename, 'w') as output_file:
    output_file.writelines('\n'.join(processed_lines))

# Print the counts for each label
for label, count in counts.items():
    print(f"Number of points with label '{label}': {count}")
