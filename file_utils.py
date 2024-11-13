import re

def sanitize_filename(filename):
    """Sanitize a filename by removing unsupported characters and limiting its length."""
    # Replace spaces with underscores, remove special characters, and limit length
    return re.sub(r'[\\/*?:"<>|\n]', "", filename)[:100]  # Limit filename length for safety
