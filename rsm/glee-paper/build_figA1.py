"""Build figA1_dotproducts.html — dot product distributions with dimension slider."""

import json
from pathlib import Path

import plotly.graph_objects as go

DATA_DIR = Path(__file__).parent / "data"
OUT = Path(__file__).parent / "figA1_dotproducts.html"

with open(DATA_DIR / "figA1_dotproducts.json") as f:
    data = json.load(f)

EDGE_COLOR = "#9b59b6"
NONEDGE_COLOR = "#4a7fb5"

dims = sorted(data.keys(), key=int)
fig = go.Figure()

for i, dim in enumerate(dims):
    d = data[dim]
    visible = i == 0
    fig.add_trace(
        go.Histogram(
            x=d["nonedge_dots"],
            name="Non-edges",
            opacity=0.6,
            marker_color=NONEDGE_COLOR,
            nbinsx=30,
            visible=visible,
            showlegend=(i == 0),
            legendgroup="nonedge",
        )
    )
    fig.add_trace(
        go.Histogram(
            x=d["edge_dots"],
            name="Edges",
            opacity=0.7,
            marker_color=EDGE_COLOR,
            nbinsx=20,
            visible=visible,
            showlegend=(i == 0),
            legendgroup="edge",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=[d["theta_c"], d["theta_c"]],
            y=[0, 50],
            mode="lines",
            name=f"\u03b8_c = {d['theta_c']}",
            line=dict(color="#e74c3c", width=2, dash="dash"),
            visible=visible,
            showlegend=(i == 0),
            legendgroup="theta",
        )
    )

# Slider steps: each dim has 3 traces
steps = []
for i, dim in enumerate(dims):
    vis = [False] * len(fig.data)
    for j in range(3):
        vis[i * 3 + j] = True
    steps.append(dict(label=str(dim), method="update", args=[{"visible": vis}]))

fig.update_layout(
    barmode="overlay",
    xaxis=dict(title="Dot product", gridcolor="#eef0f2"),
    yaxis=dict(title="Count", gridcolor="#eef0f2"),
    legend=dict(
        x=0.02, y=0.95, bgcolor="rgba(255,255,255,0.8)", bordercolor="#ddd", borderwidth=1
    ),
    margin=dict(l=55, r=20, t=10, b=50),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Source Sans 3, sans-serif", color="#2c3e50"),
    sliders=[
        dict(
            active=0,
            pad=dict(t=40),
            currentvalue=dict(prefix="Dimension: ", font=dict(size=14, color="#2c3e50")),
            steps=steps,
        )
    ],
    width=640,
    height=420,
)

html = fig.to_html(
    full_html=False, include_plotlyjs="cdn", config=dict(responsive=True, displayModeBar=False)
)
OUT.write_text(html)
print(f"Wrote {OUT} ({len(html)} bytes)")
