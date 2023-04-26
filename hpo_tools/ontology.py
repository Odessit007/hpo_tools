from typing import (
    Dict,
    Iterable,
    List,
    Optional,
    Set,
    Tuple
)

import pandas as pd  # TODO Temporary
import pronto


def _traverse_pronto(
        hpo: pronto.Ontology,
        term: pronto.term.Term,
        is_a: Dict[str, List[str]]
):
    is_a[term.id] = [t.id for t in term.superclasses(1, False) if t.id != 'HP:0000001']
    for c in term.subclasses(1, False):
        _traverse_pronto(hpo, c, is_a)


class Ontology:
    root_id = 'HP:0000118'

    @classmethod
    def from_obo_file(cls, path):
        hpo = pronto.Ontology(path)
        return cls._from_obo(hpo)

    @classmethod
    def from_obo_library(cls):
        hpo = pronto.Ontology.from_obo_library('hp.obo')
        return cls._from_obo(hpo)

    @classmethod
    def _from_obo(cls, hpo: pronto.Ontology):
        root = hpo.get_term(cls.root_id)
        version = hpo.metadata.data_version.split('/')[-1]
        is_a = {}
        _traverse_pronto(hpo, root, is_a)
        hpo_ids = list(is_a.keys())
        names = [hpo[hpo_id].name for hpo_id in hpo_ids]
        return cls(hpo_ids, names, is_a, version)

    @classmethod
    def from_phenodf(cls, phenodf: pd.DataFrame):
        hpo_ids: List[str] = list(phenodf.index)
        names: List[str] = phenodf['name'].tolist()
        is_a = {index: row['is_a'] for index, row in phenodf.iterrows()}
        return cls(hpo_ids, names, is_a)

    def __init__(
            self,
            hpo_ids: List[str],
            names: List[str],
            is_a: Dict[str, List[str]],
            version: Optional[str] = None
    ):
        self.hpo_ids = hpo_ids
        self.names = names
        self.n_terms = len(hpo_ids)
        self.version = version

        self.pheno_indexer: Dict[str, int] = {hpo_id: node for (node, hpo_id) in enumerate(hpo_ids)}
        self.inverse_pheno_indexer: List[str] = [hpo_id for (hpo_id, node) in self.pheno_indexer.items()]
        self.nodes: List[int] = list(self.pheno_indexer.values())

        self.root: int = self.pheno_indexer[self.root_id]
        children, parents = self._build_graph(is_a)
        self.children: List[List[int]] = children
        self.parents: List[List[int]] = parents

        self.category_nodes = sorted(children[self.root])
        self.categories: List[Set[int]] = self._build_categories()
        self.ancestors: List[Set[int]] = [self.get_node_ancestors(node) for node in self.nodes]
        self.annotations = {}

    def get_node(self, node, mode='name'):
        if mode == 'raw':
            return node
        elif mode == 'name':
            return self.names[node]
        elif mode == 'id':
            return self.inverse_pheno_indexer[node]
        raise RuntimeError(f"Bad mode {mode}. Must be one of 'raw', 'name' or 'id'")

    def get_node_neighborhood(self, node, mode='name'):
        return {
            self.get_node(node, mode): {
                'children': {self.get_node(child, mode) for child in self.children[node]},
                'parents': {self.get_node(parent, mode) for parent in self.parents[node]}
            }
        }

    def _build_graph(
            self,
            is_a: Dict[str, List[str]],
            sanity_check: bool = True
    ) -> Tuple[List[List[int]], List[List[int]]]:
        children = [[] for _ in self.nodes]
        parents = [[] for _ in self.nodes]
        for hpo_id, node in self.pheno_indexer.items():
            if node == self.root:  # ROOT's child is set to ROOT in the dataframe, but we want a proper DAG
                continue
            parent_ids = is_a[hpo_id]
            for parent_id in parent_ids:
                parent = self.pheno_indexer[parent_id]
                children[parent].append(node)
                parents[node].append(parent)
        if sanity_check:
            # Checking that ROOT is a source node (no parents)
            for children_ in children:
                assert self.root not in children_
            assert not parents[self.root]
            # Checking that ROOT is the only source node
            n_nodes_with_parents = sum(bool(p) for p in parents)
            assert n_nodes_with_parents == len(self.nodes) - 1
        return children, parents

    def _traverse_to_category(
            self,
            node: int,
            node2cat: Dict[int, Set[int]]
    ) -> None:
        node_categories = set()
        for p in self.parents[node]:
            if p not in node2cat:  # Previously unvisited node
                self._traverse_to_category(p, node2cat)
            node_categories.update(node2cat[p])
        node2cat[node] = node_categories

    def _build_categories(self) -> List[Set[int]]:
        node2cat = {cat: {cat} for cat in self.category_nodes}
        node2cat[self.root] = set()
        for node in self.nodes:
            if not self.children[node]:  # Traverse from leaves to the top
                self._traverse_to_category(node, node2cat)
        return [node2cat[node] for node in self.nodes]

    def get_categories(
            self,
            node: int,
            simplify: bool = False
    ) -> str:
        node_categories = [self.names[cat] for cat in self.categories[node]]
        node_categories = [
            cat.lower()
            .replace('abnormality of the', '')
            .replace('abnormality of', '')
            .replace('abnormality', '')
            .replace('abnormal', '')
            .replace('system', '')
            .replace('blood and blood-forming tissues', 'blood')
            .replace('prenatal development or birth', 'prenatal/birth')
            .strip()
            if simplify else cat
            for cat in node_categories
        ]
        return ', '.join(sorted(node_categories))

    def _get_node_ancestors(
            self,
            node: int,
            max_dist: int = -1,
            cur_dist: int = 0
    ) -> Set[int]:
        if cur_dist == max_dist or node == self.root:
            return {node}
        ans = {node}
        for p in self.parents[node]:
            # Not the best implementation (intermediate values are not stored) but fast enough and runs only once
            ans.update(self._get_node_ancestors(p, max_dist, cur_dist + 1))
        return ans

    def get_node_ancestors(
            self,
            node: int,
            max_dist: int = -1
    ) -> Set[int]:
        return self._get_node_ancestors(node, max_dist)

    def get_nodeset_ancestors(
            self,
            nodes: Iterable[int],
            max_dist: int = -1
    ) -> Set[int]:
        ans = set()
        for node in set(nodes):
            ans |= self.get_node_ancestors(node, max_dist)
        return ans
