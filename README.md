![](https://github.com/hpo-tools/hpo_tools/actions/workflows/test_and_lint.yml/badge.svg)


A set of open-source tools to simplify phenotypic research.


This package uses the Human Phenotype Ontology. Find out more at http://www.human-phenotype-ontology.org.
See also the publication: Sebastian Köhler et al., The Human Phenotype Ontology in 2021, Nucleic Acids Research, Volume 49, Issue D1, 8 January 2021, Pages D1207–D1217, https://doi.org/10.1093/nar/gkaa1043


Implementation plan - phase 1

* [ ] `Ontology` class
  * [x] produce `networkx` graph from `.obo` file with `obonet`
  * [x] support local path
  * [x] support automatic download from `OBO Foundry`
  * [ ] attributes:
    * [ ] `graph`
      * [x] extract only the subgraph under "Phenotypic abnormality" term
      * [ ] add sanity check `nx.is_directed_acyclic_graph(graph)` to `__init__` and raise custom `OntologyParsingError` exception if it fails
      * [ ] Use this: https://networkx.org/documentation/stable/auto_examples/graph/plot_dag_layout.html to add layer structure to nodes
    * [x] `undirected_graph`
    * [x] `version`
    * [x] `indexer` and `inverse_indexer`
    * [ ] `categories`
  * [ ] methods:
    * [x] `__len__`
    * [x] `__iter__`
    * [x] children(hpo_id: str)
    * [x] parents(hpo_id: str)
    * [x] descendants(hpo_id: str, include_self: bool)
      * [ ] support `n: int` for maximum distance
    * [x] ancestors(hpo_id: str, include_self: bool)
      * [ ] support `n: int` for maximum distance
    * [x] depth(hpo_id: str)
    * [x] distance(source: str, target: str, undirected: bool)
    * [ ] inverse_distance(source: str, target: str, undirected: bool)
    * [ ] get_dist_matrix(n_processes: int)
    * [ ] add Leacock and Chodorow path-based similarity: https://www.sciencedirect.com/science/article/pii/S1532046406000645?viewFullText=true#bib36
    * [ ] (*) plot_subgraph
      * [ ] simple version: show a layered view of the subgraph
      * [ ] add optional `color: str` and `alpha: float` parameters to color nodes with a given color and given intensity
    * [ ] (*) Wang similarity
  * [ ] properties:
    * [x] nodes
    * [x] depths
    * [ ] topological_order
  * tests:
    * [ ] children, parents, ancestors, descendants
    * [ ] depth
    * [ ] depths
    * [ ] distance
    * [ ] get_dist_matrix
* [ ] Datasets
  * [ ] ClinVar --> extract variants with HPO terms
  * [ ] Rao et al. --> https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6035401/#CR33 (Additional file 1)
  * [ ] Crawfard et al. --> https://www.sciencedirect.com/science/article/pii/S1098360021050280?viewFullText=true#s0165 (Spreadsheet)
* [ ] `Annotation` class
  * [ ] support smoothing for IC calculation: allow user to choose
        return IC(0/N) = 0 or IC(0/N) = 1 or IC(0/N) = -log(1/(N+1))
    * See here: https://www.sciencedirect.com/science/article/pii/S0020025514006677 
  * [ ] support normalization to [0, 1] interval (IC_normalized(v) = IC(v) / IC(root))
    * See here: https://bmcbioinformatics.biomedcentral.com/articles/10.1186/1471-2105-9-S5-S4#Sec11
  * [ ] store total term count
    * [ ] raw
    * [ ] annotated
    * [ ] not found in HPO
  * [ ] store term counts
    * [ ] raw
    * [ ] propagated
  * [ ] review code
  * [ ] remove all the checks except on_missing_nodes: Literal['ignore', 'fail']
  * [ ] add tests
* [ ] IC-based term-to-term similarity
  * [ ] Profile functions with and without `ancestors_only` flag
  * [ ] Check a review study: https://www.sciencedirect.com/science/article/pii/S1532046406000645?via%3Dihub
  * [ ] Check unifying formula, new normalization approach and comment about issues with Resnik: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3775452/
  * [ ] Check GraSM: https://bmcbioinformatics.biomedcentral.com/articles/10.1186/1471-2105-9-S5-S4#ref-CR10
  * [ ] Add the similarity sources:
    * Resnik: https://bmcbioinformatics.biomedcentral.com/articles/10.1186/1471-2105-9-S5-S4#ref-CR5
    * Lin: https://bmcbioinformatics.biomedcentral.com/articles/10.1186/1471-2105-9-S5-S4#ref-CR6
    * Jiang and Conrath: https://bmcbioinformatics.biomedcentral.com/articles/10.1186/1471-2105-9-S5-S4#ref-CR7
    * simUI: https://bmcbioinformatics.biomedcentral.com/articles/10.1186/1471-2105-9-S5-S4#ref-CR13
    * simGIC: https://bmcbioinformatics.biomedcentral.com/articles/10.1186/1471-2105-9-S5-S4#ref-CR14
    * Review this for more sources: https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0115692
  * [ ] LIST ALL THE PLANNED SIMILARITY
  * [ ] ADD TESTS
* [ ] Set-to-Set similarity
  * TBD
* [ ] Sampling
  * [ ] random sets of terms (uniformly from HPO or based on frequencies from the given `Annotation`)
  * [ ] (*) random paths starting from the given term with given transition probabilities
* [ ] p-values
  * [ ] generate and store set-to-set similarity
    * two sets of given sizes
    * 1 fixed set and 1 set of given size
  * [ ] p value calculation for given similarity on top of precomputed similarities
  * [ ] simple multiple testing correction
* (*) [ ] Embedding-based term-to-term similarity
  * [ ] get mapping term->vector and produce distance matrix
  * [ ] aggregation:
    * [ ] mean
    * [ ] (???) weighted mean (weights ???)
    * [ ] (???) combine texts and embed

The epic high-level plan:
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
