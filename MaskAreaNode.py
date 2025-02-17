import numpy as np
import torch

class MaskAreaNode:
    """
    A node that calculates the fraction of the image area covered by a mask.
    The mask is expected to be a grayscale image (values between 0 and 1) and is
    binarized using a threshold.
    """

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "mask": ("IMAGE",),
                "threshold": (
                    "FLOAT",
                    {
                        "default": 0.5,
                        "min": 0.0,
                        "max": 1.0,
                        "step": 0.01,
                        "display": "slider",
                    },
                ),
            }
        }

    RETURN_TYPES = ("FLOAT",)
    FUNCTION = "calculate_area"
    CATEGORY = "ControlNet"

    def calculate_area(self, mask, threshold):
        """
        Calculate the area ratio of the active region in the mask relative to the total image area.

        Args:
            mask (numpy.ndarray or torch.Tensor): A grayscale mask with values in [0, 1].
            threshold (float): Threshold to binarize the mask.

        Returns:
            tuple: A tuple containing only the area ratio as a float.
        """
        # Convert torch.Tensor to numpy array if needed.
        if isinstance(mask, torch.Tensor):
            mask = mask.cpu().numpy()

        # Ensure the mask is float32.
        mask = mask.astype(np.float32)

        # Binarize the mask using the provided threshold.
        binary_mask = (mask > threshold).astype(np.float32)

        # If the image has more than 2 dimensions (e.g. a channel dimension), assume the first is channels.
        if binary_mask.ndim > 2:
            total_pixels = np.prod(binary_mask.shape[1:])
        else:
            total_pixels = np.prod(binary_mask.shape)

        # Sum the binary mask to get the count of active pixels.
        active_pixels = np.sum(binary_mask)

        # Compute the ratio.
        area_ratio = active_pixels / total_pixels if total_pixels > 0 else 0.0

        # Return only the area_ratio (e.g., 0.17578125) in a tuple.
        return (area_ratio,)
