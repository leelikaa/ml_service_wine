from database.database import get_session, init_db
from services.User_Services import get_all_users, create_user
from services.Transaction_Services import get_all_transactions, top_up
from model.users import Users


if __name__ == "__main__":
    test_user_1 = Users(email='test1@mail.ru', password='test1')
    test_user_2 = Users(email='test2@mail.ru', password='test2')

    init_db()
    print('Init db has been success')

    session = get_session()
    create_user(test_user_1, session)
    create_user(test_user_2, session)
    print(get_all_users(session))

    for user in get_all_users(session):
        print(f'id: {user.user_id} - {user.email}')

    top_up(1, 10.0, session)
    top_up(2, 15.0, session)
    print(get_all_transactions(session))
