const items = $input.all();

// Control de errores: Asegurar que la entrada tiene exactamente 3 iteraciones
if (items.length !== 3) {
  throw new Error(`Error en el flujo: Se esperaban 3 iteraciones, pero llegaron ${items.length}.`);
}

// Extraemos los arrays de códigos predichos de las 3 iteraciones
const codigosIt1 = items[0].json.predicted_icf_codes || [];
const codigosIt2 = items[1].json.predicted_icf_codes || [];
const codigosIt3 = items[2].json.predicted_icf_codes || [];

// Intersección estricta: conservamos solo los códigos presentes en las 3 listas
const codigosConsenso = codigosIt1.filter(codigo => 
  codigosIt2.includes(codigo) && codigosIt3.includes(codigo)
);

// Retornamos un único objeto consolidado y aplanado
return [{
  json: {
    // Trazabilidad del texto original
    id_clinical_text: items[0].json.id_clinical_text,
    clinical_text: items[0].json.clinical_text,
    icf_codes: items[0].json.icf_codes, // Gold standard
    
    // Resultados del consenso
    predicted_icf_codes_consensus: codigosConsenso,
    consensus_criteria: "strict 3/3",
    
    // Iteraciones separadas como propiedades principales (Wide format)
    // Esto facilita la conversión directa a columnas en Python/R/SQL
    predicted_icf_it1: codigosIt1,
    predicted_icf_it2: codigosIt2,
    predicted_icf_it3: codigosIt3
  }
}];