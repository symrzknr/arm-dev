import plotly.express as px
import streamlit as st

def get_heatmap_data(df, x, y, c):

    for col in [x,y,c]:
        if col in df.columns:
            df = df.explode(col)
    if 'year' in [x,y,c] or 'month' in [x,y,c]:
        df = df.explode("dates")

        df["year"] = df["dates"].str[0:4].astype(int)
        df["month"] = df["dates"].str[5:7].astype(int)

    counts = (
        df.groupby([x,y,c])["name"]
        .apply(lambda x: ", ".join(x.unique()))  # collect names in that bucket
        .reset_index(name="names")
    )
    counts["count"] = counts["names"].apply(lambda x: len(x.split(", ")))
    counts["count"] = counts["names"].str.count("<br>") + 1
    
    fig = px.scatter(
        counts,
        x=x,
        y=y,
        color=c,
        custom_data=["names"],
        # color_discrete_sequence=["#FFA500"],  # orange
    )

    # Make markers fixed size (like GitHub squares)
    fig.update_traces(
        marker=dict(size=16, opacity=0.9, symbol="circle"),
        hovertemplate="%{customdata[0]}"   # 👈 names displayed here
    )

    # --- GRIDLINES STYLE ---
    grid_color = "#333333"  # slightly darker than background (#192130)

    fig.update_layout(
        xaxis=dict(
            title="",
            tickmode="linear",
            tickfont=dict(color="white"),
            showgrid=True,
            gridwidth=1,
            gridcolor=grid_color,
            zeroline=False,
            side="top"           # 👈 move x-axis to top
        ),
        yaxis=dict(
            title="",
            tickmode="linear",
            dtick=1,
            tickfont=dict(color="white"),
            showgrid=True,
            gridwidth=1,
            gridcolor=grid_color,
            zeroline=False,
            autorange="reversed" # 👈 flip y-axis
        ),
        plot_bgcolor="#192130",  # custom dark blue background
        paper_bgcolor="#192130",
        margin=dict(l=80, r=80, t=60, b=60),
        font=dict(color="white")
    )

    fig.update_layout(
        autosize=True,  # let Plotly fill the available space
        height=None,    # remove fixed height
    )

    return fig