from fastapi import APIRouter, Depends

from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.user import UserResponse
from app.dependencies.roles import require_admin

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.get("/me", response_model=UserResponse)
def get_my_profile(
    current_user: User = Depends(get_current_user)
):
    return current_user

@router.get("/admin")
def admin_dashboard(
    current_user: User = Depends(require_admin)
):
    return {
        "message": "Welcome Admin",
        "username": current_user.username,
        "role": current_user.role
    }