import json
import os
import xml.etree.ElementTree as ET
from xml.dom import minidom

# --- CONFIGURACIÓN DE RUTAS RELATIVAS ---
# 1. Obtenemos la carpeta donde está este script (T2-XML/src)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# 2. Subimos dos niveles para llegar a la raíz del proyecto
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "..", ".."))

# 3. Definimos las rutas de entrada (JSON) y salida (XML) desde la raíz
JSON_DIR = os.path.join(PROJECT_ROOT, "T1-MongoDB", "data")
XML_DIR = os.path.join(PROJECT_ROOT, "T2-XML", "xml")

# Crear directorio de salida si no existe
if not os.path.exists(XML_DIR):
    os.makedirs(XML_DIR)

# --- MAPEO DE LISTAS (JSON -> XSD) ---
# Este diccionario le dice al script cómo nombrar los elementos hijos de una lista.
# Ejemplo: si la clave JSON es "sample_ids", el hijo XML será <sample_id>
LIST_ITEM_MAPPING = {
    # Experiments
    "sample_ids": "sample_id",
    "publication_ids": "publication_id",
    "experiment_ids": "experiment_id",
    "gene_ids": "gene_id",
    "researcher_ids": "researcher_id",
    
    # Samples
    "drugs": "drug",
    "genes_detected": "gene_id", # En samples.json es genes_detected, en XSD es gene_id
    
    # Genes
    "tissues": "tissue",
    "go_terms": "term",
    "pathways": "pathway",
    "protein_interactions": "protein",
    "variants": "variant",
    
    # Researchers
    "grants": "grant",
    "areas": "area",
    "computational": "language", # En researchers.xsd es <language>
    
    # Publications
    "keywords": "keyword",
    "repositories": "repository"
}

def clean_mongo_types(value):
    """
    Limpia los tipos específicos de MongoDB ($oid, $date) para que sean
    strings simples o fechas válidas en XML.
    """
    if isinstance(value, dict):
        if "$oid" in value:
            return value["$oid"]
        if "$date" in value:
            # Extraemos solo la parte YYYY-MM-DD para compatibilidad con xs:date
            return value["$date"].split('T')[0] 
    return str(value)

def build_xml_element(parent, data, key_name=None):
    """
    Función recursiva que recorre el diccionario JSON y construye
    el árbol XML correspondiente.
    """
    if isinstance(data, dict):
        # Caso especial: Si es un tipo de dato de Mongo ($oid, $date), extraemos el valor
        if "$oid" in data or "$date" in data:
            parent.text = clean_mongo_types(data)
            return

        for key, value in data.items():
            # Ignoramos metadatos internos si los hubiera
            if key.startswith("__"): continue
            
            if isinstance(value, list):
                # Si es una lista, creamos el contenedor padre (ej: <sample_ids>)
                list_container = ET.SubElement(parent, key)
                
                # Determinamos el nombre del elemento hijo singular usando el MAPEO
                child_name = LIST_ITEM_MAPPING.get(key, "item")
                
                for item in value:
                    child = ET.SubElement(list_container, child_name)
                    build_xml_element(child, item)
            else:
                # Si es un diccionario o valor simple, creamos la etiqueta
                child = ET.SubElement(parent, key)
                build_xml_element(child, value)
                
    elif isinstance(data, list):
        # Este caso maneja listas que no tienen clave padre directa en la recursión
        for item in data:
            child_name = LIST_ITEM_MAPPING.get(key_name, "item")
            child = ET.SubElement(parent, child_name)
            build_xml_element(child, item)
            
    else:
        # Valor final (texto, número, booleano)
        parent.text = str(data)

def convert_file(collection_name, root_element_name):
    """
    Lee un archivo JSON y genera su equivalente XML.
    """
    json_path = os.path.join(JSON_DIR, f"{collection_name}.json")
    xml_path = os.path.join(XML_DIR, f"{collection_name}.xml")
    
    if not os.path.exists(json_path):
        print(f"⚠️  No se encontró: {json_path}")
        return

    print(f"🔄 Transformando {collection_name}.json -> {collection_name}.xml ...")
    
    with open(json_path, 'r', encoding='utf-8') as f:
        data_list = json.load(f)

    # Crear elemento raíz del archivo XML (el nombre de la colección en plural)
    # Aunque el XSD define el elemento singular, un XML válido necesita un root único
    root = ET.Element(collection_name)

    for doc in data_list:
        # Crear el elemento individual (ej: <experiment>) definido en el XSD
        item = ET.SubElement(root, root_element_name)
        build_xml_element(item, doc)

    # Formatear el XML para que sea legible (pretty print)
    xml_str = minidom.parseString(ET.tostring(root)).toprettyxml(indent="    ")
    
    with open(xml_path, "w", encoding="utf-8") as f:
        f.write(xml_str)
    
    print(f"✅ Generado correctamente en: {xml_path}")

if __name__ == "__main__":
    print("🚀 INICIANDO POBLACIÓN DE XML DESDE DATOS MONGODB")
    print(f"📂 Directorio de scripts: {SCRIPT_DIR}")
    print(f"📂 Leyendo JSON desde:   {JSON_DIR}")
    print(f"📂 Escribiendo XML en:   {XML_DIR}\n")
    
    # Lista de colecciones a procesar
    # Tupla: (Nombre archivo JSON, Nombre etiqueta raíz singular del XSD)
    collections = [
        ("experiments", "experiment"),
        ("samples", "sample"),
        ("genes", "gene"),
        ("researchers", "researcher"),
        ("publications", "publication")
    ]
    
    for col, root_name in collections:
        convert_file(col, root_name)
        
    print("\n✨ ¡Proceso completado! Los datos XML son consistentes con MongoDB.")