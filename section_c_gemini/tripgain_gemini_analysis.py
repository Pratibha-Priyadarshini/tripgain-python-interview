import os
import requests
from bs4 import BeautifulSoup
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def fetch_and_clean_webpage(url):
    """
    Fetch webpage content and clean HTML
    """
    print(f"Fetching content from: {url}")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    response = requests.get(url, headers=headers, timeout=30)
    response.raise_for_status()
    
    # Parse HTML
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Remove unwanted elements
    for element in soup(['script', 'style', 'nav', 'header', 'footer', 'aside', 'iframe', 'noscript']):
        element.decompose()
    
    # Extract text from main content areas
    main_content = soup.find('main') or soup.find('article') or soup.find('div', class_='content')
    
    if main_content:
        text = main_content.get_text(separator=' ', strip=True)
    else:
        # Fallback to body
        text = soup.get_text(separator=' ', strip=True)
    
    # Clean up whitespace
    text = ' '.join(text.split())
    
    # Limit text length (Gemini has token limits)
    max_chars = 30000
    if len(text) > max_chars:
        text = text[:max_chars]
    
    print(f"Extracted {len(text)} characters of cleaned text")
    return text

def analyze_with_gemini(content, url):
    """
    Send content to Gemini 2.5 Flash for analysis
    """
    # Configure Gemini API
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in environment variables")
    
    genai.configure(api_key=api_key)
    
    # Use Gemini 2.5 Flash
    model = genai.GenerativeModel('gemini-2.0-flash-exp')
    
    # Custom prompt for intelligent summarization
    prompt = f"""You are an expert analyst tasked with providing intelligent insights from web content.

Analyze the following webpage content from {url} and provide:

1. A concise summary in exactly 4-5 bullet points that capture the key themes, trends, or developments discussed. Focus on:
   - Main topics and their significance
   - Emerging trends or patterns
   - Key stakeholders or technologies mentioned
   - Important implications or outcomes

2. One insightful statement (1-2 sentences) that interprets what these points collectively suggest about the broader context, future direction, or underlying theme. This should be analytical, not just descriptive.

Format your response EXACTLY as follows:

Summary:
• [First key point]
• [Second key point]
• [Third key point]
• [Fourth key point]
• [Fifth key point if applicable]

Insight:
[Your analytical insight about what these trends/points suggest]

Content to analyze:
{content}

Remember: Be analytical and interpretive in your insight, not just summarizing. What do these points tell us about the bigger picture?"""
    
    print("Sending content to Gemini 2.5 Flash for analysis...")
    
    response = model.generate_content(prompt)
    
    return response.text

def main():
    # Choose a webpage to analyze
    urls = [
        "https://en.wikipedia.org/wiki/Artificial_intelligence",
        "https://www.bbc.com/news/technology",
        "https://edition.cnn.com/business"
    ]
    
    # Use the first URL (you can change this)
    url = urls[0]
    
    print("GEMINI INTEGRATION - INTELLIGENT WEBPAGE ANALYSIS")
    print()
    
    try:
        # Fetch and clean webpage
        content = fetch_and_clean_webpage(url)
        
        # Analyze with Gemini
        result = analyze_with_gemini(content, url)
        
        # Display result
        print("ANALYSIS RESULT")
        print()
        print(result)
        print()
        
        # Save to file
        output_file = "section_c_gemini/summary_output.txt"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"Source: {url}\n")
            f.write(f"Analysis Date: {requests.utils.default_headers()}\n\n")
            f.write(result)
        
        print(f"\nOutput saved to: {output_file}")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
