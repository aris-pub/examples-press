"""Build fig1_simplex.html — 3D simplex geometry hero figure."""

import json
from pathlib import Path

import plotly.graph_objects as go

DATA_DIR = Path(__file__).parent / "data"
OUT = Path(__file__).parent / "fig1_simplex.html"

with open(DATA_DIR / "fig1_simplex.json") as f:
    data = json.load(f)

BLUE = "#4a7fb5"
PURPLE = "#9b59b6"
ORANGE = "#e8913a"


def scene_axis():
    return dict(
        showgrid=False,
        zeroline=False,
        showticklabels=False,
        showspikes=False,
        showline=False,
        title="",
        backgroundcolor="rgba(0,0,0,0)",
    )


def make_scene(eye, up=None):
    return dict(
        xaxis=scene_axis(),
        yaxis=scene_axis(),
        zaxis=scene_axis(),
        bgcolor="rgba(0,0,0,0)",
        camera=dict(eye=eye, up=up or dict(x=0, y=0, z=1)),
        dragmode="orbit",
        aspectmode="data",
    )


def edge_coords(g):
    ex, ey, ez = [], [], []
    for i, j in g["edges"]:
        ex += [g["nodes"]["x"][i], g["nodes"]["x"][j], None]
        ey += [g["nodes"]["y"][i], g["nodes"]["y"][j], None]
        ez += [g["nodes"]["z"][i], g["nodes"]["z"][j], None]
    return ex, ey, ez


def simple_panel(g, eye, up=None):
    ex, ey, ez = edge_coords(g)
    fig = go.Figure()
    fig.add_trace(
        go.Scatter3d(
            x=ex,
            y=ey,
            z=ez,
            mode="lines",
            line=dict(color="rgb(155,165,180)", width=3),
            hoverinfo="skip",
            showlegend=False,
        )
    )
    fig.add_trace(
        go.Scatter3d(
            x=g["nodes"]["x"],
            y=g["nodes"]["y"],
            z=g["nodes"]["z"],
            mode="markers",
            marker=dict(size=8, color=BLUE, line=dict(width=1, color="#fff")),
            hoverinfo="skip",
            showlegend=False,
        )
    )
    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor="rgba(0,0,0,0)",
        scene=make_scene(eye, up),
        showlegend=False,
    )
    return fig


def karate_panel(g, eye):
    n = g["n"]
    deg = g["nodes"]["degree"]
    clubs = g["nodes"]["clubs"]
    min_d, max_d = min(deg), max(deg)
    sizes = [4 + (d - min_d) / (max_d - min_d) * 9 for d in deg]
    colors = [PURPLE if c == "Mr. Hi" else ORANGE for c in clubs]
    labels = g["nodes"]["labels"]
    text = [labels[str(i)] if deg[i] >= 6 else "" for i in range(n)]

    ex, ey, ez = edge_coords(g)
    fig = go.Figure()
    fig.add_trace(
        go.Scatter3d(
            x=ex,
            y=ey,
            z=ez,
            mode="lines",
            line=dict(color="rgb(190,195,200)", width=1.5),
            hoverinfo="skip",
            showlegend=False,
        )
    )
    fig.add_trace(
        go.Scatter3d(
            x=g["nodes"]["x"],
            y=g["nodes"]["y"],
            z=g["nodes"]["z"],
            mode="markers+text",
            text=text,
            textposition="top center",
            textfont=dict(size=9, color="#1a1a2e"),
            marker=dict(size=sizes, color=colors, line=dict(width=1, color="#fff")),
            customdata=list(zip(range(n), deg, clubs)),
            hovertemplate="Node %{customdata[0]}<br>Degree: %{customdata[1]}<br>%{customdata[2]}<extra></extra>",
            showlegend=False,
        )
    )
    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor="rgba(0,0,0,0)",
        scene=make_scene(eye),
        showlegend=False,
    )
    return fig


panels_spec = [
    ("K<sub>3</sub> (triangle)", "triangle", dict(x=0, y=0, z=2.5), dict(x=0, y=1, z=0)),
    ("K<sub>4</sub> (tetrahedron)", "tetrahedron", dict(x=1.8, y=1.2, z=1.2), None),
    ("Karate Club (n=34)", "karate", dict(x=1.6, y=-1.2, z=0.8), None),
]

divs = []
for title, key, eye, up in panels_spec:
    g = data[key]
    div_id = f"fig1-{key}"

    if key == "karate":
        fig = karate_panel(g, eye)
    else:
        fig = simple_panel(g, eye, up)

    inner = fig.to_html(
        full_html=False,
        include_plotlyjs=False,
        div_id=div_id,
        config=dict(responsive=True, displayModeBar=False, scrollZoom=True),
    )
    divs.append(f'<div class="fig1-panel"><div class="fig1-title">{title}</div>{inner}</div>')

css = """<style>
.fig1-wrap {
  display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 4px;
  width: 100%; max-width: 100%; overflow: hidden;
}
.fig1-panel { min-width: 0; overflow: hidden; }
.fig1-title { text-align: center; font-size: 14px; font-weight: 600; color: #1a1a2e; margin-bottom: 2px; }
.fig1-panel .plotly-graph-div { width: 100% !important; height: 320px !important; }
.fig1-panel .js-plotly-plot { width: 100% !important; }
@media (max-width: 700px) { .fig1-wrap { grid-template-columns: 1fr; } }
</style>"""

html = f"""{css}
<script src="https://cdn.plot.ly/plotly-2.35.2.min.js"></script>
<div class="fig1-wrap">
{"".join(divs)}
</div>
"""

OUT.write_text(html)
print(f"Wrote {OUT} ({len(html)} bytes)")
