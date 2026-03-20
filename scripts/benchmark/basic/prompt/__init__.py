import os

base_path = os.path.abspath(os.path.join(os.path.dirname(__file__)))

# System prompts
SYS_SMF = os.path.join(
    base_path, "system", "single_mode_forgery_system_prompt.txt"
)
SYS_CMO = os.path.join(base_path, "system", "composite_manipulation_operations_system_prompt.txt"
)
SYS_CMI = os.path.join(
    base_path, "system", "cross_modal_inconsistency_system_prompt.txt"
)
# User prompts
USR_SMF = os.path.join(
    base_path, "user", "single_mode_forgery_user_prompt.txt"
)
USR_CMO = os.path.join(base_path, "user", "composite_manipulation_operations_user_prompt.txt")
USR_CMI = os.path.join(
    base_path, "user", "cross_modal_inconsistency_user_prompt.txt"
)

__all__ = [
    "SYS_SMF",
    "USR_SMF",
    "SYS_CMO",
    "USR_CMO",
    "SYS_CMI",
    "USR_CMI",
]
