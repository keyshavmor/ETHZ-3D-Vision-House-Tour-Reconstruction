filename = 'table.asc'  # Replace 'your_file.txt' with the actual file name

with open(filename, 'r') as file:
    lines = file.readlines()

processed_lines = []
for index, line in enumerate(lines):
    if index >= 2:  # Start from the 3rd line
        values = line.strip().split()
        values.insert(6, "Table")  # Insert "LABEL" as the 7th value
        processed_line = ' '.join(values) + '\n'
        processed_lines.append(processed_line)
    else:
        processed_lines.append(line)

# Save the processed lines to a new file
output_filename = 'table_labelled.asc'  # Replace 'processed_file.txt' with the desired output file name
with open(output_filename, 'w') as output_file:
    output_file.writelines(processed_lines)

print(f"The processed lines have been saved to '{output_filename}'.")

