# Automating Fooocus Image Generation with Python

## System

You are an AI assistant designed to assist users by providing accurate information, answering questions, and offering helpful suggestions. Your main objectives are to understand the user's needs, communicate clearly, and provide responses that are informative, concise, and relevant.
- do not repeat the question. just start with the answer.
- do not generate images unless i specifically ask for them.
- provide used urls in a FOOTOTE section Current date and time is 8/13/2025, 8:35:56 PM

## You

the fooocus application uses GRADIO to build it's interface and Gradio provides an API out of the box. Attached is the documentation for that interface but it is completely indecipherable to me. I want to build a script that can control the Fooocus app and automate image creation with it. I want to use python for this.

## Assistant

I'll help you understand the Fooocus Gradio API and create a Python script to automate image creation. Let me first search for more information about the specific endpoints we need to use.Based on the documentation and tutorial I found, here's how to build a Python script to control Fooocus and automate image creation:

## Understanding the Fooocus Gradio API

The Fooocus application exposes a Gradio API with multiple endpoints. The key insight is that you need to use **two API calls**:

1. **First call (fn_index=67)**: Configure all the generation parameters
2. **Second call (fn_index=68)**: Trigger the actual image generation

## Basic Python Script

Here's a simplified Python script to automate Fooocus image generation:

```python
from gradio_client import Client
import time

def generate_image(prompt, negative_prompt="", num_images=1, seed="0"):
    """
    Generate images using Fooocus API
    
    Args:
        prompt (str): The main prompt for image generation
        negative_prompt (str): What to avoid in the image
        num_images (int): Number of images to generate (1-32)
        seed (str): Seed for reproducibility
    
    Returns:
        Result from the generation process
    """
    
    # Connect to Fooocus (make sure it's running on localhost:7865)
    client = Client("http://127.0.0.1:7865/")
    
    # Step 1: Configure generation parameters
    config_result = client.predict(
        False,  # Generate Image Grid for Each Batch
        prompt,  # Main prompt
        negative_prompt,  # Negative prompt
        ["Fooocus V2"],  # Selected styles
        "Quality",  # Performance mode (Speed/Quality/Extreme Speed)
        "1024×1024",  # Aspect ratio
        num_images,  # Number of images
        "png",  # Output format
        seed,  # Seed
        False,  # Read wildcards in order
        2,  # Image sharpness (0-30)
        7,  # Guidance scale (1-30)
        "juggernautXL_v8Rundiffusion.safetensors",  # Base model
        "None",  # Refiner model
        0.5,  # Refiner switch point
        
        # LoRA settings (5 LoRAs, all disabled)
        True, "None", -2,  # LoRA 1
        True, "None", -2,  # LoRA 2  
        True, "None", -2,  # LoRA 3
        True, "None", -2,  # LoRA 4
        True, "None", -2,  # LoRA 5
        
        # Input image settings (disabled for text-to-image)
        False,  # Input image checkbox
        "",     # Parameter textbox
        "Disabled",  # Upscale/variation mode
        "",     # Input image
        ["Left"],  # Outpaint direction
        "",     # Inpaint image
        "",     # Inpaint prompt
        "",     # Mask upload
        
        # Debug/advanced settings
        True,   # Disable preview
        True,   # Disable intermediate results
        True,   # Disable seed increment
        False,  # Black out NSFW
        1.5,    # Positive ADM guidance
        0.8,    # Negative ADM guidance
        0.3,    # ADM guidance end step
        7,      # CFG mimicking
        2,      # CLIP skip
        "dpmpp_2m_sde_gpu",  # Sampler
        "karras",            # Scheduler
        "Default (model)",   # VAE
        
        # Forced overwrites (all -1 = disabled)
        -1, -1, -1, -1, -1, -1,
        
        # More debug settings
        False, False, False, False,  # Various debug options
        64, 128,  # Canny thresholds
        "joint", 0.25,  # Refiner and ControlNet settings
        False, 1.01, 1.02, 0.99, 0.95,  # FreeU settings
        False, False, "v2.6", 1, 0.618,  # Inpaint settings
        False, False, 0, False, False, "fooocus",  # Misc settings
        
        # Image prompts (4 slots, all empty)
        "", 0, 0, "ImagePrompt",  # Image prompt 1
        "", 0, 0, "ImagePrompt",  # Image prompt 2
        "", 0, 0, "ImagePrompt",  # Image prompt 3
        "", 0, 0, "ImagePrompt",  # Image prompt 4
        
        # More debug and enhance settings
        False, 0, False, "",  # Debug settings
        False, "Disabled", "Before First Enhancement", "Original Prompts",  # Enhance settings
        
        # Three enhance blocks (all disabled)
        False, "", "", "", "sam", "full", "vit_b", 0.25, 0.3, 0, True, "v2.6", 1, 0.618, 0, False,  # Enhance 1
        False, "", "", "", "sam", "full", "vit_b", 0.25, 0.3, 0, True, "v2.6", 1, 0.618, 0, False,  # Enhance 2
        False, "", "", "", "sam", "full", "vit_b", 0.25, 0.3, 0, True, "v2.6", 1, 0.618, 0, False,  # Enhance 3
        
        fn_index=67
    )
    
    print("Configuration set successfully")
    
    # Step 2: Trigger image generation
    generation_result = client.predict(fn_index=68)
    
    return generation_result

# Example usage
if __name__ == "__main__":
    # Single image generation
    result = generate_image(
        prompt="a beautiful landscape with mountains and a lake, sunset lighting",
        negative_prompt="blurry, low quality",
        num_images=1,
        seed="42"
    )
    
    print("Generation completed!")
    print("Result:", result)
    
    # Batch generation example
    prompts = [
        "a cat sitting on a windowsill",
        "a futuristic city at night",
        "a magical forest with glowing mushrooms"
    ]
    
    for i, prompt in enumerate(prompts):
        print(f"Generating image {i+1}/{len(prompts)}: {prompt}")
        result = generate_image(prompt, seed=str(i))
        time.sleep(2)  # Small delay between generations
```

## Simplified Version for Basic Use

If you want a simpler version with fewer parameters:

```python
from gradio_client import Client

def simple_generate(prompt, num_images=1):
    client = Client("http://127.0.0.1:7865/")
    
    # Use the text input endpoint (fn_index=61) to set prompt
    client.predict(prompt, fn_index=61)
    
    # Trigger generation
    result = client.predict(fn_index=68)
    return result

# Usage
result = simple_generate("a beautiful sunset over the ocean")
```

## Important Notes

1. **Fooocus must be running**: Start Fooocus normally before running your script
2. **Check the port**: Default is 7865, but verify in your Fooocus startup
3. **API changes**: The fn_index numbers and parameters may change between Fooocus versions
4. **Output location**: Generated images will appear in Fooocus's normal output directory
5. **Install gradio_client**: `pip install gradio_client`

## Batch Processing Example

```python
import os
import time
from gradio_client import Client

def batch_generate_images(prompt_list, output_folder="generated_images"):
    """Generate multiple images from a list of prompts"""
    
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    client = Client("http://127.0.0.1:7865/")
    
    for i, prompt in enumerate(prompt_list):
        print(f"Generating {i+1}/{len(prompt_list)}: {prompt}")
        
        # Set prompt and generate
        client.predict(prompt, fn_index=61)
        result = client.predict(fn_index=68)
        
        # Wait a bit between generations
        time.sleep(3)
        
        print(f"Completed: {prompt}")

# Example usage
prompts = [
    "a steampunk robot in a Victorian setting",
    "a dragon flying over a medieval castle",
    "a cyberpunk street scene with neon lights"
]

batch_generate_images(prompts)
```

This script provides a foundation for automating Fooocus image generation. You can modify the parameters in the main `client.predict()` call to customize generation settings like styles, models, aspect ratios, and more.

**FOOTNOTES**

[1] https://tricks.one/post/get-fooocus-gradio-api-working-en/

## You

can you please break out what the "Various debug options" and "Misc settings" are?

## Assistant

Based on the API documentation and the additional research, I can now break down the "Various debug options" and "Misc settings" from the Fooocus Gradio API. Here's a detailed breakdown of what each parameter controls:

## Various Debug Options Breakdown

Here are the specific debug options in order as they appear in fn_index=67:

```python
# Various debug options (4 boolean parameters)
False,  # Mixing Image Prompt and Vary/Upscale
False,  # Mixing Image Prompt and Inpaint  
False,  # Debug Preprocessors
False,  # Skip Preprocessors
```

**1. Mixing Image Prompt and Vary/Upscale** (bool)
- Controls whether image prompts are combined with variation/upscaling operations
- When enabled, allows simultaneous use of input images and variation modes
- Useful for maintaining style consistency during upscaling

**2. Mixing Image Prompt and Inpaint** (bool)  
- Controls whether image prompts are combined with inpainting operations
- When enabled, allows using reference images while inpainting
- Perfect for face swaps or background style changes while preserving subjects

**3. Debug Preprocessors** (bool)
- Shows debug information about image preprocessing steps
- Useful for troubleshooting preprocessing issues
- Displays intermediate processing results

**4. Skip Preprocessors** (bool)
- Bypasses certain image preprocessing steps
- Can speed up generation but may affect quality
- Use when you want raw input without preprocessing

## Misc Settings Breakdown

Here are the miscellaneous settings parameters:

```python
# Canny edge detection thresholds
64,     # Canny Low Threshold (1-255)
128,    # Canny High Threshold (1-255)

# Advanced processing options  
"joint",  # Refiner swap method ("joint", "separate", "vae")
0.25,     # Softness of ControlNet (0.0-1.0)

# FreeU settings (for improved generation quality)
False,    # FreeU Enabled
1.01,     # FreeU B1 (0-2) - controls low-frequency features
1.02,     # FreeU B2 (0-2) - controls high-frequency features  
0.99,     # FreeU S1 (0-4) - scaling factor 1
0.95,     # FreeU S2 (0-4) - scaling factor 2

# Inpaint-specific debug and processing
False,    # Debug Inpaint Preprocessing
False,    # Disable initial latent in inpaint
"v2.6",   # Inpaint Engine ("None", "v1", "v2.5", "v2.6")
1.0,      # Inpaint Denoising Strength (0.0-1.0)
0.618,    # Inpaint Respective Field (0.0-1.0)

# Mask processing
False,    # Enable Advanced Masking Features
False,    # Invert Mask When Generating
0,        # Mask Erode or Dilate (-64 to 64)

# Output and metadata options
False,    # Save only final enhanced image
False,    # Save Metadata to Images  
"fooocus" # Metadata Scheme ("fooocus", "a1111")
```

## Complete Parameter Explanation

Here's what each misc setting does:

### Canny Edge Detection
- **Canny Low/High Threshold**: Controls edge detection sensitivity for ControlNet
- Lower values = more edges detected, higher values = fewer edges

### Refiner Settings
- **Refiner swap method**: How the refiner model is applied
  - "joint": Both models work together
  - "separate": Models work independently  
  - "vae": Uses VAE for switching

### ControlNet
- **Softness**: How strongly ControlNet influences generation (0=weak, 1=strong)

### FreeU (Quality Enhancement)
- **B1/B2**: Control low/high frequency feature enhancement
- **S1/S2**: Scaling factors for feature enhancement
- Generally improves generation quality when enabled

### Inpainting
- **Debug Inpaint Preprocessing**: Shows mask processing steps
- **Disable initial latent**: Affects how inpainting starts
- **Inpaint Engine**: Different inpainting algorithms (v2.6 is newest)
- **Denoising Strength**: How much the masked area changes (0=no change, 1=complete change)
- **Respective Field**: Controls influence area around mask

### Masking
- **Advanced Masking**: Enables additional mask processing features
- **Invert Mask**: Reverses which areas are modified
- **Erode/Dilate**: Shrinks (-) or expands (+) mask boundaries

### Output
- **Save only final**: Only saves end result, not intermediate steps
- **Save Metadata**: Embeds generation parameters in image files
- **Metadata Scheme**: Format for embedded metadata

## Updated Script with Clear Parameter Names

```python
from gradio_client import Client

def generate_image_detailed(prompt, **kwargs):
    client = Client("http://127.0.0.1:7865/")
    
    # Extract parameters with defaults
    negative_prompt = kwargs.get('negative_prompt', "")
    num_images = kwargs.get('num_images', 1)
    seed = kwargs.get('seed', "0")
    
    # Debug options
    mix_prompt_vary = kwargs.get('mix_prompt_vary', False)
    mix_prompt_inpaint = kwargs.get('mix_prompt_inpaint', False) 
    debug_preprocessors = kwargs.get('debug_preprocessors', False)
    skip_preprocessors = kwargs.get('skip_preprocessors', False)
    
    # FreeU settings
    freeu_enabled = kwargs.get('freeu_enabled', False)
    freeu_b1 = kwargs.get('freeu_b1', 1.01)
    freeu_b2 = kwargs.get('freeu_b2', 1.02)
    freeu_s1 = kwargs.get('freeu_s1', 0.99)
    freeu_s2 = kwargs.get('freeu_s2', 0.95)
    
    # Mask settings
    mask_erode_dilate = kwargs.get('mask_erode_dilate', 0)
    invert_mask = kwargs.get('invert_mask', False)
    
    result = client.predict(
        False,  # Generate Image Grid for Each Batch
        prompt,  # Main prompt
        negative_prompt,  # Negative prompt
        ["Fooocus V2"],  # Selected styles
        "Quality",  # Performance
        "1024×1024",  # Aspect ratio
        num_images,  # Number of images
        "png",  # Output format
        seed,  # Seed
        False,  # Read wildcards in order
        2,  # Image sharpness
        7,  # Guidance scale
        "juggernautXL_v8Rundiffusion.safetensors",  # Base model
        "None",  # Refiner
        0.5,  # Refiner switch point
        
        # LoRA settings (all disabled)
        True, "None", -2,  # LoRA 1
        True, "None", -2,  # LoRA 2
        True, "None", -2,  # LoRA 3  
        True, "None", -2,  # LoRA 4
        True, "None", -2,  # LoRA 5
        
        # Input image (disabled)
        False, "", "Disabled", "", ["Left"], "", "", "",
        
        # Basic debug settings
        True,   # Disable preview
        True,   # Disable intermediate results  
        True,   # Disable seed increment
        False,  # Black out NSFW
        1.5,    # Positive ADM guidance
        0.8,    # Negative ADM guidance
        0.3,    # ADM guidance end step
        7,      # CFG mimicking
        2,      # CLIP skip
        "dpmpp_2m_sde_gpu",  # Sampler
        "karras",            # Scheduler
        "Default (model)",   # VAE
        
        # Forced overwrites (disabled)
        -1, -1, -1, -1, -1, -1,
        
        # Various debug options (now clearly labeled)
        mix_prompt_vary,      # Mixing Image Prompt and Vary/Upscale
        mix_prompt_inpaint,   # Mixing Image Prompt and Inpaint
        debug_preprocessors,  # Debug Preprocessors
        skip_preprocessors,   # Skip Preprocessors
        
        # Canny thresholds
        64, 128,  # Canny low/high thresholds
        
        # Misc settings
        "joint",  # Refiner swap method
        0.25,     # ControlNet softness
        
        # FreeU settings
        freeu_enabled, freeu_b1, freeu_b2, freeu_s1, freeu_s2,
        
        # Inpaint settings
        False,    # Debug inpaint preprocessing
        False,    # Disable initial latent in inpaint
        "v2.6",   # Inpaint engine
        1.0,      # Inpaint denoising strength
        0.618,    # Inpaint respective field
        
        # Mask settings
        False,    # Enable advanced masking
        invert_mask,  # Invert mask
        mask_erode_dilate,  # Mask erode/dilate
        
        # Output settings
        False,    # Save only final enhanced image
        True,    # Save metadata to images
        "fooocus",  # Metadata scheme
        
        # Image prompts (4 slots, all empty)
        "", 0, 0, "ImagePrompt",  # Image prompt 1
        "", 0, 0, "ImagePrompt",  # Image prompt 2
        "", 0, 0, "ImagePrompt",  # Image prompt 3
        "", 0, 0, "ImagePrompt",  # Image prompt 4
        
        # Debug and enhance settings
        False, 0, False, "",  # More debug options
        False, "Disabled", "Before First Enhancement", "Original Prompts",
        
        # Three enhance blocks (all disabled)
        False, "", "", "", "sam", "full", "vit_b", 0.25, 0.3, 0, True, "v2.6", 1, 0.618, 0, False,
        False, "", "", "", "sam", "full", "vit_b", 0.25, 0.3, 0, True, "v2.6", 1, 0.618, 0, False,
        False, "", "", "", "sam", "full", "vit_b", 0.25, 0.3, 0, True, "v2.6", 1, 0.618, 0, False,
        
        fn_index=67
    )
    
    # Trigger generation
    generation_result = client.predict(fn_index=68)
    return generation_result

# Example usage with specific debug options
result = generate_image_detailed(
    "a beautiful landscape",
    freeu_enabled=True,  # Enable FreeU for better quality
    debug_preprocessors=True,  # Show preprocessing debug info
    mask_erode_dilate=2,  # Expand masks slightly
    mix_prompt_inpaint=True  # Allow mixing prompts with inpainting
)
```

This breakdown should help you understand exactly what each parameter controls and how to use them effectively in your automation scripts.

