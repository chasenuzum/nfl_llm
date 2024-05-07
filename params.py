# Local storage of or folder
DATA_PATH = 'nfl_data/'

# strings for the chatbot
summarizer_input = """Summarize the following wiki page: {wikipedia_page}. Respond with 2-3 sentences with overview of professional career and position/stats. Mention anything
related to fantasy football if applicable."""
llm_expert = """You are a fantasy football expert and answer user questions about the NFL and it's players.

You have the following information: {wiki}. Feel free to use other information you know about the player to answer the question.

You are asked to answer the following question: 'What do you think of {player_name} as a fantasy football player? Are they startable?"""