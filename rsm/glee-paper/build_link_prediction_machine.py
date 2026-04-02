"""Build link_prediction_machine.html — interactive edge classification ROC widget.

The reader can:
  1. Pick an embedding dimension
  2. Drag a threshold to classify node pairs as edges or non-edges
  3. Watch the ROC curve trace and see the operating point move
  4. See correctly/incorrectly predicted edges light up on the graph

Uses the full graph's GLEE embedding. The task: given dot products from
the embedding, can we rank all node pairs so that true edges score
higher (more negative dot product) than non-edges?
"""

import json
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"
OUT = Path(__file__).parent / "link_prediction_machine.html"

with open(DATA_DIR / "link_prediction_machine.json") as f:
    data = json.load(f)

data_json = json.dumps(data, separators=(",", ":"))
dims = data["dims"]
n_edges = len(data["edges"])
n_pairs = len(data["all_pairs"])
n_nonedges = n_pairs - n_edges

dim_buttons = "".join(
    f'<button class="lp-dim-btn{" lp-dim-active" if i == 0 else ""}" data-idx="{i}">{d}</button>'
    for i, d in enumerate(dims)
)

html = f"""<style>
.lp-widget {{
  font-family: "Source Sans 3", sans-serif;
  color: #2c3e50;
  max-width: 100%;
  overflow: hidden;
}}
.lp-controls {{
  display: flex;
  align-items: center;
  gap: 20px;
  flex-wrap: wrap;
  padding: 10px 0 6px;
  justify-content: center;
}}
.lp-control-group {{
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
}}
.lp-control-group label {{
  font-weight: 600;
  white-space: nowrap;
}}
.lp-dim-btns {{
  display: flex;
  gap: 0;
  border: 1px solid #c0c8d0;
  border-radius: 5px;
  overflow: hidden;
}}
.lp-dim-btn {{
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
.lp-dim-btn:last-child {{ border-right: none; }}
.lp-dim-btn:hover {{ background: #e8ecf0; }}
.lp-dim-btn.lp-dim-active {{
  background: #4a7fb5;
  color: #fff;
  font-weight: 700;
}}
.lp-theta-wrap {{
  display: flex;
  align-items: center;
  gap: 6px;
}}
.lp-theta-slider {{
  -webkit-appearance: none;
  appearance: none;
  width: 180px;
  height: 6px;
  border-radius: 3px;
  background: linear-gradient(to right, #2166ac, #d6604d);
  outline: none;
}}
.lp-theta-slider::-webkit-slider-thumb {{
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
.lp-theta-slider::-moz-range-thumb {{
  width: 16px;
  height: 16px;
  border-radius: 50%;
  background: #fff;
  border: 2px solid #4a7fb5;
  cursor: grab;
  box-shadow: 0 1px 3px rgba(0,0,0,0.2);
}}
.lp-theta-val {{
  font-variant-numeric: tabular-nums;
  font-weight: 700;
  font-size: 14px;
  min-width: 3.5em;
  text-align: right;
}}
.lp-stats {{
  display: flex;
  gap: 6px;
  justify-content: center;
  flex-wrap: wrap;
  padding: 4px 0 8px;
}}
.lp-stat {{
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
.lp-stat-val {{
  font-weight: 700;
  font-size: 13px;
}}
.lp-stat-val.lp-good {{ color: #27ae60; }}
.lp-stat-val.lp-neutral {{ color: #2c3e50; }}
.lp-stat-val.lp-bad {{ color: #e74c3c; }}
.lp-panels {{
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 6px;
  width: 100%;
}}
.lp-panel {{
  min-width: 0;
  overflow: hidden;
  border: 1px solid #e8ecf0;
  border-radius: 6px;
  background: #fafbfc;
}}
.lp-panel-head {{
  text-align: center;
  font-size: 12px;
  font-weight: 600;
  padding: 6px 0 2px;
  color: #4a5568;
  letter-spacing: 0.02em;
  text-transform: uppercase;
}}
#lp-graph, #lp-roc {{
  width: 100% !important;
  height: 370px !important;
}}
.lp-legend {{
  display: flex;
  gap: 14px;
  justify-content: center;
  font-size: 11px;
  padding: 6px 0 2px;
  color: #5a6672;
}}
.lp-legend-item {{
  display: flex;
  align-items: center;
  gap: 4px;
}}
.lp-legend-swatch {{
  width: 14px;
  height: 3px;
  border-radius: 1px;
}}
@media (max-width: 700px) {{
  .lp-panels {{ grid-template-columns: 1fr; }}
  #lp-graph, #lp-roc {{ height: 300px !important; }}
  .lp-theta-slider {{ width: 120px; }}
}}
</style>

<script src="https://cdn.plot.ly/plotly-2.35.2.min.js"></script>

<div class="lp-widget">
  <div class="lp-controls">
    <div class="lp-control-group">
      <label>Dimension <em>d</em>:</label>
      <div class="lp-dim-btns">{dim_buttons}</div>
    </div>
    <div class="lp-control-group">
      <label>Threshold:</label>
      <div class="lp-theta-wrap">
        <input type="range" class="lp-theta-slider" id="lp-theta" min="-1.5" max="0.5" step="0.01" value="-0.5">
        <span class="lp-theta-val" id="lp-theta-val">&theta; = -0.50</span>
      </div>
    </div>
  </div>
  <div class="lp-stats">
    <div class="lp-stat">AUC <span class="lp-stat-val lp-neutral" id="lp-auc">--</span></div>
    <div class="lp-stat">True pos <span class="lp-stat-val lp-neutral" id="lp-tp">--</span> / {n_edges}</div>
    <div class="lp-stat">False pos <span class="lp-stat-val lp-neutral" id="lp-fp">--</span> / {n_nonedges}</div>
    <div class="lp-stat">Precision <span class="lp-stat-val lp-neutral" id="lp-prec">--</span></div>
  </div>
  <div class="lp-panels">
    <div class="lp-panel">
      <div class="lp-panel-head">Edge classification</div>
      <div id="lp-graph"></div>
    </div>
    <div class="lp-panel">
      <div class="lp-panel-head">ROC Curve</div>
      <div id="lp-roc"></div>
    </div>
  </div>
  <div class="lp-legend">
    <div class="lp-legend-item"><div class="lp-legend-swatch" style="background:#27ae60"></div>Correctly predicted edge</div>
    <div class="lp-legend-item"><div class="lp-legend-swatch" style="background:#e74c3c"></div>False positive</div>
    <div class="lp-legend-item"><div class="lp-legend-swatch" style="background:#c8cdd2"></div>Missed edge</div>
  </div>
</div>

<script>
(function() {{
  var D = {data_json};
  var n = D.n, dims = D.dims;
  var lx = D.layout_x, ly = D.layout_y;
  var clubs = D.clubs, degrees = D.degrees;
  var allPairs = D.all_pairs;
  var nEdges = D.edges.length;
  var nNonEdges = allPairs.length - nEdges;

  var PURPLE = "#9b59b6", ORANGE = "#e8913a";
  var TP_C = "#27ae60", FP_C = "#e74c3c", MISS_C = "#c8cdd2";

  var nodeColors = clubs.map(function(c){{ return c==="Mr. Hi" ? PURPLE : ORANGE; }});
  var maxDeg = Math.max.apply(null, degrees);
  var nodeSizes = degrees.map(function(d){{ return 6 + (d/maxDeg)*12; }});
  var nodeText = degrees.map(function(d,i){{ return "Node "+i+" (deg "+d+", "+clubs[i]+")"; }});

  var curDim = dims[0], curTheta = -0.5;

  var thetaSlider = document.getElementById("lp-theta");
  var thetaVal = document.getElementById("lp-theta-val");
  var aucEl = document.getElementById("lp-auc");
  var tpEl = document.getElementById("lp-tp");
  var fpEl = document.getElementById("lp-fp");
  var precEl = document.getElementById("lp-prec");
  var dimBtns = document.querySelectorAll(".lp-dim-btn");

  function getDots(dim) {{ return D.dot_matrices[String(dim)]; }}

  // Compute ROC curve for current dimension
  function computeROC(dots) {{
    // Score each pair: negate dot product (more negative dot = more likely edge)
    var scored = allPairs.map(function(p) {{
      return {{ i: p[0], j: p[1], label: p[2], score: -dots[p[0]][p[1]] }};
    }});
    scored.sort(function(a, b) {{ return b.score - a.score; }});

    var fpr = [0], tpr = [0];
    var tp = 0, fp = 0;
    for (var k = 0; k < scored.length; k++) {{
      if (scored[k].label === 1) tp++;
      else fp++;
      tpr.push(tp / nEdges);
      fpr.push(fp / nNonEdges);
    }}
    var auc = 0;
    for (var k = 1; k < fpr.length; k++) {{
      auc += (fpr[k] - fpr[k-1]) * (tpr[k] + tpr[k-1]) / 2;
    }}
    return {{ fpr: fpr, tpr: tpr, auc: auc }};
  }}

  // Build graph traces: edges colored by prediction status at threshold
  function buildGraph(dots, theta) {{
    var tpX=[], tpY=[], fpX=[], fpY=[], mX=[], mY=[];
    var tp=0, fp=0;

    for (var k = 0; k < allPairs.length; k++) {{
      var p = allPairs[k];
      var i = p[0], j = p[1], isEdge = p[2];
      var predicted = dots[i][j] < theta;

      if (predicted && isEdge) {{
        tp++;
        tpX.push(lx[i],lx[j],null); tpY.push(ly[i],ly[j],null);
      }} else if (predicted && !isEdge) {{
        fp++;
        fpX.push(lx[i],lx[j],null); fpY.push(ly[i],ly[j],null);
      }} else if (!predicted && isEdge) {{
        mX.push(lx[i],lx[j],null); mY.push(ly[i],ly[j],null);
      }}
    }}

    var prec = (tp+fp) > 0 ? tp/(tp+fp) : 1;
    return {{
      traces: [
        {{x:mX, y:mY, mode:"lines", line:{{color:MISS_C, width:1.2}}, hoverinfo:"skip", showlegend:false}},
        {{x:fpX, y:fpY, mode:"lines", line:{{color:FP_C, width:1.8}}, hoverinfo:"skip", showlegend:false}},
        {{x:tpX, y:tpY, mode:"lines", line:{{color:TP_C, width:2}}, hoverinfo:"skip", showlegend:false}},
        {{x:lx, y:ly, mode:"markers",
          marker:{{size:nodeSizes, color:nodeColors, line:{{width:1.5, color:"#fff"}}}},
          text:nodeText, hoverinfo:"text", showlegend:false}}
      ],
      tp: tp, fp: fp, prec: prec
    }};
  }}

  function getOperatingPoint(dots, theta) {{
    var tp=0, fp=0;
    for (var k = 0; k < allPairs.length; k++) {{
      var p = allPairs[k];
      if (dots[p[0]][p[1]] < theta) {{
        if (p[2]) tp++; else fp++;
      }}
    }}
    return {{ fpr: fp/nNonEdges, tpr: tp/nEdges }};
  }}

  var gLayout = {{
    margin:{{l:5,r:5,t:8,b:5}},
    paper_bgcolor:"rgba(0,0,0,0)", plot_bgcolor:"rgba(0,0,0,0)",
    xaxis:{{showgrid:false, zeroline:false, showticklabels:false, scaleanchor:"y"}},
    yaxis:{{showgrid:false, zeroline:false, showticklabels:false}},
    hovermode:"closest",
    font:{{family:"Source Sans 3, sans-serif", size:10, color:"#2c3e50"}}
  }};

  var rocLayout = {{
    margin:{{l:50,r:15,t:8,b:45}},
    paper_bgcolor:"rgba(0,0,0,0)", plot_bgcolor:"rgba(0,0,0,0)",
    xaxis:{{title:"False positive rate", range:[-0.02,1.02], gridcolor:"#eaedf0",
            zeroline:false, dtick:0.2}},
    yaxis:{{title:"True positive rate", range:[-0.02,1.02], gridcolor:"#eaedf0",
            zeroline:false, dtick:0.2, scaleanchor:"x"}},
    font:{{family:"Source Sans 3, sans-serif", size:11, color:"#2c3e50"}},
    hovermode:false,
    shapes:[{{
      type:"line", x0:0, y0:0, x1:1, y1:1,
      line:{{color:"#c0c8d0", width:1, dash:"dot"}}
    }}]
  }};

  var dots0 = getDots(curDim);
  var roc0 = computeROC(dots0);
  var g0 = buildGraph(dots0, curTheta);
  var op0 = getOperatingPoint(dots0, curTheta);

  Plotly.newPlot("lp-graph", g0.traces, gLayout, {{responsive:true, displayModeBar:false}});

  Plotly.newPlot("lp-roc", [
    {{x:roc0.fpr, y:roc0.tpr, mode:"lines", line:{{color:"#4a7fb5", width:2.5}},
      fill:"tozeroy", fillcolor:"rgba(74,127,181,0.08)",
      hoverinfo:"skip", showlegend:false}},
    {{x:[op0.fpr], y:[op0.tpr], mode:"markers",
      marker:{{size:10, color:"#e74c3c", line:{{width:2, color:"#fff"}}}},
      hoverinfo:"skip", showlegend:false}}
  ], rocLayout, {{responsive:true, displayModeBar:false}});

  function setStats(auc, tp, fp, prec) {{
    aucEl.textContent = auc.toFixed(3);
    aucEl.className = "lp-stat-val " + (auc >= 0.9 ? "lp-good" : auc >= 0.7 ? "lp-neutral" : "lp-bad");
    tpEl.textContent = tp;
    tpEl.className = "lp-stat-val " + (tp >= nEdges*0.8 ? "lp-good" : tp >= nEdges*0.4 ? "lp-neutral" : "lp-bad");
    fpEl.textContent = fp;
    fpEl.className = "lp-stat-val " + (fp <= 5 ? "lp-good" : fp <= 20 ? "lp-neutral" : "lp-bad");
    precEl.textContent = (prec*100).toFixed(1) + "%";
    precEl.className = "lp-stat-val " + (prec >= 0.8 ? "lp-good" : prec >= 0.5 ? "lp-neutral" : "lp-bad");
  }}
  setStats(roc0.auc, g0.tp, g0.fp, g0.prec);

  function update() {{
    var dots = getDots(curDim);
    var roc = computeROC(dots);
    var g = buildGraph(dots, curTheta);
    var op = getOperatingPoint(dots, curTheta);

    Plotly.react("lp-graph", g.traces, gLayout, {{responsive:true, displayModeBar:false}});
    Plotly.react("lp-roc", [
      {{x:roc.fpr, y:roc.tpr, mode:"lines", line:{{color:"#4a7fb5", width:2.5}},
        fill:"tozeroy", fillcolor:"rgba(74,127,181,0.08)",
        hoverinfo:"skip", showlegend:false}},
      {{x:[op.fpr], y:[op.tpr], mode:"markers",
        marker:{{size:10, color:"#e74c3c", line:{{width:2, color:"#fff"}}}},
        hoverinfo:"skip", showlegend:false}}
    ], rocLayout, {{responsive:true, displayModeBar:false}});

    setStats(roc.auc, g.tp, g.fp, g.prec);
  }}

  dimBtns.forEach(function(btn) {{
    btn.addEventListener("click", function() {{
      dimBtns.forEach(function(b){{ b.classList.remove("lp-dim-active"); }});
      btn.classList.add("lp-dim-active");
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
