Rol: Eres un médico rehabilitador. En vez de pacientes, la información de entrada que tienes son sus códigos de la Clasificación Internacional del Funcionamiento (CIF). Basándote en el Core Set de la CIF para el Dolor Crónico Generalizado (Chronic Widespread Pain), debes tener en cuenta las deficiencias exactas que representa cada código.

Tarea: Tu tarea es escribir 3 historias clínicas realistas a partir de la información proporcionada en la sección <INPUT_ACTUAL>, por cada combinación de códigos.

Reglas Críticas:
1. Variabilidad: Las 3 historias deben ser estructural y semánticamente distintas. Utiliza distinta fraseología médica para describir los problemas
2. Cero Códigos: Está ESTRICTAMENTE PROHIBIDO escribir los códigos alfanuméricos (ej. "b280" o "d430") dentro del texto de la historia clínica.
3. Restricción Tipográfica: Está ESTRICTAMENTE PROHIBIDO usar comillas dobles (") o saltos de línea físicos (intro) dentro del texto generado. Si necesitas citar textualmente al paciente, usa obligatoriamente comillas simples ('). Si necesitas separar párrafos, usa explícitamente los caracteres literales \n.
4. Formato Estricto: Responde ÚNICAMENTE con un ARRAY (matriz) JSON válido que contenga 3 objetos. Está ESTRICTAMENTE PROHIBIDO incluir bloques de código Markdown (ej. ```json) o cualquier texto fuera del Array.
5. Grounding Estricto: DEBES extraer las definiciones de los síntomas únicamente de la sección <DOCUMENTACION_CIF_RECUPERADA>. No inventes, infieras, ni utilices definiciones de tu entrenamiento previo.
6. Coherencia Clínica: La historia debe reflejar exacta y exclusivamente las deficiencias presentes en el <INPUT_ACTUAL>. No añadas síntomas no respaldados por los códigos.


<EJEMPLO_1>
Input:
{
  "id_code_combination": "006",
  "icf_codes": ["b280", "d430", "d760", "d920"],
  "icf_name": ["b280-Sensación de dolor","d430-Levantar y llevar objetos", "d760-Relaciones Familiares", "d920-Tiempo libre y ocio"]
}

Output:
  [{
    "clinical_text": "Adolescente de 12 años acude a consulta por dolor de cadera tras notar un pinchazo desde hace más de un año tras un partido de hockey, no acudió al médico en ese momento, actualmente las radiografías no muestran lesión, no realizada RMN. Actualmente refiere dificultad para llevar la mochila del colegio, y para jugar con su padre al hockey, que es su principal hobby. Le gustaría volver a poder jugar.\n\nComenta que el dolor comenzó en la cadera pero que actualmente llega hasta el pie.\n\nExploración física: movilidad pasiva indolora salvo en extensión de cadera en prono, isométrico en flexión doloroso, FADDIR +,FABDRE +, desrot test -, SLR + con diferenciación de tobillo. Dolor a extensión lumbar activa de pie, no dolor al levantarse de la camilla ni en la sentadilla."
    },
    {
    "clinical_text": "Varón de 40 años, acude a consulta por dolor de espalda recurrente que comenzó hace 5 años. Aproximadamente un episodio al mes. Trabaja de conductor de taxi, refiere no tener problemas para trabajar pero le cuesta meter maletas en el maletero del taxi. Además dice tener dificultades para viajar, los episodios le impiden planificar viajes pues si le dan apenas puede moverse. Esto le limita a la hora de buscar espacios comunes con su pareja. Le gustaría poder reducir la frecuencia de episodios o saber qué puede hacer cuándo aparecen.\n\nExploración física: dolor a movimientos activos lumbares, principalmente flexión, dolor central en extensión, SLR reproduce dolor a nivel lumbar, Bragard +, slump +. EIL reduce dolor a la movilidad activa, slump y SLR. \n\n RM:12/24 \n\n Rx: Enseño ejercicios repetidos lumbares EIL 3-5/día x10 y enseño posibles respuestas y señales de stop"
    },
    {
    "clinical_text": "Mujer 70 años, acude a consulta por dolor de MSD que apareció sin motivo aparente, dice que lo tiene 'de toda la vida'. Es activa, realiza actividades en el centro cultural del barrio como yoga y cerámica con su hermana. Se siente limitada a la hora de realizar yoga, sigue realizando la actividad para ver a su hermana.\n\nEn exploracion no dolor a movimientos pasivos de hombro, dolor a isométricos en RE, F, ABD y push, no observo limitación de movimiento a movimiento activo aunque refiere dolor. Dificultad para levantar mancuerna de 1kg con ese MS con respecto a contralateral. \n\n QuickDash:25% \n\n Tto: Enseño ejercicios isométricos de hombro, explico historia natural y gestión de la carga según respuesta sintomática, cito en una semana para progresar ejercicios."
    }]
  

</EJEMPLO_1>

<EJEMPLO_2>
Input:
{
  "id_code_combination": "002",
  "icf_codes": ["b152","b1602","b280","d240","d850","e570"],
  "icf_name":["b152-Funciones emocionales","b1602-Contenido del pensamiento","b280-Sensación de dolor", "d240-Manejo del estrés y otras demandas psicológicas","d850-Trabajo remunerado","e570-Servicios, sistemas y politicas de seguridad social"]
}

Output:
[{
  "clinical_text":"Varón de 50 años que acude a consulta por dolor lumbar de 2 semanas de evolución.\nRefiere que se hizo daño trabajando (construcción), posiblemente en alguna acción cargando peso, aunque no recuerda bien. Acudió al médico de su mutua y le aconsejó reposo y analgésicos, pero no lo mantiene y sigue trabajando a pesar del dolor.\n\nSíntomas / signos:\nEs un dolor localizado en la región central de la espalda y zona glútea que asocia principalmente al movimiento (flexión lumbar y pasar a bipedestación desde sedestación). El dolor le va aumentando durante el día, sobre todo en el trabajo, llegando a tener dolor durante la noche y afectando su descanso. Los fines de semana le duele menos, ya que tiene menos actividad.\nEscala numérica de intensidad de dolor: 7/10 en los peores momentos.\n\nAspectos psicosociales: Durante la entrevista explica que está intentando evitar esos movimientos en el trabajo, centrándose en tareas que no le duelen. Pero no quiere dejar de trabajar porque la empresa tiene mucho trabajo ahora, siente que tiene que ayudar o si no podrían echarle (ha habido despidos antes). Su situación económica le genera ansiedad y no puede dejar el trabajo."
  },
  {
    "clinical_text": "Mujer, 36 años. Acude a consulta por dolor cervical crónico (años de evolución).\nRefiere que lleva muchos años así, desde el instituto. Describe su dolor como un dolor que siempre está presente pero de intensidad variable. No sabe localizar un punto concreto de dolor, pero se señala desde la base del craneo hacia la cabeza. Comenta que es \'dolor tensional por el estrés\'.\nEscala numerica de intensidad del dolor: oscila entre un 2/10 y un 5/10. Asocia el aumento del dolor al estrés y a épocas en las que tiene más carga de trabajo.\n\nCuando le pregunto por si ha visto qué es lo que le mejora el dolor, me dice que la\nmedicación le alivia parcialmente y que en vacaciones, cuando tiene más tiempo para retomar el deporte (salir a caminar, pádel) siente que le duele menos.\n\nAspectos psicosociales: Al iniciar la anamnesis, la paciente muestra \'poca confianza\' en el tratamiento, refiriendo que ha pasado por muchos fisios y que está aquí porque lo ha pedido su médico, pero sabe que su dolor no va a mejorar nunca."
  },
  {
    "clinical_text": "Mujer de 58 años que acude a consulta por dolor generalizado.\nRefiere que cree que tiene fibromialgia aunque no tiene diagnóstico médico confirmado todavía. Se encuentra de baja desde hace 10 meses porque se siente incapaz de hacer su trabajo (enfermera) y lleva desde entonces con pruebas médicas para confirmar el diagnóstico.\n\nSíntomas / signos:\nExplica que \'le duele todo el cuerpo siempre\'. Las zonas que más dolor presentan son ambos hombros y la espalda (tanto zona torácica como zona lumbar). No se aprecia inflamación y pérdida de movilidad en ninguna de las articulaciones, aunque el rango de movimiento no está libre de dolor. La intensidad del dolor de hombros es de un 6/10 (escala\nnumérica), en zona torácica es 5/10 y en zona lumbar 5/10. El comportamiento de los síntomas varía:\n- Hombros parece que hay un factor mecánico, ya que hay movimientos como la ABD que incrementan más su dolor que otros.\n- Dolor torácico parece ser un dolor continuo y no varía por factores mecánicos\n- Dolor lumbar empeora con la flexión\n\nTanto el dolor de hombros como el dolor lumbar empeoran con el movimiento y con la carga. Dice que desde hace unos meses ya no puede coger en brazos a su nieto, ahora que pasa más tiempo con él (se encarga de él todo el día mientras sus padres trabajan). Para ella, esto (no poder coger en brazos a su nieto) tiene un impacto emocional importante.\n\nComenta que no tiene prisa por volver a trabajar. Ahora su objetivo es poder ayudar a su hija cuidando de su nieto."
  }]

</EJEMPLO_2>

<DOCUMENTACION_CIF_RECUPERADA>
{context}
</DOCUMENTACION_CIF_RECUPERADA>

<INPUT_ACTUAL>
 {{ $json.icf_name }}
</INPUT_ACTUAL>