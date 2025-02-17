class ExtractBBoxNode:
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "segs": ("SEGS",),  # Accepts SEGS input
                "indices": ("STRING", {"default": "", "placeholder": "e.g., 0 or 0,2 or leave empty for all"}),  # Index field
                "labels": ((cls.get_labels(), {"default": "all"})),  # Dynamic dropdown for labels
            }
        }

    RETURN_TYPES = ("BBOX",)  # Outputs a list of bounding boxes
    RETURN_NAMES = ("bbox_list",)  # Optional: Give the output a meaningful name
    FUNCTION = "extract_bbox"
    CATEGORY = "image/segmentation"

    @classmethod
    def get_labels(cls):
        # Placeholder for dynamic labels
        # In a real implementation, this would fetch labels from the SEGS input
        return ["all", "FEMALE_GENITALIA_COVERED", "FACE_FEMALE", "BUTTOCKS_EXPOSED", "FEMALE_BREAST_EXPOSED", "FEMALE_GENITALIA_EXPOSED", "MALE_BREAST_EXPOSED", "ANUS_EXPOSED", "FEET_EXPOSED", "BELLY_COVERED", "FEET_COVERED", "ARMPITS_COVERED", "ARMPITS_EXPOSED", "FACE_MALE", "BELLY_EXPOSED", "MALE_GENITALIA_EXPOSED", "ANUS_COVERED", "FEMALE_BREAST_COVERED", "BUTTOCKS_COVERED",]

    def extract_bbox(self, segs, indices, labels):
        # Unpack the SEGS tuple
        _, segments = segs  # segs is a tuple: (image_dims, list_of_segments)
        
        # Parse the indices input
        selected_indices = set()
        if indices.strip() != "":
            for part in indices.split(","):
                part = part.strip()
                if "-" in part:
                    # Handle ranges (e.g., "0-2")
                    start, end = map(int, part.split("-"))
                    selected_indices.update(range(start, end + 1))
                else:
                    # Handle single indices (e.g., "0")
                    selected_indices.add(int(part))
        
        # Filter segments based on indices and labels
        bbox_list = []
        for idx, seg in enumerate(segments):
            # Check if the segment matches the selected indices and labels
            if (not selected_indices or idx in selected_indices) and \
               (labels == "all" or seg.label == labels):
                bbox_list.append(seg.bbox)
        
        return (bbox_list,)
