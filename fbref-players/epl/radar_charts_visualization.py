#!/usr/bin/env python
# coding: utf-8

# In[1]:


import fbrefdata as fb
import statsbombpy as st
import mplsoccer as mp
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


# In[2]:


fb.FBref.available_leagues()


# In[3]:


fbref = fb.FBref('ENG-EPL', '2024-2025')


# In[4]:


stats_list = ['standard',
         'shooting',
             'passing',
             'passing_types',
            'goal_shot_creation',
             'defense',
             'possession',
             'misc',
             ]
keeper_stats_list = ['keeper',
            'keeper_adv']
non_related_list = ['playing_time']


# In[5]:


for i in range(len(stats_list)):
    df = fbref.read_player_season_stats(stats_list[i])
    print(df.shape)


# In[6]:


df_list = []
df1 = fbref.read_player_season_stats('standard')
# Calculate the value counts for the 'player' column
player_counts = df1['player'].value_counts()

# Identify players with 2 or more occurrences
players_to_drop = player_counts[player_counts >= 2].index

# Filter the DataFrame to exclude these players
df1_filtered = df1[~df1['player'].isin(players_to_drop)]
df_list.append(df1_filtered)
dropped_columns = ['nation', 'pos', 'team', 'age', 'born' , 'league', 'season']
for i in range(1, len(stats_list)):
    df = fbref.read_player_season_stats(stats_list[i])
    df.drop(columns = dropped_columns, inplace = True)
    df.fillna(0, inplace = True)
    player_counts = df['player'].value_counts()
    
    # Identify players with 2 or more occurrences
    players_to_drop = player_counts[player_counts >= 2].index
    
    # Filter the DataFrame to exclude these players
    df_filtered = df[~df['player'].isin(players_to_drop)]
    df_list.append(df_filtered)


# In[7]:


df_list[1]


# In[8]:


# Reset index to include 'id' as a column
for i in range(len(df_list)):
    df_list[i] = df_list[i].reset_index()

# Merge all DataFrames in the list on the 'player' column
merged_df = df_list[0]
for i, df in enumerate(df_list[1:], start=1):
    merged_df = pd.merge(merged_df, df, on='player', how='inner', suffixes=('', f'_df{i}'))

# Optionally, set 'id' back as the index
merged_df.set_index('id', inplace=True)


# In[9]:


merged_df['player'].value_counts()


# In[10]:


merged_df[merged_df['player'] == 'Jordan Ayew']


# In[11]:


merged_df.columns.to_list()


# In[12]:


# Parameter names of the statistics we want to show
params = ["npxG", "Non-Penalty Goals", "xAG", "Key Passes", "Through Balls",
          "Progressive Passes", "Shot-Creating Actions", "Goal-Creating Actions",
          "Carries", "Touches In Attacking 1/3", "Miscontrol", 'Dispossessed']

# Correctly define the column names
col = [
    ['Expected', 'npxG'], 
    ['Performance', 'G-PK'], 
    ['Expected', 'xAG'], 
    ['KP'],
    ['Pass Types', 'TB'], 
    ['PrgP'],
    ['SCA', 'SCA'], 
    ['GCA', 'GCA'], 
    ['Carries', 'Carries'], 
    ['Touches', 'Att 3rd'], 
    ['Carries', 'Mis'], 
    ['Carries', 'Dis']
]

# Add anything to this list where having a lower number is better
# This flips the statistic
lower_is_better = ['Miscontrol', 'Dispossessed']


# In[13]:


bruno_df = merged_df[merged_df['player'] == 'Bruno Fernandes']
bruno_values = np.array(bruno_df[col[0][0]][col[0][1]].values[0])
for i in range(1, len(col)):
    x = col[i]
    if (len(x) == 2):
        bruno_values = np.append(bruno_values, bruno_df[x[0]][x[1]].values[0])
    else:
        bruno_values = np.append(bruno_values, bruno_df[x[0]].values[0])
# x = np.array(a['Expected']['npxG'].values[0])
# x = np.append(x, a['Expected']['npxG'].values[0])
# a['Expected']['npxG'].values[0]
bruno_values


# In[14]:


kdb_df = merged_df[merged_df['player'] == 'Kevin De Bruyne']
kdb_values = np.array(kdb_df[col[0][0]][col[0][1]].values[0])
for i in range(1, len(col)):
    x = col[i]
    if (len(x) == 2):
        kdb_values = np.append(kdb_values, kdb_df[x[0]][x[1]].values[0])
    else:
        kdb_values = np.append(kdb_values, kdb_df[x[0]].values[0])
# x = np.array(a['Expected']['npxG'].values[0])
# x = np.append(x, a['Expected']['npxG'].values[0])
# a['Expected']['npxG'].values[0]
kdb_values


# In[15]:


low = np.minimum(bruno_values, kdb_values)
high = np.maximum(bruno_values, kdb_values)
low


# In[16]:


radar = mp.Radar(params, low, high,
              lower_is_better=lower_is_better,
              # whether to round any of the labels to integers instead of decimal places
              round_int=[False]*len(params),
              num_rings=4,  # the number of concentric circles (excluding center circle)
              # if the ring_width is more than the center_circle_radius then
              # the center circle radius will be wider than the width of the concentric circles
              ring_width=1, center_circle_radius=1)


# In[17]:


URL1 = ('https://raw.githubusercontent.com/googlefonts/SourceSerifProGFVersion/main/fonts/'
        'SourceSerifPro-Regular.ttf')
serif_regular = mp.FontManager(URL1)
URL2 = ('https://raw.githubusercontent.com/googlefonts/SourceSerifProGFVersion/main/fonts/'
        'SourceSerifPro-ExtraLight.ttf')
serif_extra_light = mp.FontManager(URL2)
URL3 = ('https://raw.githubusercontent.com/google/fonts/main/ofl/rubikmonoone/'
        'RubikMonoOne-Regular.ttf')
rubik_regular = mp.FontManager(URL3)
URL4 = 'https://raw.githubusercontent.com/googlefonts/roboto/main/src/hinted/Roboto-Thin.ttf'
robotto_thin = mp.FontManager(URL4)
URL5 = ('https://raw.githubusercontent.com/google/fonts/main/apache/robotoslab/'
        'RobotoSlab%5Bwght%5D.ttf')
robotto_bold = mp.FontManager(URL5)


# In[18]:


# plot radar
fig, ax = radar.setup_axis()
rings_inner = radar.draw_circles(ax=ax, facecolor='#ffb2b2', edgecolor='#fc5f5f')

radar1, vertices1 = radar.draw_radar_solid(bruno_values, ax=ax,
                                           kwargs={'facecolor': '#aa65b2',
                                                   'alpha': 0.6,
                                                   'edgecolor': '#216352',
                                                   'lw': 3})

radar2, vertices2 = radar.draw_radar_solid(kdb_values, ax=ax,
                                           kwargs={'facecolor': '#66d8ba',
                                                   'alpha': 0.6,
                                                   'edgecolor': '#216352',
                                                   'lw': 3})



ax.scatter(vertices1[:, 0], vertices1[:, 1],
           c='#aa65b2', edgecolors='#502a54', marker='o', s=150, zorder=2)
ax.scatter(vertices2[:, 0], vertices2[:, 1],
           c='#66d8ba', edgecolors='#216352', marker='o', s=150, zorder=2)


range_labels = radar.draw_range_labels(ax=ax, fontsize=25, fontproperties=robotto_thin.prop)
param_labels = radar.draw_param_labels(ax=ax, fontsize=25, fontproperties=robotto_thin.prop)


# In[19]:


# creating the figure using the grid function from mplsoccer:
fig, axs = mp.grid(figheight=14, grid_height=0.915, title_height=0.06, endnote_height=0.025,
                title_space=0, endnote_space=0, grid_key='radar', axis=False)

# plot the radar
radar.setup_axis(ax=axs['radar'])
rings_inner = radar.draw_circles(ax=axs['radar'], facecolor='#ffb2b2', edgecolor='#fc5f5f')
radar_output = radar.draw_radar(bruno_values, ax=axs['radar'],
                                kwargs_radar={'facecolor': '#aa65b2'},
                                kwargs_rings={'facecolor': '#66d8ba'})
radar_poly, rings_outer, vertices = radar_output
range_labels = radar.draw_range_labels(ax=axs['radar'], fontsize=25,
                                       fontproperties=robotto_thin.prop)
param_labels = radar.draw_param_labels(ax=axs['radar'], fontsize=25,
                                       fontproperties=robotto_thin.prop)

# adding the endnote and title text (these axes range from 0-1, i.e. 0, 0 is the bottom left)
# Note we are slightly offsetting the text from the edges by 0.01 (1%, e.g. 0.99)
endnote_text = axs['endnote'].text(0.99, 0.5, 'Inspired By: StatsBomb / Rami Moghadam', fontsize=15,
                                   fontproperties=robotto_thin.prop, ha='right', va='center')
title1_text = axs['title'].text(0.01, 0.65, 'Bruno Fernandes', fontsize=25,
                                fontproperties=robotto_bold.prop, ha='left', va='center')
title2_text = axs['title'].text(0.01, 0.25, 'Manchester United', fontsize=20,
                                fontproperties=robotto_thin.prop,
                                ha='left', va='center', color='#B6282F')
title3_text = axs['title'].text(0.99, 0.65, 'Radar Chart', fontsize=25,
                                fontproperties=robotto_bold.prop, ha='right', va='center')
title4_text = axs['title'].text(0.99, 0.25, 'Midfielder', fontsize=20,
                                fontproperties=robotto_thin.prop,
                                ha='right', va='center', color='#B6282F')
# sphinx_gallery_thumbnail_path = 'gallery/radar/images/sphx_glr_plot_radar_004.png'


# In[20]:


# creating the figure using the grid function from mplsoccer:
fig, axs = mp.grid(figheight=14, grid_height=0.915, title_height=0.06, endnote_height=0.025,
                title_space=0, endnote_space=0, grid_key='radar', axis=False)

# plot the radar
radar.setup_axis(ax=axs['radar'])
rings_inner = radar.draw_circles(ax=axs['radar'], facecolor='#ffb2b2', edgecolor='#fc5f5f')
radar_output = radar.draw_radar(kdb_values, ax=axs['radar'],
                                kwargs_radar={'facecolor': '#aa65b2'},
                                kwargs_rings={'facecolor': '#66d8ba'})
radar_poly, rings_outer, vertices = radar_output
range_labels = radar.draw_range_labels(ax=axs['radar'], fontsize=25,
                                       fontproperties=robotto_thin.prop)
param_labels = radar.draw_param_labels(ax=axs['radar'], fontsize=25,
                                       fontproperties=robotto_thin.prop)

# adding the endnote and title text (these axes range from 0-1, i.e. 0, 0 is the bottom left)
# Note we are slightly offsetting the text from the edges by 0.01 (1%, e.g. 0.99)
endnote_text = axs['endnote'].text(0.99, 0.5, 'Inspired By: StatsBomb / Rami Moghadam', fontsize=15,
                                   fontproperties=robotto_thin.prop, ha='right', va='center')
title1_text = axs['title'].text(0.01, 0.65, 'Kevin De Bruyne', fontsize=25,
                                fontproperties=robotto_bold.prop, ha='left', va='center')
title2_text = axs['title'].text(0.01, 0.25, 'Manchester City', fontsize=20,
                                fontproperties=robotto_thin.prop,
                                ha='left', va='center', color='#B6282F')
title3_text = axs['title'].text(0.99, 0.65, 'Radar Chart', fontsize=25,
                                fontproperties=robotto_bold.prop, ha='right', va='center')
title4_text = axs['title'].text(0.99, 0.25, 'Midfielder', fontsize=20,
                                fontproperties=robotto_thin.prop,
                                ha='right', va='center', color='#B6282F')
# sphinx_gallery_thumbnail_path = 'gallery/radar/images/sphx_glr_plot_radar_004.png'


# In[21]:


# creating the figure using the grid function from mplsoccer:
fig, axs = mp.grid(figheight=14, grid_height=0.915, title_height=0.06, endnote_height=0.025,
                title_space=0, endnote_space=0, grid_key='radar', axis=False)

# plot radar
radar.setup_axis(ax=axs['radar'])  # format axis as a radar
rings_inner = radar.draw_circles(ax=axs['radar'], facecolor='#ffb2b2', edgecolor='#fc5f5f')
radar_output = radar.draw_radar_compare(bruno_values, kdb_values, ax=axs['radar'],
                                        kwargs_radar={'facecolor': '#00f2c1', 'alpha': 0.6},
                                        kwargs_compare={'facecolor': '#d80499', 'alpha': 0.6})
radar_poly, radar_poly2, vertices1, vertices2 = radar_output
range_labels = radar.draw_range_labels(ax=axs['radar'], fontsize=25,
                                       fontproperties=robotto_thin.prop)
param_labels = radar.draw_param_labels(ax=axs['radar'], fontsize=25,
                                       fontproperties=robotto_thin.prop)
axs['radar'].scatter(vertices1[:, 0], vertices1[:, 1],
                     c='#00f2c1', edgecolors='#6d6c6d', marker='o', s=150, zorder=2)
axs['radar'].scatter(vertices2[:, 0], vertices2[:, 1],
                     c='#d80499', edgecolors='#6d6c6d', marker='o', s=150, zorder=2)

# adding the endnote and title text (these axes range from 0-1, i.e. 0, 0 is the bottom left)
# Note we are slightly offsetting the text from the edges by 0.01 (1%, e.g. 0.99)
endnote_text = axs['endnote'].text(0.99, 0.5, 'Inspired By: StatsBomb / Rami Moghadam', fontsize=15,
                                   fontproperties=robotto_thin.prop, ha='right', va='center')
title1_text = axs['title'].text(0.01, 0.65, 'Bruno Fernandes', fontsize=25, color='#01c49d',
                                fontproperties=robotto_bold.prop, ha='left', va='center')
title2_text = axs['title'].text(0.01, 0.25, 'Manchester United', fontsize=20,
                                fontproperties=robotto_thin.prop,
                                ha='left', va='center', color='#01c49d')
title3_text = axs['title'].text(0.99, 0.65, 'Kevin De Bruyne', fontsize=25,
                                fontproperties=robotto_bold.prop,
                                ha='right', va='center', color='#d80499')
title4_text = axs['title'].text(0.99, 0.25, 'Manchester City', fontsize=20,
                                fontproperties=robotto_thin.prop,
                                ha='right', va='center', color='#d80499')


# In[22]:


# creating the figure using the grid function from mplsoccer:
fig, axs = mp.grid(figheight=14, grid_height=0.915, title_height=0.06, endnote_height=0.025,
                title_space=0, endnote_space=0, grid_key='radar', axis=False)

# we are creating a new radar object with more rings, integer rounding, and a larger center circle
radar2 = mp.Radar(params=['Speed', 'Agility', 'Strength', 'Passing', 'Dribbles'],
               min_range=[0, 0, 0, 0, 0],
               max_range=[5, 5, 5, 5, 5],
               # here we make the labels integers instead of floats
               round_int=[True, True, True, True, True],
               # make the center circle x2 larger than the concentric circles
               center_circle_radius=2,
               # the number of rings has been chosen to divide the max_range evenly
               num_rings=5)

# plot the radar
radar2.setup_axis(ax=axs['radar'], facecolor='None')
rings_inner = radar2.draw_circles(ax=axs['radar'], facecolor='#f77b83', edgecolor='#fe2837')
radar_output = radar2.draw_radar(values=[5, 2, 4, 3, 1], ax=axs['radar'],
                                 kwargs_radar={'facecolor': '#f9c728', 'hatch': '.', 'alpha': 1},
                                 kwargs_rings={'facecolor': '#e6dedc', 'edgecolor': '#1a1414',
                                               'hatch': '/', 'alpha': 1})
# draw the radar again but without a facecolor ('None') and an edgecolor
# we draw it again so that we can choose a different edgecolor from the radar
radar_output2 = radar2.draw_radar(values=[5, 2, 4, 3, 1], ax=axs['radar'],
                                  kwargs_radar={'facecolor': 'None', 'edgecolor': '#646366'},
                                  kwargs_rings={'facecolor': 'None'})
# draw the labels
range_labels = radar2.draw_range_labels(ax=axs['radar'], fontproperties=serif_extra_light.prop,
                                        fontsize=25)
param_labels = radar2.draw_param_labels(ax=axs['radar'], fontproperties=serif_regular.prop,
                                        fontsize=25)

# adding the endnote and title text (these axes range from 0-1, i.e. 0, 0 is the bottom left)
# Note we are slightly offsetting the text from the edges by 0.01 (1%, e.g. 0.99)
endnote_text = axs['endnote'].text(0.99, 0.5, 'The theme is inspired by Camille Walala',
                                   fontproperties=serif_extra_light.prop, fontsize=15,
                                   ha='right', va='center')
title1_text = axs['title'].text(0.01, 0.65, 'Player name', fontsize=20,
                                fontproperties=rubik_regular.prop, ha='left', va='center')
title2_text = axs['title'].text(0.01, 0.25, 'Player team', fontsize=15,
                                fontproperties=rubik_regular.prop, ha='left',
                                va='center', color='#fa1b38')
title3_text = axs['title'].text(0.99, 0.65, 'Radar Chart', fontsize=20,
                                fontproperties=rubik_regular.prop, ha='right', va='center')
title4_text = axs['title'].text(0.99, 0.25, 'Position', fontsize=15,
                                fontproperties=rubik_regular.prop, ha='right',
                                va='center', color='#fa1b38')

fig.set_facecolor('#f2dad2')

plt.show()  # If you are using a Jupyter notebook you do not need this line


# In[ ]:




