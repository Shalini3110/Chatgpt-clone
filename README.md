# Chatgpt-clone
# 🔐 API Key Setup

This project requires an API key to work properly. Follow the steps below to set it up:

1. **Obtain your API key** from the appropriate service provider (e.g., OpenAI, Google, etc.).

2. **Create a `.env` file** in the root directory of your project.

3. **Add the following line** to your `.env` file:

   ```env
   API_KEY=your_api_key_here
   ```

4. Make sure your code loads the API key from the `.env` file. Example in Python:

   ```python
   import os
   from dotenv import load_dotenv

   load_dotenv()
   api_key = os.getenv("API_KEY")
   ```

> ⚠️ **Note:** Do **not** share your API key publicly. Always keep your `.env` file private and add it to `.gitignore`.

