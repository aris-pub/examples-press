"""Pre-compute all data needed for the GLEE paper's interactive figures.

Outputs JSON files in the data/ directory, one per figure.
"""

import json
from pathlib import Path
import warnings

import glee
import networkx as nx
import numpy as np

warnings.filterwarnings("ignore", category=FutureWarning)

DATA_DIR = Path(__file__).parent / "data"
DATA_DIR.mkdir(exist_ok=True)


def log(msg):
    print(msg, flush=True)


def to_serializable(obj):
    """Convert numpy types to Python natives for JSON serialization."""
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    if isinstance(obj, np.integer):
        return int(obj)
    if isinstance(obj, np.floating):
        return float(obj)
    raise TypeError(f"Not serializable: {type(obj)}")


# ---------------------------------------------------------------------------
# Datasets
# ---------------------------------------------------------------------------


def load_karate():
    G = nx.karate_club_graph()
    G.name = "karate"
    return G


def load_triangle():
    G = nx.complete_graph(3)
    G.name = "triangle"
    return G


def load_tetrahedron():
    G = nx.complete_graph(4)
    G.name = "tetrahedron"
    return G


NETWORKS_DIR = Path(__file__).parent / "data" / "networks"


def _load_snap_edgelist(filename, directed=False):
    """Load a SNAP edge list, extract largest connected component, relabel to 0..n-1."""
    path = NETWORKS_DIR / filename
    G = nx.read_edgelist(
        str(path),
        comments="#",
        delimiter="\t",
        create_using=nx.DiGraph() if directed else nx.Graph(),
        nodetype=int,
        data=False,
    )
    if directed:
        G = G.to_undirected()
    G.remove_edges_from(nx.selfloop_edges(G))
    cc = max(nx.connected_components(G), key=len)
    G = G.subgraph(cc).copy()
    G = nx.convert_node_labels_to_integers(G)
    return G


def _load_ppi():
    """Load HI-II-14 PPI network (Ensembl gene IDs)."""
    path = NETWORKS_DIR / "HI-II-14.tsv"
    G = nx.Graph()
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split("\t")
            if len(parts) >= 2:
                G.add_edge(parts[0], parts[1])
    G.remove_edges_from(nx.selfloop_edges(G))
    cc = max(nx.connected_components(G), key=len)
    G = G.subgraph(cc).copy()
    G = nx.convert_node_labels_to_integers(G)
    return G


def load_dataset(name):
    loaders = {
        "PPI": lambda: _load_ppi(),
        "wiki-Vote": lambda: _load_snap_edgelist("wiki-Vote.txt", directed=True),
        "caida": lambda: _load_snap_edgelist("as-caida20071105.txt", directed=True),
        "CA-HepTh": lambda: _load_snap_edgelist("ca-HepTh.txt"),
        "CA-GrQc": lambda: _load_snap_edgelist("ca-GrQc.txt"),
    }
    G = loaders[name]()
    G.name = name
    return G


SMALL_GRAPHS = {
    "triangle": load_triangle,
    "tetrahedron": load_tetrahedron,
    "karate": load_karate,
}

DATASET_NAMES = ["PPI", "wiki-Vote", "caida", "CA-HepTh", "CA-GrQc"]


# ---------------------------------------------------------------------------
# Fig. 1: Simplex geometry (3D embeddings)
# ---------------------------------------------------------------------------


def compute_fig1():
    """3D GLEE embeddings for triangle, tetrahedron, and Karate Club."""
    print("Computing Fig. 1 data...")
    result = {}

    for name, loader in SMALL_GRAPHS.items():
        G = loader()
        n = G.number_of_nodes()

        if name == "karate":
            # Direct 3D GLEE embedding — shows actual simplex eigenspace
            emb = glee.eigenmaps(G, dim=3, method="glee")
            # Normalize to unit sphere so hub nodes don't dominate scale
            norms = np.linalg.norm(emb, axis=1, keepdims=True)
            norms[norms == 0] = 1
            emb = emb / norms

            # Full-dim GLEE dot products for the interaction overlay
            emb_glee = glee.eigenmaps(G, dim=min(16, n - 1), method="glee")
            glee_dots = emb_glee @ emb_glee.T
        else:
            dim = min(3, n - 1)
            emb = glee.eigenmaps(G, dim=dim, method="glee")
            # Pad to 3D if needed (triangle has dim=2)
            if emb.shape[1] < 3:
                emb = np.hstack([emb, np.zeros((n, 3 - emb.shape[1]))])

        adj = nx.to_numpy_array(G)
        edges = list(G.edges())
        degrees = [G.degree(i) for i in range(n)]

        labels = None
        clubs = None
        dot_products = None
        if name == "karate":
            labels = {i: str(i) for i in range(n)}
            clubs = [G.nodes[i].get("club", "unknown") for i in range(n)]
            dot_products = glee_dots.tolist()

        result[name] = {
            "nodes": {
                "x": emb[:, 0].tolist(),
                "y": emb[:, 1].tolist(),
                "z": emb[:, 2].tolist(),
                "degree": degrees,
                "labels": labels,
                "clubs": clubs,
            },
            "edges": [[int(u), int(v)] for u, v in edges],
            "adjacency": adj.tolist(),
            "dot_products": dot_products,
            "n": n,
        }

    with open(DATA_DIR / "fig1_simplex.json", "w") as f:
        json.dump(result, f, default=to_serializable)
    log(f"  -> {DATA_DIR / 'fig1_simplex.json'}")


# ---------------------------------------------------------------------------
# Fig. A.1: Dot product distributions
# ---------------------------------------------------------------------------


def compute_figA1():
    """Dot product distributions for Karate Club at various dimensions."""
    print("Computing Fig. A.1 data...")
    G = load_karate()
    adj = nx.to_numpy_array(G)
    n = G.number_of_nodes()
    dims = [2, 4, 8, 16, 32]

    result = {}
    for d in dims:
        emb = glee.eigenmaps(G, dim=d, method="glee")
        dots = emb @ emb.T

        # Separate edge vs non-edge dot products (upper triangle only)
        edge_dots = []
        nonedge_dots = []
        for i in range(n):
            for j in range(i + 1, n):
                dp = float(dots[i, j])
                if adj[i, j] > 0:
                    edge_dots.append(dp)
                else:
                    nonedge_dots.append(dp)

        # Threshold estimator: theta_c = -0.5
        theta_c = -0.5

        result[str(d)] = {
            "edge_dots": edge_dots,
            "nonedge_dots": nonedge_dots,
            "theta_c": theta_c,
        }

    with open(DATA_DIR / "figA1_dotproducts.json", "w") as f:
        json.dump(result, f, default=to_serializable)
    log(f"  -> {DATA_DIR / 'figA1_dotproducts.json'}")


# ---------------------------------------------------------------------------
# Fig. 2: Graph reconstruction
# ---------------------------------------------------------------------------


def reconstruct_adjacency(emb, theta):
    """Reconstruct adjacency from embeddings using threshold theta."""
    dots = emb @ emb.T
    A_hat = (dots < theta).astype(float)
    np.fill_diagonal(A_hat, 0)
    return A_hat


_n2v_walk_cache = {}


def embed_node2vec(G, dim):
    """Node2Vec embedding. Caches walks so only word2vec retrains per dim."""
    import logging

    logging.getLogger("gensim").setLevel(logging.ERROR)
    from gensim.models import Word2Vec
    from node2vec import Node2Vec

    n = G.number_of_nodes()
    walk_length = 40 if n > 10000 else 80
    num_walks = 5 if n > 10000 else 10

    cache_key = id(G)
    if cache_key not in _n2v_walk_cache:
        n2v = Node2Vec(
            G, dimensions=dim, walk_length=walk_length, num_walks=num_walks, workers=1, quiet=True
        )
        walks = [list(map(str, w)) for w in n2v.walks]
        _n2v_walk_cache[cache_key] = walks
    else:
        walks = _n2v_walk_cache[cache_key]

    model = Word2Vec(
        walks,
        vector_size=dim,
        window=10,
        min_count=1,
        sg=1,
        workers=1,
        epochs=1,
        seed=42,
    )
    emb = np.array([model.wv[str(i)] for i in range(n)])
    return emb


def embed_netmf(G, dim, window=10):
    """NetMF embedding (Qiu et al. 2018). Uses sparse spectral approximation."""
    import scipy.sparse as sp
    from scipy.sparse.linalg import eigsh

    A = nx.to_scipy_sparse_array(G, dtype=np.float64)
    n = A.shape[0]
    vol = float(A.sum())
    degrees = np.array(A.sum(axis=1)).ravel()
    D_inv = sp.diags(1.0 / np.maximum(degrees, 1))
    M = D_inv @ A

    # Spectral approximation: eigendecompose M, then compute sum of powers
    rank = min(256, n - 1)
    eigvals, eigvecs = eigsh(M.tocsc(), k=rank, which="LM")

    # M^k eigenvalues are eigvals^k, so sum = eigvals * (1 - eigvals^window) / (1 - eigvals)
    # But for stability, just sum the powers directly on the eigenvalues
    power_sums = np.zeros(rank)
    for k in range(1, window + 1):
        power_sums += eigvals**k
    power_sums *= vol / window

    # Reconstruct approximate log-PMI and take SVD
    # M_approx = eigvecs @ diag(power_sums) @ eigvecs.T
    # We want SVD of log(max(M_approx, 1)), but that destroys sparsity.
    # Instead, use the spectral NetMF approximation directly.
    S = eigvecs * np.sqrt(np.maximum(power_sums, 0))
    # Take top-dim singular vectors of S
    if dim < S.shape[1]:
        U, s, Vt = np.linalg.svd(S, full_matrices=False)
        emb = U[:, :dim] * s[:dim]
    else:
        emb = S
    return emb


def distance_reconstruct(emb, n):
    """Reconstruct adjacency from distance-based embedding using median threshold."""
    from scipy.spatial.distance import pdist, squareform

    dists = squareform(pdist(emb))
    median_dist = np.median(dists[np.triu_indices(n, k=1)])
    A_hat = (dists < median_dist).astype(float)
    np.fill_diagonal(A_hat, 0)
    return A_hat


def precision_at_k_curve(true_adj, scores, k_values):
    """Precision at k for multiple k values in a single sort pass."""
    n = true_adj.shape[0]
    iu = np.triu_indices(n, k=1)
    true_flat = true_adj[iu]
    scores_flat = scores[iu]
    order = np.argsort(-scores_flat)
    true_sorted = true_flat[order]
    cumsum = np.cumsum(true_sorted)
    k_arr = np.array(k_values)
    return (cumsum[k_arr - 1] / k_arr).tolist()


def _embed_for_graph(G, method_name, dim):
    """Compute embedding of G with given method and dimension."""
    if method_name == "GLEE":
        return glee.eigenmaps(G, dim=dim, method="glee")
    elif method_name == "LE":
        return glee.eigenmaps(G, dim=dim, method="eigen")
    elif method_name == "node2vec":
        return embed_node2vec(G, dim)
    elif method_name == "NetMF":
        return embed_netmf(G, dim)
    raise ValueError(f"Unknown method: {method_name}")


def _reconstruction_scores(emb, method_name):
    """Score all pairs for reconstruction. Higher = more likely an edge.

    Uses float32 to halve memory on large graphs.
    """
    emb32 = emb.astype(np.float32)
    if method_name == "GLEE":
        return -(emb32 @ emb32.T)
    else:
        from scipy.spatial.distance import pdist, squareform

        dists = squareform(pdist(emb32))
        return -dists


def compute_fig2_dataset(ds_name):
    """Graph reconstruction: precision at k for a single dataset."""
    dims = [12, 128, 512]
    method_names = ["GLEE", "LE", "node2vec", "NetMF"]

    log(f"[fig2] {ds_name}: loading...")
    G = load_dataset(ds_name)
    adj = nx.to_numpy_array(G, dtype=np.float32)
    n = G.number_of_nodes()
    m = G.number_of_edges()
    log(f"[fig2] {ds_name}: n={n}, m={m}")
    n_pairs = n * (n - 1) // 2
    k_values = np.unique(np.geomspace(1, n_pairs, 80, dtype=int))

    ds_result = {"k_values": k_values.tolist(), "n": n, "m": m}
    _n2v_walk_cache.clear()

    for method_name in method_names:
        dim_results = {}
        for d in dims:
            actual_d = min(d, n - 1)
            try:
                log(f"[fig2] {ds_name} / {method_name} d={d} ...")
                emb = _embed_for_graph(G, method_name, actual_d)
                log(f"[fig2] {ds_name} / {method_name} d={d} embedded, scoring...")
                scores = _reconstruction_scores(emb, method_name)
                precs = precision_at_k_curve(adj, scores, k_values.tolist())
                dim_results[str(d)] = precs
                del scores
                log(f"[fig2] {ds_name} / {method_name} d={d} done")
            except Exception as e:
                log(f"[fig2] WARN: {method_name} d={d} on {ds_name}: {e}")
                dim_results[str(d)] = []
        ds_result[method_name] = dim_results

    out_path = DATA_DIR / f"fig2_{ds_name}.json"
    with open(out_path, "w") as f:
        json.dump(ds_result, f, default=to_serializable)
    log(f"[fig2] {ds_name} -> {out_path}")


def compute_fig2(datasets=None):
    """Graph reconstruction for all (or specified) datasets."""
    targets = datasets or DATASET_NAMES
    for ds_name in targets:
        compute_fig2_dataset(ds_name)

    # Merge per-dataset files into one
    result = {}
    for ds_name in DATASET_NAMES:
        path = DATA_DIR / f"fig2_{ds_name}.json"
        if path.exists():
            with open(path) as f:
                result[ds_name] = json.load(f)
    with open(DATA_DIR / "fig2_reconstruction.json", "w") as f:
        json.dump(result, f, default=to_serializable)
    log(f"[fig2] merged -> {DATA_DIR / 'fig2_reconstruction.json'}")


# ---------------------------------------------------------------------------
# Fig. 3: Link prediction (AUC)
# ---------------------------------------------------------------------------


def _train_test_split_edges(G, train_frac=0.75, seed=42):
    """Split edges into train/test, ensuring G_train is connected and spans all nodes."""
    rng = np.random.RandomState(seed)
    edges = list(G.edges())
    rng.shuffle(edges)
    n_train = int(len(edges) * train_frac)

    # Greedily add edges; ensure connectivity
    G_train = nx.Graph()
    G_train.add_nodes_from(G.nodes())
    train_edges = []
    test_edges = []

    # First pass: build a spanning tree
    spanning = list(nx.minimum_spanning_edges(G, data=False))
    spanning_set = set((min(u, v), max(u, v)) for u, v in spanning)

    for u, v in edges:
        key = (min(u, v), max(u, v))
        if key in spanning_set:
            train_edges.append((u, v))
            G_train.add_edge(u, v)

    # Second pass: fill train set to target size
    for u, v in edges:
        key = (min(u, v), max(u, v))
        if key not in spanning_set:
            if len(train_edges) < n_train:
                train_edges.append((u, v))
                G_train.add_edge(u, v)
            else:
                test_edges.append((u, v))

    return G_train, train_edges, test_edges


def compute_fig3_dataset(ds_name):
    """Link prediction AUC for a single dataset."""
    from sklearn.metrics import roc_auc_score

    dims = [12, 128, 512]
    method_names = ["GLEE", "LE", "node2vec", "NetMF"]
    n_realizations = 3

    log(f"[fig3] {ds_name}: loading...")
    G = load_dataset(ds_name)
    n = G.number_of_nodes()
    log(f"[fig3] {ds_name}: n={n}, m={G.number_of_edges()}")

    ds_result = {"dims": dims, "n": n, "m": G.number_of_edges()}

    for method_name in method_names:
        aucs_per_dim = {str(d): [] for d in dims}

        for run in range(n_realizations):
            _n2v_walk_cache.clear()
            log(f"[fig3] {ds_name} / {method_name} run={run}: splitting edges...")
            G_train, _, test_edges = _train_test_split_edges(G, seed=run)

            # Sample equal number of non-edges as negative examples
            rng = np.random.RandomState(run + 1000)
            edge_set = set((min(u, v), max(u, v)) for u, v in G.edges())
            non_edges = []
            nodes = list(G.nodes())
            n_needed = len(test_edges)
            non_edge_set = set()
            while len(non_edges) < n_needed:
                batch = rng.choice(nodes, size=(n_needed * 2, 2), replace=True)
                for row in batch:
                    if row[0] == row[1]:
                        continue
                    key = (min(row[0], row[1]), max(row[0], row[1]))
                    if key not in edge_set and key not in non_edge_set:
                        non_edges.append((row[0], row[1]))
                        non_edge_set.add(key)
                        if len(non_edges) >= n_needed:
                            break

            for d in dims:
                actual_d = min(d, n - 1)
                try:
                    log(f"[fig3] {ds_name} / {method_name} run={run} d={d}: embedding...")
                    emb = _embed_for_graph(G_train, method_name, actual_d)

                    labels = []
                    scores = []
                    for u, v in test_edges:
                        labels.append(1)
                        if method_name == "GLEE":
                            scores.append(-float(emb[u] @ emb[v]))
                        else:
                            scores.append(-float(np.linalg.norm(emb[u] - emb[v])))
                    for u, v in non_edges:
                        labels.append(0)
                        if method_name == "GLEE":
                            scores.append(-float(emb[u] @ emb[v]))
                        else:
                            scores.append(-float(np.linalg.norm(emb[u] - emb[v])))

                    auc = roc_auc_score(labels, scores)
                    aucs_per_dim[str(d)].append(float(auc))
                    log(f"[fig3] {ds_name} / {method_name} run={run} d={d}: AUC={auc:.3f}")
                except Exception as e:
                    log(f"[fig3] WARN: {method_name} d={d} run={run} on {ds_name}: {e}")

        ds_result[method_name] = {
            str(d): {
                "mean": float(np.mean(aucs_per_dim[str(d)])) if aucs_per_dim[str(d)] else 0,
                "std": float(np.std(aucs_per_dim[str(d)])) if aucs_per_dim[str(d)] else 0,
            }
            for d in dims
        }

    out_path = DATA_DIR / f"fig3_{ds_name}.json"
    with open(out_path, "w") as f:
        json.dump(ds_result, f, default=to_serializable)
    log(f"[fig3] {ds_name} -> {out_path}")


def compute_fig3(datasets=None):
    """Link prediction for all (or specified) datasets."""
    targets = datasets or DATASET_NAMES
    for ds_name in targets:
        compute_fig3_dataset(ds_name)

    # Merge per-dataset files into one
    result = {}
    for ds_name in DATASET_NAMES:
        path = DATA_DIR / f"fig3_{ds_name}.json"
        if path.exists():
            with open(path) as f:
                result[ds_name] = json.load(f)
    with open(DATA_DIR / "fig3_linkpred.json", "w") as f:
        json.dump(result, f, default=to_serializable)
    log(f"[fig3] merged -> {DATA_DIR / 'fig3_linkpred.json'}")


# ---------------------------------------------------------------------------
# Fig. B.1: Estimator comparison
# ---------------------------------------------------------------------------


def compute_figB1():
    """Reconstruction error for theta_c vs theta_k across random graph models."""
    print("Computing Fig. B.1 data...")
    n_nodes = 100
    dims = [4, 8, 16, 32]
    n_runs = 10

    models = {
        "ER": lambda: nx.erdos_renyi_graph(n_nodes, 0.1),
        "BA": lambda: nx.barabasi_albert_graph(n_nodes, 3),
    }

    result = {}
    for model_name, model_fn in models.items():
        theta_c_errors = {d: [] for d in dims}
        for _ in range(n_runs):
            G = model_fn()
            adj = nx.to_numpy_array(G)
            for d in dims:
                try:
                    emb = glee.eigenmaps(G, dim=d, method="glee")
                    A_hat = reconstruct_adjacency(emb, -0.5)
                    err = float(np.linalg.norm(adj - A_hat, "fro"))
                    theta_c_errors[d].append(err)
                except Exception:
                    pass

        result[model_name] = {
            "dims": dims,
            "theta_c_mean": [float(np.mean(theta_c_errors[d])) for d in dims],
            "theta_c_std": [float(np.std(theta_c_errors[d])) for d in dims],
        }

    with open(DATA_DIR / "figB1_estimators.json", "w") as f:
        json.dump(result, f, default=to_serializable)
    log(f"  -> {DATA_DIR / 'figB1_estimators.json'}")


# ---------------------------------------------------------------------------
# Reconstruction Machine
# ---------------------------------------------------------------------------


def compute_reconstruction_machine():
    """Dot product matrices at multiple dims + graph layout for the reconstruction machine."""
    print("Computing Reconstruction Machine data...")
    G = load_karate()
    adj = nx.to_numpy_array(G)
    n = G.number_of_nodes()
    dims = [2, 4, 8, 16, 33]

    # Spring layout for the graph panel
    pos = nx.spring_layout(G, dim=2, seed=42, k=1.5, iterations=100)
    layout_x = [float(pos[i][0]) for i in range(n)]
    layout_y = [float(pos[i][1]) for i in range(n)]

    clubs = [G.nodes[i].get("club", "unknown") for i in range(n)]
    edges = [[int(u), int(v)] for u, v in G.edges()]
    degrees = [G.degree(i) for i in range(n)]

    # Binary adjacency (upper triangle, flattened row-major)
    adj_binary = (adj > 0).astype(int)

    # Dot product matrices at each dimension
    dot_matrices = {}
    for d in dims:
        emb = glee.eigenmaps(G, dim=d, method="glee")
        dots = emb @ emb.T
        dot_matrices[str(d)] = dots.tolist()

    result = {
        "n": n,
        "edges": edges,
        "degrees": degrees,
        "clubs": clubs,
        "adjacency": adj_binary.tolist(),
        "layout_x": layout_x,
        "layout_y": layout_y,
        "dot_matrices": dot_matrices,
        "dims": dims,
    }

    with open(DATA_DIR / "reconstruction_machine.json", "w") as f:
        json.dump(result, f, default=to_serializable)
    log(f"  -> {DATA_DIR / 'reconstruction_machine.json'}")


# ---------------------------------------------------------------------------
# Orthogonality Explorer
# ---------------------------------------------------------------------------


def compute_orthogonality_explorer():
    """Full-dimensional GLEE embedding + dot products for the orthogonality explorer."""
    print("Computing Orthogonality Explorer data...")
    G = load_karate()
    n = G.number_of_nodes()
    adj = nx.to_numpy_array(G)

    # Full simplex embedding (n-1 dimensions), projected to 3D for display
    emb_full = glee.eigenmaps(G, dim=n - 1, method="glee")
    dots_full = emb_full @ emb_full.T

    emb_3d = glee.eigenmaps(G, dim=3, method="glee")
    # Normalize to unit sphere for display
    norms = np.linalg.norm(emb_3d, axis=1, keepdims=True)
    norms[norms == 0] = 1
    emb_3d = emb_3d / norms

    clubs = [G.nodes[i].get("club", "unknown") for i in range(n)]
    degrees = [G.degree(i) for i in range(n)]
    edges = [[int(u), int(v)] for u, v in G.edges()]

    result = {
        "n": n,
        "edges": edges,
        "degrees": degrees,
        "clubs": clubs,
        "x": emb_3d[:, 0].tolist(),
        "y": emb_3d[:, 1].tolist(),
        "z": emb_3d[:, 2].tolist(),
        "dot_products": dots_full.tolist(),
        "adjacency": (adj > 0).astype(int).tolist(),
    }

    with open(DATA_DIR / "orthogonality_explorer.json", "w") as f:
        json.dump(result, f, default=to_serializable)
    log(f"  -> {DATA_DIR / 'orthogonality_explorer.json'}")


# ---------------------------------------------------------------------------
# Link Prediction Machine
# ---------------------------------------------------------------------------


def compute_link_prediction_machine():
    """Full-graph GLEE dot products for edge classification ROC widget.

    Uses the full graph embedding and scores ALL node pairs by dot product.
    The task: can we rank pairs so that true edges score higher than non-edges?
    This matches the paper's methodology in Section 5.2.
    """
    print("Computing Link Prediction Machine data...")
    G = load_karate()
    n = G.number_of_nodes()
    dims = [2, 4, 8, 16, 33]

    pos = nx.spring_layout(G, dim=2, seed=42, k=1.5, iterations=100)
    layout_x = [float(pos[i][0]) for i in range(n)]
    layout_y = [float(pos[i][1]) for i in range(n)]

    clubs = [G.nodes[i].get("club", "unknown") for i in range(n)]
    degrees = [G.degree(i) for i in range(n)]
    edges = [[int(u), int(v)] for u, v in G.edges()]

    # All upper-triangle pairs, classified as edge or non-edge
    edge_set = {(min(u, v), max(u, v)) for u, v in G.edges()}
    all_pairs = []
    for i in range(n):
        for j in range(i + 1, n):
            all_pairs.append([i, j, 1 if (i, j) in edge_set else 0])

    # Dot product matrices from full graph embedding
    dot_matrices = {}
    for d in dims:
        emb = glee.eigenmaps(G, dim=d, method="glee")
        dots = emb @ emb.T
        dot_matrices[str(d)] = dots.tolist()

    result = {
        "n": n,
        "dims": dims,
        "edges": edges,
        "all_pairs": all_pairs,
        "degrees": degrees,
        "clubs": clubs,
        "layout_x": layout_x,
        "layout_y": layout_y,
        "dot_matrices": dot_matrices,
    }

    with open(DATA_DIR / "link_prediction_machine.json", "w") as f:
        json.dump(result, f, default=to_serializable)
    log(f"  -> {DATA_DIR / 'link_prediction_machine.json'}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import sys

    args = sys.argv[1:]
    if not args:
        print("Usage: python compute_data.py <target> [dataset ...]")
        print(
            "Targets: fig1, figA1, fig2, fig3, figB1, reconstruction_machine, link_prediction_machine, all"
        )
        print("For fig2/fig3, optionally specify datasets: PPI wiki-Vote caida CA-HepTh CA-GrQc")
        sys.exit(0)

    target = args[0]
    dataset_filter = args[1:] if len(args) > 1 else None

    simple_fns = {
        "fig1": compute_fig1,
        "figA1": compute_figA1,
        "figB1": compute_figB1,
        "reconstruction_machine": compute_reconstruction_machine,
        "link_prediction_machine": compute_link_prediction_machine,
    }

    if target == "all":
        for fn in simple_fns.values():
            fn()
        compute_fig2()
        compute_fig3()
    elif target == "fig2":
        compute_fig2(datasets=dataset_filter)
    elif target == "fig3":
        compute_fig3(datasets=dataset_filter)
    elif target in simple_fns:
        simple_fns[target]()
    else:
        log(f"Unknown target: {target}")
        sys.exit(1)

    log("Done.")
