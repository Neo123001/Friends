import base64
import os
from openai import OpenAI

# Initialize OpenAI client with secure API key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY", ""))

def image_to_base64(path):
    try:
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
    except Exception as e:
        print(f"[Warning] Failed to read image {path}: {e}")
        return None

def generate_newsletter(updates):
    messages = [
        {
            "role": "system",
            "content": (
                "Generate a crisp, direct newsletter listing each user's update. "
                "Use bullet points. Show the user's name in bold. Do NOT rephrase their message. "
                "Just display what they wrote, exactly. Omit any generic greetings or summaries."
                "Format it well."
            )
        }
    ]
    added_any = False

    for update in updates:
        try:
            if not update.text and not update.image_path:
                continue  # Skip empty entries

            content = []

            if update.text:
                content.append({
                    "type": "text",
                    "text": f"{update.email or 'Someone'} said: {update.text}"
                })

            if update.image_path:
                image_data = image_to_base64(update.image_path)
                if image_data:
                    content.append({
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{image_data}"
                        }
                    })

            if content:
                messages.append({
                    "role": "user",
                    "content": content
                })
                added_any = True
        except Exception as e:
            print(f"[Error] Skipping update: {e}")
            continue

    if not added_any:
        return "No valid updates to generate newsletter."

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            max_tokens=700
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"[OpenAI Error] {e}")
        return "Failed to generate newsletter due to an AI error."
