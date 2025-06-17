import openai

openai.api_key = "your_openai_key"

def generate_newsletter(updates):
    formatted = "\n\n".join([f"{u.email} said: {u.text}" for u in updates])
    prompt = f"Write a warm and friendly newsletter summarizing these:\n{formatted}"
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content
