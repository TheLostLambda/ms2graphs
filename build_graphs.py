import os.path as path
import sys
import csv

# Some helpful mappings
chain_abbr = {"G": "GlcNAc", "M": "MurNAc_alditol"}
stem_abbr = {"J": "mDAP"}

# Extract the MS1 input filepath and graph output path from the arguments
ms1_file = sys.argv[1]
out_dir = sys.argv[2]

# Load the MS1 structures from CSV
with open(ms1_file) as f:
    rows = csv.reader(f)
    ms1 = [r[0].split("|")[0] for r in rows][1:]


# Convert a structure into node and edge lists
def write_graph(structure):
    chain, stem = structure.split("-")
    residues = [chain_abbr.get(r) for r in chain]  # Resolve chain residues
    residues += [stem_abbr.get(r) or r for r in stem]  # Resolve stem residues
    # Create the node list
    with open(path.join(out_dir, f"{structure} NL.csv"), "w") as nlf:
        nl = csv.writer(nlf)
        nl.writerow(["node", "molecule_ID", "colour", "mods"])
        # Create the edge list
        with open(path.join(out_dir, f"{structure} EL.csv"), "w") as elf:
            el = csv.writer(elf)
            el.writerow(["node1", "node2", "chain_colour_ID", "linktype"])
            for i, r in enumerate(residues):
                islast = i + 1 == len(residues)
                node_mod = "Hydroxy" if islast else "zero"
                nl.writerow([f"{r}{i}", r, "cyan", node_mod])
                if not islast:
                    nr = residues[i + 1]
                    el.writerow([f"{r}{i}", f"{nr}{i + 1}", "violet", 2])


# Generate graphs for every MS1 structure
for s in ms1:
    write_graph(s)
