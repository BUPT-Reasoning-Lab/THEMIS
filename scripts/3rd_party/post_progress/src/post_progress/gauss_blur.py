import os
from PIL import Image, ImageFilter


class GaussianBlur:
    """高斯模糊处理器"""

    def __init__(self, radius=5, verbose=True):
        """
        初始化高斯模糊处理器

        Args:
            radius: 模糊半径，值越大模糊效果越强 (默认: 5)
            verbose: 是否显示详细处理信息 (默认: True)
        """
        self.radius = radius
        self.verbose = verbose

    def process_image(self, input_path, output_path):
        """
        对单张图片应用高斯模糊

        Args:
            input_path: 输入图片路径
            output_path: 输出图片路径
        """
        # 确保输出目录存在
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        # 打开图片并应用高斯模糊
        img = Image.open(input_path)
        blurred_img = img.filter(ImageFilter.GaussianBlur(radius=self.radius))
        blurred_img.save(output_path)

        if self.verbose:
            print(f"已处理: {input_path} -> {output_path}")
