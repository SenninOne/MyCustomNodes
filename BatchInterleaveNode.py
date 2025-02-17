import torch

class BatchInterleaveNode:
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "inputcount": ("INT", {"default": 2, "min": 2, "max": 25, "step": 1}),
            },
            "optional": {
                **{f"batch_{i+1}": ("IMAGE",) for i in range(25)}
            }
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("interleaved_batch",)
    FUNCTION = "interleave"
    CATEGORY = "image/batch"

    def interleave(self, inputcount, **kwargs):
        # Collect batches in order up to inputcount
        batches = [kwargs.get(f"batch_{i+1}") for i in range(inputcount)]
        
        # Filter out None values
        valid_batches = [b for b in batches if b is not None]
        
        if not valid_batches:
            raise ValueError("At least one batch must be provided")
            
        # Validate dimensions
        shapes = [b.shape[1:] for b in valid_batches]
        if len(set(shapes)) > 1:
            raise ValueError("All batches must have the same height, width, and channels")
            
        # Find minimum batch size
        min_batch_size = min(b.shape[0] for b in valid_batches)
        
        # Interleave images
        interleaved = []
        for i in range(min_batch_size):
            for batch in valid_batches:
                interleaved.append(batch[i])
        
        return (torch.stack(interleaved), )

NODE_CLASS_MAPPINGS = {"BatchInterleave": BatchInterleaveNode}
NODE_DISPLAY_NAME_MAPPINGS = {"BatchInterleave": "Batch Interleaver"}
