class ComparisonNode:
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "segs": ("SEGS",),  # Accepts SEGS input
            }
        }

    RETURN_TYPES = ("SEGS",)  # Outputs filtered SEGS
    RETURN_NAMES = ("filtered_segs",)  # Optional: Give the output a meaningful name
    FUNCTION = "compare_segments"
    CATEGORY = "image/segmentation"

    def compare_segments(self, segs):
        # Unpack the SEGS tuple
        image_dims, segments = segs  # segs is a tuple: (image_dims, list_of_segments)
        
        # Dictionary to store the highest confidence segment for each label
        highest_confidence_segments = {}
        
        for seg in segments:
            label = seg.label
            confidence = seg.confidence[0]  # Confidence is a numpy array, so extract the value
            
            # Check if the label is already in the dictionary
            if label not in highest_confidence_segments:
                # If not, add the current segment
                highest_confidence_segments[label] = seg
            else:
                # If yes, compare confidence and keep the higher one
                if confidence > highest_confidence_segments[label].confidence[0]:
                    highest_confidence_segments[label] = seg
        
        # Convert the dictionary back to a list of segments
        filtered_segments = list(highest_confidence_segments.values())
        
        # Return the filtered SEGS
        return ((image_dims, filtered_segments),)
