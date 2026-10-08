import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)

response = client.chat.completions.create(
    model="openai/gpt-oss-120b",
    messages=[
        {"role": "system", "content": "You are a witty travel guide."},
        {"role": "user",   "content": "Suggest one thing to do in Bangalore."},
    ],
)
print("── GPT says:", response.choices[0].message.content)



import os

groq_client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)

response = groq_client.chat.completions.create(
    model="openai/gpt-oss-120b",
    messages=[
        {"role": "system", "content": "You are a witty travel guide."},
        {"role": "user",   "content": "Suggest one thing to do in Bangalore."},
    ],
)
print("── Llama says:", response.choices[0].message.content)



import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}

def fetch_website_contents(url):
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
        r.raise_for_status()
    except requests.exceptions.RequestException as e:
        return f"Could not fetch the website. Error: {e}"

    soup = BeautifulSoup(r.text, "html.parser")
    title = soup.title.string if soup.title else "No title"

    for tag in soup(["script", "style", "nav", "footer", "header", "img", "input"]):
        tag.decompose()

    text = soup.get_text(separator="\n", strip=True)
    return f"Title: {title}\n\nPage contents:\n{text}"



SYSTEM_PROMPT = """You analyze the contents of a website and
give a short, friendly summary. Ignore navigation menus.
Respond in markdown."""

def summarize(url):
    website = fetch_website_contents(url)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",   "content": f"Summarize this website:\n\n{website}"},
        ],
    )
    return response.choices[0].message.content


import gradio as gr

gr.Interface(
    fn=summarize,
    inputs=gr.Textbox(label="Website URL"),
    outputs=gr.Markdown(label="Summary"),
    title="AI Website Summarizer",
).launch(share=True)
