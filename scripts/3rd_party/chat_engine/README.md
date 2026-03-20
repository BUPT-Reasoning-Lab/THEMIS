# chat_engine / Processor 使用说明

下面的文档基于实现文件 `chat_engine/src/chat_engine/processor_builder.py`，介绍该模块的主要功能、使用方法、输入/输出格式以及可扩展点，方便你快速上手并根据需要进行定制。

目录
- 概览
- 安装与依赖
- 关键组件简介
  - `Processor` 类
- 输入数据（JSON）格式说明
- prompt 模板说明
- 快速使用示例
- 自定义点与扩展
- 错误处理与日志
- 常见问题与排查建议

概览
----
`Processor` 是一个面向批量图像（或其它 item）推理的简单流水线工具。它提供以下能力：
- 从一组 JSON 文件中读取待处理项（通常包含图片路径等元信息）
- 根据用户提供的 `kwargs_generator` 构建 prompt（包含 system/user prompt 与图片）
- 调用用户提供的 `inference_func` 进行推理（例如调用 OpenAI 风格的接口）
- 将结果写入按 `namespace`/`task_name` 组织的输出 JSON
- 记录运行时错误到错误日志文件

安装与依赖
-----------
主要依赖：
- Python 3.12
- `tqdm`（进度条）
- `openai`（如果要使用内置的 `create_default_openai_inference`）

安装示例：
```chat_engine/src/chat_engine/processor_builder.py#L1-999
# 仅示意，请在你的环境中运行
uv add /path/to/whl.whl
```

关键组件简介
------------

1) `Processor` 类
- 构造签名（关键参数）：
  - `namespace: str`，格式 `"company/model_name"`，用于输出目录命名
  - `task_name: str`，例如 `"image_inference"`
  - `sys_prompt_template_path: str`，system prompt 的文件路径（模板，使用 `.format(**kwargs)`）
  - `user_prompt_template_path: str`，user prompt 的文件路径（模板）
  - `kwargs_generator: Callable`，签名应为 `func(image_path_or_item) -> Dict`（详见下文）
  - `inference_func: Callable`，签名应支持 `inference_func(messages=messages)`，返回推理结果
  - `input_json_paths: List[str]`，包含输入数据（JSON 文件）的路径列表
  - 可选项：`image_filter`, `base_folder`, `output_folder`, `random_seed`, `sample_rate`
- 主要方法：
  - `fetch_images()`：加载 `input_json_paths` 中的内容并生成待处理项列表（合并 `base_folder`），同时支持 `sample_rate` 采样和去重（基于已有输出文件）
  - `build_prompt(image_path)`：调用 `kwargs_generator` 获取参数，填充 sys/user prompt 模板，并将 `images` 转为 message 中的 `image_url`（data URI）结构；返回 `messages, kwargs`
  - `run(drop_history=False)`：迭代待处理项，调用 `inference_func` 并把结果追加到 `results`，遇到异常时记录到 `error_log`
  - `update_json()` / `update_error_log()`：持久化结果与错误
  - `load_processed_images()`：如果存在历史输出，会把已处理的 items 载入（用于断点续跑和去重）
- 输出路径：
  - 输出 JSON: `{output_folder}/{company}/{name}/{task_name}.json`
  - 错误日志: `{output_folder}/{company}/{name}/{task_name}_error_log.json`
