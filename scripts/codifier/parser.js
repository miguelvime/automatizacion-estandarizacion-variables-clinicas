const textExtractor = (json) => {
    if (json.content && Array.isArray(json.content.parts) && json.content.parts.length > 0) {
        return json.content.parts[0].text;
    }
    return json.response || json.choices?.[0]?.message?.content || json.output || json.message || json.text || "";
};

const cleanMarkdownJSON = (text) => {
    const match = text.match(/```(?:json)?\s*([\s\S]*?)\s*```/);
    return match ? match[1] : text;
};

const llmDataParser = (rawText, index) => {
    const cleanText = cleanMarkdownJSON(rawText);
    try {
        return JSON.parse(cleanText.trim());
    } catch (error) {
        throw new Error(`Error de sintaxis JSON en la iteración ${index}. Texto crítico: ${cleanText}`);
    }
};

// 1. Ingesta de datos
const llm_output = $input.all();

// Vamos a buscar los datos originales JUSTO antes de que el LLM los destruyera.
// CORRECCIÓN: Le pasamos el currentRunIndex para que n8n no se quede atascado
// devolviendo eternamente el paciente 1.
const currentRunIndex = typeof $runIndex !== 'undefined' ? $runIndex : 0;
const inputDataToLlm = $('multiplier').all(0, currentRunIndex);

const structuredCodifiedJson = llm_output.map((item, index) => {
    const rawText = typeof item.json === 'string' ? item.json : textExtractor(item.json);

    if (!rawText) {
        throw new Error(`Variable de texto ausente en el ítem ${index}.`);
    }

    const parsedLlmData = llmDataParser(rawText, index);
    const predicted_codes = parsedLlmData.predicted_icf_codes || [];
    const codifier_reasoning = parsedLlmData.codifier_reasoning || parsedLlmData.reasoning || {};

    // 2. Emparejamiento Seguro
    // Como el LLM procesa en bloque, el 'index' (0, 1, 2) de su salida 
    // coincide EXACTAMENTE con el 'index' (0, 1, 2) del lote que le entró.
    const originalItem = inputDataToLlm[index];

    if (!originalItem || !originalItem.json) {
        throw new Error(`Error de emparejamiento. No se encontraron los datos originales para el ítem ${index}.`);
    }

    return {
        json: {
            id_code_combination: originalItem.json.id_code_combination,
            icf_name: originalItem.json.icf_name,
            icf_codes: originalItem.json.icf_codes,
            id_clinical_text: originalItem.json.id_clinical_text,
            clinical_text: originalItem.json.clinical_text,
            self_verification: originalItem.json.self_verification,
            _llm_iteration: originalItem.json._llm_iteration,
            predicted_icf_codes: predicted_codes,
            codifier_reasoning: codifier_reasoning
        }
    };
});

return structuredCodifiedJson;