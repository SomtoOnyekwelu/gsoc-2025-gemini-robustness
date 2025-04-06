# Implements character-level noise functions (substitute, delete, insert, swap) for text data augmentation.
# Specifically designed to evaluate model robustness, supporting multiple languages (English, Hindi, Igbo).
# Intended as *proof-of-concept* code for GSoC 2025 Proposal, demonstrating core mechanisms.

import random
import string # For easier definition of English character set

# --- Constants and Configuration ---

# Noise Level mapping to the approximate percentage of original characters targeted for modification.
# --- Justification for Chosen Levels (5%, 15%, 25%) ---
# These levels were chosen to balance several factors:
# 1. Observable Impact: Ensure noise levels are significant enough to likely induce measurable performance degradation
#    even in powerful models like Gemini, providing insightful results beyond negligible noise scenarios.
# 2. Realistic Simulation: While 'High' (25%) represents severe degradation, it remains potentially representative
#    of challenging real-world conditions (e.g., poor OCR + typos) without reaching levels (e.g., 40%+)
#    that might render input semantically meaningless or statistically uninformative (floor effects).
# 3. Gradation: Provide distinct steps ('Low' -> 'Medium' -> 'High') to observe how performance scales with noise intensity.
# 4. Comparability: Align broadly with noise levels explored in robustness literature (often ranging up to ~25-30%).
# The primary goal is to facilitate meaningful comparisons of robustness *across languages and noise types*.
NOISE_LEVEL_PERCENTAGES = {
    "low": 0.05,    # ~5% modification attempts - Represents subtle but potentially noticeable noise (e.g., occasional typos).
    "medium": 0.15, # ~15% modification attempts - Represents challenging noise levels, likely impacting readability/interpretation.
    "high": 0.25     # ~25% modification attempts - Represents severe noise, expected to significantly degrade performance.
}

# --- Language Alphabets (Simplified for Proof-of-Concept) ---
# WARNING: These are *highly simplified* representations, especially for Hindi and Igbo.
# A full GSoC project would require more linguistically accurate handling
# (e.g., Unicode properties, segmentation libraries, proper handling of digraphs/matras).
# This PoC focuses on demonstrating the noise *application mechanism*.

ALPHABETS = {
    "english": string.ascii_letters + string.digits + string.punctuation + " ",
    # --- HINDI (Devanagari) ---
    # Simplified: Basic consonants and vowels. Ignores matras, conjuncts, virama etc.
    # Limitation: Random insertion/substitution might produce invalid sequences.
    "hindi": "अआइईउऊएऐओऔकखगघचछजझटठडढतथदधनपफबभमयरलवशषसह" + ".,!?' ", # Added basic punctuation
    # --- IGBO (Latin Extended) ---
    # Simplified: Includes base Latin + specific Igbo characters.
    # Limitation: Digraphs (ch, gb, kp, sh etc.) are treated as single chars in alphabet *source*
    # but the noise operates on single Unicode points in the text. Igbo *text* input is handled correctly.
    # Insert/Substitute source intentionally uses single chars including dotted letters but omits digraphs for PoC simplicity.
    "igbo": "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 .,!?'" + "ịỊọỌụỤṅṄ" # Includes dotted, excludes digraph source chars for now
}
# Ensure space is included as a potential substitute/insert character

# --- Main Orchestrator Function ---

def add_char_noise(text: str, noise_level: str, language: str) -> str:
    """
    Applies character-level noise (substitute, delete, insert, swap adjacent)
    to a specified percentage of the original characters in the input text.

    Args:
        text (str): The input string.
        noise_level (str): The intensity level ("low", "medium", "high").
        language (str): The language identifier ("english", "hindi", "igbo").
                        Used to select the appropriate alphabet for insertions/substitutions.
                        Case-insensitive.

    Returns:
        str: The text with character noise applied.

    Raises:
        ValueError: If noise_level or language is invalid, or if the alphabet is missing/empty.
        TypeError: If text is not a string.

    Methodology:
    1. Determines the percentage of characters to target based on noise_level.
    2. Selects unique character indices from the *original* text to modify.
    3. Randomly assigns a noise operation (substitute, delete, insert, swap) to each selected index.
    4. Builds a *new* list of characters by iterating through the original text:
       - If an index is marked for modification, the planned operation is performed.
       - Swap operation handles adjacent characters correctly.
       - Indices affected by swaps are tracked to avoid double processing.
    5. Joins the new list of characters to form the final noisy string.
    """
    if not isinstance(text, str):
        raise TypeError("Input 'text' must be a string.")

    original_text_len = len(text)
    if original_text_len == 0:
        return "" # Return empty if input is empty

    # --- Validate Inputs ---
    noise_level = noise_level.lower()
    if noise_level not in NOISE_LEVEL_PERCENTAGES:
        raise ValueError(f"Invalid noise_level '{noise_level}'. Choose from {list(NOISE_LEVEL_PERCENTAGES.keys())}.")
    percentage = NOISE_LEVEL_PERCENTAGES[noise_level]

    language = language.lower()
    if language not in ALPHABETS:
        # Provide guidance for future extension
        raise ValueError(f"Unsupported language '{language}'. Supported: {list(ALPHABETS.keys())}. Add new alphabets to the ALPHABETS dict for extension.")
    alphabet = ALPHABETS[language]
    if not alphabet:
         raise ValueError(f"Alphabet for language '{language}' is empty or missing.")

    # --- Calculate Modifications ---
    num_chars_to_modify = int(percentage * original_text_len)
    if num_chars_to_modify == 0:
        # Important edge case: If percentage is too low or text too short
        # print(f"Warning: noise_count is 0 for text length {original_text_len} and level '{noise_level}'. Returning original text.")
        return text

    # Select unique original indices to target for modification
    indices_to_modify = sorted(random.sample(range(original_text_len), num_chars_to_modify))

    # Assign a random operation to each selected index
    operations = ['substitute', 'delete', 'insert', 'swap']
    modifications = {} # Dictionary: {index: operation}
    for idx in indices_to_modify:
        modifications[idx] = random.choice(operations)

    # --- Apply Modifications (Build New List Approach) ---
    new_text_list = []
    processed_indices = set() # Track indices handled by swap

    i = 0
    while i < original_text_len:
        if i in processed_indices:
            i += 1
            continue # Skip index if it was already handled (e.g., by a swap initiated at i-1)

        operation = modifications.get(i) # Get planned operation for current index

        if operation is None:
            # No modification planned for this index
            new_text_list.append(text[i])
            i += 1
        else:
            # Apply the planned modification
            try: # Added try-except for safety during complex ops like swap
                if operation == 'delete':
                    # Simply skip appending the character
                    pass
                    i += 1

                elif operation == 'substitute':
                    original_char = text[i]
                    # Select a random char from alphabet, try ensuring it's different
                    new_char = random.choice(alphabet)
                    attempts = 0 # Avoid infinite loop if alphabet has only 1 char
                    while new_char == original_char and len(alphabet) > 1 and attempts < 5:
                        new_char = random.choice(alphabet)
                        attempts += 1
                    new_text_list.append(new_char)
                    i += 1

                elif operation == 'insert':
                    # Insert a random character BEFORE the current original character
                    random_char = random.choice(alphabet)
                    new_text_list.append(random_char)
                    new_text_list.append(text[i]) # Append original character after insertion
                    i += 1

                elif operation == 'swap':
                    # Swap character at 'i' with character at 'i+1'
                    if i + 1 < original_text_len: # Check if there is a next character
                        # Decide how to handle if i+1 *also* has a modification planned.
                        # Simplest: Swap overrides other ops at i+1 for this turn.
                        new_text_list.append(text[i+1]) # Append char from i+1
                        new_text_list.append(text[i])   # Append char from i
                        processed_indices.add(i + 1)    # Mark i+1 as handled
                        i += 2 # Increment counter by 2 because we processed two characters
                    else:
                        # Cannot swap last character with next, fallback: just append original
                        # Could alternatively perform substitution here? Design choice. Keep simple now.
                        new_text_list.append(text[i])
                        i += 1
            except Exception as e:
                # Log error and skip modification for this index if something unexpected happens
                print(f"Warning: Error applying noise operation '{operation}' at index {i}. Error: {e}. Skipping.")
                if not i in processed_indices: # Ensure original character added if op failed mid-way
                    new_text_list.append(text[i])
                i += 1 # Move to next character even if op failed


    return "".join(new_text_list)

# --- Example Usage (PoC Demonstration) ---
if __name__ == "__main__":
    print("Running Character Noise Functions Example...")
    print("NOTE: Alphabets for Hindi/Igbo are simplified for this PoC.")
    print("---------------------------------------------------------")

    random.seed(42) # Use a fixed seed for reproducible demo output

    # For English
    english_sample_text = "A typical English question about the image content?"
    print(f"\nEnglish Reference text ({len(english_sample_text)} chars): {english_sample_text}")
    print("--- English text with noise ---")
    print(f"Low noise:    {add_char_noise(english_sample_text, 'Low', 'English')}")
    print(f"Medium noise: {add_char_noise(english_sample_text, 'Medium', 'English')}")
    print(f"High noise:   {add_char_noise(english_sample_text, 'High', 'English')}")

    # For Hindi (Devanagari Script)
    # Source: "यह छवि में क्या है?" (What is in this image?)
    hindi_sample_text = "यह छवि में क्या है?"
    print(f"\nHindi Reference text ({len(hindi_sample_text)} chars):   {hindi_sample_text}")
    print("--- Hindi text with noise (Simplified Alphabet) ---")
    print(f"Low noise:    {add_char_noise(hindi_sample_text, 'Low', 'Hindi')}")
    print(f"Medium noise: {add_char_noise(hindi_sample_text, 'Medium', 'Hindi')}")
    print(f"High noise:   {add_char_noise(hindi_sample_text, 'High', 'Hindi')}")

    # For Igbo (Latin Script with extensions)
    # Source: "Gịnị bụ ihe di n' foto a?" (What is in this photo?)
    igbo_sample_text = "Gịnị bụ ihe di n' foto a?"
    print(f"\nIgbo Reference text ({len(igbo_sample_text)} chars):    {igbo_sample_text}")
    print("--- Igbo text with noise (Simplified Alphabet Source) ---")
    print(f"Low noise:    {add_char_noise(igbo_sample_text, 'Low', 'Igbo')}")
    print(f"Medium noise: {add_char_noise(igbo_sample_text, 'Medium', 'Igbo')}")
    print(f"High noise:   {add_char_noise(igbo_sample_text, 'High', 'Igbo')}")

    print("\n---------------------------------------------------------")
    print("Example Finished.")