import streamlit as st
from huggingface_hub import InferenceClient
from dotenv import load_dotenv
import os
from PIL import Image

# Load environment variables
load_dotenv()

# Configuration
MODEL_NAME = "black-forest-labs/FLUX.1-schnell"
HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_TOKEN")

# Page configuration
st.set_page_config(
    page_title="AI Image Generator",
    page_icon="🎨",
    layout="centered"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #FF6B6B;
        color: white;
        font-weight: bold;
        padding: 0.5rem 1rem;
        border-radius: 0.5rem;
        border: none;
        font-size: 1.1rem;
    }
    .stButton>button:hover {
        background-color: #FF5252;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.title("🎨 AI Image Generator")
st.markdown("### Transform your ideas into stunning images using AI!")
st.markdown("*Powered by FLUX.1-schnell - Fast, High-Quality Image Generation*")

# Check if API token is configured
if not HUGGINGFACE_TOKEN or HUGGINGFACE_TOKEN == "your_token_here":
    st.error("⚠️ HuggingFace API token not configured!")
    st.info("""
    **Setup Instructions:**
    1. Go to https://huggingface.co/settings/tokens
    2. Create a new token with "Write" permissions
    3. Create a `.env` file in the project directory
    4. Add: `HUGGINGFACE_TOKEN=your_token_here`
    5. Restart the application

    **Note:** Read-only tokens will NOT work for the Inference API.
    """)
    st.stop()

# Initialize the InferenceClient
@st.cache_resource
def get_inference_client():
    return InferenceClient(token=HUGGINGFACE_TOKEN)

try:
    client = get_inference_client()
except Exception as e:
    st.error(f"Failed to initialize HuggingFace client: {str(e)}")
    st.stop()

# Main interface
st.markdown("---")

# Advanced settings in expander
with st.expander("⚙️ Advanced Settings (Optional)", expanded=False):
    col1, col2 = st.columns(2)

    with col1:
        image_width = st.slider(
            "Image Width",
            min_value=256,
            max_value=1024,
            value=768,
            step=128,
            help="Width of the generated image in pixels"
        )

    with col2:
        image_height = st.slider(
            "Image Height",
            min_value=256,
            max_value=1024,
            value=768,
            step=128,
            help="Height of the generated image in pixels"
        )

    guidance_scale = st.slider(
        "Guidance Scale (Precision)",
        min_value=1.0,
        max_value=20.0,
        value=7.5,
        step=0.5,
        help="Higher values make the AI follow your prompt more precisely. 7-10 is recommended."
    )

    num_steps = st.slider(
        "Inference Steps (Quality)",
        min_value=1,
        max_value=16,
        value=4,
        step=1,
        help="More steps = higher quality but slower. FLUX.1-schnell has a maximum of 16 steps."
    )

# Prompt enhancement section
st.subheader("✍️ Describe Your Image")

# Image size selection
image_size_option = st.selectbox(
    "📐 Choose Image Size:",
    [
        "Square (512x512)",
        "Portrait (512x768)",
        "Landscape (768x512)"
    ],
    index=0,
    help="Select the dimensions for your generated image"
)

# Map size options to dimensions
size_mapping = {
    "Square (512x512)": (512, 512),
    "Portrait (512x768)": (512, 768),
    "Landscape (768x512)": (768, 512)
}

selected_width, selected_height = size_mapping[image_size_option]

# Realism boost toggle
realism_mode = st.checkbox(
    "🎯 Ultra Realism Mode",
    value=False,
    help="Automatically optimizes settings for maximum photorealism"
)

# Style preset
if not realism_mode:
    style_preset = st.selectbox(
        "Choose a style preset (optional):",
        [
            "None - Use my prompt as-is",
            "Photorealistic",
            "Digital Art",
            "Oil Painting",
            "Watercolor",
            "3D Render",
            "Anime/Manga",
            "Sketch/Drawing",
            "Cinematic",
            "Fantasy Art"
        ]
    )
else:
    st.info("🎯 Ultra Realism Mode Active - Maximum quality settings enabled (16 inference steps, will take longer)")
    style_preset = "Photorealistic"

# Prompt input
prompt = st.text_area(
    "Enter your image description:",
    placeholder="e.g., A serene landscape with mountains at sunset",
    height=100,
    help="Be specific! Include details about subject, composition, lighting, colors, and mood."
)

# Negative prompt input
with st.expander("🚫 Negative Prompt (Optional) - Advanced Control", expanded=False):
    st.markdown("""
    Specify what you **DON'T** want in the image. This helps the AI avoid unwanted elements.

    **Common examples:**
    - **Artificial/Fake:** `CGI, 3D render, cartoon, anime, drawing, painting, illustration, digital art`
    - **Quality issues:** `blurry, low quality, distorted, bad anatomy, deformed, unrealistic`
    - **Mood/style:** `dark, gloomy, scary, horror, violent`
    - **Elements:** `text, watermark, signature, logo, username`
    - **Artifacts:** `duplicate, cropped, out of frame, ugly, mutation`

    **💡 For photos that look REAL, always include:** `CGI, 3D render, cartoon, illustration, unrealistic, artificial`
    """)

    negative_prompt = st.text_area(
        "Negative Prompt:",
        placeholder="e.g., CGI, 3D render, cartoon, illustration, blurry, bokeh, shallow depth of field, defocus, background blur, soft focus, unrealistic, artificial, bad anatomy, deformed hands, extra fingers, plastic skin, smooth skin, airbrushed skin, perfect skin, poreless skin, waxy skin, doll skin, mannequin skin, fake skin texture",
        height=100,
        help="Avoid fake/artificial elements, ALL types of blur, and bad anatomy! For realistic human skin: add 'plastic skin, smooth skin, airbrushed skin, poreless skin, waxy skin' to get real skin with visible pores and texture.",
        key="negative_prompt"
    )

# Add style suffix based on preset
def enhance_prompt(base_prompt, style, ultra_realism=False):
    # Detect if prompt contains human body parts
    human_body_keywords = ['hand', 'hands', 'finger', 'fingers', 'face', 'eye', 'eyes', 'nose', 'mouth', 'ear', 'ears', 'arm', 'arms', 'leg', 'legs', 'foot', 'feet', 'skin', 'body', 'person', 'human', 'portrait', 'man', 'woman', 'child', 'people']
    contains_human = any(keyword in base_prompt.lower() for keyword in human_body_keywords)

    if ultra_realism:
        # Ultra realism mode - mimicking real camera photography with authentic characteristics
        human_anatomy_detail = ", anatomically correct, realistic human anatomy, real human skin texture, visible skin pores, skin imperfections, natural skin subsurface scattering, authentic dermal details, real skin microstructure, fine skin lines, natural skin blemishes, realistic skin tone variation, genuine skin appearance, skin texture like real photographs of humans, dermatological accuracy, macro photography skin detail, individual pore visibility, natural skin oils, authentic epidermal texture, real subcutaneous details, lifelike skin translucency, biological skin accuracy, medical photography skin precision, true to life human skin, photorealistic flesh tones, natural vein visibility under skin, authentic skin undertones, real human dermis characteristics" if contains_human else ""
        return f"{base_prompt}, RAW photo, genuine photograph, real camera capture, photorealistic, ultra realistic, hyper detailed, 8k uhd, shot on Canon EOS R5, professional DSLR photography, natural photograph, real world scene, authentic lighting, real textures, film grain, natural color grading, high dynamic range, proper exposure, masterpiece quality, crystal clear, sharp focus everywhere, deep focus f/22, everything in focus, full scene detail, volumetric atmospheric lighting, physically accurate, extreme detail throughout, intricate real-world details, accurate colors, natural skin tones, realistic materials, perfect clarity, comprehensive detail, no artificial blur, infinite depth of field, everything sharp, all elements detailed, true to life, optical perfection, real photograph quality, entire scene in sharp focus, background highly detailed, foreground and background equally sharp, no depth of field blur, no bokeh, no defocus, complete scene clarity, f/32 aperture, tack sharp throughout{human_anatomy_detail}"
    elif style == "None - Use my prompt as-is":
        return base_prompt
    elif style == "Photorealistic":
        human_anatomy_detail = ", anatomically correct, realistic human anatomy, real human skin texture, visible skin pores, skin imperfections, natural skin subsurface scattering, authentic dermal details, fine skin lines, realistic skin tone variation, genuine skin appearance like real photographs, individual pore visibility, natural skin oils, authentic epidermal texture, lifelike skin translucency, photorealistic flesh tones, natural vein visibility, authentic skin undertones" if contains_human else ""
        return f"{base_prompt}, RAW photo, real photograph, photorealistic, highly detailed, 8k, sharp focus throughout entire image, deep focus f/16, everything in focus, professional DSLR photography, natural lighting, real world scene, authentic colors, film grain, no background blur, genuine camera capture, background highly detailed, foreground and background equally sharp, no bokeh, no defocus, complete scene clarity{human_anatomy_detail}"
    elif style == "Digital Art":
        return f"{base_prompt}, digital art, highly detailed throughout, sharp focus everywhere, intricate details, trending on artstation, concept art, everything in focus"
    elif style == "Oil Painting":
        return f"{base_prompt}, oil painting, classical art style, rich colors, textured brushstrokes, detailed throughout, everything clearly visible"
    elif style == "Watercolor":
        return f"{base_prompt}, watercolor painting, soft colors, flowing, artistic, detailed throughout"
    elif style == "3D Render":
        return f"{base_prompt}, 3D render, octane render, highly detailed, sharp focus throughout, volumetric lighting, everything in focus"
    elif style == "Anime/Manga":
        return f"{base_prompt}, anime style, manga art, vibrant colors, highly detailed, sharp details throughout, everything clearly drawn"
    elif style == "Sketch/Drawing":
        return f"{base_prompt}, pencil sketch, detailed drawing throughout, artistic, monochrome, sharp details everywhere"
    elif style == "Cinematic":
        return f"{base_prompt}, cinematic lighting, dramatic, film still, high quality, deep focus, everything in sharp detail"
    elif style == "Fantasy Art":
        return f"{base_prompt}, fantasy art, magical, highly detailed throughout, epic, vivid colors, intricate details everywhere"
    return base_prompt

# Quality enhancers (hidden in ultra realism mode)
if not realism_mode:
    col1, col2 = st.columns(2)
    with col1:
        add_details = st.checkbox("Add 'highly detailed'", value=True)
    with col2:
        add_quality = st.checkbox("Add quality keywords", value=True)
else:
    add_details = True
    add_quality = True

# Generate button
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    generate_button = st.button("🎨 Generate Image", use_container_width=True)

# Image generation
if generate_button:
    if not prompt.strip():
        st.warning("Please enter a description for your image!")
    else:
        # Override advanced settings for realism mode
        if realism_mode:
            # Maximum quality settings for ultra photorealism (slower but much better)
            actual_guidance_scale = 15.0  # Very high guidance for maximum precision
            actual_width = 1024
            actual_height = 1024
            actual_steps = 16  # Maximum steps allowed by FLUX.1-schnell model
        else:
            actual_guidance_scale = guidance_scale
            # Use selected size from selectbox as default, but advanced settings override if changed
            actual_width = selected_width if image_width == 768 else image_width
            actual_height = selected_height if image_height == 768 else image_height
            actual_steps = num_steps

        # Enhance the prompt
        enhanced_prompt = enhance_prompt(prompt, style_preset, ultra_realism=realism_mode)

        # Add additional quality keywords if selected (and not in realism mode - already added)
        if not realism_mode:
            if add_details and "detailed" not in enhanced_prompt.lower():
                enhanced_prompt += ", highly detailed throughout entire scene"
            if add_quality:
                enhanced_prompt += ", high quality, sharp focus everywhere, everything in focus, deep focus, no blur"

        # Show the enhanced prompt and settings
        with st.expander("📝 View Enhanced Prompt & Settings", expanded=False):
            st.info(f"**Positive Prompt:**\n{enhanced_prompt}")
            if negative_prompt and negative_prompt.strip():
                st.warning(f"**Negative Prompt:**\n{negative_prompt}")
            if realism_mode:
                st.success(f"🎯 Ultra Realism Settings Applied:\n- Resolution: {actual_width}x{actual_height}\n- Guidance Scale: {actual_guidance_scale}\n- Inference Steps: {actual_steps}")

        # Adjust spinner message based on mode
        spinner_message = "🎨 Creating ultra-realistic masterpiece... This will take 30-60 seconds for maximum quality..." if realism_mode else "🎨 Creating your masterpiece... This may take 10-30 seconds..."

        with st.spinner(spinner_message):
            try:
                # Prepare parameters for image generation
                generation_params = {
                    "prompt": enhanced_prompt,
                    "model": MODEL_NAME,
                    "width": actual_width,
                    "height": actual_height,
                    "guidance_scale": actual_guidance_scale,
                    "num_inference_steps": actual_steps
                }

                # Add negative prompt if provided
                if negative_prompt and negative_prompt.strip():
                    generation_params["negative_prompt"] = negative_prompt

                # Generate image using InferenceClient with parameters
                image = client.text_to_image(**generation_params)

                # Display the generated image
                st.success("✨ Image generated successfully!")
                st.image(image, caption=f"Generated: {prompt}", use_container_width=True)

                # Optional: Add download button
                # Convert PIL Image to bytes for download
                from io import BytesIO
                buf = BytesIO()
                image.save(buf, format="PNG")
                byte_im = buf.getvalue()

                st.download_button(
                    label="📥 Download Image",
                    data=byte_im,
                    file_name="ai_generated_image.png",
                    mime="image/png",
                    use_container_width=True
                )

                # Image refinement section
                st.markdown("---")
                st.subheader("🔧 Refine This Image")
                st.markdown("Want to improve this image? Tell the AI what to change!")

                refinement_prompt = st.text_area(
                    "What would you like to improve or change?",
                    placeholder="e.g., Make the colors more vibrant, add more detail to the face, make the lighting brighter, remove the background blur",
                    height=80,
                    key="refinement_prompt"
                )

                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    refine_button = st.button("🎨 Regenerate with Changes", use_container_width=True, key="refine_button")

                if refine_button:
                    if not refinement_prompt.strip():
                        st.warning("Please describe what you'd like to improve!")
                    else:
                        # Create enhanced prompt with refinement instructions
                        refined_prompt = f"{prompt}, {refinement_prompt}"

                        st.info(f"**Regenerating with improvements:** {refinement_prompt}")

                        with st.spinner("🎨 Creating improved version..."):
                            try:
                                # Enhance the refined prompt
                                enhanced_refined_prompt = enhance_prompt(refined_prompt, style_preset, ultra_realism=realism_mode)

                                # Add quality keywords if not in realism mode
                                if not realism_mode:
                                    if add_details and "detailed" not in enhanced_refined_prompt.lower():
                                        enhanced_refined_prompt += ", highly detailed throughout entire scene"
                                    if add_quality:
                                        enhanced_refined_prompt += ", high quality, sharp focus everywhere, everything in focus, deep focus, no blur"

                                # Generate refined image
                                refined_generation_params = {
                                    "prompt": enhanced_refined_prompt,
                                    "model": MODEL_NAME,
                                    "width": actual_width,
                                    "height": actual_height,
                                    "guidance_scale": actual_guidance_scale,
                                    "num_inference_steps": actual_steps
                                }

                                if negative_prompt and negative_prompt.strip():
                                    refined_generation_params["negative_prompt"] = negative_prompt

                                refined_image = client.text_to_image(**refined_generation_params)

                                # Display refined image
                                st.success("✨ Improved image generated!")
                                st.image(refined_image, caption=f"Refined: {refined_prompt}", use_container_width=True)

                                # Download button for refined image
                                buf_refined = BytesIO()
                                refined_image.save(buf_refined, format="PNG")
                                byte_im_refined = buf_refined.getvalue()

                                st.download_button(
                                    label="📥 Download Improved Image",
                                    data=byte_im_refined,
                                    file_name="ai_generated_image_refined.png",
                                    mime="image/png",
                                    use_container_width=True,
                                    key="download_refined"
                                )

                            except Exception as e:
                                st.error(f"❌ Error generating refined image: {str(e)}")

            except Exception as e:
                error_message = str(e)

                # Handle specific error cases
                if "rate limit" in error_message.lower() or "429" in error_message:
                    st.error("⏰ Rate limit reached! Please wait a moment before generating another image.")
                    st.info("The free tier has usage limits. Try again in a few minutes.")
                elif "authorization" in error_message.lower() or "401" in error_message or "403" in error_message:
                    st.error("🔑 Authentication failed!")
                    st.info("""
                    Please check your API token:
                    - Ensure your token has "Write" permissions
                    - Read-only tokens don't work for Inference API
                    - Get a new token at: https://huggingface.co/settings/tokens
                    """)
                elif "model" in error_message.lower() or "404" in error_message:
                    st.error("❌ Model not found or unavailable!")
                    st.info(f"The model '{MODEL_NAME}' might be unavailable. Try alternative models in the code.")
                else:
                    st.error(f"❌ Error generating image: {error_message}")
                    st.info("Please try again with a different prompt or check your internet connection.")

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #666;'>
        <p>Powered by HuggingFace FLUX.1-schnell model 🚀</p>
        <p style='font-size: 0.8rem;'>Free tier has rate limits. For unlimited access, consider upgrading your HuggingFace plan.</p>
    </div>
""", unsafe_allow_html=True)

# Sidebar with information
with st.sidebar:
    st.header("ℹ️ About")
    st.markdown("""
    This AI Image Generator uses:
    - **Model:** FLUX.1-schnell
    - **Provider:** HuggingFace
    - **Framework:** Streamlit

    ### 🎯 Ultra Realism Mode:

    **For maximum realism, enable:**
    - ✅ Ultra Realism Mode checkbox
    - Automatically sets:
      - Resolution: 1024x1024 (maximum)
      - Guidance Scale: 15 (maximum precision)
      - Inference Steps: 16 (maximum quality)
      - Enhanced photorealistic keywords
    - ⚠️ Takes 30-60 seconds per image

    **Tips for realistic images:**
    - Describe real-world scenes exactly as they appear
    - The AI uses keywords that mimic real camera captures
    - Natural lighting is automatically emphasized
    - Real camera characteristics (grain, HDR) are added
    - Everything will be sharp and detailed (no background blur)
    - Images will look like genuine photographs
    - Avoid fantasy/artistic elements

    **Keywords automatically added:**
    - "RAW photo" - mimics unprocessed camera output
    - "Canon EOS R5" - professional camera simulation
    - "Film grain" - natural camera texture
    - "Natural color grading" - authentic colors

    ### 🚫 Negative Prompts:

    **Use negative prompts to avoid:**
    - Fake/artificial: CGI, 3D render, cartoon, anime, drawing, painting, illustration
    - Quality issues: blurry, distorted, low quality, out of focus, soft focus
    - Background blur: bokeh, shallow depth of field, blurred background
    - Unwanted elements: text, watermark, signature
    - Bad aesthetics: ugly, deformed, bad anatomy, unrealistic
    - Wrong mood: dark, gloomy, horror

    **Pro tip for maximum realism:** Use this negative prompt:
    `CGI, 3D render, cartoon, anime, drawing, painting, illustration, blurry, bokeh, shallow depth of field, unrealistic, artificial`

    ### Example realistic prompts:
    - "Portrait of a person with natural lighting, shot on DSLR camera"
    - "Street photography of a busy city intersection at sunset"
    - "Close-up macro photo of a water droplet on a leaf"
    - "Product photo of a watch on marble surface, studio lighting"
    """)

    st.markdown("---")
    st.markdown("**Model:** " + MODEL_NAME)
    st.markdown("**Status:** 🟢 Ready")
