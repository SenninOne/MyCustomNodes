class TagSearchNode:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input_text": ("STRING", {"default": "", "multiline": True}),
                "search_tags": ("STRING", {"default": "", "multiline": True}),
            }
        }

    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("matching_tags", "non_matching_tags")
    FUNCTION = "find_tags"
    CATEGORY = "text processing"

    def find_tags(self, input_text, search_tags):
        # Process input tags: split by commas and strip whitespace
        input_tags_list = [t.strip() for t in input_text.split(",") if t.strip()]
        # Create a normalized set from search tags
        search_normalized = {t.strip().lower() for t in search_tags.split(",") if t.strip()}

        matching = []
        non_matching = []
        seen_match = set()
        seen_non_match = set()

        for tag in input_tags_list:
            lower_tag = tag.lower()
            if lower_tag in search_normalized:
                if lower_tag not in seen_match:
                    matching.append(tag)
                    seen_match.add(lower_tag)
            else:
                if lower_tag not in seen_non_match:
                    non_matching.append(tag)
                    seen_non_match.add(lower_tag)

        return (", ".join(matching), ", ".join(non_matching))
