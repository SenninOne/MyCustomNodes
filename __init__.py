from .TextConcatenator import TextConcatNode
from .MathOperations import AddNumbersNode
from .ImageProcessing import InvertImageNode
from .SearchReplace import SearchReplaceNode
from .ExtractBBox import ExtractBBoxNode
from .ComparisonNode import ComparisonNode
from .SEGS_to_Centers import SEGS_to_Centers_Node
from .RemoveDuplicateTags import RemoveDuplicateTags
from .MaskAreaNode import MaskAreaNode

NODE_CLASS_MAPPINGS = {
    "TextConcatNode": TextConcatNode,
    "AddNumbersNode": AddNumbersNode,
    "InvertImageNode": InvertImageNode,
    "SearchReplaceNode": SearchReplaceNode,
    "ExtractBBoxNode": ExtractBBoxNode,
    "ComparisonNode": ComparisonNode,
    "SEGS_to_Centers": SEGS_to_Centers_Node,
    "RemoveDuplicateTags": RemoveDuplicateTags,
    "MaskAreaNode": MaskAreaNode,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "TextConcatNode": "Text Concatenator",
    "AddNumbersNode": "Add Numbers",
    "InvertImageNode": "Invert Image",
    "SearchReplaceNode": "Search and Replace",
    "ExtractBBoxNode": "Extract Bounding Boxes",
    "ComparisonNode": "Comparison Node",
    "SEGS_to_Centers": "SEGS to Centers",
    "RemoveDuplicateTags": "Remove Duplicate Tags",
    "MaskAreaNode": "Mask Area Node",
}

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']
