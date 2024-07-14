from model.transaction import Transaction
from services.User_Services import get_user_by_id
from typing import List
from datetime import datetime


def get_all_transactions(session) -> List[Transaction]:
    return session.query(Transaction).all()


def get_transaction_by_id(transaction_id: int, session) -> List[Transaction]:
    transactions = session.get(Transaction, transaction_id)
    return transactions


def get_transaction_by_user(user_id: int, session) -> List[Transaction]:
    transactions = session.query(Transaction).filter(Transaction.user_id == user_id)
    return transactions


def create_transaction(new_transaction: Transaction, session) -> None:
    session.add(new_transaction)
    session.commit()
    session.refresh(new_transaction)


def top_up(user_id: int, money: float, session):
    user = get_user_by_id(user_id, session)
    user.balance += money
    session.commit()
    transaction = Transaction(user_id=user_id, time=datetime.now(), money=money, type_="top-up")
    create_transaction(transaction, session)
    return {f'User {user.email} new balance: {user.balance}'}


def decrease(user_id: int, money: float, session):
    user = get_user_by_id(user_id, session)
    user.balance -= money
    session.commit()
    transaction = Transaction(user_id=user_id, time=datetime.now(), money=money, type_="decrease")
    create_transaction(transaction, session)
    return {f'User {user.email} new balance: {user.balance}'}
