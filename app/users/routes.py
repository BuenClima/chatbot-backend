from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.guards import get_current_user
from app.users import crud, schemas

# Create a router for user-related routes
router = APIRouter()


# Route for getting a user by ID
@router.get(
    "/",
    response_model=schemas.UserRepr,
    summary="Get Current User Information",
    description="Retrieve the details of the current user.",
)
def read_current_user(
    current_user: schemas.User = Depends(get_current_user),
) -> schemas.UserRepr:
    """Retrieve the details of a user by their ID.

    - **user_id**: The unique ID of the user you want to retrieve.
    """
    return schemas.UserRepr(
        id=current_user.id, email=current_user.email, is_active=current_user.is_active
    )


# Route for updating a user by ID
@router.put(
    "/",
    response_model=schemas.UserRepr,
    summary="Update Current User",
    description="Update current user details.",
)
def update_current_user(
    user_update: schemas.UserUpdate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user),
) -> schemas.UserRepr:
    """Update the details of a user by their ID.

    - **user_id**: The unique ID of the user you want to update.
    - **user_update**: The new details of the user.
    """
    updated_user: schemas.User = crud.update_user(
        db=db, user_id=current_user.id, user=user_update
    )

    return schemas.UserRepr(
        id=updated_user.id, email=updated_user.email, is_active=updated_user.is_active
    )


# Route for deleting a user by ID
@router.delete(
    "/",
    summary="Delete Current User",
    description="Delete the current user.",
    responses={204: {}, 404: {"description": "User not found"}},
    status_code=204,
)
def delete_current_user(
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user),
) -> Response:
    """Delete a user by their ID.

    - **user_id**: The unique ID of the user you want to delete.
    """
    crud.delete_user(db=db, user_id=current_user.id)

    return Response(status_code=204)
