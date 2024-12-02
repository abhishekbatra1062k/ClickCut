import random
import string

def generate_short_url():
    """Generate a random short URL."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))
