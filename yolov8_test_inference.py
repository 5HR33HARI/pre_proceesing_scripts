import os
import glob
import cv2
from pascal_voc_writer import Writer
from infe_yv8 import Inference

# Initialize the OCR model
predictor = Inference()
predictor.weights_path = r"best.pt"
predictor.image_size = 1280
predictor.common_confidence = 0.1
predictor.defects = []
predictor.features = []
predictor.ind_thresh = {"Ruptured": 0.1}
predictor_model = predictor.load_model()

def create_xml(file, cords):
    try:
        img = cv2.imread(file)
        if img is None:
            print(f"Error: Image at {file} could not be loaded.")
            return
        
        height, width, _ = img.shape
        writer = Writer(file, height, width)

        if not cords:
            print("No coordinates to write.")
            return

        for i in cords:
            for k, v in i.items():
                xmin, ymin, xmax, ymax = v
                writer.addObject(k, xmin, ymin, xmax, ymax)

        xml_path = file.replace('.jpg', '.xml')
        writer.save(xml_path)
        print(f"Saved XML to {xml_path}")
        
    except Exception as e:
        print(f"Error in create_xml: {e}")

def create_dir(path):
    if not os.path.isdir(path):
        os.makedirs(path)

def inference_frame(images_folder_path, out_predicted, out_empty, out_input):
    images_folder_path = os.path.join(images_folder_path, '*.jpg')
    images = glob.glob(images_folder_path)
    print(f"Found {len(images)} images.")

    for image in images: 
        try:
            print(f"Processing {image}...")
            img = cv2.imread(image)
            if img is None:
                print(f"Error: Could not read image {image}.")
                continue
            
            predicted_frame, detector_predictions, cords = predictor.get_inferenece(predictor_model, img)
            print("Inference completed.")

            if detector_predictions:
                print("Predictions found.")
                create_dir(out_predicted)
                out_image_path = os.path.join(out_predicted, os.path.basename(image))
                cv2.imwrite(out_image_path, predicted_frame)

                create_dir(out_input)
                out_image_path_input = os.path.join(out_input, os.path.basename(image))
                cv2.imwrite(out_image_path_input, img)
                
                create_xml(out_image_path_input, cords)
            else:
                print("No predictions.")
                create_dir(out_empty)
                out_image_path = os.path.join(out_empty, os.path.basename(image))
                cv2.imwrite(out_image_path, predicted_frame)

        except Exception as e:
            print(f"Error processing {image}: {e}")

if __name__ == '__main__':
    images_folder_path = r"testing"
    out_predicted = r"predicted"
    out_empty = r"empty"
    out_input = r"input"

    inference_frame(images_folder_path, out_predicted, out_empty, out_input)
