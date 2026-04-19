import ollama

def ask_ai(prompt):
    """
    Convert user voice into short actionable command
    """

    try:
        response = ollama.chat(
            model='phi3',
            messages=[
                {
                    'role': 'system',
                    'content': '''
You are an AI assistant for desktop automation.

Convert user commands into SHORT actionable commands like:
- open chrome
- open notepad
- search google python
- shutdown system
- take screenshot

IMPORTANT RULES:
- Only return command
- No explanation
- No extra words
- Keep it short
'''
                },
                {
                    'role': 'user',
                    'content': prompt
                }
            ]
        )

        result = response['message']['content'].lower().strip()
        return result

    except Exception as e:
        print("Ollama Error:", e)
        return prompt  # fallback