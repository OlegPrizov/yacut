import string
import re

ALLOWED_SYMBOLS = string.ascii_letters + string.digits
SHORT_PATTERN = re.compile(f"^[{re.escape(ALLOWED_SYMBOLS)}]*$")
MAX_ORIGINAL_LINK_LENGTH = 2048
MAX_SHORT_LENGTH = 16
MAX_AUTOGENERATE_SHORT_LENGTH = 6
MAX_ITERATIONS = 10
