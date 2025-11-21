[
    {
        "$lookup": {
            "from": "researchers",
            "localField": "researcher_ids",
            "foreignField": "_id",
            "as": "author_details"
        }
    },
    {
        "$project": {
            "title": 1,
            "year": "$publication_details.year",
            "journal": "$publication_details.journal",
            "authors": "$author_details.name"
        }
    }
]