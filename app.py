import time
import streamlit as st
from langchain.llms import OpenAI
from langchain.agents.agent_types import AgentType
from langchain.agents import create_csv_agent

st.title('Fast Food Macros AI')
st.markdown('This app uses the OpenAI API to generate a whimsical response based on user input. Additionally, uses Langchain to digest a CSV file of menu items and their macros.')

openai_api_key = st.sidebar.text_input('OpenAI API Key')
csv_file_path = "menu.csv"
restaurant = st.selectbox('Choose restaurant',('Taco Bell', 'Chick-fil-a', 'In-n-Out'))
protein = st.number_input('Protein (g)', min_value=0, max_value=200, value=0, step=1)
carb = st.number_input('Carbs (g)', min_value=0, max_value=200, value=0, step=1)
fat = st.number_input('Fat (g)', min_value=0, max_value=200, value=0, step=1)
judgemental = st.checkbox('Judge me!')

def generate_response(restaurant, protein, carb, fat):
  llm = OpenAI(temperature=0.7, openai_api_key=openai_api_key)
  agent = create_csv_agent(
      llm,
      csv_file_path,
      verbose=False,
      agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
  )
  input_text = 'As a nutritionist tell me the most amount of menu items I can eat from {} that is the closest to {} grams of protein, {} grams of carbs, and {} grams of fat. Exceeding by a modest amount is ok. List the menu items as well as the macros.'.format(restaurant, protein, carb, fat)
  if judgemental:
    input_text += ' End with a quip about my food choices, with a judgemental/offensive, borderline mean tone. Add a random statistic about obesity with the intent to frighten the food consumer.'
  st.info(agent.run(input_text))

with st.form('my_form'):
  submitted = st.form_submit_button('What can I eat?')
  if not openai_api_key.startswith('sk-'):
    st.warning('Please enter your OpenAI API key!', icon='⚠')
  if submitted and openai_api_key.startswith('sk-'):
    generate_response(restaurant, protein, carb, fat)