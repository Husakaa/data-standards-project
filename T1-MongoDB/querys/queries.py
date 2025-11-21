GEN_INTERACTION_NETWORK = [
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

RESEARCHER_PRODUCTIVITY = [
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


PUBLICATION_AUTHORS = [
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


PUBLICATION_FULL_ENRICHED = [
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


COLLABORATION_NETWORK_DEPTH2 = [
    {
        "$graphLookup": {
            "from": "researchers",
            "startWith": "$_id",
            "connectFromField": "_id",
            "connectToField": "researcher_ids",
            "as": "collaborators_level2",
            "maxDepth": 2,
            "restrictSearchWithMatch": {"affiliation.department": {"$in": ["Bioinformatics", "Genomics"]}}
        }
    },
    {
        "$project": {
            "name": 1,
            "direct_collabs": {"$size": "$publication_ids"},
            "level2_collabs": {"$size": "$collaborators_level2"},
            "collaborator_names": "$collaborators_level2.name"
        }
    },
    {"$sort": {"level2_collabs": -1}},
    {"$limit": 10}
]


GENE_TEMPORAL_EVOLUTION = [
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


BRIDGING_EXPERIMENTS = [
    {"$unwind": "$sample_ids"},
    {
        "$lookup": {
            "from": "samples",
            "localField": "sample_ids",
            "foreignField": "_id",
            "as": "sample_info"
        }
    },
    {"$unwind": "$sample_info"},
    {
        "$lookup": {
            "from": "researchers",
            "localField": "researcher_id",
            "foreignField": "_id",
            "as": "pi"
        }
    },
    {"$unwind": "$pi"},
    {
        "$group": {
            "_id": "$experiment_id",
            "title": {"$first": "$title"},
            "distinct_PIs": {"$addToSet": "$pi.affiliation.research_group.pi"},
            "distinct_institutions": {"$addToSet": "$pi.affiliation.institution"}
        }
    },
    {
        "$project": {
            "title": 1,
            "pi_count": {"$size": "$distinct_PIs"},
            "institution_count": {"$size": "$distinct_institutions"},
            "bridging_score": {"$multiply": [{"$size": "$distinct_PIs"}, {"$size": "$distinct_institutions"}]}
        }
    },
    {"$sort": {"bridging_score": -1}},
    {"$limit": 10}
]


NON_RESPONDER_ENRICHMENT = [
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


GEN_TO_PATIENT_FULL_JOIN = [
    {"$limit": 5},
    {
        "$lookup": {
            "from": "samples",
            "localField": "sample_ids",
            "foreignField": "_id",
            "as": "samples"
        }
    },
    {"$unwind": "$samples"},
    {
        "$lookup": {
            "from": "experiments",
            "localField": "samples.experiment_ids",
            "foreignField": "_id",
            "as": "experiments"
        }
    },
    {
        "$project": {
            "symbol": 1,
            "patient_id": "$samples.clinical_data.patient_id",
            "diagnosis": "$samples.clinical_data.diagnosis",
            "response": "$samples.clinical_data.treatment.response.status",
            "experiment_titles": "$experiments.title"
        }
    }
]



SAMPLE_IMPACT_LEADERBOARD = [
    {
        "$lookup": {
            "from": "genes",
            "localField": "genes_detected",
            "foreignField": "_id",
            "as": "genes"
        }
    },
    {
        "$lookup": {
            "from": "experiments",
            "localField": "_id",
            "foreignField": "sample_ids",
            "as": "experiments"
        }
    },
    {
        "$unwind": {
            "path": "$experiments",
            "preserveNullAndEmptyArrays": True
        }
    },
    {
        "$lookup": {
            "from": "publications",
            "localField": "experiments.publication_ids",
            "foreignField": "_id",
            "as": "publications"
        }
    },
    {
        "$unwind": {
            "path": "$publications",
            "preserveNullAndEmptyArrays": True
        }
    },
    {
        "$group": {
            "_id": "$_id",
            "patient_id": {"$first": "$clinical_data.patient_id"},
            "diagnosis": {"$first": "$clinical_data.diagnosis"},
            "response": {"$first": "$clinical_data.treatment.response.status"},
            "mutation_count": {
                "$sum": {
                    "$cond": [
                        {"$eq": [{"$ifNull": ["$genes.variant_annotation.somatic_mutation", False]}, True]},
                        1,
                        0
                    ]
                }
            },
            "total_citations": {
                "$sum": {"$ifNull": ["$publications.publication_details.metrics.citations", 0]}
            },
            "publication_count": {"$sum": 1}
        }
    },
    {
        "$addFields": {
            "combined_score": {
                "$add": [
                    "$total_citations",
                    {"$multiply": ["$mutation_count", 10]},
                    {"$multiply": ["$publication_count", 20]}
                ]
            }
        }
    },
    {"$sort": {"combined_score": -1}},
    {"$limit": 25},
    {
        "$project": {
            "_id": 0,
            "patient_id": 1,
            "diagnosis": 1,
            "response": 1,
            "mutation_count": 1,
            "publication_count": 1,
            "total_citations": 1,
            "combined_score": 1
        }
    }
]