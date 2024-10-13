import openai

# Initialize OpenAI API
openai.api_key = 'your-openai-api-key'  # Replace with your OpenAI API key

def ask_ai(question):
    """Ask AI a question and get the response."""
    response = openai.Completion.create(
      engine="gpt-4",
      prompt=question,
      max_tokens=150
    )
    return response.choices[0].text.strip()

def ai_suggest_export_format(domain, scan_data):
    """AI suggests the best format to export based on scan size and type."""
    question = f"Would you like to export the scan results for {domain} in PDF, HTML, JSON, or CSV? Here are the first few findings: {scan_data[:3]}"
    ai_response = ask_ai(question)
    print(f"AI suggests: {ai_response}")
    return ai_response
