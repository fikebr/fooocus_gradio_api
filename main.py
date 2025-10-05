import argparse
import logging
import sys
from typing import Optional, List

from src.logger import setup_logging
from src.fooocus_client import FooocusClient
from src.models import GenerationParams
from src.prompts_parser import parse_prompts_file


def main() -> None:
    """CLI entrypoint to automate Fooocus generation."""
    logger = setup_logging()

    parser = argparse.ArgumentParser(description="Automate Fooocus via Gradio API")
    # Prompt inputs
    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument("--prompt", help="Main text prompt")
    group.add_argument("--prompts_file", help="Path to text file with prompts; separate prompts with lines containing only '---'")
    parser.add_argument("--delimiter", default="---", help="Delimiter line used to split prompts in file")
    # Generation options
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
        # Validate prompt inputs when not inspecting
        if not args.prompt and not args.prompts_file:
            parser.error("one of --prompt or --prompts_file is required unless using --inspect")

        # Single prompt path
        if args.prompt:
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
            print(result)
            return

        # Batch file path
        prompts: List[str] = parse_prompts_file(args.prompts_file, delimiter=args.delimiter)
        if not prompts:
            logger.error("No prompts found in file '%s'", args.prompts_file)
            sys.exit(2)
        total = len(prompts)
        failures = 0
        for idx, prompt_text in enumerate(prompts, start=1):
            try:
                logger.info("[%d/%d] Generating for prompt (%d chars)", idx, total, len(prompt_text))
                if args.simple:
                    client.generate_simple(prompt=prompt_text, num_images=args.num_images)
                else:
                    params = GenerationParams(
                        prompt=prompt_text,
                        negative_prompt=args.negative_prompt,
                        num_images=args.num_images,
                        seed=args.seed,
                    )
                    client.configure_and_generate(params)
                logger.info("[%d/%d] Completed", idx, total)
            except Exception as exc:  # noqa: BLE001
                failures += 1
                logging.exception("[%d/%d] Generation failed: %s", idx, total, exc)
                continue
        logger.info("Batch completed: total=%d, failures=%d", total, failures)
        print({"total": total, "failures": failures})
    except Exception as exc:  # noqa: BLE001
        logging.exception("Generation failed: %s", exc)
        sys.exit(1)


if __name__ == "__main__":
    main()
