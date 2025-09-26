"""
This module provides constants that categorize types of content based on
explicit and suggestive rules. It also includes accepted file extensions
for image processing.

Constants:
    EXPLICIT_RULES (tuple):
        Categories for explicit content classification.

    SUGGESTIVE_RULES (tuple):
        Categories for suggestive content classification.

    IMAGE_EXTS (set):
        Valid image file extensions for filtering.

"""


EXPLICIT_RULES = (
    'FEMALE_BREAST_EXPOSED',
    'FEMALE_GENITALIA_EXPOSED',
    'MALE_GENITALIA_EXPOSED',
    'ANUS_EXPOSED',
)
""" Explicit content classification categories. """


SUGGESTIVE_RULES = (
    'BELLY_EXPOSED',
    'BUTTOCKS',
    'MALE_BREAST',
    'ARMPITS',
    'UNDERWEAR',
    'LINGERIE',
    'CLEAVAGE',
)
""" Suggestive content classification categories. """


IMAGE_EXTS = {'.jpg', '.jpeg', '.png', '.webp', '.bmp', '.gif'}
""" Valid image file extensions for filtering. """


__all__ = [
    'EXPLICIT_RULES',
    'SUGGESTIVE_RULES',
    'IMAGE_EXTS',
]
