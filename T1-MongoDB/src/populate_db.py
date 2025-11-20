import json
import random
import os
from datetime import datetime, timedelta
from bson import ObjectId
from faker import Faker

# --- CONFIGURACIÓN ---
# Inicializar Faker
fake = Faker()

# Configuración de rutas robusta (funciona en Windows/Linux/Mac)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = "T1-MongoDB/data"

# --- DATOS REALES ESTÁTICOS (Mock Data de Alta Calidad) ---
# Usamos listas predefinidas para garantizar realismo sin llamar a APIs externas.

REAL_GENES = [
    {"symbol": "TP53", "id": "ENSG00000141510", "name": "Tumor Protein P53"},
    {"symbol": "BRCA1", "id": "ENSG00000012048", "name": "Breast Cancer Type 1 Susceptibility Protein"},
    {"symbol": "BRCA2", "id": "ENSG00000139618", "name": "Breast Cancer Type 2 Susceptibility Protein"},
    {"symbol": "EGFR", "id": "ENSG00000146648", "name": "Epidermal Growth Factor Receptor"},
    {"symbol": "VEGFA", "id": "ENSG00000112715", "name": "Vascular Endothelial Growth Factor A"},
    {"symbol": "APOE", "id": "ENSG00000130203", "name": "Apolipoprotein E"},
    {"symbol": "ESR1", "id": "ENSG00000091831", "name": "Estrogen Receptor 1"},
    {"symbol": "AKT1", "id": "ENSG00000142208", "name": "AKT Serine/Threonine Kinase 1"},
    {"symbol": "MYC", "id": "ENSG00000136997", "name": "MYC Proto-Oncogene"},
    {"symbol": "KRAS", "id": "ENSG00000133703", "name": "KRAS Proto-Oncogene, GTPase"},
    {"symbol": "PTEN", "id": "ENSG00000171862", "name": "Phosphatase and Tensin Homolog"},
    {"symbol": "GAPDH", "id": "ENSG00000111640", "name": "Glyceraldehyde-3-Phosphate Dehydrogenase"},
    {"symbol": "ACTB", "id": "ENSG00000075624", "name": "Actin Beta"},
    {"symbol": "TNF", "id": "ENSG00000232810", "name": "Tumor Necrosis Factor"},
    {"symbol": "IL6", "id": "ENSG00000136244", "name": "Interleukin 6"}
]

REAL_JOURNALS = [
    {"name": "Nature", "if": 69.504},
    {"name": "Science", "if": 63.714},
    {"name": "Cell", "if": 66.850},
    {"name": "Nature Genetics", "if": 41.307},
    {"name": "Bioinformatics", "if": 6.937},
    {"name": "Nucleic Acids Research", "if": 19.160},
    {"name": "The Lancet Oncology", "if": 54.433},
    {"name": "PLOS Computational Biology", "if": 4.767}
]

REAL_TISSUES = ["Liver", "Lung", "Breast Mammary Tissue", "Whole Blood", "Brain - Cortex", "Pancreas", "Colon"]

# --- UTILIDADES ---

def get_oid():
    return {"$oid": str(ObjectId())}

def random_date():
    start = datetime(2018, 1, 1)
    end = datetime.now()
    return {"$date": (start + (end - start) * random.random()).isoformat()}

# --- GENERADORES ---

def generate_genes(count=50):
    print(f"🧬 Generando {count} genes...")
    genes = []
    for i in range(count):
        # Usar datos reales cíclicamente si count > len(REAL_GENES)
        real_gene = REAL_GENES[i % len(REAL_GENES)]
        
        doc = {
            "_id": get_oid(),
            "gene_id": real_gene["id"] if i < len(REAL_GENES) else f"ENSG{fake.numerify('###########')}",
            "symbol": real_gene["symbol"] if i < len(REAL_GENES) else fake.lexify(text='???#').upper(),
            "name": real_gene["name"],
            "expression_data": {
                "avg_tpm": round(random.uniform(0.1, 1000.0), 2),
                "tissues": [{
                    "tissue_type": random.choice(REAL_TISSUES),
                    "tpm": round(random.uniform(0.5, 500.0), 2),
                    "conditions": {
                        "normal": round(random.uniform(5.0, 50.0), 2),
                        "tumor": round(random.uniform(50.0, 500.0), 2),
                        "statistics": {
                            "fold_change": round(random.uniform(1.5, 10.0), 2),
                            "p_value": random.uniform(0.00001, 0.05),
                            "adjusted_p_value": random.uniform(0.0001, 0.05)
                        }
                    }
                } for _ in range(random.randint(1, 3))]
            },
            "functional_annotation": {
                "go_terms": [f"GO:{fake.numerify('#######')}" for _ in range(3)],
                "pathways": [f"KEGG:{fake.numerify('#####')}"],
                "interactions": {
                    "protein_interactions": [random.choice(REAL_GENES)["symbol"] for _ in range(2)],
                    "network_properties": {
                        "degree": random.randint(1, 100),
                        "betweenness": random.random(),
                        "clustering_coefficient": random.random()
                    }
                }
            },
            "variants": [],
            "sample_ids": [],       # Se llena al vincular
            "publication_ids": []   # Se llena al vincular
        }
        genes.append(doc)
    return genes

def generate_researchers(count=30):
    print(f"👥 Generando {count} investigadores...")
    researchers = []
    for i in range(count):
        doc = {
            "_id": get_oid(),
            "researcher_id": f"RES_{i+1:03d}",
            "name": fake.name(),
            "email": fake.unique.email(),
            "affiliation": {
                "institution": fake.company() + " Institute",
                "department": random.choice(["Genomics", "Bioinformatics", "Oncology"]),
                "research_group": {
                    "name": f"Computational {fake.word().capitalize()} Lab",
                    "pi": fake.name(),
                    "funding": {
                        "grants": [{
                            "agency": random.choice(["NIH", "ERC", "Horizon 2020"]),
                            "project_id": f"PRJ-{fake.bothify('??##')}",
                            "amount": random.randint(100000, 2000000),
                            "period": "2022-2027"
                        }],
                        "total_budget": random.randint(500000, 5000000)
                    }
                }
            },
            "expertise": {
                "areas": ["Cancer Genomics", "Transcriptomics"],
                "skills": {
                    "computational": ["Python", "R", "Docker"],
                    "metrics": {
                        "h_index": random.randint(5, 60),
                        "total_citations": random.randint(100, 15000),
                        "publications_count": 0
                    }
                }
            },
            "experiment_ids": [],
            "publication_ids": []
        }
        researchers.append(doc)
    return researchers

def generate_samples(count=50, gene_pool=[]):
    print(f"🧪 Generando {count} muestras...")
    samples = []
    gene_ids = [g["_id"] for g in gene_pool]
    
    for i in range(count):
        doc = {
            "_id": get_oid(),
            "sample_id": f"SMP_{i+1:03d}",
            "source": random.choice(["Tumor Biopsy", "Blood Plasma", "Normal Tissue"]),
            "organism": "Homo sapiens",
            "clinical_data": {
                "patient_id": f"PAT_{fake.numerify('####')}",
                "diagnosis": "Invasive Ductal Carcinoma",
                "stage": random.choice(["I", "IIA", "IIB", "III", "IV"]),
                "treatment": {
                    "therapy_type": random.choice(["Chemotherapy", "Immunotherapy"]),
                    "drugs": random.sample(["Doxorubicin", "Paclitaxel", "Tamoxifen"], k=2),
                    "response": {
                        "evaluation_date": random_date(),
                        "status": random.choice(["Responder", "Non-Responder"]),
                        "biomarkers": {"ki67": random.randint(10, 90), "her2": random.choice(["+", "-"])}
                    }
                }
            },
            "processing": {
                "collection_date": random_date(),
                "storage_conditions": "-80C",
                "rna_extraction": {
                    "method": "TRIzol",
                    "rin_score": round(random.uniform(7.0, 10.0), 1),
                    "concentration": random.randint(50, 500),
                    "quality_metrics": {"a260_280": 2.0, "a260_230": 2.1, "integrity_assessment": "Good"}
                }
            },
            "experiment_ids": [],
            "genes_detected": random.sample(gene_ids, k=min(5, len(gene_ids))) if gene_ids else []
        }
        samples.append(doc)
    return samples

def generate_experiments(count=20, researchers_pool=[], samples_pool=[]):
    print(f"🔬 Generando {count} experimentos...")
    experiments = []
    res_ids = [r["_id"] for r in researchers_pool]
    samp_ids = [s["_id"] for s in samples_pool]
    
    for i in range(count):
        doc = {
            "_id": get_oid(),
            "experiment_id": f"EXP_{i+1:03d}",
            "title": f"RNA-Seq analysis of {fake.word()} cells",
            "type": "RNA-Seq",
            "date": random_date(),
            "status": "Completed",
            "methodology": {
                "platform": "Illumina NovaSeq 6000",
                "library_prep": "TruSeq Stranded mRNA",
                "sequencing_params": {
                    "read_length": 150,
                    "coverage": "50X",
                    "quality_control": {"q30_percentage": 92.5, "adapter_contamination": 0.1, "duplication_rate": 12.4}
                }
            },
            "researcher_id": random.choice(res_ids) if res_ids else None,
            "sample_ids": random.sample(samp_ids, k=min(3, len(samp_ids))) if samp_ids else [],
            "publication_ids": []
        }
        experiments.append(doc)
    return experiments

def generate_publications(count=15, researchers_pool=[], experiments_pool=[], genes_pool=[]):
    print(f"📚 Generando {count} publicaciones con contenido coherente...")
    publications = []
    res_ids = [r["_id"] for r in researchers_pool]
    exp_ids = [e["_id"] for e in experiments_pool]
    gene_symbols = [g["symbol"] for g in genes_pool]
    gene_ids = [g["_id"] for g in genes_pool]
    
    for i in range(count):
        # Seleccionar relaciones
        pub_researchers = random.sample(res_ids, k=min(4, len(res_ids))) if res_ids else []
        pub_experiments = random.sample(exp_ids, k=min(2, len(exp_ids))) if exp_ids else []
        
        # Seleccionar genes para el título/abstract
        selected_symbols = random.sample(gene_symbols, k=min(3, len(gene_symbols)))
        selected_gene_ids = [g_id for g_id, symbol in zip(gene_ids, gene_symbols) if symbol in selected_symbols]

        # Creación de título y abstract realista
        method = random.choice(["Integrative Analysis", "Machine Learning", "Single-Cell Sequencing"])
        topic = f"role of {selected_symbols[0]} and {selected_symbols[1]} in {random.choice(['cancer progression', 'drug resistance'])}"
        title = f"{method} reveals key findings on the {topic}"
        abstract = (
            f"This study employed {method.lower()} combined with RNA-sequencing data to investigate the {topic}. "
            f"We found that {selected_symbols[0]} expression is significantly correlated with patient survival (p={random.uniform(0.001, 0.05):.4f}). "
            f"Furthermore, {selected_symbols[1]} shows promise as a potential biomarker for early detection. "
            f"Our computational pipeline is available on GitHub/Docker."
        )

        journal = random.choice(REAL_JOURNALS)
        doc = {
            "_id": get_oid(),
            "pmid": fake.numerify('########'),
            "doi": f"10.1038/{fake.lexify('????')}.{fake.numerify('####')}",
            "title": title,
            "publication_details": {
                "journal": journal["name"],
                "year": random.randint(2021, 2024),
                "metrics": {
                    "impact_factor": journal["if"],
                    "citations": random.randint(0, 1500),
                    "altmetrics": {"news_mentions": random.randint(0, 30), "twitter_mentions": random.randint(50, 800), "attention_score": random.randint(10, 150)}
                }
            },
            "content": {
                "abstract": abstract,
                "keywords": [fake.word() for _ in range(5)],
                "datasets": {
                    "repositories": ["GEO", "SRA"],
                    "accessions": {"geo_series": f"GSE{fake.numerify('#####')}"}
                }
            },
            "researcher_ids": pub_researchers,
            "experiment_ids": pub_experiments,
            "gene_ids": selected_gene_ids
        }
        publications.append(doc)
    return publications

# --- ENLACE DE RELACIONES (Bidireccional) ---

def link_data(researchers, genes, samples, experiments, publications):
    print("🔗 Creando relaciones bidireccionales...")
    
    # Mapas para acceso rápido por OID string
    res_map = {r["_id"]["$oid"]: r for r in researchers}
    gene_map = {g["_id"]["$oid"]: g for g in genes}
    samp_map = {s["_id"]["$oid"]: s for s in samples}
    exp_map = {e["_id"]["$oid"]: e for e in experiments}
    
    # 1. Muestras <-> Genes
    for s in samples:
        for g_oid in s["genes_detected"]:
            g_id = g_oid["$oid"]
            if g_id in gene_map:
                gene_map[g_id]["sample_ids"].append(s["_id"])
    
    # 2. Experimentos <-> Investigadores y Muestras
    for e in experiments:
        r_id = e["researcher_id"]["$oid"]
        if r_id in res_map:
            res_map[r_id]["experiment_ids"].append(e["_id"])
            
        for s_oid in e["sample_ids"]:
            s_id = s_oid["$oid"]
            if s_id in samp_map:
                samp_map[s_id]["experiment_ids"].append(e["_id"])
    
    # 3. Publicaciones <-> Todo
    for p in publications:
        p_id = p["_id"]
        
        for r_oid in p["researcher_ids"]:
            r_id = r_oid["$oid"]
            if r_id in res_map:
                res_map[r_id]["publication_ids"].append(p_id)
                res_map[r_id]["expertise"]["skills"]["metrics"]["publications_count"] += 1
                
        for e_oid in p["experiment_ids"]:
            e_id = e_oid["$oid"]
            if e_id in exp_map:
                exp_map[e_id]["publication_ids"].append(p_id)
                
        for g_oid in p["gene_ids"]:
            g_id = g_oid["$oid"]
            if g_id in gene_map:
                gene_map[g_id]["publication_ids"].append(p_id)

# --- MAIN ---

if __name__ == "__main__":
    print("🚀 Iniciando generación de datos híbridos (Realistas + Sintéticos)...")
    print(f"📂 Directorio de salida: {OUTPUT_DIR}")
    
    # Generar
    genes = generate_genes(50)
    researchers = generate_researchers(30)
    samples = generate_samples(50, genes)
    experiments = generate_experiments(25, researchers, samples)
    publications = generate_publications(15, researchers, experiments, genes)
    
    # Vincular
    link_data(researchers, genes, samples, experiments, publications)
    
    # Guardar
    data_map = {
        "genes.json": genes,
        "researchers.json": researchers,
        "samples.json": samples,
        "experiments.json": experiments,
        "publications.json": publications
    }
    
    for filename, data in data_map.items():
        path = os.path.join(OUTPUT_DIR, filename)
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False, default=str)
        print(f"✅ Generado: {filename} ({len(data)} registros)")
        
    print("\n✨ ¡Proceso completado! Datos listos para importar.")