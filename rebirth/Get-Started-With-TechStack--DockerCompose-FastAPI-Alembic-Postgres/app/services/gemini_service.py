import re
import google.generativeai as genai
from app.core.config import settings

# Configure the Google Generative AI client
genai.configure(api_key=settings.GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-pro')  # Selected a free model

# Define constants
MAX_INPUT_TOKENS = 1000  # Adjust as necessary
MAX_OUTPUT_CHARACTERS = 1000  # Characters per "page"

def clean_markdown(text):
    """
    Removes Markdown formatting from the input text.
    """
    # Simple regex to eliminate common Markdown elements
    cleaned_text = re.sub(r'[_*~`#>\[\]()]', '', text)
    return cleaned_text

def paginate_text(text, max_length):
    """
    Splits the text into pages of specified maximum length.
    """
    return [text[i:i + max_length] for i in range(0, len(text), max_length)]

def gemini_response(text):
    """
    Generates a response using the Gemini model while adhering to token limits
    and providing paginated output.
    """
    # Clean the input text
    text = clean_markdown(text)
    
    # Truncate input text to meet the token limit (roughly approximating tokens by character count)
    truncated_text = text[:MAX_INPUT_TOKENS]
    
    # Generate the content
    response = model.generate_content(truncated_text)
    
    # Paginate the response text
    pages = paginate_text(response.text, MAX_OUTPUT_CHARACTERS)
    
    return pages

# Example usage:
input_text = "Your input text here..."
output_pages = gemini_response(input_text)
for i, page in enumerate(output_pages):
    print(f"Page {i + 1}:\n{page}\n")
