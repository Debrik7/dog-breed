import streamlit as st
import pandas as pd
import numpy as np
import os
from users import authenticate

# ------------------ PAGE CONFIG ------------------
st.set_page_config(
    page_title="Dog Breed Recommendation System",
    page_icon="🐶",
    layout="wide"
)

# ------------------ SESSION STATES ------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ------------------ LOGIN ------------------
if not st.session_state.logged_in:
    st.title("🔐 Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if authenticate(username, password):
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Invalid credentials")

    st.markdown("""
    **Demo Credentials**
    ```
    admin / admin123
    user / doglover
    ```
    """)
    st.stop()

# ------------------ SIDEBAR ------------------
st.sidebar.title("🐾 Navigation")
page = st.sidebar.radio("Go to", ["Preferences", "Rankings"])

if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.rerun()

# ------------------ DOG DATABASE ------------------
dogs = [
    ["Labrador Retriever",3,5,3,5,4,4,5,4],
    ["Poodle",3,4,2,4,5,2,4,4],
    ["Bulldog",3,2,2,4,2,2,2,4],
    ["Beagle",3,4,3,5,3,3,4,4],
    ["Chihuahua",1,2,1,3,2,1,2,3],
    ["German Shepherd",4,5,4,4,5,4,5,3],
    ["Golden Retriever",4,5,3,5,5,3,5,4],
    ["Shih Tzu",2,2,2,4,3,2,2,4],
    ["Rottweiler",4,4,4,3,4,3,4,3],
    ["Dachshund",2,3,2,4,3,2,3,4],
    ["Boxer",4,5,3,4,4,3,5,4],
    ["Siberian Husky",4,5,4,4,3,4,5,2],
    ["Yorkshire Terrier",1,3,2,4,3,1,3,3],
    ["Dalmatian",4,5,3,4,3,3,5,3],
    ["Great Dane",5,3,3,4,3,3,3,3],
    ["Border Collie",3,5,3,4,5,3,5,3],
    ["Cocker Spaniel",3,3,3,5,4,3,3,4],
    ["French Bulldog",2,2,2,4,3,2,2,4],
    ["Bichon Frise",2,3,2,5,4,1,3,4],
    ["Mastiff",5,2,3,3,2,3,2,3],
    ["Australian Shepherd",4,5,3,4,5,3,5,3],
    ["Cavalier King Charles",2,3,2,5,4,2,3,4],
    ["Pug",2,2,2,4,3,2,2,4],
    ["Doberman",4,5,3,3,5,3,5,3],
    ["Samoyed",4,4,4,5,3,4,4,2],
    ["Akita",4,3,4,3,3,3,3,2],
    ["Shiba Inu",3,3,3,3,3,3,3,2],
]

cols = ["Breed","Size","Energy","Grooming","Friendly",
        "Trainability","Shedding","Exercise","Climate"]

df = pd.DataFrame(dogs, columns=cols)

# ------------------ PREFERENCES PAGE ------------------
if page == "Preferences":
    st.title("🐶 Select Your Preferences")

    user_input = np.array([
        st.slider("Size",1,5,3),
        st.slider("Energy",1,5,3),
        st.slider("Grooming Needs",1,5,3),
        st.slider("Friendlyness",1,5,4),
        st.slider("Trainability",1,5,3),
        st.slider("Shedding",1,5,3),
        st.slider("Exercise",1,5,3),
        st.slider("Climate",1,5,3)
    ])

    if st.button("Recommend"):
        scores = []
        for _, row in df.iterrows():
            scores.append(np.sum(np.abs(user_input - row[1:].values)))

        df["Score"] = scores
        st.session_state.ranked = df.sort_values("Score")
        st.success("Recommendations ready! Go to Rankings.")

# ------------------ RANKINGS PAGE ------------------
if page == "Rankings":
    st.title("🏆 Recommended Dogs")

    if "ranked" not in st.session_state:
        st.warning("Select preferences first.")
    else:
        for _, dog in st.session_state.ranked.iterrows():
            st.markdown("---")
            col1, col2 = st.columns([1,3])

            with col1:
                img_name = dog["Breed"].lower().replace(" ", "_") + ".jpg"
                img_path = os.path.join("images", img_name)

                if os.path.exists(img_path):
                    st.image(img_path, width=200)
                else:
                    st.info("Image not found")

            with col2:
                st.subheader(dog["Breed"])
                st.write(f"Match Score: **{dog['Score']}**")
