import json
from rdflib import Graph, Literal, RDF, URIRef, Namespace, XSD

# 1. Configuración de Espacios de Nombres (Namespace)
# Ajustado según su archivo ontology.owl
BASE_URI = "http://www.semanticweb.org/disjsi/ontologies/2025/11/untitled-ontology-17#"
NS = Namespace(BASE_URI)

def create_rdf_graph():
    g = Graph()
    g.bind("", NS)

    # Rutas a sus archivos JSON (Entrega 1)
    files = {
        "Gene": "T1-MongoDB/data/genes.json",
        "Sample": "T1-MongoDB/data/samples.json",
        "Researcher": "T1-MongoDB/data/researchers.json",
        "Experiment": "T1-MongoDB/data/experiments.json",
        "Publication": "T1-MongoDB/data/publications.json"
    }

    # Procesamiento de cada colección
    for class_name, file_path in files.items():
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
                
            for item in data:
                # Crear URI del individuo usando su $oid de MongoDB
                id_str = item['_id']['$oid']
                subject = URIRef(NS[id_str])
                
                # Asignar Clase
                g.add((subject, RDF.type, getattr(NS, class_name)))

                # Mapeo de Propiedades de Datos (Ejemplos basados en sus JSON)
                if 'symbol' in item:
                    g.add((subject, NS.symbol, Literal(item['symbol'], datatype=XSD.string)))
                if 'avg_tpm' in item.get('expression_data', {}):
                    g.add((subject, NS.avg_tpm, Literal(item['expression_data']['avg_tpm'], datatype=XSD.decimal)))
                if 'name' in item:
                    g.add((subject, NS.name, Literal(item['name'], datatype=XSD.string)))
                if 'diagnosis' in item.get('clinical_data', {}):
                    g.add((subject, NS.diagnosis, Literal(item['clinical_data']['diagnosis'], datatype=XSD.string)))
                if 'h_index' in item.get('expertise', {}).get('skills', {}).get('metrics', {}):
                    h_index = item['expertise']['skills']['metrics']['h_index']
                    g.add((subject, NS.h_index, Literal(h_index, datatype=XSD.integer)))

                # Mapeo de Relaciones (Object Properties)
                # Ejemplo: Genes detectados en muestras
                if 'sample_ids' in item:
                    for s_id in item['sample_ids']:
                        target_id = s_id['$oid']
                        g.add((subject, NS.detectedInSample, URIRef(NS[target_id])))
                
                # Ejemplo: Publicaciones escritas por investigadores
                if 'researcher_ids' in item:
                    for r_id in item['researcher_ids']:
                        target_id = r_id['$oid']
                        g.add((subject, NS.authoredBy, URIRef(NS[target_id])))

        except FileNotFoundError:
            print(f"Advertencia: No se encontró el archivo {file_path}")

    # Guardar el grafo generado
    g.serialize(destination="grafo_generado.ttl", format="turtle")
    print("Grafo RDF generado exitosamente: grafo_generado.ttl")
    return g

def execute_generic_queries(graph, queries):
    """
    Lanza consultas SPARQL de forma genérica sobre el grafo.
    """
    print("\n--- Ejecutando Consultas SPARQL ---")
    
    # Prefijos comunes para todas las consultas
    prefix_str = f"PREFIX : <{BASE_URI}>\nPREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>\n"

    for i, q_body in enumerate(queries, 1):
        full_query = prefix_str + q_body
        print(f"\nResultado Consulta {i}:")
        try:
            results = graph.query(full_query)
            for row in results:
                # Convierte cada elemento de la fila a string para impresión genérica
                print(" | ".join([str(val) for val in row]))
        except Exception as e:
            print(f"Error en Consulta {i}: {e}")

if __name__ == "__main__":
    # Generar el grafo desde los datos de Mongo
    rdf_graph = create_rdf_graph()

    # Definir las 6 consultas (Punto 4)
    consultas_punto_4 = [
        "SELECT ?symbol ?tpm WHERE { ?g a :Gene ; :symbol ?symbol ; :avg_tpm ?tpm }",
        "SELECT ?name ?hi WHERE { ?r a :Researcher ; :name ?name ; :h_index ?hi . FILTER(?hi > 20) }",
        "SELECT ?diag WHERE { ?s a :Sample ; :diagnosis ?diag }",
        "SELECT ?gene ?sample WHERE { ?gene :detectedInSample ?sample }",
        "SELECT ?title WHERE { ?p a :Publication ; :title ?title }",
        "SELECT DISTINCT ?name WHERE { ?res :participatesInExperiment ?exp ; :name ?name . ?exp :type 'RNA-Seq' }"
    ]

    # Ejecución genérica
    execute_generic_queries(rdf_graph, consultas_punto_4)
