import logging
logging.basicConfig(level=logging.INFO)

from hpo_tools.annotation import Annotation
from hpo_tools.ontology import Ontology


if __name__ == '__main__':
    # from utils.data_flow import get_pheno_vectors
    # pheno_vectors, phenotypes_df = get_pheno_vectors(
    #     '/Users/ivustianiu/PycharmProjects/research/clustering/data/phenotypes_zoidberg50.json'
    # )
    # phenotypes_df.index = phenotypes_df.index.str.replace('EMG_PHENOTYPE_', 'HP:')
    # n_phenotypes = len(phenotypes_df)
    # assert len(set(phenotypes_df.index)) == len(phenotypes_df)
    # phenotypes_df['is_a'] = phenotypes_df['is_a'].apply(
    #     lambda vals: [val.replace('EMG_PHENOTYPE_', 'HP:') for val in vals]
    # )
    # phenotypes_df.loc['HP:0000118', 'name'] = 'Phenotypic abrnomality'
    # ontology = Ontology.from_phenodf(phenotypes_df)
    ontology = Ontology.from_obo_file('/Users/ivustianiu/hpo_tools/hp.obo')

    import json
    with open('/Users/ivustianiu/PycharmProjects/research/clustering/omim.json') as fin:
        omim = json.load(fin)
    a = Annotation(omim, ontology, name='omim')
    a.to_pickle('/opt/data/phenosets/tmp.anno')
    b = Annotation.from_pickle('/opt/data/phenosets/tmp.anno')

    # try:
    #     import numba
    #     NUMBA = True
    # except ImportError:
    #     NUMBA = False
    # if NUMBA:
    #     results = numba.typed.List(
    #         [np.array(sorted(results.get(node, [])), dtype=np.int32) for node in self.graph.nodes]
    #     )
