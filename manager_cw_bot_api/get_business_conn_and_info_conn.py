"""
Module of FIND OUT BUSINESS DATA (connection).
"""
import requests

"""
1. The resulting string (ex.: {'ok': True / False, 'result': ...}:
...

2. Find the business_connection section:
...

3. Fill in the fields in bot.json.
"""


def gets(token="YOUR_TOKEN") -> dict:
    """
    Get Business Data in first time.

    :return: dict.
    """
    url = "https://api.telegram.org/bot" + token + "/getUpdates"
    response = requests.get(url).json()
    return response

print(gets())