[
    {
        '$lookup': {
            'from': 'Experiments', 
            'localField': '_id', 
            'foreignField': 'researcher_id', 
            'as': 'experiments'
        }
    }, {
        '$unwind': {
            'path': '$experiments'
        }
    }, {
        '$lookup': {
            'from': 'Samples', 
            'localField': 'experiments.sample_ids', 
            'foreignField': '_id', 
            'as': 'samples'
        }
    }, {
        '$unwind': {
            'path': '$samples'
        }
    }, {
        '$lookup': {
            'from': 'Genes', 
            'localField': 'samples.genes_detected', 
            'foreignField': '_id', 
            'as': 'genes'
        }
    }, {
        '$unwind': {
            'path': '$genes'
        }
    }, {
        '$lookup': {
            'from': 'Publications', 
            'localField': 'genes.publication_ids', 
            'foreignField': '_id', 
            'as': 'publications'
        }
    }, {
        '$project': {
            '_id': 0, 
            'researcher_name': '$name', 
            'researcher_email': '$email', 
            'experiment_id': '$experiments.experiment_id', 
            'experiment_title': '$experiments.title', 
            'sample_id': '$samples.sample_id', 
            'sample_source': '$samples.source', 
            'gene_symbol': '$genes.symbol', 
            'gene_name': '$genes.name', 
            'publications_titles': '$publications.title'
        }
    }
]