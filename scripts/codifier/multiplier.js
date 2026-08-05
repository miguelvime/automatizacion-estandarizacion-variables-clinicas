const newItems = [];

// Iteramos sobre los elementos que llegan del nodo Loop (normalmente 1 a la vez)
for (const item of $input.all()) {
  // Multiplicamos el elemento por 3
  for (let i = 0; i < 3; i++) {
    newItems.push({
      json: {
        ...item.json,
        _llm_iteration: i + 1 // Añadimos un identificador para saber qué iteración es
      }
    });
  }
}

return newItems;