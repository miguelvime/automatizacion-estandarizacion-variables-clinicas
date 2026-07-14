const crypto = require('crypto'); 

const inputItem = $input.first();

if (!inputItem?.binary){throw new Error ("No se encontraron datos binarios en la entrada del nodo.");
                       }
const [binaryKey] = Object.keys(inputItem.binary);

if (!binaryKey) {throw new Error ("El objeto binario está vacío o mal estructurado.");
                }

let parsedData;

try {
  const binaryBuffer = await this.helpers.getBinaryDataBuffer(0,binaryKey);
  const rawString = binaryBuffer.toString('utf-8');
  parsedData = JSON.parse(rawString)
} catch (error) { throw new Error (`Fallo al parsear el archivo binario a JSON: ${error.message}`);
        }

const itemsToProcess = Array.isArray(parsedData) ? parsedData : [parsedData];

return itemsToProcess.flatMap(item =>
  (item.clinical_object || []).map((co, i) => ({
    json: {
      id_code_combination: item.id_code_combination,
      icf_codes: item.icf_codes,
      icf_names: item.icf_names,
      id_clinical_text: co.id_clinical_text,
      uuid_clinical_text: crypto.randomUUID(),
      clinical_text: co.clinical_text,
    }
  }))
);
