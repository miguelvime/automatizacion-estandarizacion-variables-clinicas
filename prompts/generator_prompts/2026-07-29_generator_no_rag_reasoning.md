Rol: Eres un médico rehabilitador. En vez de pacientes, la información de entrada que tienes son sus códigos de la Clasificación Internacional del Funcionamiento (CIF), específicamente el Core Set de la CIF para el Dolor Crónico Generalizado.

Tarea: Tu tarea es escribir 3 historias clínicas realistas a partir de la información proporcionada en la sección <INPUT_ACTUAL>, por cada combinación de códigos. Consulta las definiciones exactas de los códigos en <CODIGOS_CIF>.

Reglas Críticas:

1. Variabilidad NARRATIVA y AMNESIA (CRÍTICO): Las 3 historias deben describir a pacientes completamente distintos (distinta edad, género, contexto laboral y forma de expresar el síntoma). Cada vez que recibas un nuevo <INPUT_ACTUAL>, debes generar casos TOTALMENTE NUEVOS. Está ESTRICTAMENTE PROHIBIDO repetir pacientes, oficios o textos exactos de generaciones anteriores. Asimismo, está ESTRICTAMENTE PROHIBIDO cambiar, añadir o quitar códigos para lograr esta variabilidad. Las 3 historias deben incluir EXACTAMENTE los mismos códigos del <INPUT_ACTUAL>.
2. Autoverificación Limitada (Plan-then-Generate): Cada historia clínica debe comenzar OBLIGATORIAMENTE con un objeto "self-verification". Las claves de este objeto deben ser EXACTAMENTE las mismas que los códigos proporcionados en el <INPUT_ACTUAL>, ni una más ni una menos. Si el input tiene 3 códigos, el objeto DEBE tener exactamente 3 claves en TODAS las historias. Los valores serán los fragmentos literales de texto que vas a incluir.
3. Cero Códigos en el Texto: Está ESTRICTAMENTE PROHIBIDO escribir los códigos alfanuméricos (ej. "b280" o "d430") dentro del valor de la clave "clinical_text". Los códigos solo pueden aparecer como claves dentro de "self-verification".
4. Restricción Tipográfica de JSON: Para que el JSON sea válido, debes usar comillas dobles EXCLUSIVAMENTE para definir las claves y los valores estructurales. Está ESTRICTAMENTE PROHIBIDO usar comillas dobles no escapadas dentro del texto generado. Si necesitas citar textualmente al paciente, usa obligatoriamente comillas simples (').
5. Restricción de Saltos de Línea: Está ESTRICTAMENTE PROHIBIDO usar saltos de línea físicos (intro/enter) dentro del valor de texto generado. Si necesitas separar párrafos, escribe explícitamente los caracteres literales \n. Todo el texto de una historia clínica debe ir en una única línea de código.
6. Formato Estricto: Responde ÚNICAMENTE con un ARRAY (matriz) JSON válido. Está ESTRICTAMENTE PROHIBIDO incluir bloques de código Markdown (como ```json) o cualquier texto introductorio o de despedida. Tu respuesta debe comenzar obligatoriamente con el carácter [ y terminar con ].
7. Grounding Ultra-Estricto (CRÍTICO): La historia clínica DEBE limitarse a los elementos de <INPUT_ACTUAL>. Está ESTRICTAMENTE PROHIBIDO incluir, insinuar o inventar síntomas, deficiencias físicas, situaciones sociales o tratamientos que pertenezcan a otros códigos del diccionario <CODIGOS_CIF> que no estén en tu input. Si el input no contiene códigos de fuerza (ej. b730), no menciones debilidad; si no contiene códigos familiares (ej. e310), omite el entorno familiar. Todo elemento clínico no respaldado por el input invalidará el dataset.
8. Tono: Usa un tono clínico realista y telegráfico, propio de la rapidez de una consulta real. Puedes usar lenguaje médico directo (ej. 'Acude por dolor...', 'En tto. con...', 'Refiere impotencia funcional...').

Referencia de Formato: Consulta <EJEMPLO_1> y <EJEMPLO_2> para imitar la estructura del output, la autoverificación, el uso correcto de las comillas simples y la sintaxis JSON en una sola línea mediante \n.

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
["b280-Sensación de dolor", "d430-Levantar y llevar objetos", "d760-Relaciones Familiares", "d920-Tiempo libre y ocio"]

Output:
[
  {
    "self-verification": {
      "b280": "dolor de cadera tras notar un pinchazo",
      "d430": "dificultad para llevar la mochila",
      "d760": "jugar con su padre",
      "d920": "su principal hobby"
    },
    "clinical_text": "Adolescente de 12 años acude a consulta por dolor de cadera tras notar un pinchazo desde hace más de un año tras un partido de hockey, no acudió al médico en ese momento, actualmente las radiografías no muestran lesión, no realizada RMN. Actualmente refiere dificultad para llevar la mochila del colegio, y para jugar con su padre al hockey, que es su principal hobby. Le gustaría volver a poder jugar.\n\nComenta que el dolor comenzó en la cadera pero que actualmente llega hasta el pie e incluso en el miembro inferior contralateral.\n\nExploración física: movilidad pasiva indolora salvo en extensión de cadera en prono, isométrico en flexión doloroso, FADDIR +, FABDRE +, desrot test -, SLR + con diferenciación de tobillo. Dolor a extensión lumbar activa de pie, no dolor al levantarse de la camilla ni en la sentadilla."
  },
  {
    "self-verification": {
      "b280": "dolor de espalda recurrente",
      "d430": "le cuesta meter maletas en el maletero",
      "d760": "buscar espacios comunes con su familia",
      "d920": "planificar viajes"
    },
    "clinical_text":  "Varón de 40 años, acude a consulta por dolor de espalda recurrente que comenzó hace 5 años. Aproximadamente un episodio al mes. Trabaja de conductor de taxi, refiere no tener problemas para trabajar pero le cuesta meter maletas en el maletero del taxi. Además dice tener dificultades para viajar, los episodios le impiden planificar viajes pues si le dan apenas puede moverse. Esto le limita a la hora de buscar espacios comunes con su pareja. Le gustaría poder reducir la frecuencia de episodios o saber qué puede hacer cuándo aparecen.\n\nExploración física: dolor a movimientos activos lumbares, principalmente flexión, dolor central en extensión, SLR reproduce dolor a nivel lumbar, Bragard +, slump +. EIL reduce dolor a la movilidad activa, slump y SLR.\n\nRM:12/24\n\nRx: Enseño ejercicios repetidos lumbares EIL 3-5/día x10 y enseño posibles respuestas y señales de stop."
  },
  {
    "self-verification": {
      "b280": "dolor de MSD",
      "d430": "Dificultad para levantar mancuerna",
      "d760": "actividades con su hermana",
      "d920": "yoga y cerámica"
    },
    "clinical_text": "Mujer 70 años, acude a consulta por dolor de MSD que apareció sin motivo aparente, dice que lo tiene 'de toda la vida'. Es activa, realiza actividades en el centro cultural del barrio como yoga y cerámica con su hermana. Se siente limitada a la hora de realizar yoga, sigue realizando la actividad para ver a su hermana.\n\nEn exploración no dolor a movimientos pasivos de hombro, dolor a isométricos en RE, F, ABD y push, no observo limitación de movimiento a movimiento activo aunque refiere dolor. Dificultad para levantar mancuerna de 1kg con ese MS con respecto a contralateral.\n\nQuickDash:25%\n\nTto: Enseño ejercicios isométricos de hombro, explico historia natural y gestión de la carga según respuesta sintomática, cito en una semana para progresar ejercicios."
  }
]
</EJEMPLO_1>

<EJEMPLO_2>
Input:
["b152-Funciones emocionales", "b280-Sensación de dolor", "d850-Trabajo remunerado"]

Output:
[
  {
    "self-verification": {
      "b152": "situación le genera ansiedad",
      "b280": "dolor lumbar",
      "d850": "no quiere dejar de trabajar"
    },
    "clinical_text": "Varón de 50 años que acude a consulta por dolor lumbar de 2 semanas de evolución. Refiere que se hizo daño trabajando. Es un dolor localizado en la región central de la espalda que asocia principalmente al movimiento. Durante la entrevista explica que está intentando evitar esos movimientos en su empleo. Pero no quiere dejar de trabajar porque la empresa tiene mucha demanda ahora y su situación le genera ansiedad ante un posible despido."
  },
  {
    "self-verification": {
      "b152": "frustración constante",
      "b280": "dolor cervical crónico",
      "d850": "épocas en las que tiene más carga de trabajo"
    },
    "clinical_text": "Mujer, 36 años. Acude a consulta por dolor cervical crónico. Describe un dolor tensional que oscila entre un 2/10 y un 5/10. Asocia el aumento del dolor a épocas en las que tiene más carga de trabajo en la oficina. Refiere que la incapacidad para rendir profesionalmente al 100% le produce una sensación de frustración constante y labilidad emocional."
  },
  {
    "self-verification": {
      "b152": "impacto emocional importante",
      "b280": "dolor generalizado",
      "d850": "incapaz de hacer su trabajo"
    },
    "clinical_text": "Mujer de 58 años que acude a consulta por dolor generalizado. Se encuentra de baja desde hace 10 meses porque se siente incapaz de hacer su trabajo como enfermera. Explica que le duele todo el cuerpo siempre, especialmente ambos hombros y la zona lumbar. Para ella, verse limitada físicamente tiene un impacto emocional importante, cursando con episodios de tristeza ocasional."
  }
]
</EJEMPLO_2>

<INPUT_ACTUAL>
{{ JSON.stringify($json.icf_name) }}
</INPUT_ACTUAL>