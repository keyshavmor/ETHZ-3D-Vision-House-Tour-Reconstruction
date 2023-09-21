import csv
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# Read the first file and extract the label
file1 = 'table_labelled.asc'  # Replace with the actual file name
data1 = np.loadtxt(file1, skiprows=2, usecols=(0, 1, 2, 3, 4, 5, 6), dtype=object)

xyz1 = data1[:, :3].astype(np.float128)  # X, Y, Z coordinates
rgb1 = data1[0, 3:6].astype(np.int64).reshape(-1, 3)
label1 = np.loadtxt(file1, skiprows=2, usecols=(6), dtype=str)
label = label1[0]

num_points_file1 = len(xyz1)

# Read the second file, extract the labels, and remove the 7th value
file2 = 'points3D_colmap_backprojection_labelled.txt'  # Replace with the actual file name
num_proximate_points = 0
num_points = 0

distance_threshold = 0.0001  # Replace with your desired threshold value
cosine_similarity_thresholds = np.arange(0, 1.1, 0.1)
cosine_similarity_counts = {threshold: 0 for threshold in cosine_similarity_thresholds}

with open(file2, 'r') as f:
    lines = f.readlines()
    for line in lines:
        line_data = line.strip().split()
        if label in line_data[6:8]:  # Check if the label is present in either the 7th or 8th position
            num_points += 1
            xyz2 = np.array(line_data[1:4], dtype=np.float128)  # X, Y, Z coordinates
            rgb2 = np.array(line_data[4:7], dtype=np.int64)  # RGB values
            distances = np.linalg.norm(xyz1 - xyz2, axis=1)  # Compute distances between points
            if np.any(distances < distance_threshold):
                num_proximate_points += 1
                cosine_sim = cosine_similarity(rgb1, rgb2.reshape(1, -1))  # Compute cosine similarity
                for threshold in cosine_similarity_thresholds:
                    if threshold == 1.0:
                        if cosine_sim > threshold:
                            cosine_similarity_counts[threshold] += 1
                    else:
                        if threshold < cosine_sim <= threshold + 0.1:
                            cosine_similarity_counts[threshold] += 1

output_filename = 'cosine_similarity_counts.csv'  # Replace with your desired output filename

# Write cosine similarity counts to a CSV file
header = ['Label'] + [f'Cosine Similarity > {threshold} and <= {threshold + 0.1}' for threshold in cosine_similarity_thresholds]
row = [label] + [cosine_similarity_counts[threshold] for threshold in cosine_similarity_thresholds]

with open(output_filename, 'a', newline='') as csvfile:
    writer = csv.writer(csvfile)
    if csvfile.tell() == 0:  # Check if the file is empty
        writer.writerow(header)
    writer.writerow(row)

print("Number of points in file2 with label", label, ":", num_points)
print("Number of proximate points:", num_proximate_points)
print("Cosine Similarity Counts:")
for threshold, count in cosine_similarity_counts.items():
    if threshold == 1.0:
        print(f"Cosine Similarity > {threshold} and <= 1.0: {count}")
    else:
        print(f"Cosine Similarity > {threshold} and <= {threshold + 0.1}: {count}")

print("Results written to", output_filename)
