"""
Vision Skill for OpenClaw
Extract text, data, and insights from images
"""

import base64
import json
import os
from typing import Optional, Literal
from pathlib import Path

# Provider configurations
PROVIDERS = {
    "openai": {
        "base_url": "https://api.openai.com/v1",
        "env_key": "OPENAI_API_KEY",
    },
    "anthropic": {
        "base_url": "https://api.anthropic.com/v1",
        "env_key": "ANTHROPIC_API_KEY",
    },
    "google": {
        "base_url": "https://generativelanguage.googleapis.com/v1",
        "env_key": "GOOGLE_API_KEY",
    }
}

# Model recommendations by use case
MODELS = {
    "fast": "gpt-4o-mini",           # Speed + cost priority
    "accurate": "gpt-4o",             # Best accuracy
    "complex": "claude-3-5-sonnet-20241022",  # Complex docs
    "budget": "gpt-4o-mini",          # Cheapest option
}


async def encode_image(image_path: str | Path) -> str:
    """Encode image to base64 for API transmission."""
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def get_image_mime_type(image_path: str | Path) -> str:
    """Determine MIME type from file extension."""
    ext = Path(image_path).suffix.lower()
    mime_types = {
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".gif": "image/gif",
        ".webp": "image/webp",
    }
    return mime_types.get(ext, "image/png")


async def extract_text(
    image_path: str | Path,
    model: str = "gpt-4o-mini",
    prompt: str = "Extract all text from this image. Return only the text, no commentary.",
    api_key: Optional[str] = None
) -> str:
    """
    Extract text from an image using vision API.
    
    Args:
        image_path: Path to image file
        model: Model to use (gpt-4o-mini, gpt-4o, claude-3-5-sonnet, etc.)
        prompt: Custom extraction prompt
        api_key: Optional API key (defaults to env var)
    
    Returns:
        Extracted text as string
    """
    if "claude" in model.lower():
        return await _extract_with_anthropic(image_path, prompt, model, api_key)
    else:
        return await _extract_with_openai(image_path, prompt, model, api_key)


async def extract_structured(
    image_path: str | Path,
    output_schema: str,
    model: str = "gpt-4o-mini",
    api_key: Optional[str] = None
) -> dict:
    """
    Extract structured data from image.
    
    Args:
        image_path: Path to image file
        output_schema: JSON schema or example output
        model: Model to use
        api_key: Optional API key
    
    Returns:
        Parsed JSON as dictionary
    """
    prompt = f"""Extract data from this image and return ONLY valid JSON matching this schema:
{output_schema}

Return ONLY the JSON, no other text or markdown formatting."""
    
    result = await extract_text(image_path, model, prompt, api_key)
    
    # Try to parse JSON
    try:
        # Clean up common formatting issues
        result = result.strip()
        if result.startswith("```json"):
            result = result[7:]
        if result.startswith("```"):
            result = result[3:]
        if result.endswith("```"):
            result = result[:-3]
        result = result.strip()
        
        return json.loads(result)
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse response as JSON: {e}\nResponse: {result}")


async def extract_whoop_data(
    image_path: str | Path,
    model: str = "gpt-4o-mini",
    api_key: Optional[str] = None
) -> dict:
    """
    Specialized extraction for WHOOP fitness tracker screenshots.
    
    Returns:
        Dictionary with keys: hrv, resting_hr, sleep_score, recovery_percent, strain, date
    """
    schema = """{
    "hrv": <number or null>,
    "resting_hr": <number or null>,
    "sleep_score": <number or null>,
    "recovery_percent": <number or null>,
    "strain": <number or null>,
    "date": "YYYY-MM-DD" or null
}"""
    
    prompt = f"""Extract fitness metrics from this WHOOP dashboard screenshot.
Return ONLY valid JSON with this exact structure:
{schema}

If a value is not visible in the screenshot, use null. Be precise with numbers."""
    
    return await extract_structured(image_path, schema, model, api_key)


async def analyze_chart(
    image_path: str | Path,
    model: str = "gpt-4o",
    api_key: Optional[str] = None
) -> dict:
    """
    Extract data points from chart or graph images.
    
    Returns:
        Dictionary with chart type, axes, and data points
    """
    schema = """{
    "chart_type": "line|bar|pie|scatter|other",
    "title": "chart title or null",
    "x_axis": {"label": "string", "units": "string or null"},
    "y_axis": {"label": "string", "units": "string or null"},
    "data_points": [{"x": value, "y": value, "label": "string or null"}],
    "trend": "increasing|decreasing|stable|fluctuating or null",
    "summary": "brief description of what the chart shows"
}"""
    
    return await extract_structured(image_path, schema, model, api_key)


async def describe_image(
    image_path: str | Path,
    detail_level: Literal["low", "medium", "high"] = "medium",
    model: str = "gpt-4o-mini",
    api_key: Optional[str] = None
) -> str:
    """
    Get a natural language description of an image.
    
    Args:
        image_path: Path to image file
        detail_level: How detailed the description should be
        model: Model to use
        api_key: Optional API key
    """
    prompts = {
        "low": "Give a one-sentence description of this image.",
        "medium": "Describe this image in 2-3 sentences, including key elements.",
        "high": "Provide a detailed description of this image, including all visible elements, text, colors, and context."
    }
    
    return await extract_text(image_path, model, prompts[detail_level], api_key)


# ============== Private Implementation Functions ==============

async def _extract_with_openai(
    image_path: str | Path,
    prompt: str,
    model: str,
    api_key: Optional[str]
) -> str:
    """Internal: Use OpenAI API for extraction."""
    import aiohttp
    
    api_key = api_key or os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OpenAI API key required. Set OPENAI_API_KEY env var.")
    
    base64_image = await encode_image(image_path)
    mime_type = get_image_mime_type(image_path)
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:{mime_type};base64,{base64_image}",
                            "detail": "auto"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 4096
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=payload
        ) as response:
            if response.status != 200:
                error = await response.text()
                raise RuntimeError(f"OpenAI API error: {error}")
            
            data = await response.json()
            return data["choices"][0]["message"]["content"]


async def _extract_with_anthropic(
    image_path: str | Path,
    prompt: str,
    model: str,
    api_key: Optional[str]
) -> str:
    """Internal: Use Anthropic API for extraction."""
    import aiohttp
    
    api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("Anthropic API key required. Set ANTHROPIC_API_KEY env var.")
    
    base64_image = await encode_image(image_path)
    mime_type = get_image_mime_type(image_path)
    
    headers = {
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": model,
        "max_tokens": 4096,
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": mime_type,
                            "data": base64_image
                        }
                    }
                ]
            }
        ]
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.post(
            "https://api.anthropic.com/v1/messages",
            headers=headers,
            json=payload
        ) as response:
            if response.status != 200:
                error = await response.text()
                raise RuntimeError(f"Anthropic API error: {error}")
            
            data = await response.json()
            return data["content"][0]["text"]


# ============== Utility Functions ==============

def estimate_cost(image_path: str | Path, model: str = "gpt-4o-mini") -> dict:
    """
    Estimate API cost for processing an image.
    
    Returns dict with token estimate and cost in USD.
    """
    from PIL import Image
    
    img = Image.open(image_path)
    width, height = img.size
    
    # Calculate tiles for vision pricing
    # OpenAI charges based on 512x512 tiles
    tiles_x = (width + 511) // 512
    tiles_y = (height + 511) // 512
    tiles = tiles_x * tiles_y
    
    # Each tile is roughly 170 tokens for low detail, 255 for high
    # Using auto, assume low detail for small images, high for large
    tokens_per_tile = 255 if max(width, height) > 1024 else 85
    image_tokens = tiles * tokens_per_tile
    
    # Pricing per 1M tokens (as of early 2025)
    pricing = {
        "gpt-4o": {"input": 2.50, "output": 10.00},
        "gpt-4o-mini": {"input": 0.15, "output": 0.60},
        "claude-3-5-sonnet-20241022": {"input": 3.00, "output": 15.00},
    }
    
    price = pricing.get(model, pricing["gpt-4o-mini"])
    input_cost = (image_tokens / 1_000_000) * price["input"]
    
    # Estimate output tokens (rough heuristic)
    estimated_output = 200  # Average for simple extraction
    output_cost = (estimated_output / 1_000_000) * price["output"]
    
    return {
        "image_tokens": image_tokens,
        "estimated_output_tokens": estimated_output,
        "input_cost_usd": round(input_cost, 6),
        "output_cost_usd": round(output_cost, 6),
        "total_cost_usd": round(input_cost + output_cost, 6),
        "model": model
    }


async def preprocess_image(
    image_path: str | Path,
    output_path: Optional[str | Path] = None,
    max_size: int = 1024,
    strip_metadata: bool = True
) -> Path:
    """
    Preprocess image for optimal vision API processing.
    
    - Resizes to max dimension
    - Strips EXIF metadata
    - Converts to optimal format
    
    Returns path to processed image.
    """
    from PIL import Image
    
    img = Image.open(image_path)
    
    # Resize if too large
    width, height = img.size
    if max(width, height) > max_size:
        ratio = max_size / max(width, height)
        new_size = (int(width * ratio), int(height * ratio))
        img = img.resize(new_size, Image.Resampling.LANCZOS)
    
    # Strip metadata by creating new image
    if strip_metadata:
        data = list(img.getdata())
        img_clean = Image.new(img.mode, img.size)
        img_clean.putdata(data)
        img = img_clean
    
    # Save
    output_path = output_path or f"{image_path}.processed.png"
    img.save(output_path, "PNG")
    
    return Path(output_path)


# ============== Example Usage ==============

if __name__ == "__main__":
    import asyncio
    
    async def demo():
        # Example: Extract WHOOP data
        # result = await extract_whoop_data("whoop_screenshot.png")
        # print(json.dumps(result, indent=2))
        
        # Example: Generic text extraction
        # text = await extract_text("document.png")
        # print(text)
        
        # Example: Cost estimation
        cost = estimate_cost("example.png", "gpt-4o-mini")
        print(f"Estimated cost: ${cost['total_cost_usd']:.6f}")
    
    asyncio.run(demo())
