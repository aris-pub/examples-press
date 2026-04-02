"""Build fig3_linkpred.html — link prediction AUC across dimensions and datasets.

Matches Fig. 3 of the GLEE paper: one panel per dataset, AUC vs log2(d),
with error bars from multiple realizations.
"""

import json
import math
from pathlib import Path

import plotly.graph_objects as go
from plotly.subplots import make_subplots

DATA_DIR = Path(__file__).parent / "data"
OUT = Path(__file__).parent / "fig3_linkpred.html"

with open(DATA_DIR / "fig3_linkpred.json") as f:
    data = json.load(f)

COLORS = {"GLEE": "#9b59b6", "LE": "#4a7fb5", "node2vec": "#e8913a", "NetMF": "#27ae60"}
DATASET_ORDER = ["PPI", "wiki-Vote", "caida", "CA-HepTh", "CA-GrQc"]
METHOD_NAMES = ["LE", "node2vec", "GLEE", "NetMF"]

fig = make_subplots(
    rows=1,
    cols=len(DATASET_ORDER),
    shared_yaxes=True,
    column_titles=DATASET_ORDER,
    horizontal_spacing=0.03,
)

for col, ds_name in enumerate(DATASET_ORDER, 1):
    ds = data[ds_name]
    dims = ds["dims"]
    log_dims = [math.log2(d) for d in dims]

    for method in METHOD_NAMES:
        method_data = ds[method]
        means = [method_data[str(d)]["mean"] for d in dims]
        stds = [method_data[str(d)]["std"] for d in dims]

        fig.add_trace(
            go.Scatter(
                x=log_dims,
                y=means,
                error_y=dict(type="data", array=stds, visible=True, thickness=1.2, width=3),
                mode="lines+markers",
                name=method,
                line=dict(color=COLORS[method], width=2),
                marker=dict(size=6, color=COLORS[method]),
                showlegend=(col == len(DATASET_ORDER)),
                legendgroup=method,
                hovertemplate=f"{method}<br>d=%{{x:.0f}}<br>AUC=%{{y:.3f}}<extra></extra>",
            ),
            row=1,
            col=col,
        )

for col in range(1, len(DATASET_ORDER) + 1):
    fig.update_xaxes(
        tickvals=[math.log2(d) for d in [32, 64, 128, 256, 512]],
        ticktext=["5", "6", "7", "8", "9"],
        row=1,
        col=col,
    )

fig.update_yaxes(range=[0.2, 1.02], row=1, col=1)

fig.update_layout(
    font=dict(family="Source Sans 3, sans-serif", color="#2c3e50", size=11),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    legend=dict(
        x=0.92,
        y=0.95,
        bgcolor="rgba(255,255,255,0.9)",
        bordercolor="#ddd",
        borderwidth=1,
        font=dict(size=11),
    ),
    margin=dict(l=50, r=80, t=40, b=50),
    width=900,
    height=300,
    hovermode="closest",
)

fig.add_annotation(
    text="Dimension log<sub>2</sub> d",
    x=0.5,
    y=-0.12,
    xref="paper",
    yref="paper",
    showarrow=False,
    font=dict(size=12, color="#2c3e50"),
)
fig.add_annotation(
    text="AUC",
    x=-0.04,
    y=0.5,
    xref="paper",
    yref="paper",
    showarrow=False,
    textangle=-90,
    font=dict(size=12, color="#2c3e50"),
)

html = fig.to_html(
    full_html=False, include_plotlyjs="cdn", config=dict(responsive=True, displayModeBar=False)
)
OUT.write_text(html)
print(f"Wrote {OUT} ({len(html)} bytes)")
