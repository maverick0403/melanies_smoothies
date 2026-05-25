# Import python packages
import streamlit as st
#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col,when_matched

# Write directly to the app
st.title(f":cup_with_straw: Customise Your Smoothies!:cup_with_straw:")
st.write(
  """Choose the fruits you want in your custom Smoothie!
  """
)

# option = st.selectbox(
#     "What is your favourite fruit?",
#     ("Banana", "Strawberries", "Peaches", "Kiwi"),
# )

# st.write("You selected:", option)

name_on_order = st.text_input("Name on Smoothie")
st.write("The name on your Smoothies will be:", name_on_order)

cnx=st.connection("snowflake")
session = cnx.session()

#session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('fruit_name'))
#st.dataframe(data=my_dataframe, use_container_width=True)

fruit_list = st.multiselect(
    "chose upto 5 fruits",
    my_dataframe,
    max_selections=5
)

if fruit_list:
    
    ingredients_string = ''
    
    for fruits in fruit_list:
        ingredients_string += fruits + ' '
    st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
                values ('""" + ingredients_string + """','""" + name_on_order + """')"""

    #st.write(my_insert_stmt)
    #st.stop()

    time_to_insert = st.button('submit order')
    
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
    
        st.success('Your Smoothie is ordered, ' + name_on_order + '!', icon="✅")
