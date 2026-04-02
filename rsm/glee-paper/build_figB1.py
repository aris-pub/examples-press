"""Build figB1_estimators.html — estimator comparison across random graph models."""

import json
from pathlib import Path

import plotly.graph_objects as go

DATA_DIR = Path(__file__).parent / "data"
OUT = Path(__file__).parent / "figB1_estimators.html"

with open(DATA_DIR / "figB1_estimators.json") as f:
    data = json.load(f)

COLORS = {"ER": "#9b59b6", "BA": "#4a7fb5"}

fig = go.Figure()
for model, d in data.items():
    fig.add_trace(
        go.Scatter(
            x=d["dims"],
            y=d["theta_c_mean"],
            mode="lines+markers",
            name=f"{model} (\u03b8_c = -0.5)",
            line=dict(color=COLORS[model], width=2.5),
            marker=dict(size=7, color=COLORS[model]),
            error_y=dict(
                type="data",
                array=d["theta_c_std"],
                visible=True,
                color=COLORS[model],
                thickness=1.5,
                width=4,
            ),
        )
    )

fig.update_layout(
    xaxis=dict(title="Embedding dimension", type="log", dtick="D1", gridcolor="#eef0f2"),
    yaxis=dict(title="Reconstruction error (Frobenius norm)", gridcolor="#eef0f2"),
    legend=dict(x=0.6, y=0.95, bgcolor="rgba(255,255,255,0.8)", bordercolor="#ddd", borderwidth=1),
    margin=dict(l=60, r=20, t=10, b=50),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Source Sans 3, sans-serif", color="#2c3e50"),
    hovermode="x unified",
    width=640,
    height=380,
)

html = fig.to_html(
    full_html=False, include_plotlyjs="cdn", config=dict(responsive=True, displayModeBar=False)
)
OUT.write_text(html)
print(f"Wrote {OUT} ({len(html)} bytes)")
