import hashlib
from datetime import datetime, timedelta

from fastapi import Request
from fastapi.responses import Response
from starlette.middleware.base import BaseHTTPMiddleware


class CacheMiddleware(BaseHTTPMiddleware):
    """
    Simple in-process GET cache with 5-minute TTL.
    Does not cache endpoints that return binary (PDF) responses.
    """

    CACHE_TTL = 300  # seconds
    SKIP_PATHS = {'/api/reports'}  # never cache binary downloads

    def __init__(self, app):
        super().__init__(app)
        self._store: dict = {}

    def _key(self, request: Request) -> str:
        raw = f'{request.method}:{request.url.path}?{request.url.query}'
        return hashlib.md5(raw.encode()).hexdigest()

    def _should_skip(self, request: Request) -> bool:
        if request.method != 'GET':
            return True
        return any(request.url.path.startswith(p) for p in self.SKIP_PATHS)

    async def dispatch(self, request: Request, call_next):
        if self._should_skip(request):
            return await call_next(request)

        key = self._key(request)
        cached = self._store.get(key)

        if cached and datetime.utcnow() < cached['expires']:
            return Response(
                content=cached['content'],
                status_code=cached['status_code'],
                media_type=cached['media_type'],
            )

        response = await call_next(request)

        if response.status_code == 200:
            body = b''.join([chunk async for chunk in response.body_iterator])
            self._store[key] = {
                'content': body,
                'status_code': response.status_code,
                'media_type': response.media_type,
                'expires': datetime.utcnow() + timedelta(seconds=self.CACHE_TTL),
            }
            return Response(content=body, status_code=response.status_code, media_type=response.media_type)

        return response
