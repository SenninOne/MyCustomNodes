import numpy as np
import torch
import cv2
import os
from dataclasses import dataclass
from typing import List, Tuple
import onnxruntime

# ----------------------------
# Embedded Model Code
# ----------------------------

@dataclass
class Box:
    classid: int
    score: float
    x1: int
    y1: int
    x2: int
    y2: int
    cx: int
    cy: int
    gender: int = -1  # -1: Unknown, 0: Male, 1: Female

class YOLOv9:
    def __init__(self, model_path: str, confidence_threshold: float = 0.7):
        self.conf_thresh = confidence_threshold
        self.session = onnxruntime.InferenceSession(
            model_path,
            providers=['CPUExecutionProvider']
        )
        self.input_name = self.session.get_inputs()[0].name
        self.output_names = [output.name for output in self.session.get_outputs()]
        self.input_shape = self.session.get_inputs()[0].shape
        self.input_size = (self.input_shape[3], self.input_shape[2])  # (width, height)

    def __call__(self, image: np.ndarray):
        # Preprocess
        input_tensor = self.preprocess(image)
        
        # Inference
        outputs = self.session.run(
            self.output_names,
            {self.input_name: input_tensor}
        )
        
        # Postprocess
        return self.postprocess(outputs, image.shape)

    def preprocess(self, image: np.ndarray):
        # Resize and normalize
        img = cv2.resize(image, self.input_size)
        img = img.transpose(2, 0, 1)  # HWC to CHW
        img = np.expand_dims(img, axis=0).astype(np.float32) / 255.0
        return img

    def postprocess(self, outputs: List[np.ndarray], img_shape: Tuple[int]):
        boxes = []
        img_height, img_width = img_shape[:2]
        
        # Assuming outputs[0] contains the detection results
        detections = outputs[0][0]  # Remove batch dimension
        
        for detection in detections:
            class_id = int(detection[0])
            score = float(detection[1])
            
            if score < self.conf_thresh:
                continue
                
            x1 = int(detection[2] * img_width)
            y1 = int(detection[3] * img_height)
            x2 = int(detection[4] * img_width)
            y2 = int(detection[5] * img_height)
            
            boxes.append(Box(
                classid=class_id,
                score=score,
                x1=x1,
                y1=y1,
                x2=x2,
                y2=y2,
                cx=(x1 + x2) // 2,
                cy=(y1 + y2) // 2
            ))
            
        return boxes

# ----------------------------
# ComfyUI Node
# ----------------------------

class YOLOv9_SEGS_Node:
    def __init__(self):
        self.models = {}

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "model_type": (["yolov9_t_gender_0245", "yolov9_t_gender_post_0245"],),
                "confidence_threshold": ("FLOAT", {"default": 0.5, "min": 0.0, "max": 1.0, "step": 0.01}),
            },
        }

    RETURN_TYPES = ("SEGS",)
    RETURN_NAMES = ("segs",)
    FUNCTION = "process"
    CATEGORY = "image/segmentation"

    def process(self, image: torch.Tensor, model_type: str, confidence_threshold: float):
        # Model selection
        model_filename = f"{model_type}_1x3x416x416.onnx"
        model_path = os.path.join(os.path.dirname(__file__), model_filename)
        
        # Load model if not cached
        if model_path not in self.models:
            if not os.path.exists(model_path):
                raise ValueError(f"Model file {model_filename} not found in node directory")
                
            self.models[model_path] = YOLOv9(model_path, confidence_threshold)

        # Convert ComfyUI tensor to numpy
        img_np = image[0].cpu().numpy() * 255.0
        img_np = img_np.astype(np.uint8)[..., ::-1]  # RGB to BGR

        # Run inference
        boxes = self.models[model_path](img_np)

        # Convert to SEGS format
        segs = []
        width, height = image.shape[2], image.shape[1]
        
        for box in boxes:
            # Skip invalid boxes
            if box.x2 <= box.x1 or box.y2 <= box.y1:
                continue

            # Create mask (full region)
            mask = np.ones((box.y2 - box.y1, box.x2 - box.x1), dtype=np.float32)
            
            # Create label
            label = "person"
            if box.gender == 0:
                label = "male"
            elif box.gender == 1:
                label = "female"

            # Create SEGS entry
            seg = {
                "cropped_image": image[0, box.y1:box.y2, box.x1:box.x2].unsqueeze(0),
                "cropped_mask": mask,
                "confidence": box.score,
                "crop_region": (box.x1, box.y1, box.x2, box.y2),
                "bbox": (box.x1, box.y1, box.x2, box.y2),
                "label": label,
                "control_net_wrapper": None
            }
            
            # Convert to proper SEGS object
            segs.append(seg)

        # Return in proper SEGS format
        return ((width, height), segs),

NODE_CLASS_MAPPINGS = {"YOLOv9_SEGS": YOLOv9_SEGS_Node}
NODE_DISPLAY_NAME_MAPPINGS = {"YOLOv9_SEGS": "YOLOv9 Detector"}
