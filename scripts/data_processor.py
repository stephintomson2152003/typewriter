import sys
import json
import random
import string

# Function to clean up the sentence: remove punctuation and numbers, keep only letters and whitespace
def clean_sentence(sentence):
    allowed_characters = string.ascii_letters + ' '  # Only letters and spaces are allowed
    return ''.join(char for char in sentence if char in allowed_characters)

# Function to limit sentence to 10 words max
def limit_words(sentence, max_words=20):
    words = sentence.split()
    return ' '.join(words[:max_words])

# Function to get a random sentence from sentences.txt and limit it to 10 words
def get_random_sentence():
    try:
        with open('sentences.txt', 'r') as file:
            sentences = [line.strip() for line in file if line.strip()]
        clean_sentences = [clean_sentence(sentence) for sentence in sentences if clean_sentence(sentence)]
        if clean_sentences:
            result_sentence = random.choice(clean_sentences)
            limited_sentence = limit_words(result_sentence)  # Limit sentence to 10 words
            # print(f"Cleaned and Limited Sentence (for debugging): {limited_sentence}", file=sys.stderr)  # Debug output
            return limited_sentence
        else:
            return "No valid sentence found"
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)  # Print errors to stderr for debugging
        return str(e)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == 'get_sentence':
        # Get a random sentence from sentences.txt and limit it to 15 words
        random_sentence = get_random_sentence()
        print(json.dumps({"sentence": random_sentence}))  # JSON output for frontend
    else:
        # Process the provided data (reverse it or custom process)
        input_data = sys.argv[1]
        processed_data = input_data[::-1]  # Reversing input data as an example
        # print(f"Processed Data (for debugging): {processed_data}", file=sys.stderr)  # Debug output
        print(json.dumps({"result": processed_data}))  # JSON output
