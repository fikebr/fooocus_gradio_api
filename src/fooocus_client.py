import logging
from typing import Any

from gradio_client import Client
from contextlib import redirect_stdout
import io

from .config import config
from .models import GenerationParams


class FooocusClient:
    """Adapter over Fooocus Gradio API."""

    def __init__(self, base_url: str | None = None) -> None:
        self.base_url = base_url or config.fooocus_url
        self.logger = logging.getLogger(self.__class__.__name__)
        self.client = Client(self.base_url)

    def generate_simple(self, prompt: str, num_images: int = 1) -> Any:
        """Trigger a generation with minimal inputs using full-config fallback."""
        try:
            params = GenerationParams(prompt=prompt, num_images=num_images)
            return self.configure_and_generate(params)
        except Exception as exc:  # noqa: BLE001
            self.logger.exception("Simple generation failed via fallback: %s", exc)
            raise

    def inspect_endpoints(self) -> dict[str, Any]:
        """Return summary of available endpoints and their input counts."""
        try:
            buf = io.StringIO()
            with redirect_stdout(buf):
                self.client.view_api(all_endpoints=True)
            text = buf.getvalue()
            lines = [ln.strip() for ln in text.splitlines()]
            endpoint_lines = [ln for ln in lines if ln.startswith("- predict(")]
            total = 0
            summaries: list[str] = []
            guess_config = None
            guess_trigger = None
            for ln in endpoint_lines:
                total += 1
                # Example: - predict(fn_index=68) -> (...)
                # or: - predict(generate_image_grid_for_each_batch, ..., fn_index=67) ->
                fn_idx = None
                if "fn_index=" in ln:
                    try:
                        fn_idx = int(ln.split("fn_index=")[1].split(")")[0])
                    except Exception:  # noqa: BLE001
                        fn_idx = None
                # Crude input count heuristic: count commas before ') ->' if present
                try:
                    signature = ln.split("predict(", 1)[1].rsplit(")", 1)[0]
                    inputs_count = 0 if signature.strip().startswith("fn_index=") else (signature.count(",") + 1)
                except Exception:  # noqa: BLE001
                    inputs_count = 0
                summaries.append(f"{ln}")
                if guess_config is None and inputs_count > 50 and fn_idx is not None:
                    guess_config = fn_idx
                if guess_trigger is None and inputs_count == 0 and fn_idx is not None and fn_idx >= 60:
                    guess_trigger = fn_idx
            summary_obj = {
                "summary": {
                    "total_endpoints": total,
                    "endpoints": summaries[:20],
                    "guess_config_fn_index": guess_config,
                    "guess_trigger_fn_index": guess_trigger,
                }
            }
            self.logger.info("Endpoint inspection: %s", summary_obj["summary"]) 
            return summary_obj
        except Exception as exc:  # noqa: BLE001
            self.logger.exception("Inspection failed: %s", exc)
            raise

    def configure_via_small_endpoints(self, params: GenerationParams) -> Any:
        """Configure using smaller endpoints and then trigger generation."""
        try:
            # Minimal path observed to work across builds:
            # 1) Set prompt via fn_index=62 with default method
            self.client.predict(params.prompt, "Inpaint or Outpaint (default)", fn_index=62)
            # 2) Trigger generation
            return self.client.predict(fn_index=68)
        except Exception as exc:  # noqa: BLE001
            self.logger.exception("Small-endpoint configuration failed: %s", exc)
            raise

    def configure_and_generate(self, params: GenerationParams) -> Any:
        """Full configuration followed by trigger call."""
        try:
            args: list[Any] = []
            # Core text-to-image configuration matching fn_index=67 signature
            args.extend([
                False,  # generate_image_grid_for_each_batch
                params.prompt,  # parameter_12 (prompt)
                params.negative_prompt,  # negative_prompt
                params.styles,  # selected_styles
                params.performance,  # performance
                params.aspect_ratio,  # aspect_ratios
                params.num_images,  # image_number
                params.output_format,  # output_format
                params.seed,  # seed
                False,  # read_wildcards_in_order
                params.image_sharpness,  # image_sharpness
                params.guidance_scale,  # guidance_scale
                params.base_model,  # base_model_sdxl_only
                "None",  # refiner_sdxl_or_sd_15
                0.5,  # refiner_switch_at
                True, "None", -2,  # LoRA 1
                True, "None", -2,  # LoRA 2
                True, "None", -2,  # LoRA 3
                True, "None", -2,  # LoRA 4
                True, "None", -2,  # LoRA 5
                False,  # input_image
                "",  # parameter_212
                "Disabled",  # upscale_or_variation
                "",  # image (input)
                ["Left"],  # outpaint_direction
                "",  # image (inpaint)
                "",  # inpaint_additional_prompt
                "",  # mask_upload
                True,  # disable_preview
                True,  # disable_intermediate_results
                True,  # disable_seed_increment
                False,  # black_out_nsfw
                1.5,  # positive_adm_guidance_scaler
                0.8,  # negative_adm_guidance_scaler
                0.3,  # adm_guidance_end_at_step
                7,  # cfg_mimicking_from_tsnr
                2,  # clip_skip
                "dpmpp_2m_sde_gpu",  # sampler
                "karras",  # scheduler
                "Default (model)",  # vae
                -1, -1, -1, -1, -1, -1,  # forced overwrites
                False, False, False, False,  # debug/mix toggles
                64, 128,  # canny thresholds
                "joint",  # refiner_swap_method
                0.25,  # softness_of_controlnet
                False, 1.01, 1.02, 0.99, 0.95,  # FreeU: enabled,b1,b2,s1,s2
                False,  # debug_inpaint_preprocessing
                False,  # disable_initial_latent_in_inpaint
                "v2.6",  # inpaint_engine
                1.0,  # inpaint_denoising_strength
                0.618,  # inpaint_respective_field
                False,  # enable_advanced_masking_features
                False,  # invert_mask_when_generating
                0,  # mask_erode_or_dilate
                False,  # save_only_final_enhanced_image
                True,  # save_metadata_to_images
                "fooocus",  # metadata_scheme
            ])

            # Image prompt 1..4 blocks (image, stop_at, weight, type)
            for _ in range(4):
                args.extend(["", 0, 0, "ImagePrompt"])  # empty image prompts

            # More debug/enhance glue
            args.extend([
                False,  # debug_groundingdino
                0,      # groundingdino_box_erode_or_dilate
                False,  # debug_enhance_masks
                "",     # use_with_enhance_skips_image_generation (image)
                False,  # enhance
                "Disabled",  # upscale_or_variation
                "Before First Enhancement",  # order_of_processing
                "Original Prompts",  # prompt (radio)
            ])

            # Three enhance blocks
            def add_enhance_block() -> None:
                args.extend([
                    False,  # enable
                    "",  # detection_prompt
                    "",  # enhancement_positive_prompt
                    "",  # enhancement_negative_prompt
                    "sam",  # mask_generation_model
                    "full",  # cloth_category
                    "vit_b",  # sam_model
                    0.25,  # text_threshold
                    0.3,   # box_threshold
                    0,     # maximum_number_of_detections
                    True,  # disable_initial_latent_in_inpaint
                    "v2.6",  # inpaint_engine
                    1.0,   # inpaint_denoising_strength
                    0.618, # inpaint_respective_field
                    0,     # mask_erode_or_dilate
                    False, # invert_mask
                ])

            add_enhance_block()
            add_enhance_block()
            add_enhance_block()

            self.client.predict(*args, fn_index=67)
            try:
                return self.client.predict(fn_index=68)
            except Exception as trigger_exc:  # noqa: BLE001
                # Some Fooocus builds return non-standard objects that gradio_client
                # fails to deserialize even though images were created. Treat as soft success.
                self.logger.warning(
                    "Trigger returned a deserialization error; images may still be saved. error=%s",
                    trigger_exc,
                )
                return {
                    "status": "triggered",
                    "note": "Images likely created by Fooocus. See output folder.",
                    "error": str(trigger_exc),
                }
        except Exception as exc:  # noqa: BLE001
            self.logger.exception("Configure+Generate failed: %s", exc)
            raise


