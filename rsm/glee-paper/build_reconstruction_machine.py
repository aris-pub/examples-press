"""Build reconstruction_machine.html — linked heatmap + graph reconstruction widget.

The Reconstruction Machine lets the reader:
  1. Pick an embedding dimension (segmented buttons)
  2. Drag a threshold theta across the dot-product space
  3. Watch the reconstructed graph update in real time
  4. See live precision, recall, and Frobenius error

This requires linked interactivity beyond what Plotly Python's static
to_html() can express, so we use Plotly.js directly with the data
baked in from the precomputed JSON.
"""

import json
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"
OUT = Path(__file__).parent / "reconstruction_machine.html"

with open(DATA_DIR / "reconstruction_machine.json") as f:
    data = json.load(f)

data_json = json.dumps(data, separators=(",", ":"))
dims = data["dims"]

dim_buttons = "".join(
    f'<button class="rm-dim-btn{" rm-dim-active" if i == 0 else ""}" data-idx="{i}">{d}</button>'
    for i, d in enumerate(dims)
)

html = f"""<style>
.rm-widget {{
  font-family: "Source Sans 3", sans-serif;
  color: #2c3e50;
  max-width: 100%;
  overflow: hidden;
}}
.rm-controls {{
  display: flex;
  align-items: center;
  gap: 20px;
  flex-wrap: wrap;
  padding: 10px 0 6px;
  justify-content: center;
}}
.rm-control-group {{
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
}}
.rm-control-group label {{
  font-weight: 600;
  white-space: nowrap;
}}
.rm-dim-btns {{
  display: flex;
  gap: 0;
  border: 1px solid #c0c8d0;
  border-radius: 5px;
  overflow: hidden;
}}
.rm-dim-btn {{
  background: #f8f9fa;
  border: none;
  border-right: 1px solid #c0c8d0;
  padding: 4px 11px;
  font-size: 12px;
  font-family: inherit;
  font-weight: 500;
  color: #4a5568;
  cursor: pointer;
  transition: background 0.15s, color 0.15s;
}}
.rm-dim-btn:last-child {{ border-right: none; }}
.rm-dim-btn:hover {{ background: #e8ecf0; }}
.rm-dim-btn.rm-dim-active {{
  background: #4a7fb5;
  color: #fff;
  font-weight: 700;
}}
.rm-theta-wrap {{
  display: flex;
  align-items: center;
  gap: 6px;
}}
.rm-theta-slider {{
  -webkit-appearance: none;
  appearance: none;
  width: 180px;
  height: 6px;
  border-radius: 3px;
  background: linear-gradient(to right, #2166ac, #d6604d);
  outline: none;
}}
.rm-theta-slider::-webkit-slider-thumb {{
  -webkit-appearance: none;
  appearance: none;
  width: 16px;
  height: 16px;
  border-radius: 50%;
  background: #fff;
  border: 2px solid #4a7fb5;
  cursor: grab;
  box-shadow: 0 1px 3px rgba(0,0,0,0.2);
}}
.rm-theta-slider::-moz-range-thumb {{
  width: 16px;
  height: 16px;
  border-radius: 50%;
  background: #fff;
  border: 2px solid #4a7fb5;
  cursor: grab;
  box-shadow: 0 1px 3px rgba(0,0,0,0.2);
}}
.rm-theta-val {{
  font-variant-numeric: tabular-nums;
  font-weight: 700;
  font-size: 14px;
  min-width: 3.5em;
  text-align: right;
}}
.rm-stats {{
  display: flex;
  gap: 6px;
  justify-content: center;
  flex-wrap: wrap;
  padding: 4px 0 8px;
}}
.rm-stat {{
  display: inline-flex;
  align-items: center;
  gap: 5px;
  font-size: 12px;
  background: #f4f6f8;
  border: 1px solid #e2e6ea;
  border-radius: 4px;
  padding: 3px 10px;
  font-variant-numeric: tabular-nums;
}}
.rm-stat-val {{
  font-weight: 700;
  font-size: 13px;
}}
.rm-stat-val.rm-good {{ color: #27ae60; }}
.rm-stat-val.rm-bad {{ color: #e74c3c; }}
.rm-stat-val.rm-neutral {{ color: #2c3e50; }}
.rm-panels {{
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 6px;
  width: 100%;
}}
.rm-panel {{
  min-width: 0;
  overflow: hidden;
  border: 1px solid #e8ecf0;
  border-radius: 6px;
  background: #fafbfc;
}}
.rm-panel-head {{
  text-align: center;
  font-size: 12px;
  font-weight: 600;
  padding: 6px 0 2px;
  color: #4a5568;
  letter-spacing: 0.02em;
  text-transform: uppercase;
}}
#rm-heatmap, #rm-graph {{
  width: 100% !important;
  height: 370px !important;
}}
.rm-legend {{
  display: flex;
  gap: 14px;
  justify-content: center;
  font-size: 11px;
  padding: 6px 0 2px;
  color: #5a6672;
}}
.rm-legend-item {{
  display: flex;
  align-items: center;
  gap: 4px;
}}
.rm-legend-swatch {{
  width: 14px;
  height: 3px;
  border-radius: 1px;
}}
@media (max-width: 700px) {{
  .rm-panels {{ grid-template-columns: 1fr; }}
  #rm-heatmap, #rm-graph {{ height: 300px !important; }}
  .rm-theta-slider {{ width: 120px; }}
}}
</style>

<script src="https://cdn.plot.ly/plotly-2.35.2.min.js"></script>

<div class="rm-widget">
  <div class="rm-controls">
    <div class="rm-control-group">
      <label>Dimension <em>d</em>:</label>
      <div class="rm-dim-btns">{dim_buttons}</div>
    </div>
    <div class="rm-control-group">
      <label>Threshold:</label>
      <div class="rm-theta-wrap">
        <input type="range" class="rm-theta-slider" id="rm-theta" min="-1.5" max="0.5" step="0.01" value="-0.5">
        <span class="rm-theta-val" id="rm-theta-val">&theta; = -0.50</span>
      </div>
    </div>
  </div>
  <div class="rm-stats">
    <div class="rm-stat">Precision <span class="rm-stat-val rm-neutral" id="rm-prec">—</span></div>
    <div class="rm-stat">Recall <span class="rm-stat-val rm-neutral" id="rm-rec">—</span></div>
    <div class="rm-stat">Edges predicted <span class="rm-stat-val rm-neutral" id="rm-npred">—</span> / 78</div>
    <div class="rm-stat">Frobenius error <span class="rm-stat-val rm-neutral" id="rm-frob">—</span></div>
  </div>
  <div class="rm-panels">
    <div class="rm-panel">
      <div class="rm-panel-head">Dot-product matrix</div>
      <div id="rm-heatmap"></div>
    </div>
    <div class="rm-panel">
      <div class="rm-panel-head">Reconstructed graph</div>
      <div id="rm-graph"></div>
    </div>
  </div>
  <div class="rm-legend">
    <div class="rm-legend-item"><div class="rm-legend-swatch" style="background:#27ae60"></div>True positive</div>
    <div class="rm-legend-item"><div class="rm-legend-swatch" style="background:#e74c3c"></div>False positive</div>
    <div class="rm-legend-item"><div class="rm-legend-swatch" style="background:#c8cdd2"></div>Missed edge</div>
  </div>
</div>

<script>
(function() {{
  var D = {data_json};
  var n = D.n, adj = D.adjacency, lx = D.layout_x, ly = D.layout_y;
  var clubs = D.clubs, degrees = D.degrees, dims = D.dims;
  var trueEdges = D.edges.length;

  var PURPLE = "#9b59b6", ORANGE = "#e8913a";
  var TP = "#27ae60", FP = "#e74c3c", MISS = "#c8cdd2";

  var nodeColors = clubs.map(function(c) {{ return c === "Mr. Hi" ? PURPLE : ORANGE; }});
  var maxDeg = Math.max.apply(null, degrees);
  var nodeSizes = degrees.map(function(d) {{ return 6 + (d / maxDeg) * 12; }});
  var nodeText = degrees.map(function(d, i) {{ return "Node " + i + " (deg " + d + ", " + clubs[i] + ")"; }});

  var curDim = dims[0], curTheta = -0.5;

  // --- Elements ---
  var thetaSlider = document.getElementById("rm-theta");
  var thetaVal = document.getElementById("rm-theta-val");
  var precEl = document.getElementById("rm-prec");
  var recEl = document.getElementById("rm-rec");
  var npredEl = document.getElementById("rm-npred");
  var frobEl = document.getElementById("rm-frob");
  var dimBtns = document.querySelectorAll(".rm-dim-btn");

  // --- Heatmap ---
  var colorscale = [
    [0, "#2166ac"], [0.15, "#4393c3"], [0.35, "#92c5de"],
    [0.5, "#f7f7f7"],
    [0.65, "#f4a582"], [0.85, "#d6604d"], [1, "#b2182b"]
  ];

  function getDots(dim) {{ return D.dot_matrices[String(dim)]; }}

  Plotly.newPlot("rm-heatmap", [{{
    z: getDots(curDim), type: "heatmap",
    colorscale: colorscale, zmin: -1.5, zmax: 0.5,
    showscale: true,
    colorbar: {{ thickness: 10, len: 0.75, tickfont: {{ size: 9 }}, outlinewidth: 0 }},
    hovertemplate: "(%{{x}}, %{{y}})<br>s<sub>i</sub> &middot; s<sub>j</sub> = %{{z:.3f}}<extra></extra>",
    xgap: 0.5, ygap: 0.5
  }}], {{
    margin: {{ l: 25, r: 45, t: 8, b: 25 }},
    paper_bgcolor: "rgba(0,0,0,0)", plot_bgcolor: "rgba(0,0,0,0)",
    xaxis: {{ showgrid: false, ticks: "", showticklabels: false, constrain: "domain" }},
    yaxis: {{ showgrid: false, ticks: "", autorange: "reversed", showticklabels: false,
              scaleanchor: "x", constrain: "domain" }},
    font: {{ family: "Source Sans 3, sans-serif", size: 10, color: "#2c3e50" }}
  }}, {{ responsive: true, displayModeBar: false }});

  // --- Graph ---
  function buildGraph(dots, theta) {{
    var tpX=[], tpY=[], fpX=[], fpY=[], mX=[], mY=[];
    var tp=0, fp=0, fn=0, frobSq=0;

    for (var i = 0; i < n; i++) {{
      for (var j = i+1; j < n; j++) {{
        var real = adj[i][j] > 0;
        var pred = dots[i][j] < theta;
        var diff = (real?1:0) - (pred?1:0);
        frobSq += diff*diff;
        if (pred && real) {{
          tp++; tpX.push(lx[i],lx[j],null); tpY.push(ly[i],ly[j],null);
        }} else if (pred) {{
          fp++; fpX.push(lx[i],lx[j],null); fpY.push(ly[i],ly[j],null);
        }} else if (real) {{
          fn++; mX.push(lx[i],lx[j],null); mY.push(ly[i],ly[j],null);
        }}
      }}
    }}
    var prec = (tp+fp) > 0 ? tp/(tp+fp) : 1;
    var rec = trueEdges > 0 ? tp/trueEdges : 0;
    return {{
      traces: [
        {{ x:mX, y:mY, mode:"lines", line:{{color:MISS,width:1.2}}, hoverinfo:"skip", showlegend:false }},
        {{ x:fpX, y:fpY, mode:"lines", line:{{color:FP,width:1.8}}, hoverinfo:"skip", showlegend:false }},
        {{ x:tpX, y:tpY, mode:"lines", line:{{color:TP,width:2}}, hoverinfo:"skip", showlegend:false }},
        {{ x:lx, y:ly, mode:"markers",
           marker:{{size:nodeSizes, color:nodeColors, line:{{width:1.5,color:"#fff"}}}},
           text:nodeText, hoverinfo:"text", showlegend:false }}
      ],
      prec: prec, rec: rec, npred: tp+fp, frob: Math.sqrt(frobSq*2)
    }};
  }}

  var gLayout = {{
    margin:{{l:5,r:5,t:8,b:5}},
    paper_bgcolor:"rgba(0,0,0,0)", plot_bgcolor:"rgba(0,0,0,0)",
    xaxis:{{showgrid:false, zeroline:false, showticklabels:false, scaleanchor:"y"}},
    yaxis:{{showgrid:false, zeroline:false, showticklabels:false}},
    hovermode:"closest",
    font:{{family:"Source Sans 3, sans-serif", size:10, color:"#2c3e50"}}
  }};

  var g0 = buildGraph(getDots(curDim), curTheta);
  Plotly.newPlot("rm-graph", g0.traces, gLayout, {{responsive:true, displayModeBar:false}});

  function setStats(r) {{
    precEl.textContent = (r.prec*100).toFixed(1) + "%";
    precEl.className = "rm-stat-val " + (r.prec >= 0.8 ? "rm-good" : r.prec >= 0.5 ? "rm-neutral" : "rm-bad");
    recEl.textContent = (r.rec*100).toFixed(1) + "%";
    recEl.className = "rm-stat-val " + (r.rec >= 0.8 ? "rm-good" : r.rec >= 0.5 ? "rm-neutral" : "rm-bad");
    npredEl.textContent = r.npred;
    frobEl.textContent = r.frob.toFixed(1);
    frobEl.className = "rm-stat-val " + (r.frob < 5 ? "rm-good" : r.frob < 10 ? "rm-neutral" : "rm-bad");
  }}
  setStats(g0);

  function update() {{
    var dots = getDots(curDim);
    Plotly.restyle("rm-heatmap", {{z:[dots]}}, [0]);
    var r = buildGraph(dots, curTheta);
    Plotly.react("rm-graph", r.traces, gLayout, {{responsive:true, displayModeBar:false}});
    setStats(r);
  }}

  dimBtns.forEach(function(btn) {{
    btn.addEventListener("click", function() {{
      dimBtns.forEach(function(b){{ b.classList.remove("rm-dim-active"); }});
      btn.classList.add("rm-dim-active");
      curDim = dims[parseInt(btn.dataset.idx)];
      update();
    }});
  }});

  thetaSlider.addEventListener("input", function() {{
    curTheta = parseFloat(this.value);
    thetaVal.textContent = "\\u03b8 = " + curTheta.toFixed(2);
    update();
  }});
}})();
</script>
"""

OUT.write_text(html)
print(f"Wrote {OUT} ({len(html)} bytes)")
