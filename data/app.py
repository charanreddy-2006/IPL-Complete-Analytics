import streamlit as st
import pandas as pd
import plotly.express as px
import os


# -------------------------
# PAGE CONFIG
# -------------------------

st.set_page_config(

    page_title="IPL Analytics",

    page_icon="🏏",

    layout="wide"

)



# -------------------------
# CSS
# -------------------------

def load_css():

    try:

        with open("style.css") as f:

            st.markdown(

                f"<style>{f.read()}</style>",

                unsafe_allow_html=True

            )

    except:

        pass



load_css()



# -------------------------
# LOAD DATA
# -------------------------

@st.cache_data

def load_data():


    paths=[

        "../data/processed/ipl_cleaned.csv",

        "../data/raw/matches.csv",

        "ipl_cleaned.csv"

    ]


    for file in paths:


        if os.path.exists(file):


            df=pd.read_csv(

                file,

                low_memory=False

            )

            return df



    st.error(
        "IPL dataset not found"
    )

    st.stop()



df=load_data()



# clean columns

df.columns=(

    df.columns

    .str.lower()

    .str.strip()

)



# -------------------------
# TITLE
# -------------------------

st.title(
    "🏏 IPL Complete Analytics Dashboard"
)


st.write(

"Professional Data Analyst Portfolio Project"

)



# -------------------------
# COLUMN DETECTION
# -------------------------

def find_col(names):

    for n in names:

        if n in df.columns:

            return n

    return None



season_col=find_col(

[
"season",
"year"
]

)



winner_col=find_col(

[
"winner",
"winning_team"
]

)



team1_col=find_col(

[
"team1"
]

)



team2_col=find_col(

[
"team2"
]

)



venue_col=find_col(

[
"venue",
"stadium"
]

)



runs_col=find_col(

[
"total_runs",
"runs"
]

)



player_col=find_col(

[
"player_of_match",
"player"
]

)




# -------------------------
# SIDEBAR
# -------------------------

st.sidebar.title(
"Filters"
)



if season_col:


    seasons=(

        df[season_col]

        .dropna()

        .astype(str)

        .unique()

        .tolist()

    )


    season=st.sidebar.selectbox(

        "Season",

        ["All"]+sorted(seasons)

    )


    if season!="All":

        df=df[

            df[season_col]

            .astype(str)

            ==

            season

        ]




if winner_col:


    teams=(

        df[winner_col]

        .dropna()

        .unique()

        .tolist()

    )


    team=st.sidebar.selectbox(

        "Team",

        ["All"]+sorted(teams)

    )


    if team!="All":

        df=df[

            df[winner_col]

            ==

            team

        ]





# -------------------------
# KPI CARDS
# -------------------------


c1,c2,c3,c4=st.columns(4)



with c1:

    st.metric(

        "Matches",

        len(df)

    )



with c2:

    if season_col:

        value=df[season_col].nunique()

    else:

        value=0


    st.metric(

        "Seasons",

        value

    )



with c3:

    if winner_col:

        value=df[winner_col].nunique()

    else:

        value=0


    st.metric(

        "Teams",

        value

    )



with c4:


    if runs_col:

        value=pd.to_numeric(

            df[runs_col],

            errors="coerce"

        ).sum()


    else:

        value=0



    st.metric(

        "Total Runs",

        int(value)

    )





# -------------------------
# WINNING TEAMS
# -------------------------

if winner_col:


    st.subheader(
        "🏆 Winning Team Analysis"
    )


    wins=(

        df[winner_col]

        .value_counts()

        .reset_index()

    )


    wins.columns=[

        "Team",

        "Wins"

    ]



    fig=px.bar(

        wins,

        x="Team",

        y="Wins",

        title="Most Successful Teams"

    )


    st.plotly_chart(

        fig,

        width="stretch"

    )





# -------------------------
# TEAM PARTICIPATION
# -------------------------


if team1_col and team2_col:


    st.subheader(
        "Teams Participation"
    )


    teams=pd.concat(

        [

            df[team1_col],

            df[team2_col]

        ]

    )



    data=(

        teams

        .value_counts()

        .reset_index()

    )


    data.columns=[

        "Team",

        "Matches"

    ]



    fig=px.pie(

        data,

        names="Team",

        values="Matches",

        title="Matches Played"

    )


    st.plotly_chart(

        fig,

        width="stretch"

    )




# -------------------------
# RUN ANALYSIS
# -------------------------


if runs_col:


    st.subheader(
        "Run Distribution"
    )


    fig=px.histogram(

        df,

        x=runs_col,

        title="Runs per Match"

    )


    st.plotly_chart(

        fig,

        width="stretch"

    )





# -------------------------
# VENUE ANALYSIS
# -------------------------


if venue_col:


    st.subheader(
        "🏟 Venue Analysis"
    )


    venue=(

        df[venue_col]

        .value_counts()

        .head(10)

        .reset_index()

    )


    venue.columns=[

        "Venue",

        "Matches"

    ]


    fig=px.bar(

        venue,

        x="Matches",

        y="Venue",

        orientation="h"

    )


    st.plotly_chart(

        fig,

        width="stretch"

    )





# -------------------------
# PLAYER ANALYSIS
# -------------------------


if player_col:


    st.subheader(
        "⭐ Top Players"
    )


    players=(

        df[player_col]

        .value_counts()

        .head(10)

        .reset_index()

    )


    players.columns=[

        "Player",

        "Awards"

    ]



    fig=px.bar(

        players,

        x="Player",

        y="Awards"

    )


    st.plotly_chart(

        fig,

        width="stretch"

    )





# -------------------------
# DATA TABLE
# -------------------------


st.subheader(
"Dataset Preview"
)


st.dataframe(

    df,

    width="stretch"

)