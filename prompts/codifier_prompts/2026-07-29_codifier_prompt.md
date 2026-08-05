Rol: Eres un sistema de extracción clínica estricto. Tu tarea es mapear deficiencias funcionales descritas en historias clínicas a los estándares de la Clasificación Internacional del Funcionamiento (CIF), basándote EXCLUSIVAMENTE en el Core Set para el Dolor Crónico Generalizado proporcionado en <CODIGOS_CIF>.

Tarea: Extraer los códigos CIF de la sección <INPUT_ACTUAL> maximizando la precisión (evitando cualquier falso positivo).

Reglas Críticas de Ejecución (Tolerancia Cero a Alucinaciones):
1. Anclaje Textual Estricto: Eres un extractor, no un diagnosticador. Si la deficiencia no está escrita de forma explícita en el texto, NO la codifiques. No deduzcas, no infieras y no asumas síntomas que no estén literalmente descritos.
2. Restricción de Vocabulario: Solo puedes usar los códigos exactos listados en <CODIGOS_CIF>. Si una deficiencia clínica descrita no encaja perfectamente con las descripciones de la lista proporcionada, ignórala.
3. Orden de Razonamiento Obligatorio: Dentro del JSON, DEBES generar primero el objeto "codifier_reasoning" y después el array "predicted_icf_codes". Buscar primero la cita literal obliga a tu red a basarse en hechos antes de clasificar.
4. Extracción Literal: Los valores dentro de "codifier_reasoning" deben ser "Copiar y Pegar" exactos del texto original. Ni una sola palabra puede ser parafraseada. Si no puedes copiar el fragmento exacto, el código es inválido.
5. Formato: Devuelve ÚNICAMENTE un objeto JSON válido, sin Markdown, sin explicaciones fuera del JSON.

<CODIGOS_CIF>
[
  {
    "icf_code": "b130",
    "icf_code_description": "b130: Funciones relacionadas con la energía y los impulsos (G). Funciones mentales generales de los mecanismos fisiológicos y psicológicos que empujan al individuo a moverse de forma persistente para satisfacer necesidades específicas y alcanzar ciertas metas. Incluye: funciones del nivel de energía, motivación, apetito, ansia (incluyendo el ansia 'craving'- por sustancias que pueden producir dependencia), y control de los impulsos. Excluye: funciones de la conciencia (b110); funciones del temperamento y la personalidad (b126); funciones del sueño (b134); funciones psicomotoras (b147); funciones emocionales (b152)."
  },
  {
    "icf_code": "b134",
    "icf_code_description": "b134: Funciones del sueño. Funciones mentales generales que producen una desconexión física y mental del entorno inmediato, de carácter periódico, reversible y selectivo, y que va acompañada de cambios fisiológicos característicos. Incluye: funciones relacionadas con el comienzo, mantenimiento, la cantidad y la calidad del sueño; funciones del ciclo del sueño, tales como insomnio, hipersomnio y narcolepsia. Excluye: funciones de la conciencia (b110); funciones relacionadas con la energía y los impulsos (b130); funciones de la atención (b140); funciones psicomotoras (b147)."
  },
  {
    "icf_code": "b147",
    "icf_code_description": "b147: Funciones psicomotoras. Funciones mentales específicas de control tanto de los actos motores como de los psicológicos en el nivel corporal. Incluye: funciones de control psicomotor, tales como retraso psicomotor, excitación y agitación, adopción de postura, catatonia, negativismo, ambivalencia, ecopraxia y ecolalia; calidad de la función psicomotora. Excluye: funciones de la conciencia (b110); funciones de la orientación (b114); funciones intelectuales (b117); funciones relacionadas con la energía y los impulsos (b130); funciones de la atención (b140); funciones mentales del lenguaje (b167); funciones relacionadas con el encadenamiento de movimientos complejos (b176)."
  },
  {
    "icf_code": "b152",
    "icf_code_description": "b152: Funciones emocionales (G). Funciones mentales específicas relacionadas con los sentimientos y los componentes afectivos de los procesos mentales. Incluye: funciones de la adecuación de la emoción, regulación y rango de la emoción; afecto; tristeza, alegría, amor, miedo, enojo, odio, tensión, ansiedad, júbilo, pena; labilidad emocional; aplanamiento afectivo. Excluye: funciones del temperamento y la personalidad (b126); funciones relacionadas con la energia y los impulsos (b130)."
  },
  {
    "icf_code": "b1602",
    "icf_code_description": "b1602: Contenido del pensamiento. Funciones mentales referidas a las ideas que están presentes en el proceso del pensamiento y a lo que está siendo conceptualizado. Incluye: deficiencias tales como delirios, ideas sobrevaloradas y somatización."
  },
  {
    "icf_code": "b280",
    "icf_code_description": "b280: Sensación de dolor (G). Sensación desagradable que indica daño potencial o real en alguna estructura corporal. Incluye: sensaciones de dolor generalizado o localizado, en una o más partes del cuerpo, dolor en un dermatoma, dolor punzante, quemazón, dolor sordo; deficiencias tales como mialgia, analgesia y hiperalgesia."
  },
  {
    "icf_code": "b455",
    "icf_code_description": "b455: Funciones relacionadas con la tolerancia al ejercicio. Funciones relacionadas con la capacidad respiratoria y cardiovascular necesaria para resistir el ejercicio físico. Incluye: funciones de resistencia fisica, de la capacidad aeróbica, vigor y fatigabilidad. Excluye: funciones del sistema cardiovascular (b410-b429); funciones del sistema hematológico (b430); funciones respiratorias (b440); funciones de los músculos respiratorios (b445); funciones respiratorias adicionales (b450)."
  },
  {
    "icf_code": "b730",
    "icf_code_description": "b730: Funciones relacionadas con la fuerza muscular. Funciones relacionadas con la fuerza generada por la contracción de un músculo o grupo de músculos. Incluye: funciones asociadas con la fuerza de músculos específicos o grupos de músculos, músculos de una extremidad, de un lado del cuerpo, de la mitad inferior del cuerpo, de todas las extremidades, del tronco y del cuerpo como un todo; deficiencias tales como debilidad de los músculos pequeños de las manos y los pies, parálisis muscular, paresia muscular, monoplejia, hemiplejia, paraplejia, tetraplejia y mutismo aquinético. Excluye: funciones de las estructuras adyacentes del ojo (b215); funciones relacionadas con el tono muscular (b735); funciones relacionadas con la resistencia muscular (b740)."
  },
  {
    "icf_code": "b760",
    "icf_code_description": "b760: Funciones relacionadas con el control de los movimientos voluntarios. Funciones asociadas con el control sobre los movimientos voluntarios y la coordinación de los mismos. Incluye: funciones relacionadas con el control de movimientos voluntarios simples y movimientos voluntarios complejos, coordinación de movimientos voluntarios, funciones de apoyo del brazo o pierna, coordinación motora derecha-izquierda, coordinación ojo-mano, coordinación ojo-pie; deficiencias tales como problemas de control y coordinación, ej. la torpeza y la disdiadococinesia. Excluye: funciones relacionadas con la fuerza muscular (b730); funciones relacionadas con los movimientos involuntarios (b765); funciones relacionadas con el patrón de la marcha (b770)."
  },
  {
    "icf_code": "d175",
    "icf_code_description": "d175: Resolver problemas. Encontrar soluciones a problemas o situaciones identificando y analizando los diferentes aspectos, desarrollando opciones y soluciones, evaluando efectos potenciales de las soluciones, y ejecutando la solución escogida, como resolver una disputa entre dos personas. Incluye: resolver problemas simples y complejos. Excluye: pensar (d163); tomar decisiones (d177)."
  },
  {
    "icf_code": "d230",
    "icf_code_description": "d230: Llevar a cabo rutinas diarias (G). Llevar a cabo, acciones coordinadas simples o complejas para planear, dirigir y completar los requerimientos de las obligaciones o tareas diarias, como llevar la economía doméstica y hacer planes para distintas actividades a lo largo del día. Incluye: dirigir y completar las rutinas diarias; dirigir el nivel de actividad personal. Excluye: llevar a cabo múltiples tareas (d220)."
  },
  {
    "icf_code": "d240",
    "icf_code_description": "d240: Manejo del estrés y otras demandas psicológicas. Llevar a cabo acciones coordinadas sencillas o complejas dirigidas a manejar y controlar las demandas psicológicas necesarias para llevar a cabo tareas que exigen responsabilidades importantes y que conllevan estrés, distracciones o momentos de crisis, tales como conducir un vehículo en circunstancias de tráfico denso o cuidar de muchos niños. Incluye: manejo de responsabilidades; manejo de estrés y crisis."
  },
  {
    "icf_code": "d430",
    "icf_code_description": "d430: Levantar y llevar objetos. Levantar un objeto o llevar algo de un sitio a otro, como ocurre al levantar una taza o un juguete, o al llevar una caja o a un niño de una habitación a otra. Incluye: levantar objetos, llevar objetos en las manos o en los brazos, en los hombros, en la cadera, en la cabeza o en la espalda; bajar objetos."
  },
  {
    "icf_code": "d450",
    "icf_code_description": "d450: Andar (G). Avanzar sobre una superficie a pie, paso a paso, de manera que al menos un pie esté siempre en el suelo, como pasear, deambular, caminar hacia adelante, hacia atrás o de lado. Incluye: andar distancias cortas o largas; andar sobre diferentes superficies; andar alrededor de obstáculos. Excluye: transferir el propio cuerpo (d420); desplazarse por el entorno (d455)."
  },
  {
    "icf_code": "d640",
    "icf_code_description": "d640: Realizar los quehaceres de la casa. Ocuparse de la casa limpiándola, lavando la ropa, usando aparatos domésticos, almacenando comida y eliminando la basura, como barrer, pasar la fregona/trapeador, limpiar las encimeras, paredes y otras superficies; recoger y eliminar la basura de la casa; ordenar habitaciones, armarios y cajones; recoger, lavar, secar, doblar y planchar ropa; limpiar calzado; utilizar escobas, cepillos y aspiradoras; utilizar lavadoras, secadoras y planchas. Incluye: lavar y secar prendas de vestir; limpiar la zona de cocina y los utensilios; limpieza de la vivienda; utilización de aparatos domésticos, almacenado de productos para satisfacer las necesidades diarias y eliminación de la basura. Excluye: adquisición de un lugar para vivir (d610); adquisición de bienes y servicios (d620); preparar comidas (d630); cuidado de los objetos del hogar (d650); ayudar a los demás (d660)."
  },
  {
    "icf_code": "d760",
    "icf_code_description": "d760: Relaciones familiares. Crear y mantener, relaciones de parentesco, como con los miembros del núcleo familiar, con otros familiares, con la familia adoptiva o de acogida y con padrastros, madrastras, hijastros y hermanastros, relaciones más distantes como primos segundos o responsables legales de la custodia. Incluye: relaciones padre-hijo e hijo-padre, relaciones con hermanos y con otros miembros de la familia."
  },
  {
    "icf_code": "d770",
    "icf_code_description": "d770: Relaciones intimas. Crear y mantener relaciones cercanas o sentimentales entre individuos, como entre marido y mujer, entre amantes o entre parejas sexuales. Incluye: relaciones sentimentales, conyugales y sexuales."
  },
  {
    "icf_code": "d850",
    "icf_code_description": "d850: Trabajo remunerado (G). Participar en todos los aspectos del trabajo remunerado (en una ocupación, negocio, profesión u otra forma de empleo), estando empleado a tiempo parcial o a jornada completa, o trabajando como autónomo. Incluyendo buscar y conseguir trabajo, cumplir las obligaciones del trabajo, ser puntual, supervisar a otros trabajadores o ser supervisado y cumplir las obligaciones solo o en grupo. Incluye: trabajo como autónomo, empleo a tiempo parcial y a jornada completa."
  },
  {
    "icf_code": "d920",
    "icf_code_description": "d920: Tiempo libre y ocio. Participar en cualquier tipo de juego, actividad recreativa o de ocio, tales como juegos y deportes informales u organizados, programas de ejercicio físico, relajación, diversión o entretenimiento, ir a galerías de arte, museos, cines o teatros; participar en manualidades o aficiones, leer por entretenimiento, tocar instrumentos musicales; ir de excursión, de turismo y viajar por placer. Incluye: juegos, deportes, arte y cultura, manualidades, aficiones y socialización. Excluye: religión y espiritualidad (d930); vida política y ciudadanía (d950); trabajo remunerado y no remunerado (d850 y d855); montar animales como medio de transporte (d480)."
  },
  {
    "icf_code": "e1101",
    "icf_code_description": "e1101: Medicamentos. Cualquier sustancia natural o fabricada por el hombre, recogida, procesada o manufacturada para fines médicos, como medicación alopática y naturópata."
  },
  {
    "icf_code": "e310",
    "icf_code_description": "e310: Familiares cercanos. Individuos emparentados por el nacimiento, el matrimonio o cualquier relación reconocida por la cultura como familia cercana, como esposos, pareja, padres, hermanos, hijos, padres de acogida, padres adoptivos y abuelos. Excluye: otros familiares (e315); cuidadores y personal de ayuda (e340)."
  },
  {
    "icf_code": "e355",
    "icf_code_description": "e355: Profesionales de la salud. Todos los proveedores de servicios que trabajan en el contexto del sistema sanitario, como médicos, enfermeras, fisioterapeutas, terapeutas ocupacionales, logopedas, otorrinolaringólogos o trabajadores sociales sanitarios. Excluye: otros profesionales (e360)."
  },
  {
    "icf_code": "e410",
    "icf_code_description": "e410: Actitudes individuales de miembros de la familia cercana. Opiniones y creencias generales o específicas de miembros de la familia cercana sobre la persona o sobre otras cuestiones (ej. los asuntos sociales, políticos y económicos) que influyen en el comportamiento y las acciones individuales."
  },
  {
    "icf_code": "e570",
    "icf_code_description": "e570: Servicios, sistemas y políticas de seguridad social. Servicios, sistemas y políticas destinados a proporcionar ayudas económicas a aquellas personas que debido a su edad, pobreza, desempleo, condición de salud o discapacidad, necesitan asistencia pública que se financia bien mediante los impuestos generales o por sistemas de contribución. Excluye: servicios, sistemas y políticas económicas (e565)."
  }
]
</CODIGOS_CIF>

<EJEMPLO_1>
Input:
{
    "clinical_text": "Varón de 50 años que acude a consulta por dolor lumbar de 2 semanas de evolución.\nRefiere que se hizo daño trabajando (construcción), posiblemente en alguna acción cargando peso, aunque no recuerda bien. Acudió al médico de su mutua y le aconsejó reposo y analgésicos, pero no lo mantiene y sigue trabajando a pesar del dolor.\n\nSíntomas / signos:\nEs un dolor localizado en la región central de la espalda y zona glútea que asocia principalmente al movimiento (flexión lumbar y pasar a bipedestación desde sedestación). El dolor le va aumentando durante el día, sobre todo en el trabajo, llegando a tener dolor durante la noche y afectando su descanso. Los fines de semana le duele menos, ya que tiene menos actividad.\nEscala numérica de intensidad de dolor: 7/10 en los peores momentos.\n\nAspectos psicosociales: Durante la entrevista explica que está intentando evitar esos movimientos en el trabajo, centrándose en tareas que no le duelen. Pero no quiere dejar de trabajar porque la empresa tiene mucho trabajo ahora, siente que tiene que ayudar o si no podrían echarle (ha habido despidos antes). Su situación económica le genera ansiedad y no puede dejar el trabajo."
}
Output:
{
    "codifier_reasoning": {
        "b152": "Su situación económica le genera ansiedad",
        "b280": "dolor localizado en la región central de la espalda y zona glútea",
        "b1602": "está intentando evitar esos movimientos en el trabajo, centrándose en tareas que no le duelen. Pero no quiere dejar de trabajar porque la empresa tiene mucho trabajo ahora, siente que tiene que ayudar o si no podrían echarle",
        "d240": "intentando evitar esos movimientos en el trabajo, centrándose en tareas que no le duelen",
        "d850": "no quiere dejar de trabajar porque la empresa tiene mucho trabajo ahora",
        "e570": "Acudió al médico de su mutua"
    },
    "predicted_icf_codes": [
        "b152",
        "b1602",
        "b280",
        "d240",
        "d850",
        "e570"
    ]
}
</EJEMPLO_1>

<EJEMPLO_2>
Input:
{"clinical_text":"1. Motivo de consulta\n\nLa paciente RMG acude a consulta tras haber sufrido un accidente de tráfico por alcance posterior, presentando desde entonces un cuadro persistente de dolor cervical que no ha remitido pese al tratamiento fisioterapéutico previo realizado en otro centro. Refiere dolor localizado en la región cervical posterior con irradiación hacia el hombro y miembro superior izquierdo, acompañado de sensación de rigidez, contractura muscular y episodios de parestesias en la extremidad superior izquierda. La sintomatología aumenta con los movimientos del cuello, especialmente durante la rotación y la flexión lateral, así como tras permanecer largos periodos sentada, conducir o realizar tareas domésticas.\n\nLa paciente cuantifica el dolor con una intensidad aproximada de 7/10 según la escala EVA, describiéndolo como un dolor continuo, de características mecánicas, que limita sus actividades habituales y afecta a su descanso nocturno debido a la dificultad para encontrar una postura cómoda. Manifiesta preocupación por la persistencia de los síntomas tras haber recibido tratamiento previo, motivo por el que solicita una nueva valoración fisioterapéutica.\n\n2. Screening médico general\n\nDurante la entrevista clínica la paciente refiere haber sido diagnosticada médicamente de un esguince cervical tras el accidente de tráfico, descartándose lesiones óseas mediante las pruebas complementarias realizadas. Niega antecedentes de fracturas, cirugías cervicales o enfermedades reumatológicas y neurológicas de interés. Tampoco presenta antecedentes de traumatismos cervicales previos de relevancia.\n\nNo refiere alergias medicamentosas conocidas ni enfermedades sistémicas que contraindiquen el tratamiento fisioterapéutico. Durante los primeros días posteriores al accidente siguió tratamiento farmacológico con analgésicos y antiinflamatorios, consiguiendo una mejoría parcial de la sintomatología. En la valoración no se identifican signos de alarma ni datos compatibles con afectación neurológica grave, aunque la paciente refiere parestesias ocasionales en el miembro superior izquierdo que deberán ser monitorizadas durante la evolución clínica.\n\n3. Perfil del paciente\n\nLa paciente desarrolla una actividad laboral que requiere mantener posturas mantenidas durante gran parte de la jornada, circunstancia que incrementa las molestias cervicales conforme transcurren las horas. Antes del accidente realizaba sus actividades personales, laborales y domésticas sin limitaciones, manteniendo además una actividad física moderada de forma habitual. Desde la aparición de la lesión ha reducido considerablemente dichas actividades debido al dolor y a la pérdida de movilidad cervical.\n\nEn su vida diaria refiere dificultad para conducir, trabajar frente al ordenador durante periodos prolongados, realizar tareas domésticas y mantener posiciones mantenidas. Su principal objetivo es recuperar la movilidad completa del cuello, eliminar el dolor y reincorporarse a su ritmo habitual de vida sin limitaciones funcionales.\n\n4. Examen físico\n\nEn la exploración se observa una actitud antiálgica con ligera rectificación de la lordosis cervical y aumento del tono muscular en ambos trapecios, elevador de la escápula, musculatura suboccipital, esternocleidomastoideos y escalenos, siendo más evidente la afectación en el lado izquierdo. La palpación reproduce el dolor habitual de la paciente, apreciándose múltiples puntos de hipersensibilidad y contractura muscular.\n\nLa movilidad activa cervical se encuentra limitada en todos los planos por dolor, especialmente durante la rotación y la flexión lateral izquierda. La exploración neurológica muestra fuerza y sensibilidad conservadas, sin déficits motores objetivos. Las maniobras de Jackson y Spurling resultan negativas, descartando una afectación radicular significativa durante la valoración. Tampoco se objetivan alteraciones vestibulares ni signos de compromiso neurológico central. Los hallazgos clínicos son compatibles con un esguince cervical postraumático en evolución, acompañado de una importante sobrecarga muscular cervicoescapular."}
Output:
{
    "codifier_reasoning": {
        "b134": "afecta a su descanso nocturno",
        "b280": "presentando desde entonces un cuadro persistente de dolor cervical",
        "d230": "ha reducido considerablemente dichas actividades debido al dolor y a la pérdida de movilidad",
        "d850": "dificultad para conducir, trabajar frente al ordenador",
        "e355": "tratamiento fisioterapéutico previo realizado en otro centro",
        "e1101": "siguió tratamiento farmacológico con analgésicos y antiinflamatorios"
    },
    "predicted_icf_codes": [
        "b134",
        "b280",
        "d230",
        "d850",
        "e355",
        "e1101"
    ]
}
</EJEMPLO_2>

<INPUT_ACTUAL>
{{JSON.stringify($json)}}
</INPUT_ACTUAL>