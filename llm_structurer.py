import json
import re
import requests

TOGETHER_API_KEY = "af8affb443669b23360116602f15aea7982a51722d8d9b5cc130b15b8961650f"  # replace with real key

def extract_json_from_text(text):
    try:
        # Extract the first valid JSON object using regex
        match = re.search(r'\{[\s\S]*?\}', text)
        if match:
            return json.loads(match.group())
        else:
            return {"error": "No JSON found in LLM response", "raw": text}
    except json.JSONDecodeError:
        return {"error": "Failed to parse JSON", "raw": text}

def get_structured_output(raw_text):
    prompt = f"""
        Extract structured JSON from the following unstructured PDF text.

        {raw_text}

        Output format:
        {{
            "invoice_number": "",
            "customer": "",
            "port_of_loading": "",
            "date": "",
            "freight_amount": "",
            "freight_payable_at": "",
            "containers": [["", ""]]
        }}
    """

    headers = {
        "Authorization": f"Bearer {TOGETHER_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "mistralai/Mixtral-8x7B-Instruct-v0.1",
        "prompt": prompt,
        "max_tokens": 800,
        "temperature": 0.3,
    }

    response = requests.post(
        "https://api.together.xyz/v1/completions",
        headers=headers,
        json=data
    )

    result = response.json()

    try:
        llm_output = result["choices"][0]["text"]
        return extract_json_from_text(llm_output)
    except (KeyError, IndexError):
        return {
            "error": "Unexpected LLM response format",
            "raw": result
        }