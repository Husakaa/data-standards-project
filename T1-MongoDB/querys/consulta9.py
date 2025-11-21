[
    {"$unwind": "$genes_detected"},
    {
        "$lookup": {
            "from": "genes",
            "localField": "genes_detected",
            "foreignField": "_id",
            "as": "gene_info"
        }
    },
    {"$unwind": "$gene_info"},
    {
        "$group": {
            "_id": {
                "gene_symbol": "$gene_info.symbol",
                "response": "$clinical_data.treatment.response.status"
            },
            "avg_tpm": {"$avg": "$gene_info.expression_data.avg_tpm"},
            "count": {"$sum": 1}
        }
    },
    {"$match": {"count": {"$gte": 3}}},
    {"$sort": {"avg_tpm": -1}}
]