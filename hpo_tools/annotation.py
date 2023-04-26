import datetime
import hashlib
import json
import logging
import os
import pickle
from collections import defaultdict
from typing import Dict, List, Literal

import numpy as np

from hpo_tools.ontology import Ontology

DataDict = Dict[str, List[str]]


class Annotation:
    def __init__(
        self,
        entity2hpo: DataDict,
        ontology: Ontology,
        max_expansion: int = -1,
        name: str = "",
        on_missing_terms: Literal["accept", "skip", "raise"] = "accept",
    ):
        self.name = name
        self.input_hash = hashlib.md5(json.dumps(entity2hpo, sort_keys=True).encode("utf8")).hexdigest()
        self.entity2hpo = {key: set(vals) for key, vals in entity2hpo.items()}
        self.ontology = ontology
        self.max_expansion = max_expansion
        self.on_missing_terms = on_missing_terms
        self.indexer = {entity: i for i, entity in enumerate(entity2hpo)}
        self.inverse_indexer = np.array([entity for i, entity in enumerate(entity2hpo)])
        self.hpo2entity, self.n_input_entities, self.N = self._annotate()
        self.counter = self._get_counts()
        self.ic = self._get_ic()

    def _get_missing_terms(self, hpo_ids):
        return [hpo_id for hpo_id in hpo_ids if hpo_id not in self.ontology.pheno_indexer]

    def _get_missing_terms_report(self) -> DataDict:
        timestamp = datetime.datetime.now().strftime("%d-%m-%Y-%h-%m-%s")
        # TODO Add alternative terms to the report:
        #   alternate_ids: map them to the main ID
        #   replaced_by for obsolete terms: map main ID to them
        #   consider for obsolete terms: map main ID to them

        # TODO Extract the log path somewhere
        log_path = os.path.join(
            os.environ["HOME"],
            "hpo_tools",
            f'missing_terms_report{"_" + self.name if self.name else ""}_{timestamp}.log',
        )
        print(42)
        report = {key: self._get_missing_terms(hpo_ids) for key, hpo_ids in self.entity2hpo.items()}
        report = {key: hpo_ids for key, hpo_ids in report.items() if hpo_ids}
        if not report:
            logging.info("All terms are present in ontology.")
            return {}
        with open(log_path, "w") as fout:
            json.dump(report, fout)
            logging.warning(f"Unknown HPO terms encountered. Check entities with missing terms in {log_path} file.")
        return report

    def _annotate(self):
        report = self._get_missing_terms_report()
        if report and self.on_missing_terms == "raise":
            raise RuntimeError("Missing HPO terms found. Check report.")
        if self.on_missing_terms == "skip":
            proper_entities = [key for key in self.entity2hpo if key not in report]
        else:
            proper_entities = [
                key for key, hpo_ids in self.entity2hpo.items() if len(report.get(key, [])) < len(hpo_ids)
            ]
        n_proper_entities = len(proper_entities)
        n_input_entities = len(self.entity2hpo)
        results = defaultdict(set)
        for entity, hpo_ids in self.entity2hpo.items():
            nodes = {self.ontology.pheno_indexer[hpo_id] for hpo_id in hpo_ids if hpo_id in self.ontology.pheno_indexer}
            if not nodes:
                continue
            if self.max_expansion:
                nodes = self.ontology.get_nodeset_ancestors(nodes, self.max_expansion)
            for node in nodes:
                results[node].add(self.indexer[entity])
        return results, n_input_entities, n_proper_entities

    def _get_counts(self):
        return np.array([len(self.hpo2entity[node]) for node in self.ontology.nodes])

    def _get_ic(self):
        return self.counter / self.N

    def to_pickle(self, file):
        with open(file, "wb") as fout:
            pickle.dump(self, fout)

    @staticmethod
    def from_pickle(file):
        with open(file, "rb") as fin:
            return pickle.load(fin)
