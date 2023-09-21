input_file = 'points3D_backprojection.txt'  # Replace with the actual file name
output_file = 'points3D_backprojection_clean.txt'  # Replace with the desired output file name

with open(input_file, 'r') as f:
    lines = f.readlines()

modified_lines = []
for i, line in enumerate(lines):
    if i < 3:  # Preserve the first three lines
        modified_lines.append(line)
    else:
        line_data = line.strip().split()
        modified_line = ' '.join(line_data[1:7] + line_data[8:])
        modified_lines.append(modified_line + '\n')

with open(output_file, 'w') as f:
    f.writelines(modified_lines)
