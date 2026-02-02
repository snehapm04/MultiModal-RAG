import openai

def generate(context, question):
    prompt = f"""
Context:
{context}

Question:{question}
Answer with citations.
"""
    return openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role":"user","content":prompt}]
    )["choices"][0]["message"]["content"]
