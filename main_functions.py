import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"

import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

from groq import Groq
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import WordNetLemmatizer
import string
from sentence_transformers import SentenceTransformer
from langchain_community.docstore.document import Document
from langchain_community.vectorstores import FAISS

client = Groq(api_key="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")

base_url = 'http://www.adaderana.lk'
    
headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def get_article_content(article_url):
        """
        This function visits a single article page and extracts its main content.
        """
        print(f"Fetching article: {article_url}")
        try:
            response = requests.get(article_url, headers=headers, timeout=10)
            response.raise_for_status()
    
            article_soup = BeautifulSoup(response.content, 'html.parser')
            
            content_selectors = [
                '.article-content',
                '.story-content',
                '.main-content',
                '.content',
                '[class*="content"]',
                '[class*="body"]',
                '[class*="story"]'
            ]
            
            article_text = ""
            for selector in content_selectors:
                content_container = article_soup.select_one(selector)
                if content_container:
                    paragraphs = content_container.find_all('p')
                    article_text = '\n'.join([para.get_text(strip=True) for para in paragraphs if para.get_text(strip=True)])
                    if article_text: 
                        break
            
            if not article_text:
                print(f"  Could not find main content container for {article_url}. Using fallback.")
                all_paragraphs = article_soup.find_all('p')
                main_content_paragraphs = []
                for p in all_paragraphs:
                    if len(p.get_text(strip=True)) > 50:
                        main_content_paragraphs.append(p)
                article_text = '\n'.join([p.get_text(strip=True) for p in main_content_paragraphs])
            
            return article_text
    
        except requests.exceptions.RequestException as e:
            print(f"  Failed to fetch article: {e}")
            return "Failed to retrieve article content."
        except Exception as e:
            print(f"  An error occurred while parsing the article: {e}")
            return "Error parsing article content."
    
def scrap():
        """Main function to scrape headlines and their content."""
        try:
            print("Scraping homepage for headlines and links...")
            response = requests.get(base_url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            article_links = []
    
        
            link_selectors = [
                'h2 a[href]', 
                'h3 a[href]',
                '.title a[href]',
                '.heading a[href]',
                '.news-title a[href]'
            ]
            
            for selector in link_selectors:
                links = soup.select(selector)
                for link in links:
                    href = link.get('href')
                    title = link.get_text(strip=True)
                    if href and title and len(title) > 20:  
                        absolute_url = urljoin(base_url, href)
                        if absolute_url != base_url and '/category/' not in absolute_url:
                            article_links.append({"title": title, "url": absolute_url})
                if article_links:  
                    break
    
            if not article_links:
                print("No links found with standard selectors. Trying broad analysis...")
                all_links = soup.find_all('a', href=True)
                for link in all_links:
                    href = link.get('href')
                    title = link.get_text(strip=True)
                    if ('/news/' in href or '/article/' in href or '/breaking-news/' in href) and title and len(title) > 30:
                        absolute_url = urljoin(base_url, href)
                        article_links.append({"title": title, "url": absolute_url})
    
            seen_urls = set()
            unique_articles = []
            for article in article_links:
                if article['url'] not in seen_urls:
                    seen_urls.add(article['url'])
                    unique_articles.append(article)
            
            print(f"Found {len(unique_articles)} unique articles. Starting content scraping...\n")
            
            all_articles_data = []
            for i, article in enumerate(unique_articles, 1):
                print(f"({i}/{len(unique_articles)})")
                content = get_article_content(article['url'])
                article['content'] = content
                all_articles_data.append(article)
                
                time.sleep(1)  
                if len(all_articles_data)>=3:
                    break
            
            print("\n" + "="*80)
            print("SCRAPING COMPLETE! RESULTS:")
            print("="*80)
            
            
            news = ''
            for article in all_articles_data:
                news += f"HEADLINE: {article['title']} CONTENT: {article['content']}"
                    
            print(f"\nFull results saved to 'daily_mirror_news.txt'")
            return news
    
        except Exception as e:
            print(f"A critical error occurred: {e}")



def preprocess_news_text(text, remove_stopwords=True, lemmatize=True, min_word_length=2):
    """
    Comprehensive preprocessing function for news articles.
    
    Parameters:
    text (str): Raw input text
    remove_stopwords (bool): Whether to remove stop words
    lemmatize (bool): Whether to lemmatize words
    min_word_length (int): Minimum word length to keep
    
    Returns:
    str: Preprocessed text
    """
    if not text or text.strip() == "":
        return ""
    
    text = text.lower()
    
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    
    text = re.sub(r'\S+@\S+', '', text)
    
    text = re.sub(r'\d+', '', text)
    
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    
    text = re.sub(r'\s+', ' ', text).strip()
    
    words = word_tokenize(text)
    
    if remove_stopwords:
        stop_words = set(stopwords.words('english'))
        news_stopwords = {'said', 'says', 'according', 'reported', 'report', 'news', 'story', 'article'}
        stop_words.update(news_stopwords)
        words = [word for word in words if word not in stop_words and len(word) >= min_word_length]
    
    if lemmatize:
        lemmatizer = WordNetLemmatizer()
        words = [lemmatizer.lemmatize(word) for word in words]
    
    processed_text = ' '.join(words)
    
    return processed_text[1:5000]

def response(query, text1):
    docs = [text1]
    emb_model = SentenceTransformer("all-MiniLM-L6-v2")
    vectors = emb_model.encode(docs)
    
    doc_embeddings = [(docs[i], vectors[i]) for i in range(len(docs))]
    db = FAISS.from_embeddings(doc_embeddings, emb_model)

    query_vec = emb_model.encode([query])[0]
    retrieved = db.similarity_search_by_vector(query_vec, k=2)
    
    context = "\n".join([d.page_content for d in retrieved])
    prompt = f"""
            You are given the following context:

            {context}

            Question: {query}

            Instructions:
            - Write the answer in clean HTML.
            - Use only <h3>, <h4>, and <p> tags for structuring the response.
            - <h3> should be used for the main title.
            - <h4> should be used for subheadings.
            - <p> should be used for paragraphs of text.
            - Do not use any other HTML tags.
            """
    chat_completion = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=300,
    )
    
    return chat_completion.choices[0].message.content



