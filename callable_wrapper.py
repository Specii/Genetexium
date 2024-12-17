import asyncio


class CallableWrapper:
    def __init__(self, func, name=None, **kwargs):
        self.func = func
        self.name = name or func.__name__
        self.kwargs = kwargs

    async def __call__(self, *args, **kwargs):
        if asyncio.iscoroutinefunction(self.func):
            return await self.func(*args, **self.kwargs, **kwargs)
        return self.func(*args, **self.kwargs, **kwargs)
