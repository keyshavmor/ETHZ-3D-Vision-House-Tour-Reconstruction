import csv

asc_files = [
    'bag_labelled.asc', 'bed_labelled.asc', 'cabinet_labelled.asc',
    'chair_labelled.asc', 'clock_labelled.asc', 'cloth_labelled.asc',
    'lamp_labelled.asc', 'painting_labelled.asc', 'rug_labelled.asc',
    'screen_labelled.asc', 'shelf_labelled.asc', 'table_labelled.asc'
]

labels = [
    'Bag', 'Bed', 'Cabinet', 'Chair', 'Clock', 'Cloth',
    'Lamp', 'Labelled', 'Rug', 'Screen', 'Shelf', 'Table'
]

csv_file = 'cosine_similarity_counts.csv'  # Replace with the actual CSV file name
output_csv_file = 'updated_csv_file.csv'  # Replace with the desired output CSV file name

# Read the existing data from the CSV file
data = []
with open(csv_file, 'r') as file:
    reader = csv.reader(file)
    headers = next(reader)
    data = list(reader)

# Add a new column for the number of points in each ASC file
for asc_file, label in zip(asc_files, labels):
    num_points = 0
    with open(asc_file, 'r') as file:
        file.readline()  # Skip the first line
        num_points = int(file.readline().strip())  # Read the number of points from the second line
    for row in data:
        if row[0] == label:
            row.append(str(num_points))

# Update the headers with the new column name
headers.append("Num Points")

# Write the updated data to the output CSV file
with open(output_csv_file, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(headers)
    writer.writerows(data)

print("Updated CSV file created successfully.")