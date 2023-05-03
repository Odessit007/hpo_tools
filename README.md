![](https://github.com/hpo-tools/hpo_tools/actions/workflows/test_and_lint.yml/badge.svg)


A set of open-source tools to simplify phenotypic research.


This package uses the Human Phenotype Ontology. Find out more at http://www.human-phenotype-ontology.org.
See also the publication: Sebastian Köhler et al., The Human Phenotype Ontology in 2021, Nucleic Acids Research, Volume 49, Issue D1, 8 January 2021, Pages D1207–D1217, https://doi.org/10.1093/nar/gkaa1043


The epic plan:
* basic ontology interaction utils
  * [Phase 1] download and read .obo file (via Pronto)
  * [Phase 1] get node ancestors for arbitrary distance
  * [Phase 1] get node depth
  * [Phase 2] get distance between two nodes
  * [Phase 2] sort nodes in lexicographic order
* similarity
  * [Phase 1] information content-based similarity:
    * basic annotation utils
    * Resnik
    * Lin and variations
    * JC
    * intersection over union
    * set-to-set similarity
  * [Phase 2] node embeddings based on their text definitions
  * [Phase 2] Word2Vec-based node embeddings
  * [Phase 2] graph neural networks-based node embeddings
* sampling
  * [Phase 1] random terms
  * [Phase 1] random sets of terms
  * [Phase 2] random paths starting from the given term with given state change probabilities
* p-values
  * [Phase 1] set-to-set similarity for random/fixed content and size of the term sets
  * [Phase 1] simple multiple testing correction
* [Phase 2] check HPO terms
  * if they are deprecated suggest new options
  * if they are missing suggest updating HPO version
  * generate report
* [Phase 2] visualization
  * sub-graphs
  * similarity
    * heat matrix
    * "vertical" plot
  * phenograms for cohort analysis
    * sub-graph with nodes alpha proportional to some statistics within the cohort
    * cohort VS full dataset


The goal of phase 1 is to be able to reproduce the Phenomizer paper.
