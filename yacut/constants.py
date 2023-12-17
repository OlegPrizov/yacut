import string
import re

PATTERN = r'^[A-Za-z0-9]+$'
MAX_ORIGINAL_LINK_LENGTH = 256
MAX_CUSTOM_LINK_LENGTH = 16
MAX_AUTOGENERATE_CUSTOM_LINK_LENGTH = 6
ALLOWED_SYMBOLS = string.ascii_letters + string.digits
