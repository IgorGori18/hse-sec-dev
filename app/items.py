from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.db import get_db
from app.models import Item, User
from app.schemas import ItemCreate, ItemOut, ItemUpdate

router = APIRouter(prefix="/api/v1/items", tags=["items"])


def check_access(item: Item, user: User):
    if item.owner_id != user.id and user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "code": "FORBIDDEN",
                "message": "access denied",
                "details": {},
            },
        )


@router.post("", response_model=ItemOut, status_code=201)
def create_item(
    data: ItemCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    item = Item(title=data.title, owner_id=user.id)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.get("/{item_id}", response_model=ItemOut)
def get_item(
    item_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    item = db.query(Item).get(item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "code": "NOT_FOUND",
                "message": "item not found",
                "details": {},
            },
        )
    check_access(item, user)
    return item


@router.get("", response_model=List[ItemOut])
def list_items(
    limit: int = 10,
    offset: int = 0,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    q = db.query(Item)
    if user.role != "admin":
        q = q.filter(Item.owner_id == user.id)
    items = q.offset(offset).limit(limit).all()
    return items


@router.patch("/{item_id}", response_model=ItemOut)
def update_item(
    item_id: int,
    data: ItemUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    item = db.query(Item).get(item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "code": "NOT_FOUND",
                "message": "item not found",
                "details": {},
            },
        )
    check_access(item, user)
    item.title = data.title
    db.commit()
    db.refresh(item)
    return item


@router.delete("/{item_id}")
def delete_item(
    item_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    item = db.query(Item).get(item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "code": "NOT_FOUND",
                "message": "item not found",
                "details": {},
            },
        )
    check_access(item, user)
    db.delete(item)
    db.commit()
    return {"code": "OK", "message": "deleted", "details": {}}
