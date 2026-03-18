# Central place for rate limiting (avoids circular imports)

from slowapi import Limiter
from slowapi.util import get_remote_address

# Create limiter instance
limiter = Limiter(key_func=get_remote_address)