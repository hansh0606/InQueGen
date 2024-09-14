import requests
import PyPDF2
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from dotenv import load_dotenv
import os

# Download the NLTK data files (only need to do this once)
nltk.download('punkt')
nltk.download('stopwords')

load_dotenv()
# Set your RapidAPI key and host
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
RAPIDAPI_HOST = os.getenv("RAPIDAPI_HOST")


# Function to extract text from PDF
def extract_text_from_pdf(file_path):
    

    # print(RAPIDAPI_HOST)
    # print(RAPIDAPI_KEY)
    with open(file_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ''
        for page_num in range(len(pdf_reader.pages)):
            text += pdf_reader.pages[page_num].extract_text() or ''  # Ensure no None values
    return text


# Function to extract technical keywords from text
def extract_technical_keywords(text):
    punctuations = ['(', ')', ';', ':', '[', ']', ',', '...', '.', '']
    tokens = word_tokenize(text)
    stop_words = set(stopwords.words('english'))
    technical_keywords = []

    # Define the list of technical keywords
    technical_keyword_list = [
        'programming', 'coding', 'software', 'development', 'algorithm', 'database',
        'system design', 'data structure', 'object-oriented', 'java', 'python', 'c++',
        'javascript', 'html', 'css', 'backend', 'frontend', 'full-stack', 'git',
        'version control', 'agile', 'testing', 'debugging', 'framework', 'library',
        'api', 'restful', 'http', 'server', 'client', 'routing', 'authentication',
        'authorization', 'security', 'scalability', 'performance', 'optimization'
    ]
    additional_technical_keywords = [
        'ruby', 'php', 'swift', 'kotlin', 'typescript', 'scala', 'go', 'rust', 'perl',
        'shell', 'bash', 'r', 'matlab', 'assembly', 'haskell', 'lua', 'dart', 'groovy',
        'clojure', 'elixir', 'mongodb', 'mysql', 'postgresql', 'sqlite', 'oracle',
        'sql server', 'redis', 'cassandra', 'firebase', 'docker', 'kubernetes', 'jenkins',
        'ansible', 'terraform', 'aws', 'azure', 'google cloud', 'heroku', 'apache', 'nginx',
        'spring', 'django', 'flask', 'express', 'react', 'angular', 'vue', 'jquery', 'bootstrap',
        'tailwind css', 'sass', 'less', 'redux', 'mobx', 'webpack', 'babel', 'npm', 'yarn',
        'storybook', 'jest', 'mocha', 'chai', 'enzyme', 'selenium', 'junit', 'pytest', 'cypress',
        'gitlab', 'bitbucket', 'svn', 'mercurial', 'jira', 'trello', 'confluence', 'slack', 'discord'
    ]
    technical_keyword_list.extend(additional_technical_keywords)

    # Extract keywords
    for word in tokens:
        word = word.lower()
        if word not in stop_words and word not in punctuations:
            if word in technical_keyword_list:
                technical_keywords.append(word)
            elif word.isdigit():
                technical_keywords.append(word)
    return technical_keywords

# Function to generate interview questions using RapidAPI
def generate_interview_questions(keywords):
    url = "https://chatgpt-42.p.rapidapi.com/conversationgpt4-2"
    payload = {
        "messages": [
            {
                "role": "user",
                "content": "Generate technical interview questions based on these keywords: " + ', '.join(keywords)
            }
        ],
        "web_access": False,
        "system_prompt": "",
        "temperature": 0.9,
        "top_k": 5,
        "top_p": 0.9,
        "max_tokens": 256
    }
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": RAPIDAPI_HOST
    }
    response = requests.post(url, json=payload, headers=headers)
    
    # Debugging: Print the response status code and JSON content
    print("Response Status Code:", response.status_code)
    print("Response JSON:", response.json())

    if response.status_code == 200:
        response_data = response.json()
        # Handle the response based on actual structure
        if 'choices' in response_data:
            questions = response_data['choices'][0]['message']['content'].strip()  # Ensure there's no leading/trailing whitespace
            return {"result": questions}
        elif 'result' in response_data:
            return {"result": response_data['result']}
        elif 'text' in response_data:
            return {"result": response_data['text']}
        else:
            return {"error": "Unexpected response structure"}
    else:
        return {"error": "Failed to generate questions"}
