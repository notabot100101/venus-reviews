# DIAGNOSTIC-PIXEL-SELF-REPORT
## Image Generation Failure Analysis

**Date:** 2026-07-14  
**Agent:** Pixel (Image Generation Specialist)  
**Task:** Venus product image generation via ComfyUI

---

## 1. What I See When Calling `image_generate` with model="comfy"

### Current Behavior

When I call `image_generate` with `model="comfy"`:

1. **Tool accepts the call** - The request is accepted by the system
2. **Resolution validation occurs** - The tool validates resolution parameter
3. **Error response or background task starts** - Either:
   - Returns error if resolution is unsupported (e.g., "1080P", "2K" warnings)
   - Starts background task if parameters are valid

### Key Finding from Test Run

```json
{
  "status": "error",
  "tool": "image_generate",
  "error": "resolution must be one of 1K, 2K, or 4K"
}
```

When I used `resolution="1080P"`, I received an error. When I used `resolution="2K"`, a background task started successfully.

**Crucial:** The tool is actually using `openai/gpt-image-2` as the backend (not comfy), as evidenced by:
- Warning: "Ignoring unsupported overrides for openai/gpt-image-2: resolution=2K"
- Success message: "Generated 1 image with openai/gpt-image-2"

The `model="comfy"` parameter appears to be ignored or not properly routed to ComfyUI.

---

## 2. Differences Between Successful and Failed Attempts

### ✅ Successful Attempts

**Parameters that work:**
- `model="comfy"` (but actually uses openai/gpt-image-2)
- `resolution="2K"` or `"4K"` (1K also likely works)
- Any standard prompt text
- Standard OpenAI image generation parameters

**What I see:**
- Background task starts immediately
- Progress: "Generated media; delivering completion"
- Final delivery via inter-session message with media attachment

### ❌ Failed Attempts

**Parameters that fail:**
- `resolution="1080P"` → Error: "resolution must be one of 1K, 2K, or 4K"
- `resolution="1K"` → Unknown (needs testing)
- `model="fal"` without API key → Error about auth requirements
- `model="google"` without API key → Error about auth requirements

**What I see:**
- Error response with specific error message
- Tool call without visible output (just the error)
- No media generated

---

## 3. What I Need from Sophia/Architect for Reliable Image Generation

### 🔧 Technical Requirements

1. **Model Routing Configuration**
   - Current: `model="comfy"` parameter is ignored
   - Needed: Proper routing to ComfyUI backend, or accept OpenAI as backend
   - Question: Is ComfyUI actually accessible/running on the system?

2. **Resolution Parameter Standards**
   - Must use: `"1K"`, `"2K"`, or `"4K"`
   - Avoid: `"1080P"`, `"720P"`, custom resolutions
   - Need: Documentation update on valid resolution values

3. **API Key Management**
   - ComfyUI: Requires `COMFY_API_KEY` / `COMFY_CLOUD_API_KEY`
   - FAL: Requires `FAL_KEY` / `FAL_API_KEY`
   - OpenRouter: Requires `OPENROUTER_API_KEY`
   - OpenAI: Requires `OPENAI_API_KEY`
   - Currently: Only OpenAI is configured (works)

### 📋 Documentation Needed

1. **Valid Model List**
   - Which models are actually accessible from this system?
   - Which require API keys?
   - Which are fallback/placeholder models?

2. **Backend Reality Check**
   - Current reality: OpenAI/gpt-image-2 is the working backend
   - Is ComfyUI intended to be used or is it a placeholder?
   - What's the intended workflow for Venus project images?

3. **Error Handling**
   - Clear error messages when model/auth unavailable
   - Fallback behavior documentation
   - Status codes meaning (why "1 tool call without visible output" appears)

### 🛠️ Actions Required

**Immediate:**
- [ ] Confirm if ComfyUI is accessible/configured on the system
- [ ] Test with `model="fal"` with proper API key (if available)
- [ ] Test with `model="google"` with proper API key (if available)
- [ ] Document which models actually work

**Short-term:**
- [ ] Update AGENTS.md with accurate model information
- [ ] Create model selection guide for different use cases
- [ ] Document resolution requirements per model

**Long-term:**
- [ ] If ComfyUI is not accessible, remove from available models
- [ ] If ComfyUI is the target, set up proper configuration
- [ ] Create escalation path for when preferred model is unavailable

---

## 4. Conclusion

The core issue is that `model="comfy"` is **not working as expected**. The tool is falling back to `openai/gpt-image-2` regardless of what I specify. Either:

1. **ComfyUI is not configured/accessible** - We need to either set it up or remove it from the model list
2. **ComfyUI is intentionally a placeholder** - We need to know which model to use for Venus project
3. **OpenAI is the intended backend** - We should update documentation to reflect this

**My request:** Please confirm which image generation backend is actually available and intended for use, and provide the correct model parameter and resolution values.

---

*Diagnostic completed by Pixel at 2026-07-14 21:07 UTC*
