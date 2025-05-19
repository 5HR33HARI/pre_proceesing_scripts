# import os
# import cv2
# import xml.etree.ElementTree as ET
# from PIL import Image

# def fix_image(image_path):
#     try:
#         with Image.open(image_path) as img:
#             img.save(image_path)
#     except Exception as e:
#         print(f"Error fixing {image_path}: {e}")

# def process_annotation(xml_path, new_image_path, new_xml_path):
#     try:
#         tree = ET.parse(xml_path)
#         root = tree.getroot()
        
#         # Update filename and path in XML
#         filename = os.path.basename(new_image_path)
#         root.find('filename').text = filename
#         root.find('path').text = new_image_path
        
#         # Save the modified XML file
#         tree.write(new_xml_path)
#     except Exception as e:
#         print(f"Error processing {xml_path}: {e}")

# def process_files(source_folder, destination_folder):
#     if not os.path.exists(destination_folder):
#         os.makedirs(destination_folder)

#     for filename in os.listdir(source_folder):
#         if filename.endswith('.jpg') or filename.endswith('.jpeg'):
#             image_path = os.path.join(source_folder, filename)
#             xml_path = os.path.join(source_folder, filename.rsplit('.', 1)[0] + '.xml')

#             if os.path.exists(xml_path):
#                 # Fix the image
#                 fix_image(image_path)
                
#                 # Copy image to the destination folder
#                 new_image_path = os.path.join(destination_folder, filename)
#                 img = cv2.imread(image_path)
#                 cv2.imwrite(new_image_path, img)

#                 # Copy and modify XML file
#                 new_xml_path = os.path.join(destination_folder, os.path.basename(xml_path))
#                 process_annotation(xml_path, new_image_path, new_xml_path)

#                 print(f"Processed: {filename} and corresponding XML file.")
#             else:
#                 print(f"No annotation file found for: {filename}")


# if __name__ == "__main__":
#     source_folder = r"20_03_2025_new"
#     destination_folder = r"20_03_2025_new_ann"
#     process_files(source_folder, destination_folder)




import os
from PIL import Image
import cv2

def create_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def read_and_save_image(input_path, output_path):
    """
    Reads an image from the input path and saves it as a .jpg file to the output path.
    """
    try:
        with Image.open(input_path) as img:
            img = img.convert('RGB')
            img.save(input_path)  # Fix the image before saving with OpenCV

        img = cv2.imread(input_path)
        cv2.imwrite(output_path, img)

        print(f"Saved {output_path}")
    except Exception as e:
        print(f"Failed to process {input_path}: {e}")

def convert_images_to_jpg(input_folder, output_folder):
    create_dir(output_folder)

    for filename in os.listdir(input_folder):
        if filename.endswith(('.jpg', '.jpeg', '.png', '.bmp')):  # Supports multiple image formats
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, os.path.splitext(filename)[0] + '.jpg')
            read_and_save_image(input_path, output_path)


if __name__ == "__main__":
    input_folder = 'testing_1'  # Update with your actual input folder path
    output_folder = 'testing'  # Update with your desired output folder path
    convert_images_to_jpg(input_folder, output_folder)