# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

# Write directly to the app
st.title("🥤 Customize Your Smoothie! 🥤")

st.write(
    """Choose the fruits you want in your customer smoothie!."""
)

name_on_order = st.text_input("Name on smoothie")
st.write("The name of your smoothie will be:", name_on_order)

# ✅ SniS connection (NOT get_active_session)
cnx = st.connection("snowflake")
session = cnx.session()

my_dataframe = session.table("smoothies.public.fruit_options").select(col("FRUIT_NAME"))

ingredients_list = st.multiselect(
    "Choose up to 5 ingredients",
    my_dataframe, max_selections=5)
st.write("You selected:", ingredients_list)

if ingredients_list:

    ingredients_string = ''
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
                    values ('""" + ingredients_string + """','""" + name_on_order + """')"""

    time_to_insert = st.button("submit order")

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")

import requests
smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
st.text(smoothiefroot_response.json())
