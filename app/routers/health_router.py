from fastapi import APIRouter
import time

router = APIRouter(prefix="/health", tags=["Health"])

@router.get("/")
def api_health():

    start = time.time()

    # simulate backend check
    backend_status = "online"

    # simulate database check
    database_status = "connected"

    response_time = round((time.time() - start) * 1000, 2)

    return {
        "backend": backend_status,
        "database": database_status,
        "response_time": response_time
    }