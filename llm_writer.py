# llm_writer.py

import os
from openai import OpenAI
from dotenv import load_dotenv
import certifi

load_dotenv()
os.environ["SSL_CERT_FILE"] = certifi.where()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_batch_paragraphs(batch: list[dict], user_prompt: str) -> dict:
    numbered_blocks = []
    for entry in batch:
        numbered_blocks.append(
            f"Title: {entry['section_title']}\nContent: {entry['content']}"
        )

    full_prompt = f"""{user_prompt}

Output Format:  
### <Rephrased Title>
<Paragraph>

Items:
{chr(10).join(numbered_blocks)}
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": full_prompt}]
        )
        output = response.choices[0].message.content.strip()

        results = {}
        sections = output.split("### ")[1:]
        for block in sections:
            lines = block.strip().split("\n", 1)
            if len(lines) == 2:
                title, paragraph = lines
                results[title.strip()] = paragraph.strip()
        return results

    except Exception as e:
        return {"[ERROR]": f"Batch generation error: {str(e)}"}