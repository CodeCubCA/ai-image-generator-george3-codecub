[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/zrsH8x_3)

# 🎨 AI Image Generator

A web-based AI image generator that transforms text descriptions into stunning images using HuggingFace's FLUX.1-schnell model and Streamlit.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.31.0-FF4B4B.svg)
![HuggingFace](https://img.shields.io/badge/HuggingFace-API-yellow.svg)

## ✨ Features

- **AI-Powered Image Generation** - Generate high-quality images from text prompts
- **Modern UI** - Clean, user-friendly interface built with Streamlit
- **Fast Processing** - Uses FLUX.1-schnell model for quick generation
- **Download Images** - Save your generated images directly
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

1. Enter a detailed description of the image you want to generate
2. Click the "Generate Image" button
3. Wait 10-30 seconds for the AI to create your image
4. View the generated image
5. Click "Download Image" to save it

### Example Prompts

Try these prompts to get started:

- `A serene mountain landscape at sunset with purple and orange sky, digital art`
- `A futuristic cyberpunk city with neon lights at night, highly detailed`
- `A cute corgi wearing a space suit, floating in space, digital illustration`
- `An enchanted forest with glowing mushrooms and fireflies, fantasy art style`
- `A modern minimalist living room with large windows, architectural photography`

### Tips for Better Results

- **Be specific** - Include details about style, colors, lighting, and mood
- **Mention art style** - Add terms like "digital art", "oil painting", "photorealistic"
- **Describe composition** - Specify what should be in the foreground/background
- **Add mood/atmosphere** - Include words like "serene", "dramatic", "whimsical"

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

### "Rate limit reached" Error

- The free tier has usage limits
- Wait a few minutes before generating another image
- Consider upgrading your HuggingFace plan for unlimited access

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
