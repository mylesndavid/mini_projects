import requests
from bs4 import BeautifulSoup

# Function to make the first half of a word bold
def make_bold(word):
    # Find the length of the word
    length = len(word)
    
    # Calculate the index of the middle of the word
    middle_index = length // 2
    
    # Return the bolded first half of the word
    return "<strong>" + word[:middle_index] + "</strong>" + word[middle_index:]

# URL of the webpage to process
url = "https://stackoverflow.com/questions/4706499/how-do-i-append-to-a-file"

# Send a GET request to the URL and store the response
response = requests.get(url)

# Parse the response as HTML
soup = BeautifulSoup(response.text, "html.parser")

# Loop through all the words on the page
for word in soup.find_all(text=True):
    # Make the first half of the word bold
    word.replace_with(make_bold(word))

# Print the modified HTML
print(soup)