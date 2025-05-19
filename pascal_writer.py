import os
from pascal_voc_writer import Writer
import glob

count = 0

# Loop over the images in the specified folder
for img in glob.glob(r'E:\\factree_ai\\test\\*.jpg'):
    print(img)
    
    # Using os.path.splitext to split filename from extension
    img_name, _ = os.path.splitext(os.path.basename(img))
    print(img_name)
    
    # Assuming the image dimensions are 1040x1134, you might want to get these dynamically if needed
    img_width = 1040
    img_height = 1134
    
    writer = Writer(img, img_width, img_height)

    # Adding an object annotation (coordinates are given as an example, modify if needed)
    writer.addObject('FOD', 234, 440, 310, 550)
    # You can add more objects similarly:
    # writer.addObject('Flux', 542, 353, 640, 432)

    count += 1
    print(f'Count = {count}')
    
    # Save the annotation as an XML file in the same directory
    xml_filename = os.path.join(os.path.dirname(img), f'{img_name}.xml')
    writer.save(xml_filename)

print("Processing complete!")
