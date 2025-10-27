from django.utils.timezone import now
from rest_framework.response import Response
from rest_framework.views import exception_handler as drf_exception_handler


def custom_exception_handler(exc, context):
    resp = drf_exception_handler(exc, context)
    if resp is not None:
        return Response(
            {
                "error": {
                    "type": exc.__class__.__name__,
                    "detail": resp.data,
                    "status": resp.status_code,
                    "path": context["request"].path,
                    "timestamp": now().isoformat(),
                }
            },
            status=resp.status_code,
        )
    return None
