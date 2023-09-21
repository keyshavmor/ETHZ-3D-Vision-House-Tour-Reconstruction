import os
os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "max_split_size_mb:256"
# Number of images
num_images = 9018

# Path to the Python application
app_path = "demo.py"

# Path to the images
image_folder = "png_no_mask"

# Path to the output folder
output_folder = "png_mask_opaque"

# Arguments for the Python application
config_file = "configs/ovseg_swinB_vitL_demo.yaml"
class_names = "'Table' 'Chair' 'Lamp' 'Screen' 'Cloth' 'Cabinet' 'Bed' 'Painting' 'Shelf' 'Rug' 'Clock' 'Cushion' 'Bag' 'Shoes'"
opts = "MODEL.WEIGHTS ovseg_swinbase_vitL14_ft_mpt.pth"

# Create the output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Process each image
for i in range(0, num_images + 1):
    # Generate the image file name
    image_filename = f"frame_id_{str(i).zfill(4)}.jpg"

    # Generate the command to run the Python application
    command = f"python {app_path} --config-file {config_file} --class-names {class_names} --input {os.path.join(image_folder, image_filename)} --output {output_folder} --opts {opts}"

    # Run the command
    os.system(command)

    print(f"Processed image: {image_filename}")

print("Processing complete.")
