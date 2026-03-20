from .model_generator import *
from .prompt import *
from .task_kwargs import *


# Make sure all models do the same question
RANDOM_SEED = 42
OUTPUT_FOLDER = "response/basic"

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
    },
    "CMO": {
        "task_name": "composite_manipulation_operations",
        "sys_prompt_template_path": SYS_CMO,
        "user_prompt_template_path": USR_CMO,
        "input_json_paths": [
            "./assets/dataset/duplication.json",
        ],
        "base_folder": "assets/dataset",
        "kwargs_generator": CMO_kwargs_generator(),
        "output_folder": OUTPUT_FOLDER,
        "random_seed": RANDOM_SEED,
    },
    "CMI": {
        "task_name": "cross_modal_inconsistency",
        "sys_prompt_template_path": SYS_CMI,
        "user_prompt_template_path": USR_CMI,
        "input_json_paths": [
            "./assets/dataset/text_image_inconsistency.json",
        ],
        "base_folder": "assets/dataset",
        "kwargs_generator": CMI_kwargs_generator(),
        "output_folder": OUTPUT_FOLDER,
        "random_seed": RANDOM_SEED,
    },
    "SMF_retract": {
        "task_name": "single_mode_forgery_retract",
        "sys_prompt_template_path": SYS_SMF,
        "user_prompt_template_path": USR_SMF,
        "input_json_paths": [
            "./assets/dataset/retract/forgery_retract.json"
        ],
        "base_folder": "assets/dataset",
        "kwargs_generator": SMF_kwargs_generator(),
        "output_folder": OUTPUT_FOLDER,
        "random_seed": RANDOM_SEED,
    },
    "CMO_retract": {
        "task_name": "composite_manipulation_operations_retract",
        "sys_prompt_template_path": SYS_CMO,
        "user_prompt_template_path": USR_CMO,
        "input_json_paths": [
            "./assets/dataset/retract/duplication_partial.json",
        ],
        "base_folder": "assets/dataset",
        "kwargs_generator": CMO_kwargs_generator(),
        "output_folder": OUTPUT_FOLDER,
        "random_seed": RANDOM_SEED,
    },
}


TASK_LIST = [
    ###################################### Demo code
    # { 
    #     "namespace": "qwen/qwen-vl-max",
    #     'inference_func': {
    #         "SMF": create_openrouter_inference(
    #         task_type_name="SMF",
    #         model="qwen/qwen-vl-max",
    #         ),
    #         "CMO": create_openrouter_inference(
    #             task_type_name="CMO",
    #             model="qwen/qwen-vl-max",
    #         ),
    #         "CMI": create_openrouter_inference(
    #             task_type_name="CMI",
    #             model="qwen/qwen-vl-max",
    #         )
    #     },
    #     'sample_rate': 0.01,
    #     'task_list': ["SMF"]
    # },
    {
        "namespace": "qwen/qwen-vl-max",
        "inference_func": {
            "SMF": create_openrouter_inference(
            task_type_name="SMF",
            model="qwen/qwen-vl-max",
            ),
            "CMO": create_openrouter_inference(
                task_type_name="CMO",
                model="qwen/qwen-vl-max",
            ),
            "CMI": create_openrouter_inference(
                task_type_name="CMI",
                model="qwen/qwen-vl-max",
            ),
        },
        "sample_rate": 1,
        "task_list": [ "CMO"],
    },

    ###################################### End Demo code
    # ---- work line ----
    # Close Model
    # Opensource Model
    # ---- working line ----
]
