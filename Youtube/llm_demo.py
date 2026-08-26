from bs4 import BeautifulSoup
import requests
import xml.etree.ElementTree as ET

feeds = ['https://arstechnica.com/tag/security/feed/', 
         'https://ironscales.com/threat-intelligence/rss.xml']

output = ''

def get_rss_links(feeds):

    """
    Iterates though RSS feeds to obtain Article URLs
    """

    links = []

    # Loop through all items in each RSS feed and extract the URLs for the full reports
    for feed in feeds:
        
        response = requests.get(feed, timeout=20)

        root = ET.fromstring(response.content)
        channel = root.find("channel")
        items = channel.findall("item")

        for item in items:
            link = item.findtext("link")
            if link:
                links.append(link)

    return links

def get_page_text(url):

    """
    Downloads webpage content and extracts article text.
    """

    response = requests.get(url, timeout=20)

    soup = BeautifulSoup(response.text, "html.parser")

    # Remove non-article content
    for tag in soup(
        [
            "script",
            "style",
            "nav",
            "footer",
            "header"
        ]
    ):
        tag.decompose()

    text = soup.get_text(
        separator="\n",
        strip=True
    )

    return text


# Get all article links from RSS feeds
links = get_rss_links(feeds)

# Extract text for each article
for link in links:
    output += f'{get_page_text(link)}\n\n\n\n\n'

# Save all text to output.txt 
with open('output.txt', 'w') as f:
    f.write(output)






prompt = """
        You are a cyber threat intelligence analyst tasked with extracting relevant indicators from an article and logging them in a standardized format.

        Extract all relevant indicators and indicator types from this report.
        For each indicator return:
        -raw_indicator
        -parsed_indicator
        -indicator_type

        Rules:
        - Do not invent indicators.
        - Return only information supported by the report.
        - The only acceptable indicator types are: "IP Address", "Domain", and "CVE".
        - The raw indicator is the indicator exactly as it appears in the report. It could be defanged (Ex 192.168.1[.]1, hxxp://example[.]com, etc) or non-defanged (Ex 192.168.1.1, http://example.com, etc.)
        - The parsed indicator is the indicator in its non-defanged form. Ex 192.168.1.1, http://example.com, etc.


"""

    cve_pattern = r'^CVE-\d{4}-\d{4,}$'
    domain_pattern = r'\b(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}\b'
    ip_pattern = r'\b(?:25[0-5]|2[0-4]\d|1\d{2}|[1-9]?\d)(?:\.(?:25[0-5]|2[0-4]\d|1\d{2}|[1-9]?\d)){3}\b'
