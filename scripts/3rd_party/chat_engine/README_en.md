# ChatEngine / Processor User Manual

This documentation is based on the implementation in chat_engine/src/chat_engine/processor_builder.py. It introduces the core functions, usage methods, input/output formats, and extensibility of the module to help you quickly get started and customize it to your needs.

================================================================                
Table of Contents
================================================================
- Overview
- Installation & Dependencies
- Key Components
  - The Processor Class
- Input Data (JSON) Format
- Prompt Template Specifications
- Quick Start Example
- Customization & Extension
- Error Handling & Troubleshooting

----------------------------------------------------------------
Overview
----------------------------------------------------------------
The Processor is a streamlined pipeline tool designed for batch image (or item) inference. It provides the following capabilities:
- Reads pending items from a set of JSON files (usually containing image paths and metadata).
- Constructs prompts using a user-defined kwargs_generator (supporting system/user prompts and images).
- Executes inference via a user-provided inference_func (e.g., calling OpenAI-style APIs).
- Organizes and writes results into output JSON files categorized by namespace and task_name.
- Logs runtime exceptions to dedicated error log files for debugging.

----------------------------------------------------------------
Installation & Dependencies
----------------------------------------------------------------
Main Requirements:
- Python: 3.12+
- tqdm: For progress bar visualization.
- openai: Required if using the built-in create_default_openai_inference.

Installation Example:
# Example only; please run in your local environment
uv add /path/to/whl.whl

----------------------------------------------------------------
Key Components
----------------------------------------------------------------

1) The Processor Class
Constructor Signature (Key Parameters):
- namespace: str. Formatted as "company/model_name", used for naming output directories.
- task_name: str. Identifier for the task (e.g., "image_inference").
- sys_prompt_template_path: str. Path to the system prompt template (supports .format(**kwargs)).
- user_prompt_template_path: str. Path to the user prompt template.
- kwargs_generator: Callable. Signature func(image_path_or_item) -> Dict. This generates the variables used to fill the templates.
- inference_func: Callable. Signature inference_func(messages=messages). Returns the inference result.
- input_json_paths: List[str]. List of paths to input JSON files containing data.
- Optional Arguments: image_filter, base_folder, output_folder, random_seed, sample_rate.

Core Methods:
- fetch_images(): Loads content from input_json_paths, merges with base_folder, applies sample_rate sampling, and performs deduplication based on existing output files.
- build_prompt(image_path): Calls kwargs_generator to get parameters, populates prompt templates, and converts images into message image_url (data URI) structures. Returns (messages, kwargs).
- run(drop_history=False): Iterates through items, calls inference_func, appends results, and logs exceptions to error_log.
- update_json() / update_error_log(): Persists results and errors to disk.
- load_processed_images(): Loads previously processed items from existing output files (supports breakpoint resume and deduplication).

Output Paths:
- Results JSON: {output_folder}/{company}/{name}/{task_name}.json
- Error Log: {output_folder}/{company}/{name}/{task_name}_error_log.json

----------------------------------------------------------------
Input Data (JSON) Format
----------------------------------------------------------------
The input JSON files should typically contain a list of objects. Each object represents a task item.
Example:
[
  {
    "image_path": "path/to/image1.jpg",
    "metadata": "some_info"
  },
  {
    "image_path": "path/to/image2.png",
    "metadata": "other_info"
  }
]
The Processor will extract the image_path (or the whole item depending on your kwargs_generator) to process.

----------------------------------------------------------------
Prompt Template Specifications
----------------------------------------------------------------
Templates use standard Python format string syntax.
- System Prompt Example: "You are an AI specialized in {domain}."
- User Prompt Example: "Describe the following image. Context: {context}"

The keys {domain} and {context} must be provided by your kwargs_generator.

----------------------------------------------------------------
Quick Start Example
----------------------------------------------------------------
from chat_engine.processor_builder import Processor, create_default_openai_inference

# 1. Define how to generate prompt variables from an item
def my_kwargs_gen(item):
    return {"context": item.get("metadata", "No context")}

# 2. Setup inference (OpenAI Example)
my_inference = create_default_openai_inference(api_key="sk-...", model="gpt-4o")

# 3. Initialize Processor
proc = Processor(
    namespace="openai/gpt-4o",
    task_name="description_task",
    sys_prompt_template_path="prompts/sys.txt",
    user_prompt_template_path="prompts/user.txt",
    kwargs_generator=my_kwargs_gen,
    inference_func=my_inference,
    input_json_paths=["data/input.json"],
    base_folder="/images/root/"
)

# 4. Run
proc.run()

----------------------------------------------------------------
Customization & Extension
----------------------------------------------------------------
- Custom Inference: You can pass any function to inference_func as long as it accepts a messages list and returns a string or object that can be serialized to JSON.
- Complex Prompts: Override build_prompt if you need to support multiple images per message or custom message structures.
- Sampling: Use sample_rate (0.0 to 1.0) to test on a subset of data before running a full batch.

----------------------------------------------------------------
Error Handling & Troubleshooting
----------------------------------------------------------------
- Missing Images: If a file path is invalid, the Processor logs the error to the _error_log.json and continues to the next item.
- API Failures: Network timeouts or API errors are caught within the run loop to ensure one failure doesn't crash the entire batch.
- Checkpointing: If the process is interrupted, simply run it again with the same namespace and task_name. The Processor automatically detects and skips already processed image_paths.