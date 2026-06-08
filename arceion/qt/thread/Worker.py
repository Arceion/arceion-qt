from collections.abc import Callable
from uuid import uuid4

from PyQt6.QtCore import QObject, QRunnable, QTimer, pyqtSignal

from arceion.qt.logger import Logger

__all__ = ["Worker"]


class WorkerSignals(QObject):
    """
    Provides signals used by background worker threads in a PyQt application.

    This class defines custom PyQt signals to communicate the status and results
    of tasks executed within a PyQt worker thread. It extends QObject to enable
    signal-slot functionality, allowing client code to connect to these signals
    for handling task completion.

    Attributes:
        finished (pyqtSignal): Signal emitted when a task finishes execution,
            passing the result as an object or None.
    """

    finished = pyqtSignal(object)  # Emitted when the task finishes, passing the result or None


class Worker(QRunnable):
    def __init__(self, func: Callable, delay: float = 0):
        """
        Initializes a worker instance for executing a given function periodically with a
        specified delay. The worker is uniquely identified and is set up with necessary
        attributes to control execution and handle signals.

        Args:
            func (Callable): The function to be executed by the worker.
            delay (float): Delay between executions in seconds. Defaults to 0.
        """

        super().__init__()
        self.pk = uuid4()  # Unique identifier for this worker instance
        self._func = func
        self._delay = delay  # Delay between executions in seconds
        self._args = ()
        self._kwargs: dict = {}
        self.signals = WorkerSignals()
        self._isRunning = False
        self._timer = QTimer()  # Timer to manage periodic execution
        self._timer.setInterval(int(self._delay * 1000))  # Set interval in milliseconds
        self._timer.timeout.connect(self._run_once)

    def setData(self, *args, **kwargs):
        """
        Stores the positional and keyword arguments into instance attributes.

        Args:
            *args: Variable length positional arguments.
            **kwargs: Variable length keyword arguments.
        """

        self._args = args
        self._kwargs = kwargs

    def run(self):
        """
        Runs the core functionality of the instance, managing both single and periodic
        execution based on the configured delay.

        The method ensures the operation is not already running. If a delay greater
        than zero is configured, periodic execution begins, leveraging a timer.
        Otherwise, it executes the task immediately as a one-time operation.

        Raises:
            None

        Returns:
            None
        """

        if self._isRunning:
            return

        self._isRunning = True

        if self._delay > 0:
            # Start periodic execution
            self._timer.start()
        else:
            # Single execution without delay
            self._run_once()

    def _run_once(self):
        """
        Executes the assigned function and emits the result through a signal. If no delay is specified,
        the execution stops after a single invocation.
        """

        if not self._isRunning:
            return

        try:
            result = self._func(*self._args, **self._kwargs)
            self.signals.finished.emit(result)
        except Exception as e:  # noqa: BLE001
            Logger.error(f"Worker execution error: \n{e}")
            self.signals.finished.emit(None)

        if self._delay <= 0:  # Stop after one execution if no delay
            self.stop()

    def stop(self):
        """
        Stops the running worker process.

        This method ensures that the worker process is stopped by setting the internal
        state to indicate it is no longer running and stopping the associated timer.
        In case of an operational error during the stop process, it logs the relevant
        error for debugging.

        Raises:
            RuntimeError: If an error occurs while stopping the timer or handling the
            worker process.
        """

        try:
            if not self._isRunning:
                return

            self._isRunning = False
            self._timer.stop()  # Stop the timer
        except RuntimeError as e:
            Logger.error(f"Worker stop error: \n{e}")
