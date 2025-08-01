# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize Your SMOOTHIES ! :cup_with_straw:")
st.write(
  """Choose the fruit you want in your custom Smoothies!  """
)

name_on_order = st.text_input('Name on Smoothies:')
st.write('The Name on your Smoothies will be: ',name_on_order)

cnx=st.connection("snowflake")
session=cnx.session()
session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('Fruit_Name'))
#st.dataframe(data=my_dataframe, use_container_width=True)
ingredients_list=st.multiselect('Choose upto 5 ingredients: ', my_dataframe,max_selections=5)


if ingredients_list:
    st.write(ingredients_list)
    st.text(ingredients_list)

    ingredients_string=''

    for fruit_chosen in ingredients_list:
        ingredients_string +=fruit_chosen+' '

        
    #st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order,order_filled)
            values ('""" + ingredients_string + """', '""" + name_on_order + """',0)"""

    #st.write(my_insert_stmt)
    #st.stop()
    
    time_to_insert=st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered,'+name_on_order+'!',icon="✅")
