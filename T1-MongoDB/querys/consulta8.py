[
    {
        "$lookup": {
            "from": "publications",
            "localField": "_id",
            "foreignField": "gene_ids",
            "as": "pubs"
        }
    },
    {"$unwind": "$pubs"},
    {
        "$group": {
            "_id": "$symbol",
            "first_seen": {"$min": "$pubs.publication_details.year"},
            "last_seen": {"$max": "$pubs.publication_details.year"},
            "years_active": {"$addToSet": "$pubs.publication_details.year"},
            "total_pubs": {"$sum": 1}
        }
    },
    {"$sort": {"total_pubs": -1}}
]
