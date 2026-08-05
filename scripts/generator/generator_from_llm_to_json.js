const extractRawText = (json) => {
  // Si la respuesta viene envuelta en un array en la raíz (ej. [{ content: ... }])
  if (Array.isArray(json)) {
    json = json[0];
  }
  
  // Cubre la estructura nativa de Gemini y el output de LangChain
  return json?.content?.parts?.[0]?.text || 
         json?.text ||
         json?.response || 
         json?.choices?.[0]?.message?.content || 
         json?.output || 
         json?.message;
};

const cleanMarkdownJSON = (text) => {
  const match = text.match(/```(?:json)?\s*([\s\S]*?)\s*```/);
  return match ? match[1] : text;
};

const parseLLMData = (rawText) => {
  const cleanText = cleanMarkdownJSON(rawText);
  return JSON.parse(cleanText.trim()); 
};

const formatClinicalHistories = (parsedData, baseData) => {
  const histories = Array.isArray(parsedData) 
      ? parsedData 
      : (parsedData.clinical_object || parsedData.historias_clinicas || [parsedData]);
  
  if (!Array.isArray(histories)) return [];

  return histories.map((history, index) => {
    // Fallback seguro: garantizamos que sea un string
    const textContent = typeof history === 'string' 
      ? history 
      : (history.clinical_text || JSON.stringify(history));

    // Extraemos de forma segura el objeto usando notación de corchetes por el guion
    const verificationData = typeof history === 'object' && history['self-verification'] 
      ? history['self-verification'] 
      : null;

    return {
      id_code_combination: baseData.id_code_combination,
      icf_codes: baseData.icf_codes,
      icf_name: baseData.icf_name,
      id_clinical_text: `${baseData.id_code_combination}_${index + 1}`,
      "self-verification": verificationData, // <-- Mapeado con la nueva clave
      clinical_text: textContent
    };
  });
};

const originalData = $('doc_to_json1').all();
const currentInputs = $input.all();

const originalData = $('doc_to_json1').all();
const currentInputs = $input.all();

const finalResults = currentInputs.flatMap((item, index) => {
  try {
    const rawText = extractRawText(item.json);
    
    if (!rawText) {
      throw new Error("Missing text variable in LLM response. Estructura recibida: " + JSON.stringify(Object.keys(item.json)));
    }

    const aiData = parseLLMData(rawText);
    
    // CORRECCIÓN CLAVE: 
    // Comprobamos si existe un contexto de bucle ($runIndex). 
    // Si existe, usamos el índice global. Si no, usamos el índice del array (batch normal).
    const correctIndex = typeof $runIndex !== 'undefined' ? $runIndex : index;
    const baseData = originalData[correctIndex]?.json || {}; 

    const formattedHistories = formatClinicalHistories(aiData, baseData);

    return formattedHistories.map(history => ({
      json: history
    }));

  } catch (error) {
    return [{
      json: {
        _processing_error: true,
        error_message: error.message,
        original_index: index,
        raw_data: item.json
      }
    }];
  }
});

return finalResults;
// Imprescindible para que el nodo Code de n8n pase los datos al siguiente nodo
return finalResults;