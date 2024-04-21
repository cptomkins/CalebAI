import requests
from bs4 import BeautifulSoup
import caleb_tokenize


def expand_search(pos_tag, verb, query, debug=False):
    search_url = None
    pass


def get_most_viewed_pages_with_term(term, limit=15):
    pass
    

def search_wikipedia(query, debug=False):
    
    if debug:
        print("query", query)
    
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
            if debug:
                print("response", response)
            return "I found multiple meanings for your query. Can you please specify?"
        
        
        relevant_text = ''
        # Find relevant information sections (e.g., 'History', 'Early life')
        relevant_sections = soup.find_all('p')
        for relevant_section in relevant_sections:
            relevant_text = relevant_section.text.strip()
            if relevant_text:
                break
        
        # Check if relevant information is found
        if relevant_text:
            return relevant_text
        else:
            return "I'm sorry, I couldn't find relevant information on Wikipedia."
    else:
        return "I'm sorry, I couldn't connect to Wikipedia."

def process_question(sentence, debug=False):
    question = caleb_tokenize.find_question(sentence)
    obj = caleb_tokenize.find_object(sentence, debug=debug)
    if question and obj:
        return search_wikipedia(obj, debug=debug)
    else:
        return 'I didn\'t understand the question'


if __name__=='__main__':
    
#     term = "Python"
#     most_viewed_pages = get_most_viewed_pages_with_term(term)
#     for i, (title, views) in enumerate(most_viewed_pages, start=1):
#         print(f"{i}. Title: {title}, Views: {views}")
    
    
    sentence = input("How can I help you?\n")
    result = process_question(sentence)
    print(result)
    
    while True:
        sentence = input("Is there something else?\n")
        if sentence == 'exit':
            break
        result = process_question(sentence)
        print(result)
