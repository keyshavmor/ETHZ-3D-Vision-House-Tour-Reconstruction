input_file = 'points3D.txt'  # Replace with the actual file name
output_file = 'points3D_colmap_ovseg.txt'  # Replace with the desired output file name

with open(input_file, 'r') as f:
    lines = f.readlines()

modified_lines = []
for i, line in enumerate(lines):
    if i < 3:  # Preserve the first three lines
        modified_lines.append(line)
    else:
        line_data = line.strip().split()
        modified_line = ' '.join(line_data[:7])  # Keep the first seven values
        modified_lines.append(modified_line + '\n')

with open(output_file, 'w') as f:
    f.writelines(modified_lines)
