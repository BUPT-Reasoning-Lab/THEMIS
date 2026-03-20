import os
from PIL import Image


class JpegCompress:
    """JPEG压缩处理器"""

    def __init__(self, quality=50, verbose=True):
        """
        初始化JPEG压缩处理器

        Args:
            quality: JPEG质量，范围1-100，值越小压缩率越高 (默认: 50)
            verbose: 是否显示详细处理信息 (默认: True)
        """
        self.quality = quality
        self.verbose = verbose

    def process_image(self, input_path, output_path):
        """
        对单张图片应用JPEG压缩

        Args:
            input_path: 输入图片路径
            output_path: 输出图片路径

        Returns:
            实际的输出路径（可能被修改为.jpg后缀）
        """
        # 确保输出目录存在
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        # 打开图片并应用JPEG压缩
        img = Image.open(input_path)

        # 如果图片是RGBA模式，转换为RGB
        if img.mode == "RGBA":
            img = img.convert("RGB")

        # 确保输出路径是.jpg或.jpeg格式
        output_path_jpg = os.path.splitext(output_path)[0] + ".jpg"

        img.save(output_path_jpg, "JPEG", quality=self.quality)

        if self.verbose:
            print(f"已处理: {input_path} -> {output_path_jpg}")

        return output_path_jpg
