import hashlib

def hash_text(text: str, algorithm='sha256'):
    """Hashes a text using the specified algorithm.
    
    Args:
        text (str): The text to hash.
        algorithm (str): The hash algorithm to use (default is 'sha256').
    
    Returns:
        str: The resulting hash in hexadecimal format.
    """
    try:
        # Create a new hash object with the selected algorithm
        hash_func = hashlib.new(algorithm)
        # Encode the text to bytes and update the hash object
        hash_func.update(text.encode('utf-8'))
        # Return the hash in hexadecimal format
        return hash_func.hexdigest()
    except ValueError:
        raise ValueError(f"Unsupported hash algorithm: {algorithm}")

