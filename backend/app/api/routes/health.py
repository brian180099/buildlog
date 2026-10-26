from datetime import UTC, datetime

from fastapi import APIRouter

from app.core.config import get_settings

router = APIRouter(tags=["health"])


@router.get("/health")
def health_check() -> dict[str, object]:
    settings = get_settings()
    return {
        "data": {
            "status": "ok",
            "service": settings.app_name,
            "environment": settings.environment,
            "timestamp": datetime.now(UTC).isoformat(),
        }
    }

