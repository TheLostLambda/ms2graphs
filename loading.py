import pandas
import re


class Structure:
    regex = r'(?:(\S*) )?([A-Z-]+)(?: \(x(\d)\))?(?: \((.*)\) )?\|(\d)'
    pattern = re.compile(regex)

    def __init__(self, structure):
        ion, struct, mult, annot, mod = self.pattern.match(structure).groups()
        # FIXME: I should eventually do some validation work here!
        self.ion = ion
        self.structure = struct
        self.multiplier = int(mult) if mult else None
        self.annotation = annot
        self.modification = int(mod) if mod else None

    def __repr__(self):
        return str(vars(self))


def parse_structures(structures):
    return list(map(Structure, structures.split(',')))


# Read all non-NA `inferredStructures` from the MS1 data
ms1_structures = pandas.read_csv('data/ms1.csv')['inferredStructure'].dropna()
# Process the `inferredStructures` into a more amiable format
ms1_structures = ms1_structures.apply(parse_structures)
