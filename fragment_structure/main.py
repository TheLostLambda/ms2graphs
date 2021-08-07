import sys
import csv
from pathlib import Path
from build_graphs import load_structures, write_graphs
from graph_loading import Helper_Funcs
from bio_graph import Bio_Graph
from tempfile import TemporaryDirectory

MASSES = "./masses.csv"
MODS = "./mods.csv"

if __name__ == "__main__":
    ms1_file = sys.argv[1]
    out_dir = sys.argv[2]
    mols = load_structures(ms1_file)
    with TemporaryDirectory() as tmp:
        for mol in mols:
            write_graphs(mol, tmp)
        p = Path(tmp)
        for node_file in p.glob("* NL.csv"):
            parent = node_file.parent
            structure_name = node_file.name.removesuffix(" NL.csv")
            edge_file = parent / (structure_name + " EL.csv")
            hf = Helper_Funcs(node_file, edge_file)
            masses = hf.generate_dict(MASSES)
            mods = hf.generate_dict(MODS)
            bg = Bio_Graph(hf.nodes_df(), hf.edges_df(), masses, mods)
            graph = bg.construct_graph()
            fragments = bg.fragmentation(graph, cut_limit=3)
            nfrags, cfrags, ifrags = bg.sort_fragments(fragments)
            with open(Path(out_dir) / f"{structure_name} Fragments.csv", "w") as f:
                ff = csv.writer(f)
                ff.writerow(["Type", "Mass", "Parts"])
                for id, frag in [
                    (id, [mol for _, mol in frag.nodes(data="molecule_ID")])
                    for id, frag in fragments.items()
                ]:
                    if id in nfrags:
                        type = "N-Terminal"
                    if id in cfrags:
                        type = "C-Terminal"
                    if id in ifrags:
                        type = "Internal"
                    mass = bg.monoisotopic_mass_calculator(fragments, [id])[0][0][0]
                    ff.writerow([type, mass, frag])
