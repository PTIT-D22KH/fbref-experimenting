import os
import streamlit as st
import fbrefdata as fb
import shutil

def initialize_fbref(league, season):
    return fb.FBref(league, season)

def main():
    # Define the path to the league_dict.json file
    fbrefdata_dir = os.getenv('FBREFDATA_DIR', os.path.expanduser('~/fbrefdata'))
    config_dir = os.path.join(fbrefdata_dir, 'config')
    league_dict_path = os.path.join(config_dir, 'league_dict.json')
    print(config_dir)
    # Ensure the directory exists
    os.makedirs(config_dir, exist_ok=True)
    source = 'league_dict.json'
    shutil.copy(source, league_dict_path)
    # Load the custom league configuration

    # Example usage
    selected_league_key = 'ENG-EPL'
    season = '2023-2024'
    fbref = initialize_fbref(selected_league_key, season)
    st.write(fbref.available_leagues())

if __name__ == "__main__":
    main()