#!/usr/bin/env python3
"""Module to implement an expiring web cache and access counter using Redis."""

import redis
import requests
from typing import Callable
from functools import wraps

# Connect to Redis
r = redis.Redis()


def count_url_access(method: Callable) -> Callable:
    """Decorator to count how many times a URL is accessed."""
    @wraps(method)
    def wrapper(url: str) -> str:
        count_key = f"count:{url}"
        r.incr(count_key)
        return method(url)
    return wrapper


@count_url_access
def get_page(url: str) -> str:
    """
    Retrieve the HTML content of a URL, caching it in Redis for 10 seconds.

    Args:
        url: The URL to fetch.

    Returns:
        HTML content of the page.
    """
    cache_key = f"cached:{url}"
    cached = r.get(cache_key)

    if cached:
        return cached.decode('utf-8')

    # Not cached: fetch from the web
    response = requests.get(url)
    html = response.text

    # Cache it for 10 seconds
    r.setex(cache_key, 10, html)
    return html
