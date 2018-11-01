"""ccp_api - Cloud Commerce Pro API integration for Python."""

from .credentials import Credentials  # NOQA
from .endpoint import Endpoint  # NOQA

from .endpoints import products  # NOQA

from .__version__ import __title__, __description__, __url__  # NOQA
from .__version__ import __version__, __author__, __author_email__  # NOQA
from .__version__ import __copyright__, __license__, __release__  # NOQA

login = Credentials()
