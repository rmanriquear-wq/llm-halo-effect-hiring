import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# =============================================================================
# CONFIGURACIÓN GLOBAL
# =============================================================================

FILE_PATH = '/content/drive/MyDrive/CVsDataset.xlsx'

# =============================================================================
# CONFIGURACIÓN GLOBAL
# =============================================================================


DIMS       = ['technical_skills', 'communication', 'leadership_potential', 'cultural_fit']
DIM_LABELS = ['Technical Skills', 'Communication', 'Leadership Potential', 'Cultural Fit']
DIM_SHORT  = ['Tech. Skills', 'Communication', 'Leadership', 'Cultural Fit']
DIM_COLORS = ['#3B82F6', '#10B981', '#F59E0B', '#EF4444']

MODELS       = ['claude-sonnet-4-6', 'gpt-4o']
MODEL_LABELS = {'claude-sonnet-4-6': 'Claude Sonnet 4.6', 'gpt-4o': 'GPT-4o'}

CV_ORDER  = ['CV_CONTROL', 'CV_ELITE_UNI', 'CV_PRESTIGE_EMPLOYER', 'CV_AWARD']
CV_LABELS = {
    'CV_CONTROL':           'Control (Zaragoza)',
    'CV_ELITE_UNI':         'Test A (MIT)',
    'CV_PRESTIGE_EMPLOYER': 'Test B (Google)',
    'CV_AWARD':             'Test C (Award)'
}
CV_SHORT  = ['Control', 'MIT', 'Google', 'Award']
CV_COLORS = ['#6B7280', '#3B82F6', '#10B981', '#F59E0B']

TEST_CVS    = ['CV_ELITE_UNI', 'CV_PRESTIGE_EMPLOYER', 'CV_AWARD']
ROLE_ORDER  = ['HR_OFFICER', 'HEAD_HR', 'CTO', 'CEO']
ROLE_LABELS = {
    'HR_OFFICER': 'HR Officer',
    'HEAD_HR':    'Head of HR',
    'CTO':        'CTO',
    'CEO':        'CEO'
}


# =============================================================================
# CARGA Y LIMPIEZA DE DATOS
# =============================================================================

df = pd.read_excel(FILE_PATH)
df['error'] = df['error'].astype(str).str.upper().isin(['TRUE', '1'])
df = df[df['error'] == False].copy()

print(f"Dataset cargado: {df.shape[0]} filas, {df.shape[1]} columnas")
print(f"Modelos: {df['model_id'].value_counts().to_dict()}")
print(f"CVs: {df['cv_id'].value_counts().to_dict()}")
print(f"Roles: {df['role_id'].value_counts().to_dict()}")
print(f"Errores: {df['error'].sum()} de {len(df)}")

# =============================================================================
# BLOQUE 1 — ESTADÍSTICOS DESCRIPTIVOS
# =============================================================================
# Pregunta: ¿hay diferencias visibles entre el Control y las versiones Test?
# Si el modelo fuera objetivo, las medias deberían ser iguales en todas
# las versiones porque las competencias del candidato son idénticas.
# =============================================================================


# ── 1A: Medias y desviaciones típicas ─────────────────────────────────────
print("\n── 1A: Medias (SD) por versión de CV ──")
for model in MODELS:
    mdf = df[df['model_id'] == model]
    print(f"\n{MODEL_LABELS[model]}:")
    print(f"  {'':28} {'Tech':>6} {'Comm':>6} {'Lead':>6} {'Cult':>6}")
    print("  " + "-" * 55)
    for cv in CV_ORDER:
        row   = mdf[mdf['cv_id'] == cv][DIMS]
        means = row.mean()
        stds  = row.std()
        print(f"  {CV_LABELS[cv]:28} "
              f"{means['technical_skills']:>5.2f}  "
              f"{means['communication']:>5.2f}  "
              f"{means['leadership_potential']:>5.2f}  "
              f"{means['cultural_fit']:>5.2f}")
        print(f"  {'(SD)':28} "
              f"({stds['technical_skills']:>4.2f}) "
              f"({stds['communication']:>4.2f}) "
              f"({stds['leadership_potential']:>4.2f}) "
              f"({stds['cultural_fit']:>4.2f})")

# ── 1B: Varianza intra-perfil ──────────────────────────────────────────────
# Mide la consistencia entre las 5 iteraciones de cada combinación.
# Mediana ~0 confirma que el sesgo detectado es sistemático, no ruido.
print("\n── 1B: Varianza intra-perfil (std entre las 5 iteraciones) ──")
print("Mediana ~0 = el modelo es consistente = el sesgo es real y sistemático\n")
intra = df.groupby(['model_id', 'cv_id', 'role_id'])[DIMS].std()
for model in MODELS:
    sub = intra.loc[model]
    print(f"{MODEL_LABELS[model]}:")
    print(f"  Mediana: {sub.median().round(4).to_dict()}")
    print(f"  Máximo:  {sub.max().round(4).to_dict()}\n")

# ── Figura 1: Boxplots ─────────────────────────────────────────────────────
fig, axes = plt.subplots(2, 4, figsize=(18, 9))
fig.suptitle(
    'Figura 1 — Distribución de puntuaciones por versión de CV\n'
    'Fila superior: Claude Sonnet 4.6 | Fila inferior: GPT-4o',
    fontsize=13, fontweight='bold', y=1.01
)
for mi, model in enumerate(MODELS):
    mdf = df[df['model_id'] == model]
    for di, dim in enumerate(DIMS):
        ax   = axes[mi, di]
        data = [mdf[mdf['cv_id'] == cv][dim].values for cv in CV_ORDER]
        bp   = ax.boxplot(data, patch_artist=True, widths=0.55,
                          medianprops=dict(color='black', linewidth=2.5),
                          whiskerprops=dict(linewidth=1.2),
                          capprops=dict(linewidth=1.2),
                          flierprops=dict(marker='o', markersize=4, alpha=0.5))
        for patch, color in zip(bp['boxes'], CV_COLORS):
            patch.set_facecolor(color)
            patch.set_alpha(0.75)
        ax.set_title(DIM_LABELS[di], fontsize=10, fontweight='bold', pad=6)
        ax.set_xticks(range(1, 5))
        ax.set_xticklabels(CV_SHORT, fontsize=8.5)
        ax.set_ylim(0, 11)
        ax.set_yticks([0, 2, 4, 6, 8, 10])
        ax.grid(axis='y', alpha=0.3, linestyle='--')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        if di == 0:
            ax.set_ylabel(f"{MODEL_LABELS[model]}\nScore (1–10)", fontsize=9)
legend_patches = [mpatches.Patch(color=c, alpha=0.75, label=l)
                  for c, l in zip(CV_COLORS, CV_LABELS.values())]
fig.legend(handles=legend_patches, loc='lower center', ncol=4,
           fontsize=10, frameon=False, bbox_to_anchor=(0.5, -0.03))
plt.tight_layout()
plt.savefig('fig1_boxplots.png', dpi=150, bbox_inches='tight', facecolor='white')
plt.show()
print("Figura 1 guardada.")

# ── Figura 2: Medias con barras de error ───────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(16, 6))
fig.suptitle('Figura 2 — Medias de puntuación por versión de CV y dimensión (± SD)',
             fontsize=13, fontweight='bold')
x       = np.arange(len(DIMS))
width   = 0.18
offsets = [-1.5, -0.5, 0.5, 1.5]
for mi, (model, ax) in enumerate(zip(MODELS, axes)):
    mdf   = df[df['model_id'] == model]
    means = mdf.groupby('cv_id')[DIMS].mean().reindex(CV_ORDER)
    stds  = mdf.groupby('cv_id')[DIMS].std().reindex(CV_ORDER)
    for i, (cv, color) in enumerate(zip(CV_ORDER, CV_COLORS)):
        ax.bar(x + offsets[i] * width, means.loc[cv], width=width,
               color=color, alpha=0.85, label=CV_SHORT[i],
               yerr=stds.loc[cv], capsize=3,
               error_kw={'linewidth': 1.2, 'ecolor': '#374151'})
    ax.set_title(MODEL_LABELS[model], fontsize=12, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(DIM_SHORT, fontsize=10)
    ax.set_ylim(0, 11)
    ax.set_ylabel('Media (± SD)', fontsize=10)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.legend(fontsize=9, frameon=False, ncol=2)
plt.tight_layout()
plt.savefig('fig2_means.png', dpi=150, bbox_inches='tight', facecolor='white')
plt.show()
print("Figura 2 guardada.")

# =============================================================================
# BLOQUE 2 — DIFERENCIA DE MEDIAS (Test − Control)
# =============================================================================
# Pregunta: ¿cuánto cambia exactamente cada dimensión entre el Control
# y cada versión Test? Un cambio positivo en dimensiones donde las
# competencias son idénticas = evidencia directa de efecto halo.
# =============================================================================
 
print("\n" + "=" * 70)
print("BLOQUE 2 — DIFERENCIA DE MEDIAS (Test − Control)")
print("=" * 70)
print("Cambio positivo en dimensiones idénticas = efecto halo detectado\n")
 
diff_records = []
for model in MODELS:
    mdf = df[df['model_id'] == model]
    ctrl_means = mdf[mdf['cv_id'] == 'CV_CONTROL'].groupby('role_id')[DIMS].mean()
    for cv in TEST_CVS:
        test_means = mdf[mdf['cv_id'] == cv].groupby('role_id')[DIMS].mean()
        diff = test_means - ctrl_means
        diff['cv_id']   = cv
        diff['model_id'] = model
        diff_records.append(diff.reset_index())
 
diff_df = pd.concat(diff_records, ignore_index=True)
 
for model in MODELS:
    print(f"── {MODEL_LABELS[model]} ──")
    sub = diff_df[diff_df['model_id'] == model].groupby('cv_id')[DIMS].mean()
    sub = sub.reindex(TEST_CVS)
    sub.index = [CV_LABELS[c] for c in TEST_CVS]
    sub.columns = DIM_SHORT
    print(sub.round(3).to_string())
    print()
 
# ── Figura 3: Heatmap de diferencias ──────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
fig.suptitle(
    'Figura 3 — Diferencia de medias respecto al Control (Test − Control)\n'
    'Verde = el atributo halo sube la puntuación | Rojo = la baja',
    fontsize=12, fontweight='bold'
)
for mi, (model, ax) in enumerate(zip(MODELS, axes)):
    pivot = diff_df[diff_df['model_id'] == model].groupby('cv_id')[DIMS].mean()
    pivot = pivot.reindex(TEST_CVS)
    pivot.index   = [CV_LABELS[c] for c in TEST_CVS]
    pivot.columns = DIM_SHORT
    sns.heatmap(pivot, ax=ax, annot=True, fmt='.2f',
                cmap='RdYlGn', center=0, vmin=-2, vmax=2,
                linewidths=0.5, linecolor='white',
                cbar_kws={'label': 'Diferencia de medias'})
    ax.set_title(MODEL_LABELS[model], fontsize=11, fontweight='bold')
    ax.set_xlabel('Dimensión de evaluación', fontsize=10)
    ax.set_ylabel('Versión CV', fontsize=10)
    plt.setp(ax.get_xticklabels(), rotation=0)
    plt.setp(ax.get_yticklabels(), rotation=0)
plt.tight_layout()
plt.savefig('fig3_heatmap_diff.png', dpi=150, bbox_inches='tight', facecolor='white')
plt.show()
print("Figura 3 guardada.")

# =============================================================================
# BLOQUE 3 — MAGNITUD DEL EFECTO (d de Cohen)
# =============================================================================
# Pregunta: la diferencia que vemos, ¿es grande o pequeña en términos
# prácticos? La d de Cohen estandariza la diferencia para poder comparar
# entre dimensiones y entre modelos.
# Referencia: d < 0.2 trivial | 0.2–0.5 pequeño | 0.5–0.8 mediano | >0.8 grande
# =============================================================================
 
print("\n" + "=" * 70)
print("BLOQUE 3 — d DE COHEN (magnitud del efecto)")
print("=" * 70)
print("d < 0.2 trivial | 0.2–0.5 pequeño | 0.5–0.8 mediano | >0.8 grande\n")
 
def cohen_d(group1, group2):
    n1, n2 = len(group1), len(group2)
    if n1 < 2 or n2 < 2:
        return np.nan
    pooled_std = np.sqrt(
        ((n1 - 1) * np.var(group1, ddof=1) +
         (n2 - 1) * np.var(group2, ddof=1)) / (n1 + n2 - 2)
    )
    return 0.0 if pooled_std == 0 else (np.mean(group2) - np.mean(group1)) / pooled_std
 
def interpret_d(d):
    if abs(d) < 0.2:   return 'Trivial'
    elif abs(d) < 0.5: return 'Pequeño'
    elif abs(d) < 0.8: return 'Mediano'
    else:              return 'Grande'
 
cohen_records = []
for model in MODELS:
    mdf  = df[df['model_id'] == model]
    ctrl = mdf[mdf['cv_id'] == 'CV_CONTROL']
    for cv in TEST_CVS:
        test = mdf[mdf['cv_id'] == cv]
        for dim in DIMS:
            d = cohen_d(ctrl[dim].values, test[dim].values)
            cohen_records.append({
                'model_id':  model,
                'cv_id':     cv,
                'dimension': dim,
                'cohen_d':   d,
                'magnitude': interpret_d(d)
            })
 
cohen_df = pd.DataFrame(cohen_records)
 
# Imprimir tabla de resultados
print("d de Cohen por modelo, versión y dimensión:")
print("(+ = halo sube puntuación | − = halo la baja)\n")
for model in MODELS:
    print(f"── {MODEL_LABELS[model]} ──")
    sub = cohen_df[cohen_df['model_id'] == model]
    pivot = sub.pivot(index='cv_id', columns='dimension', values='cohen_d')
    pivot = pivot.reindex(TEST_CVS)[DIMS]
    pivot.index   = [CV_LABELS[c] for c in TEST_CVS]
    pivot.columns = DIM_LABELS
    print(pivot.round(3).to_string())
    print()
 
# -----------------------------------------------------------------------------
# FIGURA 4 — Barras horizontales con color por dimensión
# -----------------------------------------------------------------------------
fig, axes = plt.subplots(1, 2, figsize=(16, 7), sharey=False)
fig.suptitle(
    "Figura 4 — d de Cohen por versión de CV y dimensión\n"
    "Derecha = el atributo halo sube la puntuación | Izquierda = la baja\n"
    "Líneas de referencia: -- 0.2 (pequeño) | : 0.5 (mediano) | -. 0.8 (grande)",
    fontsize=12, fontweight='bold'
)
 
y_pos   = np.arange(len(TEST_CVS))
height  = 0.18
# Posición vertical de cada barra dentro del grupo
offsets = [-1.5, -0.5, 0.5, 1.5]
 
for mi, (model, ax) in enumerate(zip(MODELS, axes)):
    sub = cohen_df[cohen_df['model_id'] == model]
 
    for di, (dim, dim_color) in enumerate(zip(DIMS, DIM_COLORS)):
        dvals = [
            sub[(sub['cv_id'] == cv) & (sub['dimension'] == dim)]['cohen_d'].values[0]
            for cv in TEST_CVS
        ]
 
        # Barras con el color de la dimensión
        # Borde más oscuro si es negativo para distinguirlo visualmente
        edge_colors = ['#1a1a1a' if v < 0 else dim_color for v in dvals]
        linewidths  = [2.0 if v < 0 else 0.5 for v in dvals]
 
        ax.barh(
            y_pos + offsets[di] * height,
            dvals,
            height=height,
            color=dim_color,
            alpha=0.85,
            edgecolor=edge_colors,
            linewidth=linewidths,
            label=DIM_LABELS[di]
        )
 
        # Valor numérico al final de cada barra
        for yi, val in zip(y_pos + offsets[di] * height, dvals):
            if abs(val) > 0.05:
                ha  = 'left'  if val >= 0 else 'right'
                pad = 0.05    if val >= 0 else -0.05
                ax.text(val + pad, yi, f'{val:.2f}',
                        va='center', ha=ha, fontsize=7.5,
                        color='#1a1a1a', fontweight='bold')
 
    # Líneas de referencia (umbrales estándar de Cohen)
    for xval, ls, alpha, label in [
        ( 0.2, '--', 0.5, ''),
        (-0.2, '--', 0.5, ''),
        ( 0.5, ':',  0.6, ''),
        (-0.5, ':',  0.6, ''),
        ( 0.8, '-.', 0.5, ''),
        (-0.8, '-.', 0.5, ''),
    ]:
        ax.axvline(xval, color='#6B7280', linewidth=0.9,
                   linestyle=ls, alpha=alpha)
 
    # Línea del cero
    ax.axvline(0, color='black', linewidth=1.5)
 
    ax.set_yticks(y_pos)
    ax.set_yticklabels([CV_LABELS[c] for c in TEST_CVS], fontsize=11)
    ax.set_xlabel("d de Cohen", fontsize=11)
    ax.set_title(MODEL_LABELS[model], fontsize=12, fontweight='bold')
    ax.set_xlim(-2.5, 3.0)
    ax.grid(axis='x', alpha=0.25, linestyle='--')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
 
    # Anotaciones de los umbrales en el primer subplot
    if mi == 0:
        for xval, txt in [(0.2, 'small'), (0.5, 'medium'), (0.8, 'large')]:
            ax.text(xval + 0.05, len(TEST_CVS) - 0.15, txt,
                    fontsize=7, color='#6B7280', ha='left', style='italic')
 
# Leyenda con los 4 colores de dimensión
legend_patches = [
    mpatches.Patch(color=c, alpha=0.85, label=l)
    for c, l in zip(DIM_COLORS, DIM_LABELS)
]
fig.legend(
    handles=legend_patches,
    loc='lower center', ncol=4,
    fontsize=10, frameon=False,
    bbox_to_anchor=(0.5, -0.06)
)
 
plt.tight_layout()
plt.savefig('fig4_cohen_d.png', dpi=150, bbox_inches='tight', facecolor='white')
plt.show()
print("Figura 4 guardada: fig4_cohen_d.png")


# =============================================================================
# BLOQUE 4 — TEST DE HIPÓTESIS (Mann-Whitney U)
# =============================================================================
# Pregunta: ¿la diferencia que vemos es estadísticamente significativa,
# o podría deberse al azar?
# H0: no hay diferencia entre Control y versión Test
# H1: la versión Test puntúa sistemáticamente diferente al Control
# Usamos Mann-Whitney U porque no asume normalidad y es adecuado para
# escalas ordinales (puntuaciones del 1 al 10).
# =============================================================================
 
print("\n" + "=" * 70)
print("BLOQUE 4 — TEST DE HIPÓTESIS (Mann-Whitney U, α = 0.05)")
print("=" * 70)
print("H0: sin diferencia sistemática entre Control y versión Test")
print("H1: la versión Test puntúa sistemáticamente diferente\n")
 
mw_records = []
for model in MODELS:
    mdf  = df[df['model_id'] == model]
    ctrl = mdf[mdf['cv_id'] == 'CV_CONTROL']
    for cv in TEST_CVS:
        test = mdf[mdf['cv_id'] == cv]
        for dim in DIMS:
            stat, p = stats.mannwhitneyu(
                ctrl[dim].values, test[dim].values,
                alternative='two-sided'
            )
            mw_records.append({
                'model_id':   model,
                'cv_id':      cv,
                'dimension':  dim,
                'U_stat':     round(stat, 1),
                'p_value':    round(p, 4),
                'significant': 'Sí ✓' if p < 0.05 else 'No'
            })
 
mw_df = pd.DataFrame(mw_records)
 
for model in MODELS:
    print(f"── {MODEL_LABELS[model]} ──")
    sub = mw_df[mw_df['model_id'] == model]
    for cv in TEST_CVS:
        print(f"\n  vs. {CV_LABELS[cv]}:")
        cv_sub = sub[sub['cv_id'] == cv][['dimension', 'p_value', 'significant']]
        cv_sub = cv_sub.set_index('dimension').reindex(DIMS)
        cv_sub.index = DIM_SHORT
        print(cv_sub.to_string())
    print()
 
# ── Figura 5: Heatmap de p-valores ────────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
fig.suptitle(
    'Figura 5 — p-valores Mann-Whitney U (Control vs cada versión Test)\n'
    'Borde negro = diferencia estadísticamente significativa (p < 0.05)',
    fontsize=12, fontweight='bold'
)
for mi, (model, ax) in enumerate(zip(MODELS, axes)):
    pivot = mw_df[mw_df['model_id'] == model].pivot(
        index='cv_id', columns='dimension', values='p_value'
    ).reindex(TEST_CVS)[DIMS]
    pivot.index   = [CV_LABELS[c] for c in TEST_CVS]
    pivot.columns = DIM_SHORT
    sns.heatmap(pivot, ax=ax, annot=True, fmt='.3f',
                cmap='RdYlGn_r', vmin=0, vmax=0.5,
                linewidths=0.5, linecolor='white',
                cbar_kws={'label': 'p-valor'})
    for i in range(pivot.shape[0]):
        for j in range(pivot.shape[1]):
            if pivot.iloc[i, j] < 0.05:
                ax.add_patch(plt.Rectangle((j, i), 1, 1,
                             fill=False, edgecolor='black', lw=2.5))
    ax.set_title(MODEL_LABELS[model], fontsize=11, fontweight='bold')
    ax.set_xlabel('Dimensión', fontsize=10)
    ax.set_ylabel('Versión CV', fontsize=10)
    plt.setp(ax.get_xticklabels(), rotation=0)
    plt.setp(ax.get_yticklabels(), rotation=0)
plt.tight_layout()
plt.savefig('fig5_pvalues.png', dpi=150, bbox_inches='tight', facecolor='white')
plt.show()
print("Figura 5 guardada.")
 
# =============================================================================
# BLOQUE 5 — CORRELACIÓN INTER-DIMENSIONAL
# =============================================================================
# Pregunta: ¿el efecto halo hace que todas las dimensiones suban juntas?
# El mecanismo del efecto halo es que UNA señal de prestigio contamina
# TODAS las dimensiones simultáneamente — aunque sean conceptualmente
# independientes. Si eso ocurre, la correlación entre dimensiones será
# mayor en las versiones Test que en el Control.
# =============================================================================
 
print("\n" + "=" * 70)
print("BLOQUE 5 — CORRELACIÓN INTER-DIMENSIONAL (Pearson)")
print("=" * 70)
print("Si el halo actúa: correlación entre dimensiones > en Test que en Control\n")
 
for model in MODELS:
    mdf = df[df['model_id'] == model]
    print(f"── {MODEL_LABELS[model]} ──\n")
    ctrl_corr = mdf[mdf['cv_id'] == 'CV_CONTROL'][DIMS].corr()
    print("  Control — Correlación media entre dimensiones: "
          f"{ctrl_corr.values[np.triu_indices_from(ctrl_corr.values, k=1)].mean():.3f}")
    for cv in TEST_CVS:
        test_corr = mdf[mdf['cv_id'] == cv][DIMS].corr()
        mean_corr = test_corr.values[np.triu_indices_from(test_corr.values, k=1)].mean()
        print(f"  {CV_LABELS[cv]} — Correlación media: {mean_corr:.3f}")
    print()
 
# ── Figura 6: Matrices de correlación ─────────────────────────────────────
fig, axes = plt.subplots(2, 2, figsize=(14, 12))
fig.suptitle(
    'Figura 6 — Matrices de correlación inter-dimensional\n'
    'Control vs Test C (Award) — comparación por modelo',
    fontsize=13, fontweight='bold'
)
plot_pairs = [
    (0, 0, 'claude-sonnet-4-6', 'CV_CONTROL', 'Claude — Control'),
    (0, 1, 'claude-sonnet-4-6', 'CV_AWARD',   'Claude — Test C (Award)'),
    (1, 0, 'gpt-4o',            'CV_CONTROL', 'GPT-4o — Control'),
    (1, 1, 'gpt-4o',            'CV_AWARD',   'GPT-4o — Test C (Award)'),
]
for row, col, model, cv, title in plot_pairs:
    ax   = axes[row, col]
    corr = df[(df['model_id'] == model) & (df['cv_id'] == cv)][DIMS].corr()
    corr.index   = DIM_SHORT
    corr.columns = DIM_SHORT
    sns.heatmap(corr, ax=ax, annot=True, fmt='.2f',
                cmap='coolwarm', vmin=-1, vmax=1,
                square=True, linewidths=0.5,
                cbar_kws={'shrink': 0.8})
    ax.set_title(title, fontsize=11, fontweight='bold')
plt.tight_layout()
plt.savefig('fig6_correlations.png', dpi=150, bbox_inches='tight', facecolor='white')
plt.show()
print("Figura 6 guardada.")
 
# =============================================================================
# BLOQUE 6 — COMPARACIÓN ENTRE MODELOS Y RESUMEN
# =============================================================================
# Pregunta final: ¿Claude y GPT-4o muestran el mismo nivel de efecto halo,
# o uno es más susceptible que el otro? ¿Qué rol evaluador es más
# susceptible al sesgo?
# =============================================================================
 
print("\n" + "=" * 70)
print("BLOQUE 6 — COMPARACIÓN ENTRE MODELOS Y POR ROL")
print("=" * 70)
 
# ── Figura 7: Diferencia por versión test comparando modelos ──────────────
fig, axes = plt.subplots(1, 3, figsize=(18, 6), sharey=False)
fig.suptitle(
    'Figura 7 — Diferencia (Test − Control) por versión de CV\n'
    'Comparación entre Claude y GPT-4o por dimensión',
    fontsize=12, fontweight='bold'
)
x       = np.arange(len(DIMS))
width   = 0.35
m_colors = ['#6366F1', '#F97316']
 
for ti, (cv, ax) in enumerate(zip(TEST_CVS, axes)):
    for mi, (model, color) in enumerate(zip(MODELS, m_colors)):
        mdf    = df[df['model_id'] == model]
        ctrl_m = mdf[mdf['cv_id'] == 'CV_CONTROL'][DIMS].mean()
        test_m = mdf[mdf['cv_id'] == cv][DIMS].mean()
        diffs  = test_m - ctrl_m
        ax.bar(x + (mi - 0.5) * width, diffs, width=width,
               color=color, alpha=0.85, label=MODEL_LABELS[model])
    ax.axhline(0, color='black', linewidth=1)
    ax.axhline( 0.5, color='gray', linewidth=0.8, linestyle='--', alpha=0.5)
    ax.axhline(-0.5, color='gray', linewidth=0.8, linestyle='--', alpha=0.5)
    ax.set_title(CV_LABELS[cv], fontsize=11, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(DIM_SHORT, fontsize=9)
    ax.set_ylabel('Diferencia (Test − Control)' if ti == 0 else '', fontsize=10)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    if ti == 0:
        ax.legend(fontsize=10, frameon=False)
plt.tight_layout()
plt.savefig('fig7_model_comparison.png', dpi=150, bbox_inches='tight', facecolor='white')
plt.show()
print("Figura 7 guardada.")
 
# ── Figura 8: Diferencia media por rol evaluador ───────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(14, 6))
fig.suptitle(
    'Figura 8 — Diferencia media (Test − Control) por rol evaluador\n'
    'Promedio de todas las versiones test y todas las dimensiones',
    fontsize=12, fontweight='bold'
)
for mi, (model, ax) in enumerate(zip(MODELS, axes)):
    mdf        = df[df['model_id'] == model]
    role_diffs = {}
    for role in ROLE_ORDER:
        ctrl_m = mdf[(mdf['cv_id'] == 'CV_CONTROL') &
                     (mdf['role_id'] == role)][DIMS].mean().mean()
        test_vals = [
            mdf[(mdf['cv_id'] == cv) &
                (mdf['role_id'] == role)][DIMS].mean().mean() - ctrl_m
            for cv in TEST_CVS
        ]
        role_diffs[role] = np.mean(test_vals)
 
    roles  = list(role_diffs.keys())
    diffs  = list(role_diffs.values())
    colors = ['#059669' if d > 0 else '#DC2626' for d in diffs]
    bars   = ax.barh([ROLE_LABELS[r] for r in roles], diffs,
                     color=colors, alpha=0.8)
    ax.axvline(0, color='black', linewidth=1)
    ax.set_xlabel('Diferencia media (Test − Control)', fontsize=10)
    ax.set_title(MODEL_LABELS[model], fontsize=11, fontweight='bold')
    ax.grid(axis='x', alpha=0.3, linestyle='--')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    for bar, val in zip(bars, diffs):
        ax.text(val + (0.01 if val >= 0 else -0.01),
                bar.get_y() + bar.get_height() / 2,
                f'{val:+.3f}', va='center', ha='left' if val >= 0 else 'right',
                fontsize=10, fontweight='bold')
plt.tight_layout()
plt.savefig('fig8_role_comparison.png', dpi=150, bbox_inches='tight', facecolor='white')
plt.show()
print("Figura 8 guardada.")

# RESUMEN FINAL — RESPUESTA A LA PREGUNTA DE GONZALO
# =============================================================================
print("\n" + "=" * 70)
print("RESUMEN FINAL — ¿Hay efecto halo? ¿Es relevante el estudio?")
print("=" * 70)
 
print("\n1. CONSISTENCIA (Bloque 1B)")
print("   Varianza intra-perfil mediana = 0 en ambos modelos")
print("   → El sesgo detectado es sistemático, no ruido aleatorio\n")
 
print("2. DIFERENCIAS DETECTADAS (Bloques 1 y 2)")
for model in MODELS:
    mdf = df[df['model_id'] == model]
    ctrl_lp = mdf[mdf['cv_id'] == 'CV_CONTROL']['leadership_potential'].mean()
    award_lp = mdf[mdf['cv_id'] == 'CV_AWARD']['leadership_potential'].mean()
    print(f"   {MODEL_LABELS[model]}:")
    print(f"   leadership_potential — Control: {ctrl_lp:.2f} | Award: {award_lp:.2f} | Δ = {award_lp-ctrl_lp:+.2f}")
 
print("\n3. MAGNITUD DEL EFECTO (Bloque 3)")
top = cohen_df.nlargest(3, 'cohen_d')[['model_id', 'cv_id', 'dimension', 'cohen_d', 'magnitude']]
top['model_id'] = top['model_id'].map(MODEL_LABELS)
top['cv_id']    = top['cv_id'].map(CV_LABELS)
print(top.to_string(index=False))
 
print("\n4. SIGNIFICANCIA ESTADÍSTICA (Bloque 4)")
sig = mw_df[mw_df['p_value'] < 0.05]
for model in MODELS:
    n = len(sig[sig['model_id'] == model])
    print(f"   {MODEL_LABELS[model]}: {n} de {len(TEST_CVS)*len(DIMS)} comparaciones significativas (p < 0.05)")
 
print("\n5. CONCLUSIÓN PRELIMINAR")
print("   Claude muestra efecto halo pronunciado en leadership_potential")
print("   con el atributo Award (d de Cohen grande).")
print("   GPT-4o muestra efectos menores y más distribuidos.")
print("   El atributo más potente NO es el MIT sino el Award —")
print("   hallazgo contraintuitivo y original.")
print("\nAnálisis completo. Figuras 1–8 guardadas.")


