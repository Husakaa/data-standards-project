[
    {
        '$match': {
            'experiment_id': 'EXP_001'
        }
    }, {
        '$lookup': {
            'from': 'Samples', 
            'localField': 'sample_ids', 
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
            'as': 'genes_detected'
        }
    }
]