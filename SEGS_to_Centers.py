import json

class SEGS_to_Centers_Node:
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "segs": ("SEGS",),  # Accepts single SEGS input
            },
            "optional": {
                "segs_2": ("SEGS",),  # Optional second SEGS input
                "segs_3": ("SEGS",),  # Optional third SEGS input
            }
        }

    RETURN_TYPES = ("STRING",)  # Outputs a JSON string
    RETURN_NAMES = ("centers_json",)  # Optional: Give the output a meaningful name
    FUNCTION = "get_centers"
    CATEGORY = "image/segmentation"

    def get_centers(self, segs, segs_2=None, segs_3=None):
        # Collect all SEGS inputs
        all_segs = [segs]
        if segs_2 is not None:
            all_segs.append(segs_2)
        if segs_3 is not None:
            all_segs.append(segs_3)

        centers = []
        
        # Process each SEGS input
        for segs_input in all_segs:
            # Unpack the SEGS tuple
            image_dims, segments = segs_input
            
            # Calculate center coordinates for each segment
            for seg in segments:
                # Get bounding box coordinates from the correct attribute
                bbox = seg.bbox  # Access bbox directly from the SEG object
                x1, y1, x2, y2 = bbox[0], bbox[1], bbox[2], bbox[3]

                # Calculate center
                cx = int((x1 + x2) / 2)
                cy = int((y1 + y2) / 2)
                
                # Append to list with source identifier
                centers.append({
                    "x": cx,
                    "y": cy,
                    "source": seg.label if hasattr(seg, 'label') else "unknown"  # Include label if available
                })
        
        # Convert to JSON string
        centers_json = json.dumps(centers, indent=2)
        
        return (centers_json,)

NODE_CLASS_MAPPINGS = {"SEGS_to_Centers": SEGS_to_Centers_Node}
NODE_DISPLAY_NAME_MAPPINGS = {"SEGS_to_Centers": "SEGS to Centers"}
