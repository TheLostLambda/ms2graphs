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
```

# Questions

- What are the "mods" in the `masses.txt` file? Are they the numbers after the inferred structures in MS1?
- On that note, what are the modifications after the MS1 structures?
- What are the different link-types again? The ones in the edge-list?
- If mDAP is J, then what is J in the mass list?
- Anhydro is usually on the downstream MurNAc, but how do I know where Deacetyl modifcations are? GlcNAc vs MurNAc
- GM-AEJA-GM-AEJ (Amidase Product) / (Amidase) How does that work? Both chains seem to be there
- Can I have a list of MS1 -> MS2 graphs as test data?
- How important is it to match the residue IDs from the example? Do they matter or can they be anything?
- Can I assume that I'll never run into a Gly-Met stem? Or just Gly / Met? It is ambiguous...
- How do ions and multipliers affect the graph structures?
- Can I have a copy of the graph visualizing software?
- How should I color things?
- Where / what are the molecule IDs for anhydro-MurNAc?
- Are all of my stem residues actually valid?
