# Running

```bash
python build_graphs.py data/monomers.csv tests/
```

# Developing

```bash
# First-time setup
python -m venv .venv

# Activate (for fish)
source .venv/bin/activate.fish

# Upgrade pip and install packages
pip install --upgrade pip
pip install -r requirements.txt

# Deactivate virtual environment
deactivate
```

# Things to Parse

```
Na+ GM-AEJA-GM-AEJ (x2) (Anhydro) |2
Na+ GM-AEJA-GM-AEJ (Anhydro) |2
Na+ GM-AEJA-GM-AEJ|2
GM-AEJA-GM-AEJ|2

GM-AQK(AA)
GM-AQKAA
GM-AQK(A)A

GM-AEJA=GM-AEJA
```

# Questions

- Wasn't the link type supposed to be switched from 2 to 3 on branching?
- Related, does swapping node 1 and 2 effect the link type?
- What to do about dimers linked by glycosidic *and* peptide bonds?
- Are we interested at all in trimers and beyond?

- What are the "mods" in the `masses.txt` file? Are they the numbers after the inferred structures in MS1?
They are applied per-residue in the node list, marking how their masses differ from the canonical mass
- On that note, what are the modifications after the MS1 structures?
Used for sorting purposes. I don't need them, I only need the structures!
- What are the different link-types again? The ones in the edge-list?
This is the direction of the peptide (just 2 for now)
- If mDAP is J, then what is J in the mass list?
Some other symbols for compatibility. I don't need to know about anything but the amino acids and J (mDAP)
- Anhydro is usually on the downstream MurNAc, but how do I know where Deacetyl modifcations are? GlcNAc vs MurNAc
Don't worry about it, we need a better interchange format
- GM-AEJA-GM-AEJ (Amidase Product) / (Amidase) How does that work? Both chains seem to be there
Means that a GM is missing, as it's cleaved off. This isn't actually reflected in the structure here!
- Can I have a list of MS1 -> MS2 graphs as test data?
Yep, I've got it now!
- How important is it to match the residue IDs from the example? Do they matter or can they be anything?
- Can I assume that I'll never run into a Gly-Met stem? Or just Gly / Met? It is ambiguous...
Assume there are some non-GM
- How do ions and multipliers affect the graph structures?
- Can I have a copy of the graph visualizing software?
Can get a link at some point
- How should I color things?
- Where / what are the molecule IDs for anhydro-MurNAc?
MurNAc as normal, take away in mods section NegHOxy?
- Are all of my stem residues actually valid?
- Mods in the NL files mean:
They are mass corrections to the "canonical" residue weights. 5 means hydoxyl for the exposed C-terminus
- Should I build to resolve the current format, or will it change an I should wait?
Start with basic monomers
- Bond direction is flipped on branching! linktype 2 -> 3
