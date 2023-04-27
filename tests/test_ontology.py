from hpo_tools.ontology import Ontology


class TestBuild:
    def test_from_obo_file(self):
        path = '../data/hp.obo'
        ontology = Ontology.from_obo_file(path)
        assert ontology.version == '2023-04-05', 'Version mismatch.'
        term = 'HP:0041117'
        node = ontology.pheno_indexer[term]
        assert ontology.names[node] == 'Fractured lower limb segment', 'Name mismatch'
        parents = {ontology.inverse_pheno_indexer(p) for p in ontology.parents[node]}
        assert parents == {'HP:0040064'}, 'Parent mismatch'
        children = [ontology.inverse_pheno_indexer(c) for c in ontology.children[node]]
        assert children == {'HP:0041064', 'HP:0041162'}
