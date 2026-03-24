"""agent-dispatcher: Concurrent task dispatcher for parallel agent execution."""

from .task import Task
from .result import DispatchResult
from .dispatcher import Dispatcher
from .decorators import dispatch_parallel

__all__ = ["Task", "DispatchResult", "Dispatcher", "dispatch_parallel"]
__version__ = "1.0.0"
