from fastapi import APIRouter

router = APIRouter(prefix="/health-check", tags=["Health Check Endpoint"])

@router.get("/")
def check_health():
    return {"message": "The API service is online"}