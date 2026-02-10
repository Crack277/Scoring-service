from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.loan.schemas import LoanCreate
from src.models import Loan, db_helper


async def create_loan(
    loan_create: LoanCreate,
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> Loan:
    loan = Loan(
        client_id=loan_create.client_id,
        amount=loan_create.amount,
        loan_data=loan_create.loan_data,
        is_closed=loan_create.is_closed,
    )
    session.add(loan)
    await session.commit()
    return loan
