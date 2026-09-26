import requests
from bs4 import BeautifulSoup


def fetch_web_content(url):
    response = requests.get(
        url,
        timeout=10,
        headers={
            "User-Agent": "ArrowLens/1.0"
        }
    )

    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    # Remove the styles etc
    for element in soup(["script", "style", "noscript"]):
        element.decompose()

    # Get the imp contetn
    title = soup.title.get_text(strip=True) if soup.title else ""

    # Limit the content scraped
    main = soup.find("main")

    if main:
        text = main.get_text(" ", strip=True)
    else:
        text = soup.get_text(" ", strip=True)

    text = text[:30000]
    return {
        "title": title,
        "content": text[:30000],
        "url": url
    }