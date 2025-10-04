import argparse
import logging
import sys
from typing import Optional

from src.logger import setup_logging
from src.fooocus_client import FooocusClient
from src.models import GenerationParams


def main() -> None:
    """CLI entrypoint to automate Fooocus generation."""
    logger = setup_logging()

    parser = argparse.ArgumentParser(description="Automate Fooocus via Gradio API")
    parser.add_argument("--prompt", required=True, help="Main text prompt")
    parser.add_argument("--negative_prompt", default="", help="Negative prompt")
    parser.add_argument("--num_images", type=int, default=1, help="Number of images to generate")
    parser.add_argument("--seed", default="0", help="Seed value as string (0 for random)")
    parser.add_argument("--simple", action="store_true", help="Use simplified generation route")
    parser.add_argument("--inspect", action="store_true", help="Inspect Fooocus API endpoints and exit")

    args = parser.parse_args()

    client = FooocusClient()

    try:
        if args.inspect:
            info = client.inspect_endpoints()
            logger.info("Inspection summary: %s", info.get("summary"))
            print(info.get("summary"))
            return
        if args.simple:
            result = client.generate_simple(prompt=args.prompt, num_images=args.num_images)
        else:
            params = GenerationParams(
                prompt=args.prompt,
                negative_prompt=args.negative_prompt,
                num_images=args.num_images,
                seed=args.seed,
            )
            result = client.configure_and_generate(params)

        logger.info("Generation completed")
        # Print minimal result to stdout for scripting
        print(result)
    except Exception as exc:  # noqa: BLE001
        logging.exception("Generation failed: %s", exc)
        sys.exit(1)


if __name__ == "__main__":
    main()
