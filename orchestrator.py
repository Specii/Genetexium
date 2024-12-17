import time
import random
import asyncio
from typing import Callable, List, Union, Any


class FunctionOrchestrator:
    def __init__(self, driver):
        self.driver = driver

    def __retry(
            self,
            func: Callable,
            *args,
            retries: int = 3,
            delay: float = 0,
            refresh: bool = False,
            **kwargs
    ) -> Any:
        """
        Retry the given function on failure

        Args:
            func: The function to be retried
            *args: Positional arguments for the function
            retries: Number of retry attempts (default is 3)
            delay: Delay between retries (default is 0 seconds)
            refresh: Whether to refresh the page before retrying (default is False)
            **kwargs: Keyword arguments for the function

        Returns:
            The result of the function if successful

        Raises:
            Exception: The last exception raised if all retries fail
        """
        last_exception = None
        for attempt in range(retries):
            try:
                if refresh and attempt > 0:
                    self.driver.refresh()
                return func(*args, **kwargs)
            except Exception as e:
                last_exception = e
                time.sleep(delay)
        raise last_exception

    async def __retry_async(
            self,
            func: Callable,
            *args,
            retries: int = 3,
            delay: float = 0,
            refresh: bool = False,
            **kwargs
    ) -> Any:
        """
        Async version of __retry.
        """
        last_exception = None
        for attempt in range(retries):
            try:
                if refresh and attempt > 0:
                    await self.driver.refresh()
                return await func(*args, **kwargs)
            except Exception as e:
                last_exception = e
                await asyncio.sleep(delay)
        raise last_exception

    async def initialize(
            self,
            functions: Union[Callable, List[Callable]],
            shuffle: bool = False,
            require_success: bool = False,
            retries: int = 0,
            delay: float = 0,
            refresh: bool = False,
            *args,
            **kwargs
    ) -> Union[dict, List[dict]]:
        """
        Initialize and execute the given function(s).

        Args:
            functions: A single function or a list of functions to be executed
            shuffle: Whether to randomize the execution order of functions (default is False, only applicable for lists)
            require_success: If True, stop execution if any function fails (default is False)
            retries: Number of retry attempts for each function (default is 3)
            delay: Delay between retries (default is 0 seconds)
            refresh: Whether to refresh the page before retrying (default is False)
            *args: Positional arguments for the functions
            **kwargs: Keyword arguments for the functions

        Returns:
            A dictionary (for a single function) or a list of dictionaries (for multiple functions),
            containing function results and their identifiers.
        """
        if callable(functions):
            functions = [functions]
            single_function_mode = True
        else:
            single_function_mode = False

        results = []
        original_order = {id(func): func.__name__ for func in functions}

        if shuffle and not single_function_mode:
            random.shuffle(functions)

        for func in functions:
            func_name = func.__name__
            try:
                if asyncio.iscoroutinefunction(func):
                    result = await self.__retry_async(
                        func,
                        *args,
                        retries=retries,
                        delay=delay,
                        refresh=refresh,
                        **kwargs
                    )
                else:
                    result = await self.__retry(
                        func,
                        *args,
                        retries=retries,
                        delay=delay,
                        refresh=refresh,
                        **kwargs
                    )

                results.append({'function': func_name, 'result': result})

                if require_success and not result:
                    break

            except Exception as e:
                results.append({'function': func_name, 'result': None, 'error': str(e)})
                if require_success:
                    break

        if shuffle and not single_function_mode:
            results = sorted(results, key=lambda x: list(original_order.values()).index(x['function']))

        return results[0] if single_function_mode else results
