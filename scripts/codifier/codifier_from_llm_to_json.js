const textExtractor = (json) => {
    return json.response ||
           json.choices?.[0]?.message?.content ||
           json.output ||
           json.message;
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
        throw new Error(`Invalid JSON in iteration ${index}. Text: ${cleanText}`);
    }
};

const formatPredictedCodes = (parsedData) => {
    const predictedCodes = parsedData.clinical_object || parsedData.historias_clinicas || parsedData.predicted_icf_codes || parsedData;
    if (!Array.isArray(predictedCodes)) return predictedCodes;
    
    return predictedCodes.map(story => story.predicted_icf_codes || story);
};

const originalData = $('binary_json_parser').all();
const llm_output = $input.all();

const structuredCodifiedJson = llm_output.map((item, index) => {
    const rawText = textExtractor(item.json);

    if (!rawText) {
        throw new Error(`There's no text variable in item ${index}.`);
    }

    const parsedLlmData = llmDataParser(rawText, index);
    const extracted_codes = formatPredictedCodes(parsedLlmData);
    const originalDataConnection = originalData[$runIndex].json;

    return {
        json: {
            id_code_combination: originalDataConnection.id_code_combination,
            icf_codes: originalDataConnection.icf_codes,
            icf_names: originalDataConnection.icf_names,
            predicted_icf_codes: extracted_codes,
            id_clinical_text: originalDataConnection.id_clinical_text,
            clinical_text: originalDataConnection.clinical_text
        }
    };
});

return structuredCodifiedJson;