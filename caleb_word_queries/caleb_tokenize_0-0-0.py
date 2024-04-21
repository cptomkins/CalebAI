import requests
from bs4 import BeautifulSoup
import caleb_tokenize


def search_wikipedia(query):
    # Prepare the search URL
    search_url = f"https://en.wikipedia.org/wiki/{query.replace(' ', '_')}"
    
    # Send a GET request to Wikipedia
    response = requests.get(search_url)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Check for disambiguation pages
        disambiguation_tag = soup.find('div', {'id': 'disambigbox'})
        if disambiguation_tag:
            return "I found multiple meanings for your query. Can you please specify?"
        
        # Find relevant information sections (e.g., 'History', 'Early life')
        relevant_sections = soup.find_all('p')
        
        # Extract the text content from the relevant sections
        relevant_text = '\n'.join([section.text.strip() for section in relevant_sections])
        
        # Check if relevant information is found
        if relevant_text:
            return relevant_text
        else:
            return "I'm sorry, I couldn't find relevant information on Wikipedia."
    else:
        return "I'm sorry, I couldn't connect to Wikipedia."


if __name__=='__main__':
    sentence = input("How can I help you?\n")
    obj = caleb_tokenize.find_object(sentence)
    print(obj)
