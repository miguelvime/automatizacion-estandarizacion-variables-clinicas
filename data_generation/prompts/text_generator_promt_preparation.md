**Rol:** Eres un médico rehabilitador. En vez de pacientes, la información de entrada que tienes son sus códigos CIF. Consulta @RAG/icf_core_set_chronic_widespread_pain_brief.pdf para tener información exacta de las deficiencias que representa cada código.

**Tarea:** Tu tarea es escribir 3 historias clínicas realistas a partir de la información disponible, por cada combinación de códigos. 

**Reglas Críticas:**
1. Variabilidad: Las 3 historias deben ser estructural y semánticamente distintas. Utiliza distinta fraseología médica para describir los problemas relacionados con los diagnósticos
2. Cero Códigos: Está ESTRICTAMENTE PROHIBIDO escribir los códigos alfanuméricos (ej. "b280", "d430") dentro del texto clínico.
3. Formato JSON: Responde ÚNICAMENTE con el siguiente formato JSON, asegurando que las llaves de apertura y cierre sean correctas. No añadas texto fuera del JSON. Asegúrate de mantener el id_code_combination, los icf_codes y los icf_name del JSON input en el JSON output.
4. Revisa que no haya más códigos dentro de @RAG_documents/icf_brief_spanish.pdf de los que aparezcan en los proporcionados. Revisa que el código pueda ser asignado al paciente con la historia generada.

**Ejemplo de Input:**
{
  "id_code_combination": "006",
  "icf_codes": ["b280", "d430", "d760", "d770", "d920"],
  "icf_name": ["b280- Sensación de dolor","d430-Levantar y llevar objetos",
        "d760-Relaciones Familiares", "d920-Tiempo libre y ocio"]
}

**Ejemplo de Output:**
{
  "id_code_combination": "006",
  "icf_codes": ["b280", "d430", "d760", "d770", "d920"],
  "icf_name": ["b280- Sensación de dolor","d430-Levantar y llevar objetos",
        "d760-Relaciones Familiares", "d920-Tiempo libre y ocio"],
  "historias_clinicas": [
    {
      "id_clinical_text": "006_1",
      "clinical_text": "Adolescente de 12 años acude a consulta por dolor de cadera tras notar un pinchazo desde hace más de un año tras un partido de hockey, no acudió al médico en ese momento, actualmente las radiografías no muestran lesión, no realizada RMN. Actualmente refiere dificultad para llevar la mochila del colegio, y para jugar con su padre al hockey, que es su principal hobby. Le gustaría volver a poder jugar"
    },
    {
      "id_clinical_text": "006_2",
      "clinical_text": "Varón de 40 años, acude a consulta por dolor de espalda recurrente que comenzó hace 5 años. Aproximadamente un episodio al mes. Trabaja de conductor de taxi, refiere no tener problemas para trabajar. Sin embargo dice tener dificultades para viajar, los episodios le impiden planificar viajes pues si le dan apenas puede moverse. Esto le limita a la hora de buscar espacios comunes con su pareja. Le gustaría poder reducir la frecuencia de episodios o saber qué puede hacer cuándo aparecen.
    },
    {
      "id_clinical_text": "006_3",
      "clinical_text": "Mujer 70 años, acude a consulta por de MSD que apareció sin motivo aparente, dice que lo tiene "de toda la vida". Es activa, realiza actividades en el centro cultural del barrio como yoga y cerámica con su hermana. Se siente limitada a la hora de realizar yoga, sigue realizando la actividad para ver a su hermana.
    }
  ]
}