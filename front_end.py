import streamlit as st
import pandas as pd
from utils import wiki_load  # Assuming this handles position information
from params import *
import os

# langchain toolkit
from langchain_core.prompts import ChatPromptTemplate
# import llama-7b
from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from operator import itemgetter

# llm 
llm = ChatOllama(model="llama2")

# load base directory
base_dir = os.path.dirname(os.getcwd())

# get roster data
rosters = pd.read_csv(os.path.join(base_dir, 'nfl_data', 'rosters.csv'))

# get player names and their position played from rosters
players = rosters[["player_name", "position"]].drop_duplicates()

# create chains (modified to use chain_expert directly)
prompt = ChatPromptTemplate.from_template(summarizer_input)
expert_prompt = ChatPromptTemplate.from_template(llm_expert)
chain_summarizer = prompt | llm | StrOutputParser()
chain_expert = {"wiki": chain_summarizer, "player_name": itemgetter("player_name")} | \
expert_prompt | llm | StrOutputParser()

# set up app; streamlit components
st.title("NFL Chatbot")
st.subheader("Select a NFL player and I'll give you a response!")

# Player selection dropdown
selected_player = st.selectbox("Select a player:", players['player_name'].tolist())
wikipage = wiki_load(search_string=selected_player, position=players.loc[players['player_name'] == selected_player, 'position'].values[0])

# Generate response based on selected player and wikipage
answer = chain_expert.invoke({"wikipedia_page": wikipage, "player_name": selected_player})

# Display response
st.write(f"About {selected_player}:")
st.markdown(answer)