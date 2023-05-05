from hpo_tools.ontology import Ontology


class TestBuild:
    ontology = Ontology('data/hp.obo')

    def test_ontology_sanity(self):
        ontology = self.ontology
        assert ontology.version == "2023-04-05", "Version mismatch"
        assert ontology.nodes["HP:0000118"]["name"] == "Phenotypic abnormality", "Issues with `nodes` access"
        assert isinstance(next(iter(ontology)), str), "Iteration doesn't work or returns a wrong type"
        assert len(ontology) == len(ontology.graph), "__len__ is not implemented or incorrect"

    def test_children(self):
        ontology = self.ontology
        msg = "Wrong children for node {node}"

        node = "HP:0041117"
        children = ontology.children(node)
        assert children == {"HP:0041064", "HP:0041162"}, msg.format(node=node)

        node = "HP:0100751"
        children = ontology.children(node)
        assert children == {"HP:0011459", "HP:0031463", "HP:0100580"}, msg.format(node=node)

        node = "HP:0001621"
        children = ontology.children(node)
        assert children == set(), msg.format(node=node)

    def test_parents(self):
        ontology = self.ontology
        msg = "Wrong parents for node {node}"

        node = "HP:0041117"
        parents = ontology.parents(node)
        assert parents == {"HP:0040064"}, msg.format(node=node)

        node = "HP:0100751"
        parents = ontology.parents(node)
        assert parents == {"HP:0007378", "HP:0002031", "HP:0012288"}, msg.format(node=node)

        node = "HP:0001621"
        parents = ontology.parents(node)
        assert parents == {"HP:0001608"}, msg.format(node=node)

        node = "HP:0000118"
        parents = ontology.parents(node)
        assert parents == set(), msg.format(node=node)

    def test_descendants(self):
        ontology = self.ontology
        msg = "Wrong descendants for node {node}"

        node = "HP:0001621"
        assert ontology.descendants(node) == {"HP:0001621"}, msg.format(node=node)
        assert ontology.descendants(node, include_self=False) == set(), msg.format(node=node)

        # TODO More test cases

    def test_ancestors(self):
        ontology = self.ontology
        msg = "Wrong ancestors for node {node}"

        node = "HP:0000118"
        assert ontology.ancestors(node) == {"HP:0000118"}, msg.format(node=node)
        assert ontology.ancestors(node, include_self=False) == set(), msg.format(node=node)

        # TODO More test cases

    def test_depths(self):
        ontology = self.ontology
        nodes = ["HP:0000118", "HP:0002664", "HP:0012243", "HP:0030675"]
        expected_depths = [0, 1, 3, 9]
        for node, expected_depth in zip(nodes, expected_depths):
            assert ontology.depth(node) == expected_depth, f"Wrong depth for node {node} via Ontology().depth()"
            assert ontology.depths[node] == expected_depth, f"Wrong depth for node {node} via Ontology().depths"

    def test_distance(self):
        # TODO
        pass

    def test_dist_matrix(self):
        # TODO
        pass
