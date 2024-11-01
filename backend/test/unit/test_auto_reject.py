import pytest
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from unittest.mock import MagicMock

from controllers.requests_controller import auto_reject_pending_requests