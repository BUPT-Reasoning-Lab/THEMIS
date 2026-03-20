import os

base_path = os.path.abspath(os.path.join(os.path.dirname(__file__)))

# System prompts
SYS_SMF = os.path.join(
    base_path, "system", "single_mode_forgery_system_prompt.txt"
)

# User prompts
USR_SMF = os.path.join(
    base_path, "user", "single_mode_forgery_user_prompt.txt"
)
__all__ = [
    "SYS_SMF",
    "USR_SMF",
]
