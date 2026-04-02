"""Build morph.html — 3-state looping 3D morph.

Three states:
  1. Network (force-directed spring layout)
  2. Simplex (full 33-dim GLEE simplex, PCA-projected to 3D)
  3. Sphere (3D GLEE embedding, unit-sphere normalized)

Loops continuously with smooth eased transitions and pauses at each state.
Slider follows the animation and can be grabbed to take manual control.
"""

import json
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"
OUT = Path(__file__).parent / "morph.html"

with open(DATA_DIR / "morph.json") as f:
    data = json.load(f)

data_json = json.dumps(data, separators=(",", ":"))

html = f"""<style>
.morph-widget {{
  font-family: "Source Sans 3", sans-serif;
  color: #2c3e50;
  max-width: 100%;
  overflow: hidden;
}}
.morph-controls {{
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  padding: 8px 8px 0;
}}
.morph-track {{
  display: flex;
  flex-direction: column;
  flex: 1;
  max-width: 400px;
}}
.morph-slider {{
  -webkit-appearance: none;
  appearance: none;
  width: 100%;
  height: 5px;
  border-radius: 3px;
  background: linear-gradient(to right, #7f8c8d 0%, #4a7fb5 50%, #9b59b6 100%);
  outline: none;
  cursor: pointer;
  margin: 0;
}}
.morph-slider::-webkit-slider-thumb {{
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
.morph-slider::-moz-range-thumb {{
  width: 16px;
  height: 16px;
  border-radius: 50%;
  background: #fff;
  border: 2px solid #4a7fb5;
  cursor: grab;
  box-shadow: 0 1px 3px rgba(0,0,0,0.2);
}}
.morph-btn {{
  background: #f4f6f8;
  border: 1px solid #d0d5da;
  border-radius: 4px;
  padding: 3px 10px;
  font-size: 12px;
  font-family: inherit;
  cursor: pointer;
  color: #4a5568;
  margin-left: 10px;
  transition: background 0.15s;
}}
.morph-btn:hover {{ background: #e8ecf0; }}
.morph-btn.morph-active {{ background: #4a7fb5; color: #fff; border-color: #4a7fb5; }}
.morph-ticks {{
  display: flex;
  justify-content: space-between;
  width: 100%;
  margin-top: 2px;
  padding: 0;
}}
.morph-tick {{
  font-size: 10px;
  font-weight: 600;
  color: #a0a8b0;
  transition: color 0.3s;
  white-space: nowrap;
  flex: 1;
}}
.morph-tick:first-child {{ text-align: left; }}
.morph-tick:nth-child(2) {{ text-align: center; }}
.morph-tick:last-child {{ text-align: right; }}
.morph-tick.morph-lit {{ color: #2c3e50; }}
.morph-plot-wrap {{
  border: 1px solid #e8ecf0;
  border-radius: 6px;
  background: #fafbfc;
  overflow: hidden;
}}
#morph-plot {{
  width: 100% !important;
  height: 460px !important;
}}
.morph-legend {{
  display: flex;
  gap: 16px;
  justify-content: center;
  font-size: 11px;
  padding: 6px 0 2px;
  color: #5a6672;
}}
.morph-legend-item {{
  display: flex;
  align-items: center;
  gap: 4px;
}}
.morph-legend-dot {{
  width: 10px;
  height: 10px;
  border-radius: 50%;
  border: 1px solid #fff;
  box-shadow: 0 0 0 1px rgba(0,0,0,0.1);
}}
@media (max-width: 600px) {{
  #morph-plot {{ height: 340px !important; }}
  .morph-lbl {{ font-size: 10px; padding: 0 4px; }}
}}
</style>

<script src="https://cdn.plot.ly/plotly-2.35.2.min.js"></script>

<div class="morph-widget">
  <div class="morph-controls">
    <div class="morph-track">
      <input type="range" class="morph-slider" id="morph-slider" min="0" max="1" step="0.003" value="0">
      <div class="morph-ticks">
        <span class="morph-tick morph-lit" id="morph-lbl-0b">Network</span>
        <span class="morph-tick" id="morph-lbl-1">Simplex</span>
        <span class="morph-tick" id="morph-lbl-2b">3D sphere</span>
      </div>
    </div>
    <button class="morph-btn morph-active" id="morph-play">Pause</button>
  </div>
  <div class="morph-plot-wrap">
    <div id="morph-plot"></div>
  </div>
  <div class="morph-legend">
    <div class="morph-legend-item"><div class="morph-legend-dot" style="background:#9b59b6"></div>Mr. Hi's faction</div>
    <div class="morph-legend-item"><div class="morph-legend-dot" style="background:#e8913a"></div>Officer's faction</div>
  </div>
</div>

<script>
(function() {{
  var D = {data_json};
  var n = D.n, edges = D.edges;
  var clubs = D.clubs, degrees = D.degrees;

  // Three states: [network, simplex, sphere]
  var states = [
    {{ x: D.net_x, y: D.net_y, z: D.net_z }},
    {{ x: D.simplex_x, y: D.simplex_y, z: D.simplex_z }},
    {{ x: D.sphere_x, y: D.sphere_y, z: D.sphere_z }}
  ];

  var PURPLE = "#9b59b6", ORANGE = "#e8913a";
  var maxDeg = Math.max.apply(null, degrees);
  var nodeColors = clubs.map(function(c){{ return c==="Mr. Hi" ? PURPLE : ORANGE; }});
  var nodeSizes = degrees.map(function(d){{ return 5 + (d/maxDeg)*10; }});
  var nodeLabels = degrees.map(function(d,i){{ return d >= 8 ? String(i) : ""; }});
  var nodeText = degrees.map(function(d,i){{ return "Node "+i+" (deg "+d+", "+clubs[i]+")"; }});

  var slider = document.getElementById("morph-slider");
  var lbl0 = document.getElementById("morph-lbl-0b");
  var lbl1 = document.getElementById("morph-lbl-1");
  var lbl2 = document.getElementById("morph-lbl-2b");
  var playBtn = document.getElementById("morph-play");

  function lerp(a, b, t) {{
    var out = new Array(a.length);
    for (var i = 0; i < a.length; i++) out[i] = a[i]*(1-t) + b[i]*t;
    return out;
  }}

  function ease(t) {{
    return t < 0.5 ? 4*t*t*t : 1 - Math.pow(-2*t+2, 3)/2;
  }}

  // t in [0,1] maps to 3 states: 0=network, 0.5=simplex, 1=sphere
  function getPositions(t) {{
    var seg, local;
    if (t <= 0.5) {{
      seg = 0;
      local = ease(t * 2);
    }} else {{
      seg = 1;
      local = ease((t - 0.5) * 2);
    }}
    var A = states[seg], B = states[seg + 1];
    return {{
      x: lerp(A.x, B.x, local),
      y: lerp(A.y, B.y, local),
      z: lerp(A.z, B.z, local)
    }};
  }}

  function updateLabels(t) {{
    var near0 = t < 0.15, near1 = t > 0.35 && t < 0.65, near2 = t > 0.85;
    lbl0.classList.toggle("morph-lit", near0);
    lbl1.classList.toggle("morph-lit", near1);
    lbl2.classList.toggle("morph-lit", near2);
    slider.value = t;
  }}

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

  function buildTraces(pos) {{
    var ex=[], ey=[], ez=[];
    edges.forEach(function(e) {{
      ex.push(pos.x[e[0]], pos.x[e[1]], null);
      ey.push(pos.y[e[0]], pos.y[e[1]], null);
      ez.push(pos.z[e[0]], pos.z[e[1]], null);
    }});
    return [
      {{x:ex, y:ey, z:ez, type:"scatter3d", mode:"lines",
        line:{{color:"rgb(190,195,200)", width:1.5}},
        hoverinfo:"skip", showlegend:false}},
      {{x:pos.x, y:pos.y, z:pos.z, type:"scatter3d", mode:"markers+text",
        marker:{{size:nodeSizes, color:nodeColors, line:{{width:1.5, color:"#fff"}}}},
        text:nodeLabels, textposition:"top center",
        textfont:{{size:9, color:"#1a1a2e"}},
        hovertext:nodeText, hoverinfo:"text",
        showlegend:false}}
    ];
  }}

  Plotly.newPlot("morph-plot", buildTraces(getPositions(0)), layout, {{
    responsive:true, displayModeBar:false, scrollZoom:true
  }});

  // Animation: 0 → 0.5 → 1 → 0.5 → 0 → ... with pauses at 0, 0.5, 1
  var playing = true;
  var t = 0;
  var direction = 1;
  var pauseTimer = 0;
  var PAUSE_FRAMES = 90;
  var SPEED = 0.004;
  var raf = null;

  function tick() {{
    if (!playing) return;

    if (pauseTimer > 0) {{
      pauseTimer--;
      raf = requestAnimationFrame(tick);
      return;
    }}

    t += direction * SPEED;

    // Pause at each state (0, 0.5, 1)
    if (direction > 0 && t >= 0.5 && t - direction * SPEED < 0.5) {{
      t = 0.5;
      pauseTimer = PAUSE_FRAMES;
    }} else if (direction > 0 && t >= 1) {{
      t = 1;
      direction = -1;
      pauseTimer = PAUSE_FRAMES;
    }} else if (direction < 0 && t <= 0.5 && t - direction * SPEED > 0.5) {{
      t = 0.5;
      pauseTimer = PAUSE_FRAMES;
    }} else if (direction < 0 && t <= 0) {{
      t = 0;
      direction = 1;
      pauseTimer = PAUSE_FRAMES;
    }}

    var pos = getPositions(t);
    updateLabels(t);

    Plotly.react("morph-plot", buildTraces(pos), layout, {{
      responsive:true, displayModeBar:false, scrollZoom:true
    }});

    raf = requestAnimationFrame(tick);
  }}

  slider.addEventListener("input", function() {{
    if (playing) {{
      playing = false;
      playBtn.textContent = "Play";
      playBtn.classList.remove("morph-active");
    }}
    t = parseFloat(this.value);
    var pos = getPositions(t);
    updateLabels(t);
    Plotly.react("morph-plot", buildTraces(pos), layout, {{
      responsive:true, displayModeBar:false, scrollZoom:true
    }});
  }});

  playBtn.addEventListener("click", function() {{
    playing = !playing;
    playBtn.textContent = playing ? "Pause" : "Play";
    playBtn.classList.toggle("morph-active", playing);
    if (playing) tick();
  }});

  raf = requestAnimationFrame(tick);
}})();
</script>
"""

OUT.write_text(html)
print(f"Wrote {OUT} ({len(html)} bytes)")
