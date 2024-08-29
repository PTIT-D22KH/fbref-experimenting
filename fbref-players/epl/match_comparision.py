
import fbrefdata as fb
import statsbombpy as st
import mplsoccer as mp
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st
import json
import os
import shutil

def get_player_match_values(merged_df, player_name, match_name, col):
    """Get player values for radar chart."""
    player_df = merged_df[(merged_df['player'] == player_name) & (merged_df['game'] == match_name)]
    player_values = np.array(player_df[col[0][0]][col[0][1]].values[0])
    
    for x in col[1:]:
        if len(x) == 2:
            player_values = np.append(player_values, player_df[x[0]][x[1]].values[0])
        else:
            player_values = np.append(player_values, player_df[x[0]].values[0])
    
    return player_values

def match_compare():
    with open('league_dict.json', 'r') as f:
            league_dict = json.load(f)

    # Create a mapping from league names to keys
    league_name_to_key = {v['FBref']: k for k, v in league_dict.items()}

    # User selects the league
    league_options = list(league_name_to_key.keys())
    selected_league_name = st.selectbox("Select the league", league_options)

    # Get the corresponding league key
    selected_league_key = league_name_to_key[selected_league_name]

    # User selects the season
    season = st.selectbox("Select the season", ['2024-2025', '2023-2024', '2022-2023', '2021-2022', '2020-2021', '2019-2020', '2018-2019', '2017-2018'])
    fbref = initialize_fbref(selected_league_key, season)
    stats_list, _, _ = get_stats_lists()
    df_list = read_and_filter_stats(fbref, stats_list)

    param_mapping = {
        "Goals": ['Performance', 'Gls'],
        "Assists": ['Performance', 'Ast'],
        "Penalty Goals": ['Performance', 'PK'],
        "Penalty Attempts": ['Performance', 'PKatt'],
        "Shots": ['Performance', 'Sh'],
        "Shots on Target": ['Performance', 'SoT'],
        "Yellow Cards": ['Performance', 'CrdY'],
        "Red Cards": ['Performance', 'CrdR'],
        "Touches": ['Performance', 'Touches'],
        "Tackles": ['Performance', 'Tkl'],
        "Interceptions": ['Performance', 'Int'],
        "Blocks": ['Performance', 'Blocks'],
        "xG": ['Expected', 'xG'],
        "npxG": ['Expected', 'npxG'],
        "xAG": ['Expected', 'xAG'],
        "Shot-Creating Actions": ['SCA', 'SCA'],
        "Goal-Creating Actions": ['SCA', 'GCA'],
        "Passes Completed": ['Passes', 'Cmp'],
        "Passes Attempted": ['Passes', 'Att'],
        "Pass Completion %": ['Passes', 'Cmp%'],
        "Progressive Passes": ['Passes', 'PrgP'],
        "Carries": ['Carries', 'Carries'],
        "Progressive Carries": ['Carries', 'PrgC'],
        "Take-Ons Attempted": ['Take-Ons', 'Att'],
        "Successful Take-Ons": ['Take-Ons', 'Succ']
    }

    merged_df = merge_dataframes(df_list)

    # Get list of players
    players = merged_df['player'].unique().tolist()

    # Get list of games
    games = merged_df['game'].unique().tolist()

    # Streamlit UI elements
    selected_game = st.selectbox("Select the match", games)
    player1 = st.selectbox("Select the first player", players)
    player2 = st.selectbox("Select the second player", players)

    params = list(param_mapping.keys())
    selected_params = st.multiselect("Select parameters to compare", params, default=params[:5])

    lower_is_better_options = st.multiselect("Select parameters where lower is better", params)

    if st.button("Compare Players"):
        match_df = filter_match_data(merged_df, selected_game)
        compare_players_and_create_radar(match_df, player1, player2, selected_params, param_mapping, lower_is_better_options)