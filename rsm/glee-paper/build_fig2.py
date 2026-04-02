"""Build fig2_reconstruction.html — precision at k grid across datasets and dimensions.

Matches Fig. 2 of the GLEE paper: columns = datasets (ordered by clustering
coefficient), rows = embedding dimensions, lines = methods.
"""

import json
from pathlib import Path

import plotly.graph_objects as go
from plotly.subplots import make_subplots

DATA_DIR = Path(__file__).parent / "data"
OUT = Path(__file__).parent / "fig2_reconstruction.html"

with open(DATA_DIR / "fig2_reconstruction.json") as f:
    data = json.load(f)

COLORS = {"GLEE": "#9b59b6", "LE": "#4a7fb5", "node2vec": "#e8913a", "NetMF": "#27ae60"}
DATASET_ORDER = ["PPI", "wiki-Vote", "caida", "CA-HepTh", "CA-GrQc"]
DIMS = ["12", "128", "512"]
METHOD_NAMES = ["LE", "node2vec", "GLEE", "NetMF"]

fig = make_subplots(
    rows=len(DIMS),
    cols=len(DATASET_ORDER),
    shared_xaxes=True,
    shared_yaxes=True,
    column_titles=DATASET_ORDER,
    row_titles=[f"d={d}" for d in DIMS],
    vertical_spacing=0.06,
    horizontal_spacing=0.03,
)

for col, ds_name in enumerate(DATASET_ORDER, 1):
    ds = data[ds_name]
    k_values = ds["k_values"]
    n_pairs = k_values[-1] if k_values else 1
    k_norm = [k / n_pairs for k in k_values]

    for row, d in enumerate(DIMS, 1):
        for method in METHOD_NAMES:
            precs = ds[method].get(d, [])
            if not precs:
                continue
            fig.add_trace(
                go.Scatter(
                    x=k_norm,
                    y=precs,
                    mode="lines",
                    name=method,
                    line=dict(color=COLORS[method], width=1.8),
                    showlegend=(row == 1 and col == len(DATASET_ORDER)),
                    legendgroup=method,
                    hovertemplate=f"{method}<br>k/total=%{{x:.2f}}<br>prec=%{{y:.3f}}<extra></extra>",
                ),
                row=row,
                col=col,
            )

for row in range(1, len(DIMS) + 1):
    for col in range(1, len(DATASET_ORDER) + 1):
        fig.update_xaxes(range=[0, 1], row=row, col=col, showticklabels=(row == len(DIMS)))
        fig.update_yaxes(range=[0, 1.05], row=row, col=col, showticklabels=(col == 1))

fig.update_layout(
    font=dict(family="Source Sans 3, sans-serif", color="#2c3e50", size=11),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    legend=dict(
        x=0.92,
        y=0.5,
        bgcolor="rgba(255,255,255,0.9)",
        bordercolor="#ddd",
        borderwidth=1,
        font=dict(size=11),
    ),
    margin=dict(l=50, r=80, t=40, b=50),
    width=900,
    height=550,
    hovermode="closest",
)

# Axis labels
fig.add_annotation(
    text="k (fraction of all pairs)",
    x=0.5,
    y=-0.06,
    xref="paper",
    yref="paper",
    showarrow=False,
    font=dict(size=12, color="#2c3e50"),
)
fig.add_annotation(
    text="Precision at k",
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
