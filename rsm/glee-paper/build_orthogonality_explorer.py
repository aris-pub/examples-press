"""Build orthogonality_explorer.html — click a node, see orthogonality in action.

Click any node in the 3D GLEE embedding of the Karate Club. All other nodes
recolor by their full-dimensional dot product with the selected node:
  - Neighbors: dot product = -w_ij (red, proportional to edge weight)
  - Non-neighbors: dot product = 0 (white/neutral, orthogonal)
"""

import json
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"
OUT = Path(__file__).parent / "orthogonality_explorer.html"

with open(DATA_DIR / "orthogonality_explorer.json") as f:
    data = json.load(f)

data_json = json.dumps(data, separators=(",", ":"))

html = f"""<style>
.orth-widget {{
  font-family: "Source Sans 3", sans-serif;
  color: #2c3e50;
  max-width: 100%;
  overflow: hidden;
}}
.orth-header {{
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 6px 4px 4px;
  flex-wrap: wrap;
  gap: 8px;
}}
.orth-prompt {{
  font-size: 13px;
  color: #5a6672;
}}
.orth-prompt strong {{ color: #2c3e50; }}
.orth-badges {{
  display: flex;
  gap: 6px;
  font-size: 12px;
}}
.orth-badge {{
  display: inline-flex;
  align-items: center;
  gap: 4px;
  background: #f4f6f8;
  border: 1px solid #e2e6ea;
  border-radius: 4px;
  padding: 2px 8px;
}}
.orth-badge-val {{ font-weight: 700; }}
.orth-3d-wrap {{
  border: 1px solid #e8ecf0;
  border-radius: 6px;
  background: #fafbfc;
  overflow: hidden;
}}
#orth-3d {{
  width: 100% !important;
  height: 440px !important;
}}
.orth-bottom {{
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 6px;
  margin-top: 6px;
}}
.orth-col {{
  border: 1px solid #e8ecf0;
  border-radius: 6px;
  background: #fafbfc;
  padding: 8px 10px;
  max-height: 180px;
  overflow-y: auto;
}}
.orth-col-title {{
  font-size: 11px;
  font-weight: 600;
  color: #4a5568;
  text-transform: uppercase;
  letter-spacing: 0.03em;
  margin-bottom: 4px;
  display: flex;
  align-items: center;
  gap: 6px;
}}
.orth-col-title .orth-swatch {{
  width: 10px;
  height: 10px;
  border-radius: 2px;
}}
.orth-row {{
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 12px;
  padding: 2px 4px;
  border-radius: 3px;
}}
.orth-row:nth-child(even) {{ background: rgba(0,0,0,0.02); }}
.orth-val {{
  font-weight: 600;
  font-variant-numeric: tabular-nums;
  min-width: 3.5em;
  text-align: right;
}}
.orth-colorbar {{
  display: flex;
  align-items: center;
  gap: 6px;
  justify-content: center;
  padding: 6px 0 2px;
  font-size: 11px;
  color: #5a6672;
}}
.orth-cbar-grad {{
  width: 140px;
  height: 10px;
  border-radius: 2px;
  background: linear-gradient(to right, #b2182b, #ef8a62, #f7f7f7);
  border: 1px solid #e2e6ea;
}}
.orth-placeholder {{
  font-size: 12px;
  color: #8a95a0;
  padding: 12px 0;
  text-align: center;
}}
@media (max-width: 600px) {{
  #orth-3d {{ height: 320px !important; }}
  .orth-bottom {{ grid-template-columns: 1fr; }}
}}
</style>

<script src="https://cdn.plot.ly/plotly-2.35.2.min.js"></script>

<div class="orth-widget">
  <div class="orth-header">
    <div class="orth-prompt" id="orth-prompt"><strong>Click any node</strong> to see its dot products with all others</div>
    <div class="orth-badges" id="orth-badges"></div>
  </div>
  <div class="orth-3d-wrap">
    <div id="orth-3d"></div>
  </div>
  <div class="orth-colorbar">
    <span>&minus;w<sub>ij</sub> (neighbor)</span>
    <div class="orth-cbar-grad"></div>
    <span>0 (orthogonal)</span>
  </div>
  <div class="orth-bottom">
    <div class="orth-col" id="orth-neighbors">
      <div class="orth-col-title"><div class="orth-swatch" style="background:#b2182b"></div>Neighbors (s<sub>i</sub> &middot; s<sub>j</sub> = &minus;w<sub>ij</sub>)</div>
      <div class="orth-placeholder">Select a node</div>
    </div>
    <div class="orth-col" id="orth-nonneighbors">
      <div class="orth-col-title"><div class="orth-swatch" style="background:#4a7fb5"></div>Non-neighbors (s<sub>i</sub> &middot; s<sub>j</sub> = 0)</div>
      <div class="orth-placeholder">Select a node</div>
    </div>
  </div>
</div>

<script>
(function() {{
  var D = {data_json};
  var n = D.n, x = D.x, y = D.y, z = D.z;
  var clubs = D.clubs, degrees = D.degrees;
  var dots = D.dot_products, adj = D.adjacency, edges = D.edges;

  var PURPLE = "#9b59b6", ORANGE = "#e8913a";
  var maxDeg = Math.max.apply(null, degrees);

  var defaultColors = clubs.map(function(c){{ return c==="Mr. Hi" ? PURPLE : ORANGE; }});
  var defaultSizes = degrees.map(function(d){{ return 5 + (d/maxDeg)*10; }});

  var ex=[], ey=[], ez=[];
  edges.forEach(function(e) {{
    ex.push(x[e[0]], x[e[1]], null);
    ey.push(y[e[0]], y[e[1]], null);
    ez.push(z[e[0]], z[e[1]], null);
  }});

  function sceneAxis() {{
    return {{showgrid:false, zeroline:false, showticklabels:false,
            showspikes:false, showline:false, title:"",
            backgroundcolor:"rgba(0,0,0,0)"}};
  }}

  var layout = {{
    margin:{{l:0,r:0,t:0,b:0}},
    paper_bgcolor:"rgba(0,0,0,0)",
    scene:{{
      xaxis:sceneAxis(), yaxis:sceneAxis(), zaxis:sceneAxis(),
      bgcolor:"rgba(0,0,0,0)",
      camera:{{eye:{{x:1.6, y:-1.2, z:0.8}}}},
      dragmode:"orbit", aspectmode:"data"
    }},
    showlegend:false
  }};

  Plotly.newPlot("orth-3d", [
    {{x:ex, y:ey, z:ez, type:"scatter3d", mode:"lines",
      line:{{color:"rgb(190,195,200)", width:1.5}}, hoverinfo:"skip", showlegend:false}},
    {{x:x, y:y, z:z, type:"scatter3d", mode:"markers+text",
      marker:{{size:defaultSizes, color:defaultColors, line:{{width:1.5, color:"#fff"}}}},
      text:degrees.map(function(d,i){{ return d>=6 ? String(i) : ""; }}),
      textposition:"top center", textfont:{{size:9, color:"#1a1a2e"}},
      customdata:degrees.map(function(d,i){{ return [i,d,clubs[i]]; }}),
      hovertemplate:"Node %{{customdata[0]}}<br>Degree: %{{customdata[1]}}<br>%{{customdata[2]}}<extra></extra>",
      showlegend:false}}
  ], layout, {{responsive:true, displayModeBar:false, scrollZoom:true}});

  var promptEl = document.getElementById("orth-prompt");
  var badgesEl = document.getElementById("orth-badges");
  var neighborsEl = document.getElementById("orth-neighbors");
  var nonneighborsEl = document.getElementById("orth-nonneighbors");

  // Find min dot product for color scaling
  var minDot = 0;
  dots.forEach(function(row) {{ row.forEach(function(v) {{ if (v < minDot) minDot = v; }}); }});

  function dotToColor(dp) {{
    if (minDot >= 0) return "rgb(247,247,247)";
    var t = Math.max(0, Math.min(1, dp / minDot));
    var r = Math.round(247 + (178 - 247) * t);
    var g = Math.round(247 + (24 - 247) * t);
    var b = Math.round(247 + (43 - 247) * t);
    return "rgb("+r+","+g+","+b+")";
  }}

  function selectNode(idx) {{
    var nd = dots[idx];
    var newColors = [], newSizes = [];
    for (var j = 0; j < n; j++) {{
      if (j === idx) {{
        newColors.push("#1a1a2e");
        newSizes.push(14);
      }} else {{
        newColors.push(dotToColor(nd[j]));
        newSizes.push(6 + (degrees[j]/maxDeg)*10);
      }}
    }}

    var hx=[], hy=[], hz=[], ox=[], oy=[], oz=[];
    edges.forEach(function(e) {{
      if (e[0]===idx || e[1]===idx) {{
        hx.push(x[e[0]],x[e[1]],null);
        hy.push(y[e[0]],y[e[1]],null);
        hz.push(z[e[0]],z[e[1]],null);
      }} else {{
        ox.push(x[e[0]],x[e[1]],null);
        oy.push(y[e[0]],y[e[1]],null);
        oz.push(z[e[0]],z[e[1]],null);
      }}
    }});

    Plotly.react("orth-3d", [
      {{x:ox, y:oy, z:oz, type:"scatter3d", mode:"lines",
        line:{{color:"rgb(225,227,230)", width:1}}, hoverinfo:"skip", showlegend:false}},
      {{x:hx, y:hy, z:hz, type:"scatter3d", mode:"lines",
        line:{{color:"rgb(178,24,43)", width:3}}, hoverinfo:"skip", showlegend:false}},
      {{x:x, y:y, z:z, type:"scatter3d", mode:"markers+text",
        marker:{{size:newSizes, color:newColors, line:{{width:1.5, color:"#fff"}}}},
        text:Array.from({{length:n}}, function(_,j){{
          if (j===idx) return String(j);
          return degrees[j]>=6 ? String(j) : "";
        }}),
        textposition:"top center", textfont:{{size:9, color:"#1a1a2e"}},
        customdata:degrees.map(function(d,j){{ return [j,d,clubs[j],nd[j].toFixed(2)]; }}),
        hovertemplate:"Node %{{customdata[0]}}<br>Degree: %{{customdata[1]}}<br>%{{customdata[2]}}<br>s &middot; s = %{{customdata[3]}}<extra></extra>",
        showlegend:false}}
    ], layout, {{responsive:true, displayModeBar:false, scrollZoom:true}});

    promptEl.innerHTML = "Selected <strong>node "+idx+"</strong> (degree "+degrees[idx]+", "+clubs[idx]+")";

    var neighbors = [], nonneighbors = [];
    for (var j = 0; j < n; j++) {{
      if (j === idx) continue;
      if (adj[idx][j] > 0) neighbors.push({{j:j, dp:nd[j]}});
      else nonneighbors.push({{j:j, dp:nd[j]}});
    }}
    neighbors.sort(function(a,b){{ return a.dp - b.dp; }});
    nonneighbors.sort(function(a,b){{ return Math.abs(a.dp) - Math.abs(b.dp); }});

    badgesEl.innerHTML =
      '<div class="orth-badge">Neighbors <span class="orth-badge-val" style="color:#b2182b">'+neighbors.length+'</span></div>' +
      '<div class="orth-badge">Non-neighbors <span class="orth-badge-val" style="color:#4a7fb5">'+nonneighbors.length+'</span></div>';

    var nhtml = '<div class="orth-col-title"><div class="orth-swatch" style="background:#b2182b"></div>Neighbors (s<sub>'+idx+'</sub> &middot; s<sub>j</sub> = &minus;w<sub>ij</sub>)</div>';
    neighbors.forEach(function(p) {{
      nhtml += '<div class="orth-row"><span>Node '+p.j+' <span style="color:#8a95a0">(deg '+degrees[p.j]+')</span></span><span class="orth-val" style="color:#b2182b">'+p.dp.toFixed(1)+'</span></div>';
    }});
    neighborsEl.innerHTML = nhtml;

    var ohtml = '<div class="orth-col-title"><div class="orth-swatch" style="background:#4a7fb5"></div>Non-neighbors (s<sub>'+idx+'</sub> &middot; s<sub>j</sub> = 0)</div>';
    nonneighbors.forEach(function(p) {{
      ohtml += '<div class="orth-row"><span>Node '+p.j+' <span style="color:#8a95a0">(deg '+degrees[p.j]+')</span></span><span class="orth-val" style="color:#4a7fb5">'+p.dp.toFixed(1)+'</span></div>';
    }});
    nonneighborsEl.innerHTML = ohtml;
  }}

  document.getElementById("orth-3d").on("plotly_click", function(data) {{
    if (data.points && data.points.length > 0) {{
      var pt = data.points[0];
      if (pt.customdata) selectNode(pt.customdata[0]);
    }}
  }});
}})();
</script>
"""

OUT.write_text(html)
print(f"Wrote {OUT} ({len(html)} bytes)")
