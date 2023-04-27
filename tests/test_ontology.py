from typing import List

from hpo_tools.ontology import Ontology


class TestBuild:
    @staticmethod
    def _get_term_set(ontology: Ontology, nodes: List[int]):
        return {ontology.inverse_pheno_indexer[node] for node in nodes}

    def test_from_obo_file(self):
        path = "data/hp.obo"
        ontology = Ontology.from_obo_file(path)
        assert ontology.version == "2023-04-05", "Version mismatch."
        term = "HP:0041117"
        node = ontology.pheno_indexer[term]
        assert ontology.names[node] == "Fractured lower limb segment", "Name mismatch"
        parents = self._get_term_set(ontology, ontology.parents[node])
        assert parents == {"HP:0040064"}, "Parent mismatch"
        children = self._get_term_set(ontology, ontology.children[node])
        assert children == {"HP:0041064", "HP:0041162"}
