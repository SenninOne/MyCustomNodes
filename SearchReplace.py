class SearchReplaceNode:
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {"default": "", "multiline": True}),
                "replacements": ("STRING", {"default": "search1:replace1;search2:replace2"}),
            }
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "perform_replacements"
    CATEGORY = "text processing"

    def perform_replacements(self, text, replacements):
        # Split the replacements string into individual search:replace pairs
        pairs = replacements.split(";")
        
        # Process each pair
        for pair in pairs:
            if ":" in pair:  # Ensure the pair is valid
                search, replace = pair.split(":", 1)  # Split on the first colon only
                text = text.replace(search, replace)
        
        return (text,)
