import os
import uuid
from urllib.parse import urlparse


def get_filename_from_url(url):
    parsed_url = urlparse(url)
    return os.path.basename(parsed_url.path) if parsed_url.path else None


def generate_unique_filename():
    return f"{uuid.uuid4().hex}.tmp"
