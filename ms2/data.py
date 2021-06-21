chain_abbr = {"G": "GlcNAc", "M": "MurNAc_alditol"}
stem_abbr = {"J": "mDAP"}

chain_residues = {"G", "M"}
stem_residues = {
    "A",
    "B",
    "R",
    "N",
    "D",
    "C",
    "E",
    "Q",
    "G",
    "H",
    "I",
    "J",  # This is mDAP
    "L",
    "K",
    "M",
    "F",
    "O",
    "P",
    "S",
    "T",
    "U",
    "W",
    "Y",
    "V",
    "X",
    "Z",
}

bond_acceptors = {
    "MurNAc_alditol": {"N_terminus"},
    "MurNAc": {"N_terminus", "GlcNAc", "GlcN"},
    "MurN_alditol": {"N_terminus"},
    "MurN": {"N_terminus", "GlcNAc", "GlcN"},
    "mDAP": {"mDAP", "C_terminus"},
    "K": {"C_terminus"},
}
