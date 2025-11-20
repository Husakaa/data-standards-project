[
    {
        '$match': {
            'expression_data.tissues.tissue_type': 'Liver'
        }
    }, {
        '$lookup': {
            'from': 'Publications', 
            'localField': 'publication_ids', 
            'foreignField': '_id', 
            'as': 'publications'
        }
    }
]