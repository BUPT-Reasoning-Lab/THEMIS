# post_progress

轻量级的图像后处理工具包，提供常用的图像退化/压缩处理器，用于数据增强、对抗样本制作、或模拟低质量图片场景。该包包含三个主要处理类：

- `GaussianBlur`：高斯模糊
- `JpegCompress`：JPEG 压缩（支持 RGBA->RGB 转换）
- `ScaleImage`：图片缩放（支持多种重采样方法）

这些类设计为易于集成到脚本或数据处理流水线中，返回和保存结果到磁盘，并在 `verbose=True` 时打印处理信息。

包导出（入口）
```post_progress/src/post_progress/__init__.py#L1-50
from .gauss_blur import GaussianBlur
from .jpeg_compress import JpegCompress
from .scale_image import ScaleImage

__all__ = ["GaussianBlur", "JpegCompress", "ScaleImage"]

__version__ = "0.1.0"
__author__ = "April"
__email__ = "zhao_yizhuo@bupt.edu.cn"
```

快速开始

1. 安装依赖（推荐在虚拟环境中）：

```/dev/null/example-install.sh#L1-10
uv add /path/to/whl.whl
```

2. 在脚本中使用（最小示例）：

```/dev/null/usage_example.py#L1-200
from post_progress import GaussianBlur, JpegCompress, ScaleImage

# 高斯模糊
gb = GaussianBlur(radius=3, verbose=True)
gb.process_image("data/input.jpg", "out/blurred.jpg")

# JPEG 压缩
jc = JpegCompress(quality=30, verbose=True)
jc.process_image("data/input.png", "out/compressed.jpg")

# 缩放
si = ScaleImage(scale_factor=0.5, resample_method="LANCZOS", verbose=True)
si.process_image("data/input.jpg", "out/scaled.jpg")
```

详细 API

- GaussianBlur
  - 文件：`post_progress/src/post_progress/gauss_blur.py`
  - 初始化：
    - `GaussianBlur(radius=5, verbose=True)`
      - `radius`：模糊半径，值越大模糊越明显（默认 5）
      - `verbose`：是否打印处理信息（默认 True）
  - 方法：
    - `process_image(input_path, output_path)`：对 `input_path` 的图片应用高斯模糊并保存到 `output_path`。会自动创建输出目录。

参考实现：
```post_progress/src/post_progress/gauss_blur.py#L1-200
import os
from PIL import Image, ImageFilter

class GaussianBlur:
    """高斯模糊处理器"""

    def __init__(self, radius=5, verbose=True):
        ...
    def process_image(self, input_path, output_path):
        ...
```

- JpegCompress
  - 文件：`post_progress/src/post_progress/jpeg_compress.py`
  - 初始化：
    - `JpegCompress(quality=50, verbose=True)`
      - `quality`：JPEG 质量，1-100（值越小压缩越强，默认 50）
      - `verbose`：是否打印处理信息
  - 方法：
    - `process_image(input_path, output_path)`：将图片保存为 JPEG 格式并应用指定 `quality`，如果输入为 RGBA 模式会自动转换为 RGB。返回实际保存的输出路径（会强制 `.jpg` 后缀）。

参考实现：
```post_progress/src/post_progress/jpeg_compress.py#L1-200
import os
from PIL import Image

class JpegCompress:
    """JPEG压缩处理器"""

    def __init__(self, quality=50, verbose=True):
        ...
    def process_image(self, input_path, output_path):
        ...
```

- ScaleImage
  - 文件：`post_progress/src/post_progress/scale_image.py`
  - 初始化：
    - `ScaleImage(scale_factor=0.5, resample_method="LANCZOS", verbose=True)`
      - `scale_factor`：缩放比例，相对原始尺寸（例如 0.5 表示缩小到 50%）
      - `resample_method`：可选 `"LANCZOS"`, `"BILINEAR"`, `"BICUBIC"`, `"NEAREST"`
      - `verbose`：是否打印处理信息
  - 方法：
    - `process_image(input_path, output_path)`：按 `scale_factor` 计算目标尺寸，使用指定的重采样方法进行缩放并保存到 `output_path`。

参考实现：
```post_progress/src/post_progress/scale_image.py#L1-200
import os
from PIL import Image

class ScaleImage:
    """图像缩放处理器"""

    def __init__(self, scale_factor=0.5, resample_method="LANCZOS", verbose=True):
        ...
    def process_image(self, input_path, output_path):
        ...
```

实用建议与注意事项

- 输入/输出格式
  - `process_image` 接受任意 Pillow 支持的图片格式作为输入路径，会自动创建输出文件夹。
  - `JpegCompress` 会将输出强制为 `.jpg`，且在遇到有透明通道（RGBA）时会自动转换为 RGB，以避免保存 JPEG 时异常。

- 性能
  - 这些处理器针对单张图片进行同步处理；如果需要并行处理大量图片，可以在上层脚本中结合 `concurrent.futures.ThreadPoolExecutor` 或 `ProcessPoolExecutor` 来并发运行 `process_image`。

- 重采样方法
  - 对于高质量缩放（下采样或上采样），建议使用 `LANCZOS`。`NEAREST` 用于快速但质量最低的场景。

- 错误处理
  - 函数不会对所有异常进行捕获，调用者应在脚本中根据需要捕获和记录异常以保证批处理鲁棒性。

示例：批处理目录中的图片，按顺序应用链式处理（缩放 -> 高斯模糊 -> JPEG 压缩）
```/dev/null/chain_example.py#L1-200
from pathlib import Path
from post_progress import ScaleImage, GaussianBlur, JpegCompress

src_dir = Path("dataset/images")
out_dir = Path("dataset/processed")
out_dir.mkdir(parents=True, exist_ok=True)

scale = ScaleImage(scale_factor=0.6, resample_method="LANCZOS", verbose=False)
blur = GaussianBlur(radius=2, verbose=False)
compress = JpegCompress(quality=40, verbose=True)

for p in src_dir.glob("*.*"):
    scaled_path = out_dir / f"{p.stem}_scaled{p.suffix}"
    scale.process_image(str(p), str(scaled_path))

    blurred_path = out_dir / f"{p.stem}_scaled_blur{p.suffix}"
    blur.process_image(str(scaled_path), str(blurred_path))

    final_path = out_dir / f"{p.stem}_final.jpg"
    compress.process_image(str(blurred_path), str(final_path))
```

开发者信息与版本
- 当前版本：`0.1.0`
- 作者：April
- 邮箱：`zhao_yizhuo@bupt.edu.cn`
