// ============================================================================
// NODO PARSER — Limpia la respuesta de Claude y extrae todo lo necesario
// para el análisis estadístico y el reporte metodológico de la tesis.
// ============================================================================

const items = $input.all();
const results = [];

for (const item of items) {
  try {
    // -------------------------------------------------------------------
    // PASO 1 — Extraer el texto de la respuesta de Claude
    // -------------------------------------------------------------------
    // La respuesta real de Claude vive dentro de choices[0].message.content.
    // Todo lo demás en la respuesta (id, model, usage, etc.) es metadata
    // sobre la llamada a la API en sí, no el contenido de la evaluación.
    const rawContent = item.json.choices[0].message.content;

    // -------------------------------------------------------------------
    // PASO 2 — Quitar las marcas de markdown
    // -------------------------------------------------------------------
    // A veces Claude envuelve su respuesta JSON dentro de ```json ... ```
    // aunque se le pida que no lo haga. JSON.parse() no puede leer texto
    // que tiene esas marcas de markdown alrededor, así que las quitamos
    // aquí antes de intentar convertir el texto en JSON real.
    let cleanContent = rawContent.trim();
    cleanContent = cleanContent.replace(/^```json\s*/i, '');
    cleanContent = cleanContent.replace(/^```\s*/, '');
    cleanContent = cleanContent.replace(/```\s*$/, '');
    cleanContent = cleanContent.trim();

    // -------------------------------------------------------------------
    // PASO 3 — Convertir el texto limpio en un objeto JSON real
    // -------------------------------------------------------------------
    // Antes de esta línea, "cleanContent" es solo un texto que se parece
    // a JSON. Después de esta línea, se convierte en un objeto real cuyos
    // campos (technical_skills, communication, etc.) podemos leer
    // directamente, como si fueran variables.
    const parsed = JSON.parse(cleanContent);

    // -------------------------------------------------------------------
    // MEJORA 2 — Capturar el coste real y el uso de tokens de esta llamada
    // -------------------------------------------------------------------
    // Por qué importa: la sección de presupuesto de tu TFG debe reportar
    // el coste REAL del experimento, no solo una estimación. OpenRouter
    // devuelve esta información automáticamente en el campo "usage" de
    // cada respuesta, solo hay que leerla en lugar de descartarla.
    // "?." (optional chaining) evita un error si "usage" no existiera
    // por algún motivo; simplemente devuelve null en vez de romper el código.
    const cost_usd = item.json.usage?.cost ?? null;
    const prompt_tokens = item.json.usage?.prompt_tokens ?? null;
    const completion_tokens = item.json.usage?.completion_tokens ?? null;
    const total_tokens = item.json.usage?.total_tokens ?? null;

    // -------------------------------------------------------------------
    // MEJORA 3 — Añadir una marca de tiempo para esta llamada exacta
    // -------------------------------------------------------------------
    // Por qué importa: una buena práctica científica es que cada dato
    // pueda rastrearse hasta el momento exacto en que se produjo. Esto
    // también te permite ordenar tus resultados cronológicamente más
    // adelante, o notar si algo raro pasó durante un momento específico.
    const timestamp = new Date().toISOString();

    // -------------------------------------------------------------------
    // MEJORA 6 — Capturar la versión exacta del modelo usado
    // -------------------------------------------------------------------
    // Por qué importa: decir solo "Claude" no es suficientemente preciso
    // para una metodología reproducible. La respuesta de la API incluye
    // la versión exacta del modelo (ej. "anthropic/claude-4.6-sonnet-20260217").
    // Registrar esto significa que cualquiera que lea tu tesis sabe
    // exactamente qué versión del modelo produjo tus resultados, algo
    // esencial si Anthropic lanza una versión más nueva después y alguien
    // intenta replicar tu estudio.
    const model_used = item.json.model ?? null;

    // -------------------------------------------------------------------
    // PASO FINAL — Juntar todo en una sola fila limpia
    // -------------------------------------------------------------------
    // Este objeto se convierte en una fila de tu Google Sheet: tiene los
    // metadatos del diseño experimental (qué CV, qué rol, qué iteración),
    // las cuatro puntuaciones, la justificación, y ahora también el coste,
    // los tokens, la marca de tiempo y la versión del modelo para
    // trazabilidad completa.
    results.push({
      json: {
        // Metadata del diseño experimental (ya funcionando desde tu arreglo)
        call_id: item.json.call_id,
        cv_id: item.json.cv_id,
        cv_label: item.json.cv_label,
        role_id: item.json.role_id,
        role_label: item.json.role_label,
        iteration: item.json.iteration,

        // Los resultados reales de la evaluación
        technical_skills: parsed.technical_skills,
        communication: parsed.communication,
        leadership_potential: parsed.leadership_potential,
        cultural_fit: parsed.cultural_fit,
        justification: parsed.justification,

        // Metadata de reproducibilidad y reporte (mejoras nuevas)
        model_used: model_used,
        // model_id y model_label se derivan de model_used para garantizar
        // que siempre estén presentes independientemente de qué campos
        // lleguen desde el nodo anterior.
        model_id: item.json.model_used
          ? item.json.model_used.split('/').pop().replace(/-\d{8}$/, '')
          : (item.json.model_id ?? null),
        model_label: item.json.model_used
          ? (item.json.model_used.includes('claude') ? 'Claude Sonnet 4.6' : 'GPT-4o')
          : (item.json.model_label ?? null),
        cost_usd: cost_usd,
        prompt_tokens: prompt_tokens,
        completion_tokens: completion_tokens,
        total_tokens: total_tokens,
        timestamp: timestamp,

        error: false
      }
    });

  } catch (e) {
    // -----------------------------------------------------------------
    // MANEJO DE ERRORES — Que un solo error no rompa todo el flujo
    // -----------------------------------------------------------------
    // Por qué importa: con 80 llamadas, si incluso una sola respuesta
    // sale mal formada (ej. Claude devuelve un JSON roto en un caso
    // extremo), no quieres perder los otros 79 resultados. En su lugar,
    // esta fila se marca con error: true y se guarda la respuesta cruda
    // para que puedas revisarla después y decidir si repetir solo esa
    // combinación específica.
    results.push({
      json: {
        call_id: item.json.call_id ?? null,
        cv_id: item.json.cv_id ?? null,
        cv_label: item.json.cv_label ?? null,
        role_id: item.json.role_id ?? null,
        role_label: item.json.role_label ?? null,
        iteration: item.json.iteration ?? null,
        technical_skills: null,
        communication: null,
        leadership_potential: null,
        cultural_fit: null,
        justification: null,
        model_used: item.json.model ?? null,
        cost_usd: item.json.usage?.cost ?? null,
        prompt_tokens: item.json.usage?.prompt_tokens ?? null,
        completion_tokens: item.json.usage?.completion_tokens ?? null,
        total_tokens: item.json.usage?.total_tokens ?? null,
        timestamp: new Date().toISOString(),
        error: true,
        error_message: e.message,
        raw_response: JSON.stringify(item.json)
      }
    });
  }
}

return results;

