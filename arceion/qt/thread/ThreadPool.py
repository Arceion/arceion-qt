from collections.abc import Callable
from typing import ClassVar, Self

from PyQt6.QtCore import QThreadPool

from arceion.qt.logger import Logger

from .Worker import Worker

__all__ = ['ThreadPool']


class ThreadPoolManager:
    _instance: Self | None = None
    threadPool: QThreadPool = QThreadPool()
    _tasks: ClassVar[dict[int, Worker]] = {}  # Use id(func) as key

    @classmethod
    def getInstance(cls) -> Self:
        """
        Returns the singleton instance of the class, ensuring a single instance is
        created across the application lifecycle.

        This method implements the Singleton design pattern by returning the single
        instance of the class. If an instance does not already exist, it creates one.
        Subsequent calls to this method will return the same instance.

        Returns:
            Self: The singleton instance of the class.
        """

        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        """
        Initializes a ThreadPool singleton instance.

        Raises:
            Exception: If an attempt is made to directly instantiate the class when an
                instance already exists. Use `getInstance()` to access the existing
                ThreadPool instance.
        """

        if ThreadPool._instance is not None:
            raise Exception("Use getInstance() to access the ThreadPool instance.")
        ThreadPool._instance = self

    def add(self, func: Callable, delay: float = 0):
        """
        Adds a function to the task queue for execution.

        This method schedules a specified function for delayed execution. If a
        function has already been added, it will not be re-added to the queue.

        Args:
            func (Callable): The function to be scheduled for execution.
            delay (float): The delay (in seconds) before the function is executed.
                Default is 0.
        """

        func_id = id(func)
        if func_id in self._tasks:
            return
        runnable = Worker(func, delay)
        self._tasks[func_id] = runnable

    def start(
        self,
        func: Callable,
        *args,
        delay: float = 0,
        callback: Callable | None = None,
        retry: bool = True,
        **kwargs,
    ):
        """
        Starts a task in the thread pool by scheduling the specified function with
        optional arguments, delay, and callback. If an error occurs while adding the
        task, retries once if allowed.

        Args:
            func (Callable): The function to be executed in the thread pool.
            *args: Positional arguments to be passed to the function.
            delay (float, optional): A delay in seconds before the task starts. Defaults to 0.
            callback (Optional[Callable], optional): A callable to be invoked after
                the task is completed. Defaults to None.
            retry (bool, optional): If True, retries once in case of a RuntimeError.
                Defaults to True.
            **kwargs: Additional keyword arguments to be passed to the function.
        """

        func_id = id(func)
        try:
            self.add(func, delay)
            worker = self._tasks[func_id]
            worker.setData(*args, **kwargs)
            if callback:
                try:
                    worker.signals.finished.disconnect()
                except TypeError:
                    pass
                worker.signals.finished.connect(callback)
            self.threadPool.start(worker)
        except RuntimeError as e:
            Logger.error(f"RuntimeError in ThreadPool.start: {e}")
            self._tasks.pop(func_id, None)
            if retry:
                self.start(func, *args, delay=delay, callback=callback, retry=False, **kwargs)

    def stop(self, func: Callable):
        """
        Stops the execution of a specified task.

        This method halts the execution of a task identified by the function
        provided. It ensures that the task associated with the given function
        is properly stopped if it exists in the internal task registry.

        Args:
            func (Callable): The function whose associated task needs to be stopped.

        """

        func_id = id(func)
        if func_id in self._tasks:
            runnable = self._tasks.pop(func_id, None)
            if runnable:
                runnable.stop()

    def stopAll(self):
        """
        Stops and cancels all currently running tasks in the thread pool.

        This method iterates through the list of active tasks, stops each task, and removes it
        from the task collection. If the thread pool supports cancellation, it also cancels
        the associated runnable task.

        Raises:
            RuntimeError: If a runtime error occurs during the stop or cancellation process.
        """

        try:
            for func_id, runnable in list(self._tasks.items()):
                runnable.stop()
                if hasattr(self.threadPool, 'cancel'):
                    self.threadPool.cancel(runnable)
                del self._tasks[func_id]
        except RuntimeError as e:
            Logger.error(f"Error in ThreadPool.stopAll: {e}")

    def clearAll(self):
        """
        Clears all threads in the thread pool and halts their execution.

        This method attempts to stop all active threads, followed by clearing the
        thread pool. If a runtime error occurs during this process, it logs the
        error message for debugging purposes.

        Raises:
            RuntimeError: If an error occurs while stopping threads or clearing
            the thread pool.
        """
        try:
            self.stopAll()
            self.threadPool.clear()
        except RuntimeError as e:
            Logger.error(f"Error in ThreadPool.clearAll: {e}")


ThreadPool = ThreadPoolManager.getInstance()
