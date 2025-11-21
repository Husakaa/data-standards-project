[
    {
        "$lookup": {
            "from": "researchers",
            "localField": "researcher_ids",
            "foreignField": "_id",
            "as": "authors"
        }
    },
    {
        "$lookup": {
            "from": "genes",
            "localField": "gene_ids",
            "foreignField": "_id",
            "as": "genes_info"
        }
    },
    {
        "$project": {
            "title": 1,
            "year": "$publication_details.year",
            "journal": "$publication_details.journal",
            "authors": "$authors.name",
            "genes": "$genes_info.symbol",
            "citations": "$publication_details.metrics.citations"
        }
    },
    {"$sort": {"citations": -1}}
]