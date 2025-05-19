from ultralytics import YOLO
import  cv2
# from ultralytics.utils.plots import Annotator 

class Inference():
	def __init__(self):
		self.weights_path = r''
		self.image_size = 1280
		self.common_confidence = 0.3
		self.common_iou = 0.45
		# self.defects = ["damage","scratch","dent","crushed","stain"]
		self.ind_thresh = {"damage":0.1,"scratch":0.15,"dent":0.15,"crushed":0.2,"stain":0.15} #{"dent":0.6,"crack":0.67,"scratch":0.6,"stepmark_P":0.76,"chamfer_A":0.6,"burr":0.4,"white_rust":0.6,"bulge":0.3,"stepmark_A":0.2,"chamfer_P":0.2}
		self.iou = 0.1
		self.max_det = 100
		self.hide_labels = False
		self.hide_conf = True
		self.line_width = 4
		self.defects =[]
		self.features =[]
		# self.hide_conf=False

	def load_model(self):
		model = YOLO(self.weights_path) 
		return model

	# def get_inferenece(self,model,img):
	# 	annotator = Annotator(img,line_width=self.line_width)
	# 	ind_thresh=self.ind_thresh
	# 	results = model.predict(source=img,conf=self.common_confidence,imgsz=self.image_size,iou=self.iou,max_det=self.max_det)
	# 	boxes = results[0].boxes
	# 	# predicted_image = results.show()
	# 	coordinates = []
	# 	detector_labels = []
	# 	for box in boxes:
	# 		cords = box.xyxy[0].tolist()
	# 		label_cls = int(box.cls[0].item())
	# 		label = model.names[label_cls]
	# 		xmin,ymin,xmax,ymax = int(cords[0]),int(cords[1]),int(cords[2]),int(cords[3])
	# 		if model.names[int(box.cls)] in list(ind_thresh.keys()):
	# 			if float(box.conf) > ind_thresh[model.names[int(box.cls)]]:
	# 				if label in self.defects:
	# 					color = (0,0,255)
	# 				else:
	# 					color = (0,128,0) 
	# 				label = None if self.hide_labels else (model.names[int(box.cls)] if self.hide_conf else f'{model.names[int(box.cls)]} {float(box.conf):.2f}')
	# 				annotator.box_label(box.xyxy[0],label,color=color)
	# 				detector_labels.append(label)
	# 				coordinates.append({label:[xmin,ymin,xmax,ymax]})
	# 		else:
	# 			if label in self.defects:
	# 				color = (0,0,255)
	# 			else:
	# 				color = (0,128,0)
	# 			label = None if self.hide_labels else (model.names[int(box.cls)] if self.hide_conf else f'{model.names[int(box.cls)]} {float(box.conf):.2f}')
	# 			annotator.box_label(box.xyxy[0],label,color=color)
	# 			detector_labels.append(label)
	# 			coordinates.append({label:[xmin,ymin,xmax,ymax]})
	# 	return img, detector_labels, coordinates

	def get_inferenece(self, model, img):
		ind_thresh = self.ind_thresh
		results = model.predict(source=img, conf=self.common_confidence, imgsz=self.image_size, iou=self.iou, max_det=self.max_det)
		boxes = results[0].boxes
		coordinates = []
		detector_labels = []
		for box in boxes:
			cords = box.xyxy[0].tolist()
			label_cls = int(box.cls[0].item())
			label = model.names[label_cls]
			confidence = float(box.conf)
			xmin, ymin, xmax, ymax = int(cords[0]), int(cords[1]), int(cords[2]), int(cords[3])
			if model.names[int(box.cls)] in list(ind_thresh.keys()):
				if confidence > ind_thresh[model.names[int(box.cls)]]:
					if label in self.defects:
						color = (0, 0, 255)
					else:
						color = (0, 128, 0)
					label_text = None if self.hide_labels else (f'{label} {confidence:.2f}' if self.hide_conf else f'{label} {confidence:.2f}')
					cv2.rectangle(img, (xmin, ymin), (xmax, ymax), color, self.line_width)
					cv2.putText(img, label_text, (xmin, ymin - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
					detector_labels.append(label_text)
					coordinates.append({label: [xmin, ymin, xmax, ymax]})
			else:
				if label in self.defects:
					color = (0, 0, 255)
				else:
					color = (0, 128, 0)
				label_text = None if self.hide_labels else (f'{label} {confidence:.2f}' if self.hide_conf else f'{label} {confidence:.2f}')
				cv2.rectangle(img, (xmin, ymin), (xmax, ymax), color, self.line_width)
				cv2.putText(img, label_text, (xmin, ymin - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
				detector_labels.append(label_text)
				coordinates.append({label: [xmin, ymin, xmax, ymax]})
		return img, detector_labels, coordinates




if __name__ == '__main__':
	inference = Inference()
	model = inference.load_model()

# while True:
# 	img = cv2.imread(r"D:\python_programs\bus.jpg")
# 	pre_img, detector_labels, coordinates = inf.get_inferenece(model,img)
# 	print(detector_labels)
# 	cv2.imshow("pred",pre_img)
# 	cv2.waitKey(0)
	

