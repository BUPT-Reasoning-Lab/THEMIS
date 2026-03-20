# THEMIS Benchmark Scripts

This directory contains benchmark scripts for evaluating AI models on the THEMIS dataset, which focuses on detecting academic image manipulation and forgery in scientific publications.

## Overview

The benchmark framework is designed to evaluate models on three main tasks:
- **SMF** (Single Mode Forgery): Single image forgery detection
- **CMO** (Composite Manipulation Operations): Duplication detection across multiple images  
- **CMI** (Cross Modal Inconsistency): Text-image inconsistency detection

## Directory Structure

```
benchmark/
├── main.py              # Main execution script with parallel processing
├── basic/               # Basic benchmark configurations
│   ├── basic_config.py  # Core configuration for all task types
│   ├── model_generator/ # Model and inference function generators
│   ├── prompt/          # System and user prompt templates
│   └── task_kwargs/     # Task-specific argument generators
├── few_shot/            # Few-shot learning configurations
├── CoT/                 # Chain-of-Thought configurations
└── .env-example         # Environment variables template
```

## Task Types

### Single Mode Forgery Identification and Localization (SMF)
- **Purpose**: Detect forgery in individual scientific images
- **Dataset**: `assets/dataset/forgery.json`
- **Output**: Single Selection (fraude type/authentic/not sure) with mask and explanation

### Composite Manipulation Operations Identification(CMO)
- **Purpose**: Detect duplication across multiple panels/figures
- **Dataset**: `assets/dataset/duplication.json`
- **Output**: Multiple Selection (types of manipulation operations/autehntic/not sure) and explanation

### Cross Modal Inconsistency Identification and Localization(CMI)
- **Purpose**: Detect inconsistencies between text descriptions and images
- **Dataset**: `assets/dataset/text_image_inconsistency.json`
- **Output**: Single Selection (inconsistency type/authentic/not sure) with tampered region and explanation

## Usage

### Environment Setup
1. Copy `.env-example` to `.env` and configure your API keys
2. Install dependencies using uv:
   ```bash
   uv sync --group benchmark
   ```

### Running Benchmarks

#### Basic Mode
```bash
cd scripts/benchmark
python main.py
```

#### Few-Shot Mode
```bash
# Modify main.py to import few_shot config
from few_shot.few_shot_config import *
python main.py
```

#### Chain-of-Thought Mode
```bash
# Modify main.py to import CoT config
from CoT.CoT_config import *
python main.py
```

## Configuration

### Task Parameters
Each task type is configured in `basic_config.py` with:
- `task_name`: Unique identifier for the task
- `sys_prompt_template_path`: System prompt template file
- `user_prompt_template_path`: User prompt template file
- `input_json_paths`: Dataset file paths
- `kwargs_generator`: Argument generator for model inputs
- `output_folder`: Results output directory
- `random_seed`: Reproducibility seed

### Parallel Processing
- `MAX_WORKERS`: Number of parallel processes (default: 2)
- Adjust based on your system capabilities
- Each worker processes tasks independently with progress bars

### Customization
To add new task types:
1. Create prompt templates in `prompt/` directory
2. Implement kwargs generator in `task_kwargs/`
3. Add configuration to `TASK_TYPE_PARAMS` in `basic_config.py`

## Output Format

Results are saved in the specified `output_folder` with:
- Model responses in JSON format
- Performance metrics and statistics
- Unprocessed image lists for debugging

## Dependencies

Core dependencies managed by uv:
- `chat-engine`: Model inference framework
- `llm-json-parser`: Response parsing utilities
- `openai`: OpenAI API client
- `pillow`: Image processing

## Model Support

The framework supports multiple models through configurable inference functions:
- OpenAI GPT models
- Local models via API endpoints
- Custom model implementations

## Troubleshooting

### Common Issues
1. **API Key Errors**: Ensure `.env` file is properly configured
2. **Memory Issues**: Reduce `MAX_WORKERS` if running out of memory
3. **Dataset Path Errors**: Verify dataset files exist in `assets/dataset/`
```

## Performance Tips

1. **Batch Processing**: Use appropriate batch sizes for your model
2. **Caching**: Enable response caching for repeated evaluations
3. **Resource Management**: Monitor GPU/CPU usage during parallel execution

## Contributing

To add new benchmark tasks:
1. Create task-specific configuration in appropriate directory
2. Add prompt templates for the task
3. Implement kwargs generation logic
4. Update this README with task documentation

## License

This benchmark framework is part of the THEMIS project for academic integrity research.
