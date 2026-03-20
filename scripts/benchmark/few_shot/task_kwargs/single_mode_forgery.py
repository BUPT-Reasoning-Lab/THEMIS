from typing import Dict

from .utils import (
    image2base64,
)


def SMF_kwargs_generator(base_folder="assets"):
    """
    Generate function kwargs for image inference task.
    args:
        base_folder: str, the base folder of the reference_answer folder.
    """

    def image_kwargs(image_paths, mask_caption, figure_caption, figure_related) -> Dict:
        mask_required = 'aigc/global' not in image_paths[0]
        note = ("MASK IS REQUIRED if you choose A/B/C; output indices from mask_caption."
        if mask_required else
        "MASK IS NOT REQUIRED for this question; LEAVE <MASK> EMPTY.")
        return {
            "images": [
                image2base64(image_path) for image_path in image_paths
            ],
            "NOTE": note,
            "MASK_CAPTION": mask_caption,
        }

    return image_kwargs
