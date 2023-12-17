def cleanup_text(text):
	return "".join([c if ord(c) < 128 else "" for c in text]).strip()