import ms2.data
import os.path as path
import csv


# FIXME Numbering of residues should be per-Peptidoglycan (it should restart)
class Peptidoglycan:
    def __init__(self, structure):
        # 1. Split on `-` into letter groups
        # 2. Try to convert each into either a `Chain` or `Stem`, returning
        #    `None` if attempting to construct a `Chain` from Stem residues
        #    or vice versa
        # 3. Remove any `None`s and store the `Chain`s and `Stem`s separately
        # 4. Determine how the components are connected, building a bond-list
        self.structure = structure
        self.components = [Chain(p) or Stem(p) for p in structure.split("-")]
        # Build a tree of possible bonds? Some might be mutually exclusive, so
        # this can be done recusively to generate different possible structures
        # FIXME Bonds need to be stored in Residues. Perhaps residues should
        # have a map of bonding sites (formed during construction) that stores
        # to residue each site is bound to
        self.bonds = []
        for comp in self.components:
            acceptors = comp.bond_acceptors()
            for donor in [d for d in self.components if d != comp]:
                self.bonds += [
                    (a, dr)
                    for a, ds in acceptors.items()
                    for d in ds
                    for dr in donor.get_residues(d)
                ]

    def write_graph(self, directory):
        # Write the node list
        with open(path.join(directory, f"{self.structure} NL.csv"), "w") as f:
            w = csv.writer(f)
            w.writerow(["node", "molecule_ID"])
            for comp in self.components:
                w.writerows([r.id, r.residue] for r in comp.residues)

        # Write the edge list
        with open(path.join(directory, f"{self.structure} EL.csv"), "w") as f:
            w = csv.writer(f)
            w.writerow(["node1", "node2"])
            for a, d in self.bonds:
                w.writerow([a.id, d.id])
            for comp in self.components:
                for i in range(len(comp.residues) - 1):
                    w.writerow([r.id for r in comp.residues[i : i + 2]])


# FIXME This is a somewhat vile OO pattern... I think I need to move away from
# the hacky __new__ + inheritance magic
class Component:
    def __new__(cls, structure, ischain):
        valid = ms2.data.chain_residues if ischain else ms2.data.stem_residues
        if all(r in valid for r in structure):
            instance = object.__new__(cls)
            super(cls, instance).__init__(structure, ischain)
            return instance
        else:
            return None

    def __init__(self, structure, ischain):
        self.residues = [Residue(r, inchain=ischain) for r in structure]

    def __repr__(self):
        return str(f"{type(self).__name__}: {self.residues}")

    def bond_acceptors(self):
        return {
            r: ba
            for r in self.residues
            if (ba := ms2.data.bond_acceptors.get(r.residue))
        }

    def get_residues(self, residue_type):
        return [r for r in self.residues if r.residue == residue_type]

    # FIXME Add a get_bonds once I move inter-component bond tracking from
    # Peptidoglycan to Residue. This function will also return the implied,
    # linear bonds within the component


class Chain(Component):
    def __new__(cls, structure):
        return super().__new__(cls, structure, True)

    def __init__(*_):
        pass


class Stem(Component):
    def __new__(cls, structure):
        return super().__new__(cls, structure, False)

    def __init__(*_):
        pass

    def get_residues(self, residue_type):
        if residue_type == "N_terminus":
            return self.residues[:1]
        elif residue_type == "C_terminus":
            return self.residues[-1:]
        else:
            return super().get_residues(residue_type)


class Residue:
    count = 0

    def __init__(self, residue, *, inchain=False):
        # The same letter can mean different things in a chain and in a stem!
        abbr_dict = ms2.data.chain_abbr if inchain else ms2.data.stem_abbr
        # Attempt to resolve residues like GlcNAc, MurNAc, and mDAP
        self.residue = abbr_dict.get(residue) or residue
        # Generate a unique residue ID using the class counter
        Residue.count += 1
        self.id = self.residue + str(Residue.count)

    def __repr__(self):
        return self.residue
