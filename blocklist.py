"""

blocklist.py

This file just contains a blocklist of the JWT tokens.
It will be imported by the app and the logout resources
so that tokens can be added to the blocklist when the user logs out.

"""


BLOCKLIST = set()
