from gpt4all import GPT4All
import os

def download_model():
    print("Starting Tman AI model download...")
    try:
        model = GPT4All("mistral-7b-instruct-v0.1.Q4_0.gguf")
        print("✅ Model downloaded successfully!")
        return True
    except Exception as e:
        print(f"❌ Error downloading model: {e}")
        return False

if __name__ == "__main__":
    print("📚 Setting up Tman AI...")
    success = download_model()
    if success:
        print("🎉 Tman AIt lm9owd is ready to help with study scheduling!")
    else:
        print("❌ Setup failed. Please check your internet connection and try again.")
