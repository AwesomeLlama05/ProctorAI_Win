import os
import yaml
from dotenv import find_dotenv, load_dotenv
from api_models import *
from procrastination_event import ProcrastinationEvent
from utils import take_screenshot

dotenv_file = find_dotenv()
load_dotenv(dotenv_file)

SCREENSHOTS_FOLDER = os.getenv("SCREENSHOTS_FOLDER", default=os.path.dirname(__file__))

with open(os.path.dirname(__file__) + "/config_prompts.yaml", "r") as file:
    config = yaml.safe_load(file)

def model_pipeline(
    model: Model,
    judge_model,
    user_prompt: str,
    total_cost: float,
    image_filepaths: list,
    print_CoT=False,
):
    # goes from model to determination of "productive" or "procrastinating"
    response = model.call_model(
        user_prompt, system_prompt=config["system_prompt"], image_paths=image_filepaths
    )
    if print_CoT:
        print(response)
    pricing_info_dict = model.count_tokens(
        config["system_prompt"],
        config["user_prompt"],
        response,
        image_paths=image_filepaths,
    )
    if pricing_info_dict is not None:
        total_cost += pricing_info_dict["total_cost"]
    determination = judge_model.call_model(
        config["user_prompt_judge"] + response,
        system_prompt=config["system_prompt_judge"],
    )
    pricing_info_dict = model.count_tokens(
        config["system_prompt_judge"],
        config["user_prompt_judge"] + response,
        determination,
    )
    if pricing_info_dict is not None:
        total_cost += pricing_info_dict["total_cost"]
    return determination, total_cost

def analyze_procrastination(
    user_spec: str,
    model_name: str = "claude-3-5-sonnet-20240620",
    print_CoT: bool = False,
    two_tier: bool = False,
    router_model_name: str = "llava"
) -> tuple[str, list]:
    """
    Analyzes screenshots for procrastination.
    Returns (determination, screenshot_paths)
    """
    proctor_model = create_model(model_name)
    router_model = create_model(router_model_name) if two_tier else None
    total_cost = 0
    
    image_filepaths = take_screenshots()
    
    if two_tier:
        # First check with router model
        determination, total_cost = model_pipeline(
            router_model,
            proctor_model,
            config["user_prompt_strict"].format(user_spec=user_spec),
            total_cost,
            image_filepaths,
            print_CoT=print_CoT,
        )
        if "procrastinating" not in determination.lower():
            return determination, image_filepaths
            
    # Either no two_tier or router detected procrastination
    determination, total_cost = model_pipeline(
        proctor_model,
        proctor_model,
        config["user_prompt"].format(user_spec=user_spec),
        total_cost,
        image_filepaths,
        print_CoT=print_CoT,
    )
    
    return determination, image_filepaths

def handle_procrastination(
    user_spec: str,
    user_name: str,
    proctor_model: Model,
    tts: bool = False,
    voice: str = "Patrick",
    countdown_time: int = 15,
    image_filepaths: list = None
):
    """Handles procrastination event with popups and audio"""
    api_params = [
        {
            "role": "heckler",
            "user_prompt": config["user_prompt_heckler"].format(
                user_spec=user_spec, user_name=user_name
            ),
            "system_prompt": config["system_prompt_heckler"].format(
                user_name=user_name
            ),
            "image_paths": image_filepaths,
        },
        {
            "role": "pledge",
            "user_prompt": config["user_prompt_pledge"].format(
                user_spec=user_spec, user_name=user_name
            ),
            "system_prompt": config["system_prompt_pledge"],
            "image_paths": image_filepaths,
        },
        {
            "role": "countdown",
            "user_prompt": config["user_prompt_countdown"].format(user_spec=user_spec),
            "system_prompt": config["system_prompt_countdown"],
            "image_paths": image_filepaths,
        },
    ]

    api_results = parallel_api_calls(proctor_model, api_params)

    for api_result in api_results:
        if api_result["role"] == "heckler":
            heckler_message = api_result["result"]
        if api_result["role"] == "pledge":
            pledge_message = api_result["result"]
        if api_result["role"] == "countdown":
            countdown_message = api_result["result"]

    if tts:
        voice_file = get_text_to_speech(heckler_message, voice)
        tts_thread = threading.Thread(target=play_text_to_speech, args=(voice_file,))
        tts_thread.start()

    procrastination_event = ProcrastinationEvent()
    procrastination_event.show_popup(heckler_message, pledge_message)
    procrastination_event.play_countdown(
        countdown_time,
        brief_message=f"You have {countdown_time} seconds to close "
        + countdown_message.strip(),
    )
