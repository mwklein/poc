import requests
import streamlit as st
import snowflake.connector

my_cnx = snowflake.connector.connect(**st.secrets["TOKEN_OWNERSHIP"])
my_cur = my_cnx.cursor()

# Token details
tokens = [
    {"name": "My Say Token", "cost": 1000, "image_url": "https://github.com/mergray0521/poc/blob/main/images/MicrosoftTeams-image%20(16).png?raw=true"},
    {"name": "My Way Token", "cost": 2000, "image_url": "https://github.com/mergray0521/poc/blob/main/images/MicrosoftTeams-image%20(17).png?raw=true"},
    {"name": "My Day Token", "cost": 3000, "image_url": "https://github.com/mergray0521/poc/blob/main/images/MicrosoftTeams-image%20(17).png?raw=true"},
    {"name": "Park Ticket", "cost": 4000, "image_url": "https://github.com/mergray0521/poc/blob/main/images/ticket.png?raw=true"},
    {"name": "Dragon", "cost": 4000, "image_url": "https://cdn.dribbble.com/users/1061278/screenshots/14605165/media/f27c0bfd48d70f3aa755d3617b287f3e.png?resize=400x300&vertical=center"},
    {"name": "Hatching Egg", "cost": 3000, "image_url": "https://cdn3.iconfinder.com/data/icons/fantasy-and-role-play-game-adventure-quest/512/Dragon_Egg-512.png"},
]

user_id = 1

# Function to handle button click
def handle_purchase(token_name, token_cost):
    # 1. Get User Points
    user_points_query = f"SELECT point_quantity FROM point_ownership WHERE user_id = {user_id}"
    my_cur.execute(user_points_query)
    user_points = my_cur.fetchone()[0]

    # 2. Check Sufficient Points
    if user_points >= token_cost:
        # 3. Update Point Ownership
        new_points = user_points - token_cost
        update_points_query = f"UPDATE point_ownership SET point_quantity = {new_points} WHERE user_id = {user_id}"
        my_cur.execute(update_points_query)
        # 4. Insert Token Ownership
        insert_token_query = f"INSERT INTO token_ownership (owner_id, token_id, quantity) VALUES ({user_id}, '{token_name}', 1)"
        my_cur.execute(insert_token_query)
        st.success(f"You have successfully purchased {token_name}!")
    else:
        st.error("Insufficient points to purchase this token.")

# UI Code
st.header("Token Marketplace")

for token in tokens:
    st.markdown(
        f"""
        <div class="custom-container">
            <img src="{token['image_url']}" alt="{token['name']}" class="custom-image">
            <p>{token['name']} - {token['cost']} points</p>
            <button class="custom-button" onclick="handle_purchase('{token['name']}', {token['cost']})">Purchase {token['name']}</button>
        </div>
        """,
        unsafe_allow_html=True,
    )
