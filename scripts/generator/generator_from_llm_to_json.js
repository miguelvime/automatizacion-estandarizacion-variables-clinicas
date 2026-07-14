// 1. Funciones puras (Single Responsibility Principle)
const extraerTextoBruto = (json) => {
  // El operador '?.' (Optional Chaining) evita errores si una propiedad no existe
  return json.response || 
         json.choices?.[0]?.message?.content || 
         json.output || 
         json.message;
};

const limpiarMarkdownJSON = (texto) => {
  const match = texto.match(/```(?:json)?\s*([\s\S]*?)\s*```/);
  return match ? match[1] : texto;
};

const parsearDatosLLM = (textoBruto, indice) => {
  const textoLimpio = limpiarMarkdownJSON(textoBruto);
  try {
    return JSON.parse(textoLimpio.trim());
  } catch (error) {
    throw new Error(`JSON inválido en iteración ${indice}. Texto: ${textoLimpio}`);
  }
};

const formatearHistoriasClinicas = (datosParseados, idCombinacion) => {
  const historias = datosParseados.clinical_object || datosParseados.historias_clinicas;
  
  if (!Array.isArray(historias)) return [];

  // Mapeo directo en lugar de bucles manuales
  return historias.map((historia, index) => ({
    id_clinical_text: `${idCombinacion}_${index + 1}`,
    clinical_text: historia.clinical_text
  }));
};

// 2. Ejecución principal
const datosOriginales = $('doc_to_json').all();
const inputsActuales = $input.all();

// En lugar de mutar un array con un bucle 'for', devolvemos uno nuevo con '.map()'
const resultadosFinales = inputsActuales.map((item, index) => {
  const textoBruto = extraerTextoBruto(item.json);
  
  if (!textoBruto) {
    throw new Error(`Variable de texto ausente en item ${index}.`);
  }

  const datosIA = parsearDatosLLM(textoBruto, index);
  const datosBase = datosOriginales[index].json; // Datos de referencia

  // 3. Ensamblaje final
  return {
    json: {
      id_code_combination: datosBase.id_code_combination,
      icf_codes: datosBase.icf_codes,
      icf_name: datosBase.icf_name,
      clinical_object: formatearHistoriasClinicas(datosIA, datosBase.id_code_combination)
    }
  };
});

return resultadosFinales;