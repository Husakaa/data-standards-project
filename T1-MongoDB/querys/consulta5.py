[
    {
        "$lookup": {
            "from": "publications",
            "localField": "publication_ids",
            "foreignField": "_id",
            "as": "pubs"
        }
    },
    {
        "$project": {
            "name": 1,
            "email": 1,
            "total_publications": {"$size": "$pubs"},
            "total_impact_factor": {"$sum": "$pubs.publication_details.metrics.impact_factor"}
        }
    },
    {"$sort": {"total_publications": -1, "total_impact_factor": -1}},
    {"$limit": 10}
]