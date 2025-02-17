class RemoveDuplicateTags:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input_string": ("STRING", {
                    "multiline": True,
                    "default": "kidaxlp, very dark skin, grey hair, banana breasts, perky breasts, dark skin, blue eyes, long hair, jewelry, white hair, facial mark, bangs, lips, makeup, jungle, 1girl, solo, breasts, looking at viewer, large breasts, cleavage, jewelry, flower, hair bow, earrings, pants, realistic"
                }),
                "delimiter": ("STRING", {"default": ","}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("unique_tags",)
    FUNCTION = "remove_duplicates"
    CATEGORY = "text processing"

    def remove_duplicates(self, input_string: str, delimiter: str):
        # Split the string into individual tags
        tags = [tag.strip() for tag in input_string.split(delimiter)]
        
        # Remove duplicates while preserving order
        seen = set()
        unique_tags = []
        for tag in tags:
            if tag not in seen:
                seen.add(tag)
                unique_tags.append(tag)
        
        # Join back into a single string
        result = delimiter.join(unique_tags)
        
        return (result,)

NODE_CLASS_MAPPINGS = {"RemoveDuplicateTags": RemoveDuplicateTags}
NODE_DISPLAY_NAME_MAPPINGS = {"RemoveDuplicateTags": "Remove Duplicate Tags"}
