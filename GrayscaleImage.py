import torch
import numpy as np
from PIL import ImageOps, Image

class GrayscaleImageNode:
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
FUNCTION = "grayscale_image"
CATEGORY = "image processing"

def grayscale_image(self, image):

# Ensure input image has correct dimensions.
if len(image.shape) == 3:
    # Single channel case e.g., grayscale -> already good.
    pass
elif len(image.shape) == 4 and image.shape[0] in [1, 3]:
    # Channel-first format: batch_size x channels x height x width
    if image.shape[0] == 1:
        image = image.squeeze(0)

# Convert tensor to PIL Image
img_tensor = (255 * image).cpu().numpy()
img_array = img_tensor.transpose((1, 2, 0))   # HWC Format for PIL
img = Image.fromarray(img_array.clip(0, 255).astype(np.uint8))

# Convert to grayscale
grayscale_img = ImageOps.grayscale(img)

# Convert back to torch Tensor with proper shape
grayscale_tensor = torch.from_numpy(
np.array(grayscale_img).astype(np.float32) / 255.0).unsqueeze(0)


return (grayscale_tensor, )
