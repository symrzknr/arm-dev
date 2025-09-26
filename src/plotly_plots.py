import streamlit as st
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go

def get_heatmap_data(df, x, y, c):
    # --- Preprocessing ---
    for col in [x, y, c]:
        if col in df.columns:
            df = df.explode(col)
    if "year" in [x, y, c] or "month" in [x, y, c]:
        df = df.explode("dates")
        df["year"] = df["dates"].str[0:4].astype(int)
        df["month"] = df["dates"].str[5:7].astype(int)

    counts = (
        df.groupby([x, y, c])["name"]
        .apply(lambda x: ", ".join(x.unique()))
        .reset_index(name="names")
    )

    counts["count"] = counts["names"].apply(lambda x: len(x.split(", ")))
    counts["count"] = counts["names"].str.count("<br>") + 1

    # --- Build Subplot Layout (scatter left, bar right) ---
    fig = make_subplots(
        rows=1, cols=2,
        column_widths=[0.85, 0.15],  # narrower bar plot
        horizontal_spacing=0.06,
        shared_yaxes=False
    )

    # --- Scatter (LEFT) ---
    scatter_fig = px.scatter(
        counts,
        x=x,
        y=y,
        color=c,
        custom_data=["names"]
    )

    # Extract color mapping from scatter
    color_map = {}
    for trace in scatter_fig.data:
        color_map[trace.name] = trace.marker.color
        fig.add_trace(trace, row=1, col=1)

    # --- Bar (RIGHT, aligned colors, with percentage labels) ---
    c_distribution = counts.groupby(c, as_index=False)["count"].sum()
    total = c_distribution["count"].sum()
    c_distribution["pct"] = (c_distribution["count"] / total * 100).round(0).astype(int)

    for _, row in c_distribution.iterrows():
        fig.add_trace(
            go.Bar(
                x=["Distribution"],
                y=[row["pct"]],
                name=str(row[c]),
                marker_color=color_map.get(str(row[c]), "#CCCCCC"),
                orientation="v",
                text=f"{row['pct']}%",
                textposition="inside",        # 👈 puts text inside bar
                insidetextanchor="middle",    # 👈 vertically center inside bar
                textfont=dict(size=12, color="black"),  # small text inside bars
                hovertemplate=(
                    f"{c}: {row[c]}<br>"
                    f"Count: {row['count']}<br>"
                    f"Share: {row['pct']}%<extra></extra>"
                ),
                showlegend=False  # legend only for scatter
            ),
            row=1, col=2
        )

    # --- Layout & Style ---
    grid_color = "#333333"

    fig.update_traces(
        marker=dict(size=16, opacity=0.9, symbol="circle"),
        hovertemplate="%{customdata[0]}",
        selector=dict(type="scatter")
    )

    fig.update_layout(
        barmode="stack",
        plot_bgcolor="#192130",
        paper_bgcolor="#192130",
        font=dict(color="white"),
        margin=dict(l=60, r=60, t=60, b=70),
        autosize=True,
        height=None,
        legend=dict(
            title=c,
            orientation="h",
            x=0.3,             # 👈 center horizontally
            y=-0.05,           # closer to bottom
            xanchor="center",
            yanchor="top",
            bgcolor="rgba(0,0,0,0)",
        )
    )

    # Left subplot (scatter) axis styling
    fig.update_xaxes(
        title="",
        tickmode="linear",
        tickfont=dict(color="white"),
        showgrid=True,
        gridwidth=1,
        gridcolor=grid_color,
        zeroline=False,
        side="top",
        row=1, col=1
    )
    fig.update_yaxes(
        title="",
        tickmode="linear",
        dtick=1,
        tickfont=dict(color="white"),
        showgrid=True,
        gridwidth=1,
        gridcolor=grid_color,
        zeroline=False,
        autorange="reversed",
        row=1, col=1
    )

    # Right subplot (bar) axis styling
    fig.update_yaxes(
        title="Share (%)",
        range=[0, 100],
        tickformat=".0f",
        ticksuffix="%",
        tickfont=dict(color="white"),
        gridcolor=grid_color,
        showgrid=True,
        row=1, col=2
    )
    fig.update_xaxes(
        showticklabels=False,
        row=1, col=2
    )

    return fig
