import streamlit as st
from huggingface_hub import InferenceClient
from dotenv import load_dotenv
import os
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import random

# Load environment variables
load_dotenv()

# Configuration
MODEL_NAME = "stabilityai/stable-diffusion-xl-base-1.0"
HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_TOKEN")
DEMO_MODE = os.getenv("DEMO_MODE", "false").lower() == "true"  # Disable demo mode by default

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
if DEMO_MODE:
    st.markdown("### Transform your ideas into stunning images using AI!")
    st.info("🎭 **DEMO MODE ACTIVE** - Generating placeholder images for UI/UX demonstration. All features work!")
else:
    st.markdown("### Transform your ideas into stunning images using AI!")
    st.markdown("*Powered by Stable Diffusion XL - High-Quality Image Generation*")

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

# Initialize session state for image history
if 'image_history' not in st.session_state:
    st.session_state.image_history = []

# Style preset definitions (must be defined before sidebar)
STYLE_PRESETS = {
    "None": "",
    "Anime": ", anime style, vibrant colors, Studio Ghibli inspired, detailed illustration, manga art, highly detailed",
    "Realistic": ", photorealistic, highly detailed, 8K resolution, professional photography, sharp focus, natural lighting, realistic materials",
    "Digital Art": ", digital painting, artstation trending, concept art, highly detailed, intricate details, professional digital illustration",
    "Watercolor": ", watercolor painting, soft colors, artistic, flowing brushstrokes, traditional art, delicate details",
    "Oil Painting": ", oil painting, classical art style, rich colors, textured brushstrokes, traditional painting, masterpiece",
    "Cyberpunk": ", cyberpunk style, neon lights, futuristic, sci-fi, dystopian city, technology, glowing elements, dark atmosphere",
    "Fantasy": ", fantasy art, magical, enchanted, epic, mystical atmosphere, dramatic lighting, otherworldly, highly detailed"
}

# Demo mode function to generate placeholder images
def generate_demo_image(prompt, style, width=768, height=768):
    """Generate a colorful placeholder image for demo purposes"""
    # Style-based color schemes
    style_colors = {
        "None": [(100, 150, 200), (150, 200, 250)],
        "Anime": [(255, 182, 193), (255, 105, 180)],
        "Realistic": [(139, 69, 19), (210, 180, 140)],
        "Digital Art": [(138, 43, 226), (75, 0, 130)],
        "Watercolor": [(173, 216, 230), (135, 206, 250)],
        "Oil Painting": [(184, 134, 11), (218, 165, 32)],
        "Cyberpunk": [(0, 255, 255), (255, 0, 255)],
        "Fantasy": [(148, 0, 211), (75, 0, 130)]
    }

    # Get colors for the selected style
    colors = style_colors.get(style, [(100, 150, 200), (150, 200, 250)])

    # Create gradient image
    img = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(img)

    # Draw gradient background
    for i in range(height):
        r = int(colors[0][0] + (colors[1][0] - colors[0][0]) * i / height)
        g = int(colors[0][1] + (colors[1][1] - colors[0][1]) * i / height)
        b = int(colors[0][2] + (colors[1][2] - colors[0][2]) * i / height)
        draw.rectangle([(0, i), (width, i + 1)], fill=(r, g, b))

    # Add text overlay
    try:
        # Try to use default font, if not available use basic
        font_size = 40
        # Draw text with background
        text = f"DEMO: {style} Style"
        prompt_text = prompt[:50] + "..." if len(prompt) > 50 else prompt

        # Calculate text position
        text_bbox = draw.textbbox((0, 0), text)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]

        # Draw semi-transparent background for text
        padding = 20
        draw.rectangle(
            [(width//2 - text_width//2 - padding, height//2 - 60),
             (width//2 + text_width//2 + padding, height//2 + 60)],
            fill=(0, 0, 0, 180)
        )

        # Draw text
        draw.text((width//2, height//2 - 30), text, fill=(255, 255, 255), anchor="mm")
        draw.text((width//2, height//2 + 10), prompt_text, fill=(200, 200, 200), anchor="mm")
    except:
        pass

    return img

# Sidebar with style selector (must come before main content to define style_preset)
with st.sidebar:
    st.header("🎨 Style Presets")
    st.markdown("Choose a style to automatically enhance your prompts:")

    # Style selector in sidebar - using session state to handle realism mode
    if 'realism_mode_temp' not in st.session_state:
        st.session_state.realism_mode_temp = False

    style_preset = st.selectbox(
        "Select Style:",
        list(STYLE_PRESETS.keys()),
        index=0,
        help="Select a style preset to automatically add style-specific keywords to your prompt",
        disabled=st.session_state.get('realism_mode_temp', False)
    )

    # Show what the style adds
    if style_preset != "None":
        with st.expander("💡 See what this style adds", expanded=False):
            st.code(STYLE_PRESETS[style_preset], language=None)

    if st.session_state.get('realism_mode_temp', False):
        st.info("🎯 Ultra Realism Mode is active - style presets are disabled")


    st.markdown("---")
    st.header("🚫 Negative Prompts")
    st.markdown("Specify what you **DON'T** want in the image:")

    negative_prompt = st.text_area(
        "Negative Prompt (Optional):",
        placeholder="blurry, low quality, deformed, unrealistic, artificial",
        height=80,
        help="Specify unwanted elements to exclude from the image",
        key="negative_prompt"
    )

    st.markdown("---")
    st.header("⚙️ Advanced Settings")
    with st.expander("Customize generation parameters", expanded=False):
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

    st.markdown("---")
    st.header("ℹ️ About")
    st.markdown(f"""
    **Model:** {MODEL_NAME}
    **Status:** 🟢 Ready

    **Made with:** Streamlit + HuggingFace API
    """)

# Main interface
st.markdown("---")

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

# Update session state for realism mode
st.session_state.realism_mode_temp = realism_mode

# Override style preset if realism mode is enabled
if realism_mode:
    style_preset = "None"

# Prompt input
prompt = st.text_area(
    "Enter your image description:",
    placeholder="e.g., A serene landscape with mountains at sunset",
    height=100,
    help="Be specific! Include details about subject, composition, lighting, colors, and mood."
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
    else:
        # Use style preset
        style_suffix = STYLE_PRESETS.get(style, "")
        return base_prompt + style_suffix

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
        with st.expander("📝 View Enhanced Prompt & Settings", expanded=True):
            st.markdown("**Your Base Prompt:**")
            st.code(prompt, language=None)

            if style_preset != "None" and not realism_mode:
                st.markdown(f"**Selected Style:** {style_preset}")
                st.markdown("**Style Keywords Added:**")
                st.code(STYLE_PRESETS[style_preset], language=None)

            st.markdown("**Final Enhanced Prompt:**")
            st.info(enhanced_prompt)

            if negative_prompt and negative_prompt.strip():
                st.markdown("**Negative Prompt:**")
                st.warning(negative_prompt)

            if realism_mode:
                st.success(f"🎯 Ultra Realism Settings Applied:\n- Resolution: {actual_width}x{actual_height}\n- Guidance Scale: {actual_guidance_scale}\n- Inference Steps: {actual_steps}")

        # Adjust spinner message based on mode
        if DEMO_MODE:
            spinner_message = "🎨 Generating demo image..."
        else:
            spinner_message = "🎨 Creating ultra-realistic masterpiece... This will take 30-60 seconds for maximum quality..." if realism_mode else "🎨 Creating your masterpiece... This may take 10-30 seconds..."

        with st.spinner(spinner_message):
            try:
                # Generate image - use demo mode if enabled or if API fails
                if DEMO_MODE:
                    # Generate demo placeholder image
                    import time
                    time.sleep(1)  # Simulate processing time
                    image = generate_demo_image(prompt, style_preset, actual_width, actual_height)
                else:
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

                # Add to image history
                image_data = {
                    'image': image,
                    'prompt': prompt,
                    'enhanced_prompt': enhanced_prompt,
                    'style': style_preset,
                    'timestamp': datetime.now(),
                    'realism_mode': realism_mode
                }
                st.session_state.image_history.insert(0, image_data)

                # Limit to 10 images
                if len(st.session_state.image_history) > 10:
                    st.session_state.image_history = st.session_state.image_history[:10]

                # Display the generated image
                st.success("✨ Image generated successfully!")
                st.image(image, caption=f"Generated: {prompt}", use_column_width=True)

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
                                if DEMO_MODE:
                                    import time
                                    time.sleep(1)
                                    refined_image = generate_demo_image(refined_prompt, style_preset, actual_width, actual_height)
                                else:
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

                                # Add refined image to history
                                refined_image_data = {
                                    'image': refined_image,
                                    'prompt': refined_prompt,
                                    'enhanced_prompt': enhanced_refined_prompt,
                                    'style': style_preset,
                                    'timestamp': datetime.now(),
                                    'realism_mode': realism_mode
                                }
                                st.session_state.image_history.insert(0, refined_image_data)

                                # Limit to 10 images
                                if len(st.session_state.image_history) > 10:
                                    st.session_state.image_history = st.session_state.image_history[:10]

                                # Display refined image
                                st.success("✨ Improved image generated!")
                                st.image(refined_image, caption=f"Refined: {refined_prompt}", use_column_width=True)

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

# Image History Gallery
if st.session_state.image_history:
    st.markdown("---")
    st.header("🖼️ Image History")
    st.markdown(f"*Showing {len(st.session_state.image_history)} of 10 maximum images*")

    # Clear history button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🗑️ Clear History", use_container_width=True, key="clear_history"):
            st.session_state.image_history = []
            st.rerun()

    st.markdown("---")

    # Display images in grid (3 columns)
    for idx in range(0, len(st.session_state.image_history), 3):
        cols = st.columns(3)

        for col_idx, col in enumerate(cols):
            img_idx = idx + col_idx
            if img_idx < len(st.session_state.image_history):
                img_data = st.session_state.image_history[img_idx]

                with col:
                    # Display image
                    st.image(img_data['image'], use_column_width=True)

                    # Show style badge
                    if img_data['realism_mode']:
                        st.markdown("🎯 **Ultra Realism Mode**")
                    elif img_data['style'] != "None":
                        st.markdown(f"🎨 **Style:** {img_data['style']}")

                    # Show prompt in expander
                    with st.expander(f"📝 Prompt #{img_idx + 1}", expanded=False):
                        st.markdown(f"**Original:** {img_data['prompt']}")
                        st.caption(f"*Generated: {img_data['timestamp'].strftime('%H:%M:%S')}*")

                    # Download button for this image
                    from io import BytesIO
                    buf_history = BytesIO()
                    img_data['image'].save(buf_history, format="PNG")
                    byte_im_history = buf_history.getvalue()

                    st.download_button(
                        label="📥 Download",
                        data=byte_im_history,
                        file_name=f"ai_image_{img_idx + 1}.png",
                        mime="image/png",
                        use_container_width=True,
                        key=f"download_history_{img_idx}"
                    )

                    # Regenerate with same prompt button
                    if st.button("🔄 Regenerate", use_container_width=True, key=f"regen_{img_idx}"):
                        st.session_state.regen_prompt = img_data['prompt']
                        st.session_state.regen_style = img_data['style']
                        st.info(f"💡 Scroll up and click 'Generate Image' to recreate with prompt: '{img_data['prompt']}'")

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #666;'>
        <p>Powered by HuggingFace FLUX.1-schnell model 🚀</p>
        <p style='font-size: 0.8rem;'>Free tier has rate limits. For unlimited access, consider upgrading your HuggingFace plan.</p>
    </div>
""", unsafe_allow_html=True)
