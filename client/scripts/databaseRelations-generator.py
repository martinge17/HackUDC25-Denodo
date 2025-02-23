import csv
import os
import itertools

def obtener_metadata(directorio):
    """Recopila metadatos y cabeceras de los archivos CSV"""
    metadata = {}
    for archivo in os.listdir(directorio):
        if not archivo.endswith('.csv'):
            continue
            
        nombre_base = os.path.splitext(archivo)[0].lower()
        ruta = os.path.join(directorio, archivo)
        
        with open(ruta, 'r', encoding='utf-8') as f:
            lector = csv.reader(f)
            try:
                columnas = [col.strip().lower() for col in next(lector)]
            except StopIteration:
                continue
                
            # Identificar columnas clave
            claves = {
                'code_cols': [col for col in columnas if col in ['code', nombre_base + '_code']],
                'codes_cols': [col for col in columnas if col.endswith('_codes')],
                'tiene_code': 'code' in columnas
            }
            
            metadata[nombre_base] = {
                'columnas': columnas,
                'claves': claves,
                'nombre_archivo': archivo,
                'cabecera': columnas  # Guardamos la cabecera completa
            }
    
    return metadata

def encontrar_relaciones(metadata):
    """Encuentra relaciones significativas excluyendo 'code' solitario"""
    relaciones = []
    nombres_archivos = metadata.keys()
    
    # Relación tipo 1: [nombre]_codes -> code en otro archivo
    for nombre, datos in metadata.items():
        for columna in datos['claves']['codes_cols']:
            archivo_destino = columna[:-6]  # Eliminar '_codes'
            if archivo_destino in nombres_archivos:
                if metadata[archivo_destino]['claves']['tiene_code']:
                    relaciones.append((
                        datos['nombre_archivo'],
                        metadata[archivo_destino]['nombre_archivo'],
                        columna,
                        'code'
                    ))
    
    # Relación tipo 2: Columnas code comunes (excluyendo solo 'code')
    for a, b in itertools.permutations(nombres_archivos, 2):
        comunes = set(metadata[a]['claves']['code_cols']) & set(metadata[b]['columnas'])
        if comunes and (comunes != {'code'} or len(comunes) > 1):
            relaciones.append((
                metadata[a]['nombre_archivo'],
                metadata[b]['nombre_archivo'],
                list(comunes),
                'code_comun'
            ))
    
    return relaciones

def formatear_relaciones(relaciones, metadata):
    """Formatea relaciones y añade cabeceras"""
    if not relaciones:
        return "No se encontraron relaciones significativas"
    
    reporte = ["Relaciones significativas encontradas:\n"]
    
    # Agrupar relaciones por tipo
    relaciones_code = [r for r in relaciones if r[3] == 'code']
    relaciones_comunes = [r for r in relaciones if r[3] == 'code_comun']
    
    if relaciones_code:
        reporte.append("\n🔑 Relaciones de clave externa:")
        for rel in relaciones_code:
            reporte.append(f"- {rel[0]} -> {rel[1]} (via {rel[2]} → code)")
    
    if relaciones_comunes:
        reporte.append("\n⇄ Relaciones por columnas comunes:")
        for rel in relaciones_comunes:
            cols = ', '.join(sorted(rel[2]))
            reporte.append(f"- {rel[0]} ↔ {rel[1]} (columnas: {cols})")
    
    # Añadir cabeceras de todos los archivos
    reporte.append("\n\nCabeceras de los archivos:")
    for nombre, datos in sorted(metadata.items(), key=lambda x: x[1]['nombre_archivo']):
        reporte.append(f"\n📄 {datos['nombre_archivo']}:")
        reporte.append(f"   {', '.join(datos['cabecera'])}")
    
    return '\n'.join(reporte)

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 2:
        print("Uso: python relaciones.py <directorio_csv>")
        sys.exit(1)
    
    directorio = sys.argv[1]
    metadata = obtener_metadata(directorio)
    relaciones = encontrar_relaciones(metadata)
    print(formatear_relaciones(relaciones, metadata))