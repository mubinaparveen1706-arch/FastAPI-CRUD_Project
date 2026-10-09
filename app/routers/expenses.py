from typing import Annotated, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_db
from app.models import Expense, User
from app.schemas import Category, ExpenseCreate, ExpenseRead, ExpenseUpdate

router = APIRouter(prefix="/expenses", tags=["Expenses"])

CurrentUser = Annotated[User, Depends(get_current_user)]
DbSession = Annotated[Session, Depends(get_db)]


def get_owned_expense(db: Session, expense_id: int, user: User) -> Expense:
    """Return the expense only if it belongs to this user, otherwise 404."""
    expense = db.scalar(
        select(Expense).where(Expense.id == expense_id, Expense.user_id == user.id)
    )
    if expense is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Expense not found")
    return expense


# CREATE
@router.post("", response_model=ExpenseRead, status_code=status.HTTP_201_CREATED)
def create_expense(payload: ExpenseCreate, db: DbSession, user: CurrentUser):
    expense = Expense(**payload.model_dump(), user_id=user.id)
    db.add(expense)
    db.commit()
    db.refresh(expense)
    return expense


# READ MANY (with pagination)
@router.get("", response_model=List[ExpenseRead])
def list_expenses(
    db: DbSession,
    user: CurrentUser,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    category: Optional[Category] = None,
):
    query = select(Expense).where(Expense.user_id == user.id)
    if category is not None:
        query = query.where(Expense.category == category.value)
    query = query.order_by(Expense.expense_date.desc(), Expense.id.desc())
    query = query.offset(skip).limit(limit)
    return db.scalars(query).all()


# READ ONE
@router.get("/{expense_id}", response_model=ExpenseRead)
def get_expense(expense_id: int, db: DbSession, user: CurrentUser):
    return get_owned_expense(db, expense_id, user)


# UPDATE (full)
@router.put("/{expense_id}", response_model=ExpenseRead)
def replace_expense(
    expense_id: int, payload: ExpenseCreate, db: DbSession, user: CurrentUser
):
    expense = get_owned_expense(db, expense_id, user)
    for field, value in payload.model_dump().items():
        setattr(expense, field, value)
    db.commit()
    db.refresh(expense)
    return expense


# UPDATE (partial)
@router.patch("/{expense_id}", response_model=ExpenseRead)
def update_expense(
    expense_id: int, payload: ExpenseUpdate, db: DbSession, user: CurrentUser
):
    expense = get_owned_expense(db, expense_id, user)
    for field, value in payload.model_dump(exclude_unset=True).items():
        if value is None and field != "description":
            continue  # required columns can't be set to null
        setattr(expense, field, value)
    db.commit()
    db.refresh(expense)
    return expense


# DELETE
@router.delete("/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_expense(expense_id: int, db: DbSession, user: CurrentUser) -> None:
    expense = get_owned_expense(db, expense_id, user)
    db.delete(expense)
    db.commit()