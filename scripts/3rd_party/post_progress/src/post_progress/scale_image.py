import os
from PIL import Image


class ScaleImage:
    """图像缩放处理器"""

    def __init__(self, scale_factor=0.5, resample_method="LANCZOS", verbose=True):
        """
        初始化图像缩放处理器

        Args:
            scale_factor: 缩放比例，相对于原始尺寸 (默认: 0.5)
            resample_method: 重采样方法，可选 'LANCZOS', 'BILINEAR', 'BICUBIC', 'NEAREST' (默认: 'LANCZOS')
            verbose: 是否显示详细处理信息 (默认: True)
        """
        self.scale_factor = scale_factor
        self.resample_method = resample_method
        self.verbose = verbose

    def _get_resample_method(self):
        """
        获取PIL重采样方法

        Returns:
            PIL重采样方法常量
        """
        methods = {
            "LANCZOS": Image.LANCZOS,
            "BILINEAR": Image.BILINEAR,
            "BICUBIC": Image.BICUBIC,
            "NEAREST": Image.NEAREST,
        }
        return methods.get(self.resample_method, Image.LANCZOS)

    def process_image(self, input_path, output_path):
        """
        对单张图片应用缩放

        Args:
            input_path: 输入图片路径
            output_path: 输出图片路径
        """
        # 确保输出目录存在
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        # 打开图片并应用缩放
        img = Image.open(input_path)
        new_width = int(img.width * self.scale_factor)
        new_height = int(img.height * self.scale_factor)

        # 使用指定的重采样方法
        resample = self._get_resample_method()
        scaled_img = img.resize((new_width, new_height), resample)
        scaled_img.save(output_path)

        if self.verbose:
            print(f"已处理: {input_path} -> {output_path}")
            print(f"  尺寸: {img.width}x{img.height} -> {new_width}x{new_height}")
