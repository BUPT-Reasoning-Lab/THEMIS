from typing import Dict

from .utils import (
    image2base64,
)


def CMO_kwargs_generator(base_folder="assets"):
    """
    Generate function kwargs for image inference task.
    args:
        base_folder: str, the base folder of the reference_answer folder.
    """

    def image_kwargs(image_paths,mask_caption, figure_caption, figure_related) -> Dict:
        
        return {
            "images": [
                image2base64(image_path) for image_path in image_paths
            ],
            "MASK_CAPTION": mask_caption,
        }

    return image_kwargs
