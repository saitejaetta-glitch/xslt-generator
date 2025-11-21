def summarize_text(text, max_length=1500):
    """Summarize or truncate long spec text for use in prompts"""
    return text[:max_length] + '...' if len(text) > max_length else text
