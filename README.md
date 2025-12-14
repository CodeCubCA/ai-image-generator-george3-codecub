   [![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/zrsH8x_3)

# 🎨 AI Image Generator

A web-based AI image generator that transforms text descriptions into stunning images using HuggingFace's FLUX.1-schnell model and Streamlit.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.31.0-FF4B4B.svg)
![HuggingFace](https://img.shields.io/badge/HuggingFace-API-yellow.svg)

## ✨ Features

- **AI-Powered Image Generation** - Generate high-quality images from text prompts
- **Style Presets** - 8 built-in artistic styles (Anime, Realistic, Digital Art, Watercolor, Oil Painting, Cyberpunk, Fantasy)
- **Ultra Realism Mode** - Advanced photorealistic settings with human skin detection
- **Modern UI** - Clean, user-friendly interface built with Streamlit
- **Fast Processing** - Uses FLUX.1-schnell model for quick generation
- **Image Refinement** - Regenerate images with improvements
- **Download Images** - Save your generated images directly
- **Negative Prompts** - Advanced control over what to exclude
- **Error Handling** - Comprehensive error messages and troubleshooting
- **Secure** - API tokens stored securely in environment variables

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- HuggingFace account and API token

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/CodeCubCA/ai-image-generator-george3-codecub.git
   cd ai-image-generator
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your API token**

   Create a `.env` file in the project root:
   ```bash
   copy .env.example .env
   ```

   Edit the `.env` file and add your HuggingFace token:
   ```
   HUGGINGFACE_TOKEN=hf_your_actual_token_here
   ```

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

   The app will open in your browser at `http://localhost:8501`

## 🔑 Getting Your HuggingFace API Token

1. Go to [HuggingFace Settings - Tokens](https://huggingface.co/settings/tokens)
2. Click "New token"
3. Give it a descriptive name (e.g., "image-generator")
4. **Important:** Select **"Write"** permissions (or at minimum "Make calls to the serverless Inference API")
5. Click "Generate token"
6. Copy the token (starts with `hf_`)
7. Paste it in your `.env` file

**Note:** Read-only tokens will NOT work for the Inference API!

## 📖 Usage

### Basic Workflow

1. **Select a Style** (in sidebar) - Choose from 8 artistic presets or "None" for custom prompts
2. **Enter Your Prompt** - Describe the image you want to generate
3. **Optional: Enable Ultra Realism Mode** - For photorealistic results
4. **Optional: Add Negative Prompt** - Specify what to avoid in the image
5. **Click "Generate Image"** - Wait 10-30 seconds for creation
6. **View & Download** - Save your generated image
7. **Refine if Needed** - Use the refinement feature to improve the image

### 🎨 Style Presets

The app includes 8 built-in style presets in the sidebar:

- **None** - Uses your prompt exactly as written
- **Anime** - Studio Ghibli-inspired, vibrant illustrated style
- **Realistic** - Photorealistic 8K photography
- **Digital Art** - Modern concept art, trending on ArtStation
- **Watercolor** - Soft, flowing traditional watercolor painting
- **Oil Painting** - Classical art with rich colors and texture
- **Cyberpunk** - Futuristic neon-lit sci-fi aesthetic
- **Fantasy** - Magical, enchanted epic fantasy art

Each style automatically adds appropriate keywords to your prompt. Click "See what this style adds" to preview the keywords.

### Example Prompts

**With Style Presets:**
- Style: Anime → Prompt: `a girl walking through a cherry blossom garden`
- Style: Cyberpunk → Prompt: `a city street at night`
- Style: Watercolor → Prompt: `a peaceful lakeside scene`
- Style: Fantasy → Prompt: `a dragon perched on a mountain peak`

**Without Style Presets (None):**
- `A serene mountain landscape at sunset with purple and orange sky, digital art`
- `A futuristic cyberpunk city with neon lights at night, highly detailed`
- `A cute corgi wearing a space suit, floating in space, digital illustration`
- `An enchanted forest with glowing mushrooms and fireflies, fantasy art style`

### 🎯 Ultra Realism Mode

For maximum photorealism:

1. Enable the "Ultra Realism Mode" checkbox
2. The app automatically:
   - Sets resolution to 1024x1024 (maximum)
   - Increases guidance scale to 15 (maximum precision)
   - Uses 16 inference steps (maximum quality)
   - Adds professional camera keywords (Canon EOS R5, RAW photo, film grain)
   - Detects human subjects and adds realistic skin texture keywords
3. Generation takes 30-60 seconds for best quality
4. Style presets are disabled (conflicts with realism settings)

**Best for:** Product photography, portraits, architectural shots, nature photography

### 🚫 Negative Prompts (Advanced)

Use negative prompts to avoid unwanted elements:

**For Realistic Images:**
```
CGI, 3D render, cartoon, illustration, blurry, bokeh, shallow depth of field, unrealistic, artificial
```

**For Human Portraits:**
```
plastic skin, smooth skin, airbrushed skin, poreless skin, waxy skin, bad anatomy, deformed hands
```

**General Quality:**
```
blurry, low quality, distorted, ugly, deformed, text, watermark
```

### 🔧 Image Refinement

After generating an image, you can refine it:

1. Scroll to the "Refine This Image" section
2. Describe what you'd like to improve (e.g., "make colors more vibrant", "add more detail to the face")
3. Click "Regenerate with Changes"
4. The app combines your original prompt + refinement request
5. Download the improved version

### Tips for Better Results

- **Be specific** - Include details about style, colors, lighting, and mood
- **Use style presets** - They add professional keywords automatically
- **Check enhanced prompt** - Expand "View Enhanced Prompt & Settings" to see what's being sent to the AI
- **Describe composition** - Specify what should be in the foreground/background
- **Add mood/atmosphere** - Include words like "serene", "dramatic", "whimsical"
- **Use negative prompts** - Avoid unwanted elements like blur, artifacts, or wrong styles

## 📁 Project Structure

```
ai-image-generator/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── .env.example          # Template for environment variables
├── .gitignore            # Git ignore file
└── README.md             # This file
```

## 🛠️ Technologies Used

- **[Streamlit](https://streamlit.io/)** - Web framework for the UI
- **[HuggingFace Inference API](https://huggingface.co/docs/huggingface_hub/guides/inference)** - AI image generation
- **[FLUX.1-schnell](https://huggingface.co/black-forest-labs/FLUX.1-schnell)** - Fast, high-quality image generation model
- **[Python-dotenv](https://github.com/theskumar/python-dotenv)** - Environment variable management
- **[Pillow](https://python-pillow.org/)** - Image processing

## ⚠️ Troubleshooting

### "API token not configured" Error

- Make sure you created a `.env` file (not `.env.example`)
- Verify your token is correctly pasted in the `.env` file
- Ensure there are no extra spaces or quotes around the token

### "Authentication failed" Error

- Your token might be read-only - create a new token with "Write" permissions
- Token might be expired - generate a new one
- Check that your token starts with `hf_`

### "Rate limit reached" or "402 Payment Required" Error

- You've reached the free monthly usage limit
- Options to continue:
  - **Wait until next month** - Free tier resets monthly
  - **Subscribe to HuggingFace PRO** - Get 20x more included usage
  - **Add pre-paid credits** - Pay as you go for additional generation
- Check your usage at [HuggingFace Settings](https://huggingface.co/settings/billing)

### "Model not found" Error

- The model might be temporarily unavailable
- Try alternative models by editing `MODEL_NAME` in [app.py](app.py):
  - `stabilityai/stable-diffusion-xl-base-1.0`
  - `runwayml/stable-diffusion-v1-5`

### Image generation is slow

- FLUX.1-schnell typically takes 10-30 seconds
- Slower internet connections may increase wait time
- Free tier might have slower processing during peak hours

## 🔒 Security Notes

- **Never commit your `.env` file** - It's already in `.gitignore`
- **Keep your API token secret** - Don't share it or post it online
- **Regenerate tokens** if accidentally exposed

## 📝 Requirements

All dependencies are listed in `requirements.txt`:

```
streamlit==1.31.0
python-dotenv==1.0.0
Pillow==10.2.0
huggingface_hub==0.20.3
```

## 🤝 Contributing

This is a GitHub Classroom assignment. Follow your instructor's guidelines for contributions.

## 📄 License

This project is created for educational purposes as part of a coding course.

## 🙋 Support

If you encounter issues:

1. Check the troubleshooting section above
2. Verify your API token has correct permissions
3. Check the [HuggingFace API status](https://status.huggingface.co/)
4. Review the error messages in the app - they provide specific guidance

## 🎓 Learning Resources

- [Streamlit Documentation](https://docs.streamlit.io/)
- [HuggingFace Inference API Guide](https://huggingface.co/docs/huggingface_hub/guides/inference)
- [FLUX.1 Model Card](https://huggingface.co/black-forest-labs/FLUX.1-schnell)

---

**Created with ❤️ using Streamlit and HuggingFace**
