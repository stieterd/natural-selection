from dataclasses import dataclass
import numpy as np

@dataclass
class Gene(object): # size

    dnaType: dict


gene = Gene({"MotherP": 2, "Motherq":32, "FatherP": 32, "Fatherq": 112})
for keys in gene.dnaType:

    gene.dnaType()