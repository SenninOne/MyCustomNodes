import torch
import numpy as np
from PIL import Image, ImageOps

class InvertImageNode:
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "invert_image"
    CATEGORY = "image processing"

    def invert_image(self, image):
        # Convert tensor to PIL Image
        image = 255.0 * image.cpu().numpy()
        img = Image.fromarray(np.clip(image, 0, 255).astype(np.uint8))
        
        # Invert colors
        inverted_img = ImageOps.invert(img)
        
        # Convert back to tensor
        inverted_image = torch.from_numpy(np.array(inverted_img).astype(np.float32) / 255.0).unsqueeze(0)
        return (inverted_image,)
