import time
import sys
import os
import argparse
from core import analyze_procrastination, handle_procrastination
from api_models import create_model, api_name_to_colloquial

def main(
    model_name="claude-3-5-sonnet-20240620",
    tts=False,
    cli_mode=False,
    voice="Patrick",
    delay_time=0,
    initial_delay=0,
    countdown_time=15,
    user_name="Procrastinator",
    print_CoT=False,
    two_tier=False,
    router_model_name="llava",
):
    os.makedirs("screenshots", exist_ok=True)

    if cli_mode:
        user_spec = input("What do you plan to work on?\n")
    else:
        user_spec = sys.stdin.read()  # read until EOF

    proctor_model = create_model(model_name)
    time.sleep(initial_delay)

    while True:
        # Analyze screenshots for procrastination
        determination, image_filepaths = analyze_procrastination(
            user_spec,
            model_name=model_name,
            print_CoT=print_CoT,
            two_tier=two_tier,
            router_model_name=router_model_name
        )
        
        print(f"{api_name_to_colloquial[model_name]} Determination: ", determination)
        
        if "procrastinating" in determination.lower():
            handle_procrastination(
                user_spec,
                user_name,
                proctor_model,
                tts,
                voice,
                countdown_time,
                image_filepaths
            )
        
        time.sleep(delay_time)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--model_name",
        help="Set model name",
        default="claude-3-5-sonnet-20240620",
        type=str,
    )
    parser.add_argument("--tts", help="Enable heckling", action="store_true")
    parser.add_argument("--voice", help="Set voice", default="Patrick", type=str)
    parser.add_argument("--cli_mode", help="Enable CLI mode", action="store_true")
    parser.add_argument("--delay_time", help="Set delay time", default=0, type=int)
    parser.add_argument(
        "--initial_delay",
        help="Initial delay so user can open relevant apps",
        default=0,
        type=int,
    )
    parser.add_argument(
        "--countdown_time", help="Set countdown time", default=15, type=int
    )
    parser.add_argument(
        "--user_name", help="Set user name", default="Procrastinator", type=str
    )
    parser.add_argument(
        "--print_CoT", help="Show model's chain of thought", action="store_true"
    )
    parser.add_argument(
        "--two_tier", help="Enable two-tier model pipeline", action="store_true"
    )
    parser.add_argument(
        "--router_model", help="Set router model", default="llava", type=str
    )

    args = parser.parse_args()
    main(
        model_name=args.model_name,
        tts=args.tts,
        cli_mode=args.cli_mode,
        voice=args.voice,
        delay_time=args.delay_time,
        initial_delay=args.initial_delay,
        countdown_time=args.countdown_time,
        user_name=args.user_name,
        print_CoT=args.print_CoT,
        two_tier=args.two_tier,
        router_model_name=args.router_model,
    )
