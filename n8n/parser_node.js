// =============================================================================
// n8n PARSER NODE — Limpieza y extracción de respuestas
// PFG TECNUN — ¿Simulan los LLMs el efecto halo en selección de personal?
// =============================================================================
// Este nodo va justo después del nodo Wait (después del HTTP Request).
// Recibe la respuesta cruda de OpenRouter y extrae los 5 campos de evaluación,
// los combina con los metadatos del experimento, y añade campos de trazabilidad.
//
// Campos de salida (23 columnas para Google Sheets):
//   call_id, model_id, model_label, position_id, position_label,
//   cv_id, cv_label, role_id, role_label, iteration,
//   technical_skills, communication, leadership_potential, teamwork, cultural_fit,
//   justification, model_used, cost_usd, prompt_tokens, completion_tokens,
//   total_tokens, timestamp, error
// =============================================================================

const items = $input.all();
const results = [];

for (const item of items) {
  try {

    // ── PASO 1: Extraer el texto de la respuesta ──────────────────────────
    // La respuesta de OpenRouter sigue el formato de OpenAI:
    // choices[0].message.content contiene el texto generado por el modelo.
    const rawContent = item.json.choices[0].message.content;

    // ── PASO 2: Limpiar marcas de markdown ───────────────────────────────
    // Los modelos a veces envuelven el JSON en ```json ... ``` aunque se
    // les pida que no lo hagan. JSON.parse() falla con esas marcas,
    // así que las eliminamos antes de parsear.
    let cleanContent = rawContent.trim();
    cleanContent = cleanContent.replace(/^```json\s*/i, '');
    cleanContent = cleanContent.replace(/^```\s*/, '');
    cleanContent = cleanContent.replace(/```\s*$/, '');
    cleanContent = cleanContent.trim();

    // ── PASO 3: Parsear el JSON limpio ───────────────────────────────────
    const parsed = JSON.parse(cleanContent);

    // ── PASO 4: Extraer metadatos de trazabilidad de la respuesta API ────
    // Estos campos vienen de la respuesta de OpenRouter, no del item original.
    // Por eso se extraen aquí y no dependen de que lleguen desde el Code node.
    const model_used        = item.json.model            ?? null;
    const cost_usd          = item.json.usage?.cost       ?? null;
    const prompt_tokens     = item.json.usage?.prompt_tokens     ?? null;
    const completion_tokens = item.json.usage?.completion_tokens ?? null;
    const total_tokens      = item.json.usage?.total_tokens      ?? null;
    const timestamp         = new Date().toISOString();

    // ── PASO 5: Derivar model_id y model_label desde model_used ──────────
    // No confiamos en que lleguen desde el Code node anterior porque el
    // HTTP Request puede perder esos campos. Los derivamos directamente
    // de la respuesta de la API, que siempre los incluye.
    let model_id    = null;
    let model_label = null;
    if (model_used) {
      if (model_used.toLowerCase().includes('claude')) {
        model_id    = 'claude-sonnet-4-6';
        model_label = 'Claude Sonnet 4.6';
      } else if (model_used.toLowerCase().includes('gpt')) {
        model_id    = 'gpt-4o';
        model_label = 'GPT-4o';
      }
    }

    // ── PASO 6: Construir la fila de resultado ────────────────────────────
    results.push({
      json: {
        // Metadatos del experimento — vienen del Code node original
        call_id:        item.json.call_id        ?? null,
        model_id:       model_id,
        model_label:    model_label,
        position_id:    item.json.position_id    ?? null,
        position_label: item.json.position_label ?? null,
        cv_id:          item.json.cv_id          ?? null,
        cv_label:       item.json.cv_label       ?? null,
        role_id:        item.json.role_id        ?? null,
        role_label:     item.json.role_label     ?? null,
        iteration:      item.json.iteration      ?? null,

        // Puntuaciones extraídas de la respuesta del modelo (5 dimensiones)
        technical_skills:     parsed.technical_skills     ?? null,
        communication:        parsed.communication        ?? null,
        leadership_potential: parsed.leadership_potential ?? null,
        teamwork:             parsed.teamwork             ?? null,
        cultural_fit:         parsed.cultural_fit         ?? null,
        justification:        parsed.justification        ?? null,

        // Trazabilidad de la llamada a la API
        model_used:        model_used,
        cost_usd:          cost_usd,
        prompt_tokens:     prompt_tokens,
        completion_tokens: completion_tokens,
        total_tokens:      total_tokens,
        timestamp:         timestamp,

        error: false
      }
    });

  } catch (e) {

    // ── MANEJO DE ERRORES ─────────────────────────────────────────────────
    // Si una respuesta es malformada o la API falla, no se rompe el flujo.
    // La fila se marca con error: true y se guarda la respuesta cruda
    // (truncada a 500 caracteres) para poder identificar qué falló.
    results.push({
      json: {
        call_id:        item.json.call_id        ?? null,
        model_id:       item.json.model_id       ?? null,
        model_label:    item.json.model_label    ?? null,
        position_id:    item.json.position_id    ?? null,
        position_label: item.json.position_label ?? null,
        cv_id:          item.json.cv_id          ?? null,
        cv_label:       item.json.cv_label       ?? null,
        role_id:        item.json.role_id        ?? null,
        role_label:     item.json.role_label     ?? null,
        iteration:      item.json.iteration      ?? null,

        technical_skills:     null,
        communication:        null,
        leadership_potential: null,
        teamwork:             null,
        cultural_fit:         null,
        justification:        null,

        model_used:        item.json.model                    ?? null,
        cost_usd:          item.json.usage?.cost              ?? null,
        prompt_tokens:     item.json.usage?.prompt_tokens     ?? null,
        completion_tokens: item.json.usage?.completion_tokens ?? null,
        total_tokens:      item.json.usage?.total_tokens      ?? null,
        timestamp:         new Date().toISOString(),

        error:         true,
        error_message: e.message,
        raw_response:  JSON.stringify(item.json).substring(0, 500)
      }
    });
  }
}

return results;
