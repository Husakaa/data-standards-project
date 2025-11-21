[
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