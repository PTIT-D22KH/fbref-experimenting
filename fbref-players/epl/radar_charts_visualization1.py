#!/usr/bin/env python
# coding: utf-8

import fbrefdata as fb
import statsbombpy as st
import mplsoccer as mp
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def get_available_leagues():
    """Print available leagues."""
    fb.FBref.available_leagues()

def initialize_fbref(league, season):
    """Initialize FBref object for a given league and season."""
    return fb.FBref(league, season)

def get_stats_lists():
    """Return lists of stats categories."""
    stats_list = ['standard', 'shooting', 'passing', 'passing_types', 'goal_shot_creation', 'defense', 'possession', 'misc']
    keeper_stats_list = ['keeper', 'keeper_adv']
    non_related_list = ['playing_time']
    return stats_list, keeper_stats_list, non_related_list

def read_and_filter_stats(fbref, stats_list):
    """Read and filter player season stats."""
    df_list = []
    df1 = fbref.read_player_season_stats('standard')
    df1_filtered = filter_duplicate_players(df1)
    df_list.append(df1_filtered)
    dropped_columns = ['nation', 'pos', 'team', 'age', 'born', 'league', 'season']
    
    for stat in stats_list[1:]:
        df = fbref.read_player_season_stats(stat)
        df.drop(columns=dropped_columns, inplace=True)
        df.fillna(0, inplace=True)
        df_filtered = filter_duplicate_players(df)
        df_list.append(df_filtered)
    
    return df_list

def filter_duplicate_players(df):
    """Filter out players with 2 or more occurrences."""
    player_counts = df['player'].value_counts()
    players_to_drop = player_counts[player_counts >= 2].index
    return df[~df['player'].isin(players_to_drop)]

def merge_dataframes(df_list):
    """Merge list of dataframes on the 'player' column."""
    for i in range(len(df_list)):
        df_list[i] = df_list[i].reset_index()
    
    merged_df = df_list[0]
    for i, df in enumerate(df_list[1:], start=1):
        merged_df = pd.merge(merged_df, df, on='player', how='inner', suffixes=('', f'_df{i}'))
    
    merged_df.set_index('id', inplace=True)
    return merged_df

def get_player_values(merged_df, player_name, col):
    """Get player values for radar chart."""
    player_df = merged_df[merged_df['player'] == player_name]
    player_values = np.array(player_df[col[0][0]][col[0][1]].values[0])
    
    for x in col[1:]:
        if len(x) == 2:
            player_values = np.append(player_values, player_df[x[0]][x[1]].values[0])
        else:
            player_values = np.append(player_values, player_df[x[0]].values[0])
    
    return player_values

def create_radar_chart(params, low, high, lower_is_better, bruno_values, kdb_values):
    """Create radar chart comparing two players."""
    radar = mp.Radar(params, low, high, lower_is_better=lower_is_better, round_int=[False]*len(params), num_rings=4, ring_width=1, center_circle_radius=1)
    
    URL1 = ('https://raw.githubusercontent.com/googlefonts/SourceSerifProGFVersion/main/fonts/SourceSerifPro-Regular.ttf')
    serif_regular = mp.FontManager(URL1)
    URL2 = ('https://raw.githubusercontent.com/googlefonts/SourceSerifProGFVersion/main/fonts/SourceSerifPro-ExtraLight.ttf')
    serif_extra_light = mp.FontManager(URL2)
    URL3 = ('https://raw.githubusercontent.com/google/fonts/main/ofl/rubikmonoone/RubikMonoOne-Regular.ttf')
    rubik_regular = mp.FontManager(URL3)
    URL4 = 'https://raw.githubusercontent.com/googlefonts/roboto/main/src/hinted/Roboto-Thin.ttf'
    robotto_thin = mp.FontManager(URL4)
    URL5 = ('https://raw.githubusercontent.com/google/fonts/main/apache/robotoslab/RobotoSlab%5Bwght%5D.ttf')
    robotto_bold = mp.FontManager(URL5)
    
    fig, axs = mp.grid(figheight=14, grid_height=0.915, title_height=0.06, endnote_height=0.025, title_space=0, endnote_space=0, grid_key='radar', axis=False)
    
    radar.setup_axis(ax=axs['radar'])
    rings_inner = radar.draw_circles(ax=axs['radar'], facecolor='#ffb2b2', edgecolor='#fc5f5f')
    radar_output = radar.draw_radar_compare(bruno_values, kdb_values, ax=axs['radar'], kwargs_radar={'facecolor': '#00f2c1', 'alpha': 0.6}, kwargs_compare={'facecolor': '#d80499', 'alpha': 0.6})
    radar_poly, radar_poly2, vertices1, vertices2 = radar_output
    range_labels = radar.draw_range_labels(ax=axs['radar'], fontsize=25, fontproperties=robotto_thin.prop)
    param_labels = radar.draw_param_labels(ax=axs['radar'], fontsize=25, fontproperties=robotto_thin.prop)
    axs['radar'].scatter(vertices1[:, 0], vertices1[:, 1], c='#00f2c1', edgecolors='#6d6c6d', marker='o', s=150, zorder=2)
    axs['radar'].scatter(vertices2[:, 0], vertices2[:, 1], c='#d80499', edgecolors='#6d6c6d', marker='o', s=150, zorder=2)
    
    endnote_text = axs['endnote'].text(0.99, 0.5, 'Inspired By: StatsBomb / Rami Moghadam', fontsize=15, fontproperties=robotto_thin.prop, ha='right', va='center')
    title1_text = axs['title'].text(0.01, 0.65, 'Bruno Fernandes', fontsize=25, color='#01c49d', fontproperties=robotto_bold.prop, ha='left', va='center')
    title2_text = axs['title'].text(0.01, 0.25, 'Manchester United', fontsize=20, fontproperties=robotto_thin.prop, ha='left', va='center', color='#01c49d')
    title3_text = axs['title'].text(0.99, 0.65, 'Kevin De Bruyne', fontsize=25, fontproperties=robotto_bold.prop, ha='right', va='center', color='#d80499')
    title4_text = axs['title'].text(0.99, 0.25, 'Manchester City', fontsize=20, fontproperties=robotto_thin.prop, ha='right', va='center', color='#d80499')
    
    fig.set_facecolor('#f2dad2')
    plt.show()

def main():
    get_available_leagues()
    fbref = initialize_fbref('ENG-EPL', '2024-2025')
    stats_list, _, _ = get_stats_lists()
    df_list = read_and_filter_stats(fbref, stats_list)
    merged_df = merge_dataframes(df_list)
    
    params = ["npxG", "Non-Penalty Goals", "xAG", "Key Passes", "Through Balls", "Progressive Passes", "Shot-Creating Actions", "Goal-Creating Actions", "Carries", "Touches In Attacking 1/3", "Miscontrol", 'Dispossessed']
    col = [['Expected', 'npxG'], ['Performance', 'G-PK'], ['Expected', 'xAG'], ['KP'], ['Pass Types', 'TB'], ['PrgP'], ['SCA', 'SCA'], ['GCA', 'GCA'], ['Carries', 'Carries'], ['Touches', 'Att 3rd'], ['Carries', 'Mis'], ['Carries', 'Dis']]
    lower_is_better = ['Miscontrol', 'Dispossessed']
    
    bruno_values = get_player_values(merged_df, 'Bruno Fernandes', col)
    kdb_values = get_player_values(merged_df, 'Kevin De Bruyne', col)
    
    low = np.minimum(bruno_values, kdb_values)
    high = np.maximum(bruno_values, kdb_values)
    
    create_radar_chart(params, low, high, lower_is_better, bruno_values, kdb_values)

if __name__ == "__main__":
    main()