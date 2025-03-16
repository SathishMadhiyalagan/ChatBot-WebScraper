from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

from api.views import add_text_content

def setup_driver():
    """Initializes and returns a Selenium WebDriver with configured options."""
    options = Options()
    options.add_argument("--headless")  # Run without UI
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)

def scrape_website(driver, url):
    """Fetches the page source and returns HTML content."""
    driver.get(url)
    time.sleep(2)  # Allow time for dynamic content to load
    return driver.page_source

def scrape_page(driver, url):
    """Scrapes detailed content from an individual page."""
    html_content = scrape_website(driver, url)
    soup = BeautifulSoup(html_content, "html.parser")

    scraped_data = {
        "headings": [h2.get_text(strip=True) for h2 in soup.find_all('h2')],
        "paragraphs": [p.get_text(strip=True) for p in soup.find_all('p')],
        "images": [img['src'] for img in soup.find_all('img') if 'src' in img.attrs],
        "list_items": [li.get_text(strip=True) for li in soup.find_all('li')]
    }
    return scraped_data

def extract_blog_posts(driver, html_content, base_url):
    """Extracts blog post details from the HTML content."""
    soup = BeautifulSoup(html_content, "html.parser")
    body_content = list(soup.body.div.div.children)[-2] if soup.body else None

    if not body_content:
        return []

    blog_posts = []
    content_tags = body_content.find_all("a")

    for link in content_tags:
        href = link.get("href")
        full_link = f"{base_url}{href}" if href else "No link"
        title = link.find("h2")
        content = link.find("p", class_="text-[#909090]")
        sub_page_content = scrape_page(driver, full_link)

        blog_posts.append({
            "title": title.text.strip() if title else "No title",
            "content": content.text.strip() if content else "No content",
            "link": full_link,
            "sub_page_content": sub_page_content
        })

    return blog_posts

def format_as_text(blogs):
    """Converts blog data into a formatted string (like a text file)."""
    text_output = "=== Blog Posts ===\n"
    
    for index, blog in enumerate(blogs, start=1):
        text_output += f"\nPost {index}:\n"
        text_output += f"Title: {blog['title']}\n"
        text_output += f"Content: {blog['content']}\n"
        text_output += f"Link: {blog['link']}\n"
        text_output += "Sub Page Content:\n"
        
        text_output += "  Headings:\n"
        for heading in blog["sub_page_content"]["headings"]:
            text_output += f"    - {heading}\n"

        text_output += "  Paragraphs:\n"
        for para in blog["sub_page_content"]["paragraphs"]:
            text_output += f"    - {para}\n"

        text_output += "  Images:\n"
        for img in blog["sub_page_content"]["images"]:
            text_output += f"    - {img}\n"

        text_output += "  List Items:\n"
        for item in blog["sub_page_content"]["list_items"]:
            text_output += f"    - {item}\n"
        
        text_output += "-" * 40  # Separator for readability
    
    return text_output

@api_view(['GET'])
def scraper(request):
    """API endpoint to scrape blog posts from a website."""
    BASE_URL = "https://blogs.falconreality.in"
    URL = "https://blogs.falconreality.in/"

    driver = setup_driver()
    try:
        html_content = scrape_website(driver, URL)
        blog_posts = extract_blog_posts(driver, html_content, BASE_URL)
        
        # Convert JSON data to formatted text output
        text_format = format_as_text(blog_posts)
        add_text_content(text_format)
        return Response({
            "blogs": blog_posts,
            "text_format": text_format  # Add the formatted string at the end
        })
    finally:
        driver.quit()



@api_view(["POST"])
def contentRag(request):
    try:
        data = request.data
        text_format = data.get("text", "")

        if not text_format:
            return Response({"error": "Text content is required"}, status=status.HTTP_400_BAD_REQUEST)

        response = add_text_content(text_format)
        return Response("Content added successfully", status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)