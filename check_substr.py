from difflib import SequenceMatcher

def is_90_percent_match(substring, main_string):
    substring_length = len(substring)
    for i in range(len(main_string) - substring_length + 1):
        part = main_string[i:i + substring_length]
        similarity = SequenceMatcher(None, substring, part).ratio()
        if similarity >= 0.9:  # 90% match
            return True, part, similarity
    return False, None, 0

# Example Usage
main_string = "Hello, this is a sample string for testing."
substring = "smple"

result, matched_part, similarity = is_90_percent_match(substring, main_string)
if result:
    print(f"The substring '{substring}' matches '{matched_part}' with {similarity * 100:.2f}% similarity.")
else:
    print(f"No match found for '{substring}' with at least 90% similarity.")
