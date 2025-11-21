[
    {"$match": {"symbol": "BRCA2"}},
    {
        "$graphLookup": {
            "from": "genes",
            "startWith": "$functional_annotation.interactions.protein_interactions",
            "connectFromField": "functional_annotation.interactions.protein_interactions",
            "connectToField": "symbol",
            "as": "interaction_network",
            "maxDepth": 4
        }
    },
    {
        "$lookup": {
            "from": "publications",
            "localField": "interaction_network._id",
            "foreignField": "gene_ids",
            "as": "network_publications"
        }
    },
    {
        "$project": {
            "_id": 0,
            "start_gene": "$symbol",
            "network_size": {"$size": "$interaction_network"},
            "interacting_genes": "$interaction_network.symbol",
            "publications": "$network_publications.title"
        }
    }
]