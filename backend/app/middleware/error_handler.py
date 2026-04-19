import logging
from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger(__name__)


class ErrorHandlerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            return await call_next(request)
        except ValueError as e:
            logger.error(f'ValueError: {str(e)}', exc_info=True)
            return JSONResponse(
                status_code=400,
                content={'detail': str(e), 'type': 'ValueError'},
            )
        except KeyError as e:
            logger.error(f'KeyError: {str(e)}', exc_info=True)
            return JSONResponse(
                status_code=400,
                content={'detail': f'Missing field: {str(e)}', 'type': 'KeyError'},
            )
        except Exception as e:
            logger.error(f'Unhandled exception: {str(e)}', exc_info=True)
            return JSONResponse(
                status_code=500,
                content={
                    'detail': 'Internal server error',
                    'type': type(e).__name__,
                    'message': str(e) if str(e) else 'Unknown error',
                },
            )


def add_error_handler(app):
    """Add error handler to FastAPI app"""
    app.add_middleware(ErrorHandlerMiddleware)
