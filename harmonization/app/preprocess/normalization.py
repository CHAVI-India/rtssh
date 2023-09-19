
import re

def capitalize_after_underscore(input_string):
    words = input_string.split("_")
    capitalized_words = [word.capitalize() for word in words]
    return "_".join(capitalized_words)

def clean_contour_label(label):
    """
    Cleans a contour label:
    1. Converts all characters to lowercase.
    2. Removes leading and trailing spaces.
    3. Replaces special characters with spaces.
    4. Condenses consecutive spaces and special characters into a single space.
    5. Converts all spaces to underscores, except the trailing space if it exists.
    6. Capitalizes the first character after each space.
    
    Args:
    label (str): The input contour label.
    
    Returns:
    str: The cleaned contour label.
    """
    
    # Convert all characters to lowercase
    label = label.lower()
    
    # Remove leading and trailing spaces
    label = label.strip()
    
    # Replace special characters with spaces
    label = re.sub(r'[^\w\s]', ' ', label)
    
    # Condense consecutive spaces and special characters into a single space
    label = re.sub(r'[\s]+', ' ', label)
    
    # Check if there is a trailing space, and if so, remove it
    if label.endswith(' '):
        label = label[:-1]
    
    # Split the label into words and capitalize the first character of each word
    words = label.split(' ')
    words = [word.capitalize() for word in words]
    
    # Join the words with underscores
    label_ = '_'.join(words)
    label = capitalize_after_underscore(label_)
    
    
    return label
