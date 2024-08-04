from database.database import get_session, init_db
from services.User_Services import get_all_users, create_user
from services.Transaction_Services import get_all_transactions, top_up
from services.Prediction_Services import get_all_predictions, create_prediction, prediction
from model.users import Users
from model.prediction import Prediction
from datetime import datetime


if __name__ == "__main__":
    test_user_1 = Users(email='test1@mail.ru', password='test1')
    test_user_2 = Users(email='test2@mail.ru', password='test2')

    init_db()
    print('Init db has been success')

    session = get_session()
    create_user(test_user_1, session)
    create_user(test_user_2, session)

    for user in get_all_users(session):
        print(f'id: {user.user_id} - {user.email}')

    top_up(1, 10.0, session)
    top_up(2, 15.0, session)

    for transaction in get_all_transactions(session):
        print(f'transaction id: {transaction.transaction_id}, user id: {transaction.user_id}, time: {transaction.time}, money: {transaction.money}')

    wine_params = {
        'fixed_acidity': 7.4,
        'volatile_acidity': 0.7,
        'citric_acid': 0.0,
        'residual_sugar': 1.9,
        'chlorides': 0.076,
        'free_sulfur_dioxide': 11,
        'total_sulfur_dioxide': 34,
        'density': 0.9978,
        'pH': 3.51,
        'sulphates': 0.56,
        'alcohol': 9.4
    }

    new_prediction = Prediction(
        user_id=1,
        time=datetime.now(),
        fixed_acidity=wine_params['fixed_acidity'],
        volatile_acidity=wine_params['volatile_acidity'],
        citric_acid=wine_params['citric_acid'],
        residual_sugar=wine_params['residual_sugar'],
        chlorides=wine_params['chlorides'],
        free_sulfur_dioxide=wine_params['free_sulfur_dioxide'],
        total_sulfur_dioxide=wine_params['total_sulfur_dioxide'],
        density=wine_params['density'],
        pH=wine_params['pH'],
        sulphates=wine_params['sulphates'],
        alcohol=wine_params['alcohol']
    )

    result = prediction(new_prediction)
    new_prediction.result = result

    print(create_prediction(new_prediction, session))

    for prediction in get_all_predictions(session):
        print(f'prediction id: {prediction.prediction_id}, user id: {prediction.user_id}, time: {prediction.time}, result:{prediction.result}')
