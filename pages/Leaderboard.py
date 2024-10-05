import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(layout="wide")

num_users = 10
user_names = [f"User {i+1}" for i in range(num_users)]
scores = np.random.randint(0, 1000, size=num_users)
leaderboard_data = pd.DataFrame({
    'User': user_names,
    'Score': scores
})

leaderboard_data = leaderboard_data.sort_values(by='Score', ascending=False).reset_index(drop=True)
leaderboard_data['Rank'] = leaderboard_data.index + 1
leaderboard_data = leaderboard_data[['Rank', 'User', 'Score']]

# Streamlit App
st.write(f"""# Leaderboard 🏆
### Here are the top 10 thriftiest users of all time:""")
st.table(leaderboard_data.set_index('Rank'))
