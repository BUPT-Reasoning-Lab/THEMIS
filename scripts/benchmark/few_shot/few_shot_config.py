from .model_generator import *
from .prompt import *
from .task_kwargs import *


# Make sure all models do the same question
RANDOM_SEED = 42
OUTPUT_FOLDER = "response/few_shot"

TASK_TYPE_PARAMS = {
    "SMF": {
        "task_name": "single_mode_forgery",
        "sys_prompt_template_path": SYS_SMF,
        "user_prompt_template_path": USR_SMF,
        "input_json_paths": [
            "./assets/dataset/forgery.json"
        ],
        "base_folder": "assets/dataset",
        "kwargs_generator": SMF_kwargs_generator(),
        "output_folder": OUTPUT_FOLDER,
        "random_seed": RANDOM_SEED,
    }
}


TASK_LIST = [
    ###################################### Demo code
    {
        "namespace": "qwen/qwen-vl-max",
        "inference_func": {
            "SMF": create_openrouter_inference(
            task_type_name="SMF",
            model="openai/gpt-5",
            ),
        },
        "sample_rate": 0.1,
        "task_list": [ "SMF"],
    },

    ###################################### End Demo code
    # ---- work line ----

    # ---- working line ----
]
