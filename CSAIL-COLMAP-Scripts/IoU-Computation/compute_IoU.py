import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# Read the first file and extract the label
file1 = 'rug_labelled.asc'  # Replace with the actual file name
data1 = np.loadtxt(file1, skiprows=2, usecols=(0, 1, 2, 3, 4, 5, 6), dtype=object)

xyz1 = data1[:, :3].astype(np.float128)  # X, Y, Z coordinates
rgb1 = data1[0, 3:6].astype(np.int64).reshape(-1, 3)  # RGB values
print(rgb1)

label1 = np.loadtxt(file1, skiprows=2, usecols=(6), dtype=str)
label = label1[0]
print(label)

num_points_file1 = len(xyz1)

# Read the second file, extract the labels, and remove the 7th value
file2 = 'points3D_colmap_backprojection_labelled.txt'  # Replace with the actual file name
num_proximate_points = 0
num_points = 0

distance_threshold = 0.0001  # Replace with your desired threshold value
cosine_threshold = 0.9  # Replace with your desired cosine similarity threshold
cosine_similar_points = 0
cosine_similarity_sum = 0.0
num_points_file2 = 0

with open(file2, 'r') as f:
    lines = f.readlines()
    for line in lines:
        line_data = line.strip().split()
        if label in line_data[6:8]:  # Check if the label is present in either the 7th or 8th position
            num_points += 1
            num_points_file2 += 1
            xyz2 = np.array(line_data[1:4], dtype=np.float128)  # X, Y, Z coordinates
            rgb2 = np.array(line_data[4:7], dtype=np.int64)  # RGB values
            distances = np.linalg.norm(xyz1 - xyz2, axis=1)  # Compute distances between points
            if np.any(distances < distance_threshold):
                num_proximate_points += 1
                cosine_sim = cosine_similarity(rgb1, rgb2.reshape(1, -1))  # Compute cosine similarity
                cosine_similarity_sum += cosine_sim
                if cosine_sim > cosine_threshold:
                    cosine_similar_points += 1


print("Number of points in file2 with label", label, ":", num_points)
print("Number of proximate points:", num_proximate_points)
average_cosine_similarity = cosine_similarity_sum / cosine_similar_points if cosine_similar_points > 0 else 0.0
print("Average cosine similarity:", average_cosine_similarity)
print("Intersection points:", cosine_similar_points)

union = num_points_file1 + num_points_file2 - cosine_similar_points
iou = cosine_similar_points / union if union > 0 else 0.0

print("Intersection over Union (IoU):", iou)