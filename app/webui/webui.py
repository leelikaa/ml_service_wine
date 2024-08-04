import streamlit as st
import requests
from requests.exceptions import HTTPError

API_BASE_URL = "http://app:8080"


def authenticate(username, password):
    response = requests.post(f"{API_BASE_URL}/user/signin", data={"username": username, "password": password})
    if response.status_code == 200:
        return response.json()['access_token']
    else:
        st.error("Authentication failed. Please check your credentials.")
        return None


def register_user(username, password):
    user_data = {
        "email": username,
        "password": password
    }
    try:
        response = requests.post(f"{API_BASE_URL}/user/signup", json=user_data)
        response.raise_for_status()
        response_json = response.json()
        st.success(response_json.get("message", "User created successfully!"))
    except requests.exceptions.HTTPError as e:
        st.error(f"Failed to create user: {e.response.json().get('detail', str(e))}")
    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred: {e}")


def check_balance(user_id, token):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(f"{API_BASE_URL}/user{user_id}/balance", headers=headers)
    if response.status_code == 200:
        return response.json()['balance']
    else:
        st.error("Failed to retrieve balance.")
        return None


def top_up(user_id, amount, token):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(f"{API_BASE_URL}/user{user_id}/topup", params={"money": amount}, headers=headers)
    if response.status_code == 200:
        st.success("Top-up successful!")
    else:
        st.error("Failed to top up.")


def make_prediction(user_id, wine_description, token):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(f"{API_BASE_URL}/prediction{user_id}/predict", json=wine_description, headers=headers)
    if response.status_code == 200:
        st.success("Prediction task sent!")
    else:
        st.error("Failed to send prediction task.")


def get_user_predictions(user_id, token):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{API_BASE_URL}/prediction{user_id}/my_predictions", headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Failed to retrieve predictions.")
        return None


def get_user_id(username, token):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{API_BASE_URL}/user/{username}", headers=headers)
    if response.status_code == 200:
        return response.json().get('user_id')
    else:
        st.error("Failed to retrieve user id.")
        return None


def main():
    st.title("User Authentication")

    action = st.radio("Choose an action:", ("Login", "Register"))

    if action == "Register":
        new_username = st.text_input("Email")
        new_password = st.text_input("New Password", type="password")
        register_button = st.button("Register")

        if register_button:
            register_user(new_username, new_password)

    elif action == "Login":
        username = st.sidebar.text_input("Username")
        password = st.sidebar.text_input("Password", type="password")
        login_button = st.sidebar.button("Login")

        if login_button:
            token = authenticate(username, password)
            if token:
                st.session_state.token = token
                user_id = get_user_id(username, token)
                if user_id:
                    st.session_state.user_id = user_id

        if 'token' in st.session_state:
            st.sidebar.success("Logged in")

            st.subheader("Check Balance")
            if st.button("Check Balance"):
                balance = check_balance(st.session_state.user_id, st.session_state.token)
                if balance is not None:
                    st.write(f"Your balance: {balance}")

            st.subheader("Top-Up")
            top_up_amount = st.number_input("Amount to top up", min_value=0.0)
            if st.button("Top-Up"):
                top_up(st.session_state.user_id, top_up_amount, st.session_state.token)

            st.subheader("Make Prediction")
            wine_description = {
                "fixed_acidity": st.number_input("Fixed Acidity", value=7.4),
                "volatile_acidity": st.number_input("Volatile Acidity", value=0.7),
                "citric_acid": st.number_input("Citric Acid", value=0.0),
                "residual_sugar": st.number_input("Residual Sugar", value=1.9),
                "chlorides": st.number_input("Chlorides", value=0.076),
                "free_sulfur_dioxide": st.number_input("Free Sulfur Dioxide", value=11),
                "total_sulfur_dioxide": st.number_input("Total Sulfur Dioxide", value=34),
                "density": st.number_input("Density", value=0.9978),
                "pH": st.number_input("pH", value=3.51),
                "sulphates": st.number_input("Sulphates", value=0.56),
                "alcohol": st.number_input("Alcohol", value=9.4)
            }
            if st.button("Predict"):
                make_prediction(st.session_state.user_id, wine_description, st.session_state.token)

            st.subheader("View Predictions")
            if st.button("Get My Predictions"):
                predictions = get_user_predictions(st.session_state.user_id, st.session_state.token)
                if predictions is not None:
                    st.write(predictions)


if __name__ == "__main__":
    main()
