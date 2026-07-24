import os
import streamlit as st
import pandas as pd
import plotly.express as px


# ======================================================
# PAGE CONFIG
# ======================================================

st.set_page_config(
    page_title="IPL Complete Analytics Dashboard",
    page_icon="🏏",
    layout="wide"
)


# ======================================================
# LOAD CSS
# ======================================================

def load_css():

    css_path = os.path.join(
        os.path.dirname(__file__),
        "..",
        "style.css"
    )

    if os.path.exists(css_path):

        with open(css_path, encoding="utf-8") as f:

            st.markdown(
                f"<style>{f.read()}</style>",
                unsafe_allow_html=True
            )


load_css()



# ======================================================
# LOAD DATA
# ======================================================

@st.cache_data
def load_data():

    PROJECT_ROOT = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "..",
            ".."
        )
    )


    dataset_path = os.path.join(
        PROJECT_ROOT,
        "data",
        "processed",
        "ipl_cleaned.csv"
    )


    if os.path.exists(dataset_path):

        return pd.read_csv(
            dataset_path,
            low_memory=False
        )


    st.error("❌ IPL Dataset Not Found")

    st.code(dataset_path)

    st.stop()



df = load_data()



# ======================================================
# CLEAN COLUMNS
# ======================================================

df.columns = (
    df.columns
    .str.lower()
    .str.strip()
)



# ======================================================
# FIND COLUMN
# ======================================================

def find_col(names):

    for col in names:

        if col in df.columns:

            return col

    return None



# ======================================================
# COLUMN MAPPING
# ======================================================

match_col = find_col(
    ["match_id"]
)


season_col = find_col(
    ["season","year"]
)


winner_col = find_col(
    ["winner"]
)


team1_col = find_col(
    ["team1"]
)


team2_col = find_col(
    ["team2"]
)


venue_col = find_col(
    ["venue"]
)


runs_col = find_col(
    [
        "runs_scored",
        "total_runs",
        "runs"
    ]
)


player_col = find_col(
    ["player_of_match"]
)



# ======================================================
# TITLE
# ======================================================

st.title(
    "🏏 IPL Complete Analytics Dashboard"
)



# ======================================================
# SIDEBAR FILTERS
# ======================================================

st.sidebar.header(
    "Filters"
)


if season_col:

    seasons = sorted(
        df[season_col]
        .dropna()
        .astype(str)
        .unique()
    )


    selected_season = st.sidebar.selectbox(
        "Season",
        ["All"] + list(seasons)
    )


    if selected_season != "All":

        df = df[
            df[season_col]
            .astype(str)
            ==
            selected_season
        ]



if team1_col and team2_col:

    all_teams = sorted(
        pd.concat(
            [
                df[team1_col],
                df[team2_col]
            ]
        )
        .dropna()
        .unique()
    )


    selected_team = st.sidebar.selectbox(
        "Team",
        ["All"] + list(all_teams)
    )


    if selected_team != "All":

        df = df[
            (df[team1_col] == selected_team) |
            (df[team2_col] == selected_team)
        ]



# ======================================================
# KPI CARDS
# ======================================================

col1,col2,col3,col4 = st.columns(4)


with col1:

    st.metric(
        "Matches",
        df[match_col].nunique()
        if match_col else len(df)
    )


with col2:

    st.metric(
        "Seasons",
        df[season_col].nunique()
        if season_col else 0
    )


with col3:

    if team1_col and team2_col:

        teams_count = pd.concat(
            [
                df[team1_col],
                df[team2_col]
            ]
        ).nunique()


        st.metric(
            "Teams",
            teams_count
        )


with col4:

    if runs_col:

        total_runs = pd.to_numeric(
            df[runs_col],
            errors="coerce"
        ).sum()


        st.metric(
            "Total Runs",
            int(total_runs)
        )
        # ======================================================
# WINNING TEAM ANALYSIS
# ======================================================

if winner_col:

    st.subheader(
        "🏆 Winning Teams"
    )


    wins = (
        df[winner_col]
        .dropna()
        .value_counts()
        .reset_index()
    )


    wins.columns = [
        "Team",
        "Wins"
    ]


    fig = px.bar(
        wins,
        x="Team",
        y="Wins",
        color="Wins",
        title="Most Successful IPL Teams"
    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )



# ======================================================
# TEAM PARTICIPATION
# ======================================================

if team1_col and team2_col:

    st.subheader(
        "📊 Team Participation"
    )


    teams = pd.concat(
        [
            df[team1_col],
            df[team2_col]
        ]
    )


    team_df = (
        teams
        .dropna()
        .value_counts()
        .reset_index()
    )


    team_df.columns = [
        "Team",
        "Matches"
    ]


    fig = px.pie(
        team_df,
        names="Team",
        values="Matches",
        title="Matches Played By Teams"
    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )



# ======================================================
# TEAM WISE RUNS
# ======================================================

if "batting_team" in df.columns and runs_col:


    st.subheader(
        "🏏 Team Wise Total Runs"
    )


    team_runs = (
        df.groupby("batting_team")[runs_col]
        .sum()
        .sort_values(
            ascending=False
        )
        .reset_index()
    )


    team_runs.columns = [
        "Team",
        "Runs"
    ]


    fig = px.bar(
        team_runs,
        x="Team",
        y="Runs",
        color="Runs",
        title="Total Runs Scored By Teams"
    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )



# ======================================================
# TOP PLAYER OF MATCH
# ======================================================

if player_col:


    st.subheader(
        "⭐ Top Player Of Match Awards"
    )


    players = (
        df[player_col]
        .dropna()
        .value_counts()
        .head(10)
        .reset_index()
    )


    players.columns = [
        "Player",
        "Awards"
    ]


    fig = px.bar(
        players,
        x="Player",
        y="Awards",
        color="Awards",
        title="Most Player Of Match Awards"
    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )



# ======================================================
# TOP RUN SCORERS
# ======================================================

if runs_col and "batter" in df.columns:


    st.subheader(
        "🏏 Top Run Scorers"
    )


    batsmen = (
        df.groupby("batter")[runs_col]
        .sum()
        .sort_values(
            ascending=False
        )
        .head(10)
        .reset_index()
    )


    batsmen.columns = [
        "Batter",
        "Runs"
    ]


    fig = px.bar(
        batsmen,
        x="Batter",
        y="Runs",
        color="Runs",
        title="Highest Run Scorers"
    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )



# ======================================================
# FOOTER
# ======================================================

st.markdown("---")


st.caption(
    "Built using Python • SQL • Pandas • Plotly • Streamlit"
)
