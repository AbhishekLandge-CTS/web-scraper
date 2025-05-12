from flask import Flask, request, jsonify
import asyncio
from playwright.async_api import async_playwright

app = Flask(__name__)

async def scrape_google(query):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        url = f"https://html.duckduckgo.com/html/?q=JW+Marriott+Pune+phone+number"
        await page.goto(url, timeout=60000)
        await page.wait_for_selector('body')

        content = await page.content()
        await browser.close()

        return content

@app.route("/scrape", methods=["POST"])
def scrape():
    data = request.get_json()
    query = data.get("query")

    if not query:
        return jsonify({"error": "Missing 'query'"}), 400

    html_content = asyncio.run(scrape_google(query))
    return jsonify({"html": html_content})

if __name__ == '__main__':
    app.run(debug=True)
