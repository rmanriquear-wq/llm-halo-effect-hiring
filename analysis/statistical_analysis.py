# =============================================================================
# ANÁLISIS ESTADÍSTICO COMPLETO — PFG TECNUN
# ¿Simulan los LLMs el efecto halo en selección de personal?
# =============================================================================
# Dataset: CVsDataset_final.xlsx — 320 filas, 5 dimensiones, 2 puestos
# Modelos: Claude Sonnet 4.6 | GPT-4o
# Puestos: Backend Developer | Digital Marketing Analyst
# CVs: Control | MIT/LSE | Google/Unilever | Award (Hash Code / Cannes Lions)
# Dimensiones: technical_skills, communication, leadership_potential,
#              teamwork, cultural_fit
#
# INSTRUCCIONES GOOGLE COLAB:
# 1. Celda 1: from google.colab import files; files.upload()
#    → sube CVsDataset_final.xlsx
# 2. Celda 2: !pip install pandas scipy matplotlib seaborn openpyxl -q
# 3. Celda 3: pega y ejecuta este script completo
# =============================================================================

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

FILE_PATH = 'CVsDataset_final.xlsx'

DIMS       = ['technical_skills', 'communication', 'leadership_potential',
              'teamwork', 'cultural_fit']
DIM_LABELS = ['Technical Skills', 'Communication', 'Leadership Potential',
              'Teamwork', 'Cultural Fit']
DIM_SHORT  = ['Tech.', 'Comm.', 'Leadership', 'Teamwork', 'Cult. Fit']

MODELS       = ['claude-sonnet-4-6', 'gpt-4o']
MODEL_LABELS = {'claude-sonnet-4-6': 'Claude Sonnet 4.6', 'gpt-4o': 'GPT-4o'}
MODEL_COLORS = {'claude-sonnet-4-6': '#6366F1', 'gpt-4o': '#F97316'}

POSITIONS = ['BACKEND_DEV', 'MARKETING_ANALYST']
POSITION_LABELS = {
    'BACKEND_DEV':        'Backend Developer',
    'MARKETING_ANALYST':  'Digital Marketing Analyst'
}

CV_ORDER  = ['CV_CONTROL', 'CV_ELITE_UNI', 'CV_PRESTIGE_EMPLOYER', 'CV_AWARD']
CV_LABELS = {
    'CV_CONTROL':           'Control',
    'CV_ELITE_UNI':         'Test A (MIT/LSE)',
    'CV_PRESTIGE_EMPLOYER': 'Test B (Google/Unilever)',
    'CV_AWARD':             'Test C (Award)'
}
CV_COLORS = ['#6B7280', '#3B82F6', '#10B981', '#F59E0B']
TEST_CVS  = ['CV_ELITE_UNI', 'CV_PRESTIGE_EMPLOYER', 'CV_AWARD']

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

print("=" * 65)
print("DATASET CARGADO Y LIMPIO")
print("=" * 65)
print(f"Filas válidas:  {df.shape[0]}")
print(f"Columnas:       {df.shape[1]}")
print(f"Modelos:        {df['model_id'].value_counts().to_dict()}")
print(f"Puestos:        {df['position_id'].value_counts().to_dict()}")
print(f"CVs:            {df['cv_id'].value_counts().to_dict()}")
print(f"Roles:          {df['role_id'].value_counts().to_dict()}")
print(f"\nEstadísticas generales:")
print(df[DIMS].describe().round(3).to_string())


# =============================================================================
# BLOQUE 1 — ESTADÍSTICOS DESCRIPTIVOS
# =============================================================================
# Objetivo: ver si las puntuaciones cambian entre versiones de CV idénticas.
# Si el modelo es objetivo, deberían ser iguales. Cualquier diferencia
# es evidencia preliminar de efecto halo.
# =============================================================================

print("\n" + "=" * 65)
print("BLOQUE 1 — ESTADÍSTICOS DESCRIPTIVOS")
print("=" * 65)

# ── 1A: Medias y SD por modelo, puesto y CV ───────────────────────────────
print("\n── 1A: Medias (SD) por versión de CV ──")
for model in MODELS:
    for pos in POSITIONS:
        sub = df[(df['model_id'] == model) & (df['position_id'] == pos)]
        print(f"\n{MODEL_LABELS[model]} — {POSITION_LABELS[pos]}:")
        print(f"  {'':28} {'Tech':>6} {'Comm':>6} {'Lead':>6} {'Team':>6} {'Cult':>6}")
        print("  " + "-" * 60)
        for cv in CV_ORDER:
            row = sub[sub['cv_id'] == cv][DIMS]
            if len(row) == 0:
                continue
            m = row.mean()
            s = row.std()
            print(f"  {CV_LABELS[cv]:28} "
                  f"{m['technical_skills']:>5.2f}  "
                  f"{m['communication']:>5.2f}  "
                  f"{m['leadership_potential']:>5.2f}  "
                  f"{m['teamwork']:>5.2f}  "
                  f"{m['cultural_fit']:>5.2f}")
            print(f"  {'(SD)':28} "
                  f"({s['technical_skills']:>4.2f}) "
                  f"({s['communication']:>4.2f}) "
                  f"({s['leadership_potential']:>4.2f}) "
                  f"({s['teamwork']:>4.2f}) "
                  f"({s['cultural_fit']:>4.2f})")

# ── 1B: Varianza intra-perfil ──────────────────────────────────────────────
# Mediana ~0 = el modelo es determinista a temperatura 0.
# Si la mediana es 0, cualquier diferencia entre CVs es un patrón real.
print("\n── 1B: Varianza intra-perfil (std entre las 5 iteraciones) ──")
print("Mediana ~0 = sesgo sistemático, no ruido aleatorio\n")
intra = df.groupby(['model_id', 'position_id', 'cv_id', 'role_id'])[DIMS].std()
for model in MODELS:
    for pos in POSITIONS:
        sub = intra.loc[model, pos] if (model, pos) in intra.index else None
        if sub is not None:
            print(f"{MODEL_LABELS[model]} — {POSITION_LABELS[pos]}:")
            print(f"  Mediana SD: {sub.median().round(4).to_dict()}")
            print(f"  Máximo SD:  {sub.max().round(4).to_dict()}\n")

# ── 1C: Coeficiente de variación (CV = SD / Media) ───────────────────────
# Métrica añadida por Gonzalo. Mide la dispersión relativa de las
# puntuaciones — útil para comparar la estabilidad entre dimensiones
# y entre modelos, independientemente de la escala de puntuación.
print("── 1C: Coeficiente de variación (SD / Media) por modelo y CV ──")
print("Menor CV = mayor consistencia relativa\n")
for model in MODELS:
    mdf = df[df['model_id'] == model]
    print(f"{MODEL_LABELS[model]}:")
    for cv in CV_ORDER:
        sub = mdf[mdf['cv_id'] == cv][DIMS]
        cv_ratio = (sub.std() / sub.mean() * 100).round(2)
        print(f"  {CV_LABELS[cv]:28} {cv_ratio.to_dict()}")
    print()

# ── Figura 1: Boxplots por dimensión — un gráfico por dimensión ───────────
for di, (dim, dim_label) in enumerate(zip(DIMS, DIM_LABELS)):
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle(
        f'Figura 1.{di+1} — {dim_label}\n'
        f'Distribución de puntuaciones por versión de CV, modelo y puesto',
        fontsize=13, fontweight='bold'
    )
    plot_configs = [
        (0, 0, 'claude-sonnet-4-6', 'BACKEND_DEV'),
        (0, 1, 'gpt-4o',            'BACKEND_DEV'),
        (1, 0, 'claude-sonnet-4-6', 'MARKETING_ANALYST'),
        (1, 1, 'gpt-4o',            'MARKETING_ANALYST'),
    ]
    for row, col, model, pos in plot_configs:
        ax = axes[row, col]
        sub = df[(df['model_id'] == model) & (df['position_id'] == pos)]
        data = [sub[sub['cv_id'] == cv][dim].values for cv in CV_ORDER]
        bp = ax.boxplot(data, patch_artist=True, widths=0.5,
                        medianprops=dict(color='black', linewidth=2.5),
                        whiskerprops=dict(linewidth=1.3),
                        capprops=dict(linewidth=1.3))
        for patch, color in zip(bp['boxes'], CV_COLORS):
            patch.set_facecolor(color)
            patch.set_alpha(0.8)
        for i, cv in enumerate(CV_ORDER):
            mean_val = sub[sub['cv_id'] == cv][dim].mean()
            if not np.isnan(mean_val):
                ax.plot(i + 1, mean_val, marker='D', color='white',
                        markeredgecolor=CV_COLORS[i], markeredgewidth=2,
                        markersize=7, zorder=5)
                ax.text(i + 1, mean_val + 0.3, f'{mean_val:.1f}',
                        ha='center', va='bottom', fontsize=8,
                        fontweight='bold', color='#374151')
        ax.set_title(f"{MODEL_LABELS[model]}\n{POSITION_LABELS[pos]}",
                     fontsize=10, fontweight='bold')
        ax.set_xticks(range(1, 5))
        ax.set_xticklabels(['Control', 'MIT/LSE', 'Google/\nUnilever', 'Award'],
                           fontsize=8)
        ax.set_ylim(0, 11)
        ax.set_yticks([0, 2, 4, 6, 8, 10])
        ax.set_ylabel('Score (1–10)', fontsize=9)
        ax.grid(axis='y', alpha=0.3, linestyle='--')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

    legend_patches = [mpatches.Patch(color=c, alpha=0.8, label=l)
                      for c, l in zip(CV_COLORS, CV_LABELS.values())]
    fig.legend(handles=legend_patches, loc='lower center', ncol=4,
               fontsize=9, frameon=False, bbox_to_anchor=(0.5, -0.02))
    plt.tight_layout()
    plt.savefig(f'fig1_{di+1}_{dim}.png', dpi=150, bbox_inches='tight',
                facecolor='white')
    plt.show()
    print(f"Figura 1.{di+1} guardada: fig1_{di+1}_{dim}.png")


# =============================================================================
# BLOQUE 2 — DIFERENCIA DE MEDIAS (Test − Control)
# =============================================================================
# Objetivo: cuantificar exactamente cuánto cambia cada dimensión entre
# el Control y cada versión Test. Un cambio positivo en dimensiones donde
# las competencias son idénticas = evidencia directa de efecto halo.
# =============================================================================

print("\n" + "=" * 65)
print("BLOQUE 2 — DIFERENCIA DE MEDIAS (Test − Control)")
print("=" * 65)
print("Cambio positivo en dimensiones idénticas = efecto halo detectado\n")

diff_records = []
for model in MODELS:
    for pos in POSITIONS:
        sub = df[(df['model_id'] == model) & (df['position_id'] == pos)]
        ctrl_means = sub[sub['cv_id'] == 'CV_CONTROL'].groupby('role_id')[DIMS].mean()
        for cv in TEST_CVS:
            test_means = sub[sub['cv_id'] == cv].groupby('role_id')[DIMS].mean()
            diff = test_means - ctrl_means
            diff['cv_id']       = cv
            diff['model_id']    = model
            diff['position_id'] = pos
            diff_records.append(diff.reset_index())

diff_df = pd.concat(diff_records, ignore_index=True)

for model in MODELS:
    for pos in POSITIONS:
        print(f"── {MODEL_LABELS[model]} — {POSITION_LABELS[pos]} ──")
        sub = diff_df[(diff_df['model_id'] == model) &
                      (diff_df['position_id'] == pos)]
        pivot = sub.groupby('cv_id')[DIMS].mean().reindex(TEST_CVS)
        pivot.index = [CV_LABELS[c] for c in TEST_CVS]
        pivot.columns = DIM_SHORT
        print(pivot.round(3).to_string())
        print()

# ── Figura 2: Heatmaps de diferencias — 2x2 (modelo × puesto) ────────────
fig, axes = plt.subplots(2, 2, figsize=(16, 10))
fig.suptitle(
    'Figura 2 — Diferencia de medias respecto al Control (Test − Control)\n'
    'Verde = el atributo halo sube la puntuación | Rojo = la baja',
    fontsize=12, fontweight='bold'
)
for mi, model in enumerate(MODELS):
    for pi, pos in enumerate(POSITIONS):
        ax = axes[mi, pi]
        sub = diff_df[(diff_df['model_id'] == model) &
                      (diff_df['position_id'] == pos)]
        pivot = sub.groupby('cv_id')[DIMS].mean().reindex(TEST_CVS)
        pivot.index   = [CV_LABELS[c] for c in TEST_CVS]
        pivot.columns = DIM_SHORT
        sns.heatmap(pivot, ax=ax, annot=True, fmt='.2f',
                    cmap='RdYlGn', center=0, vmin=-2, vmax=2,
                    linewidths=0.5, linecolor='white',
                    cbar_kws={'label': 'Diferencia de medias'})
        ax.set_title(f"{MODEL_LABELS[model]}\n{POSITION_LABELS[pos]}",
                     fontsize=10, fontweight='bold')
        ax.set_xlabel('Dimensión', fontsize=9)
        ax.set_ylabel('Versión CV', fontsize=9)
        plt.setp(ax.get_xticklabels(), rotation=0, fontsize=8)
        plt.setp(ax.get_yticklabels(), rotation=0, fontsize=9)
plt.tight_layout()
plt.savefig('fig2_heatmap_diff.png', dpi=150, bbox_inches='tight',
            facecolor='white')
plt.show()
print("Figura 2 guardada: fig2_heatmap_diff.png")


# =============================================================================
# BLOQUE 3 — MAGNITUD DEL EFECTO (d de Cohen)
# =============================================================================
# Objetivo: estandarizar las diferencias para poder compararlas entre
# dimensiones y entre modelos.
# d < 0.2 trivial | 0.2–0.5 pequeño | 0.5–0.8 mediano | >0.8 grande
# =============================================================================

print("\n" + "=" * 65)
print("BLOQUE 3 — d DE COHEN (magnitud del efecto)")
print("=" * 65)
print("d < 0.2 trivial | 0.2–0.5 pequeño | 0.5–0.8 mediano | >0.8 grande\n")

def cohen_d(g1, g2):
    n1, n2 = len(g1), len(g2)
    if n1 < 2 or n2 < 2:
        return np.nan
    pooled = np.sqrt(((n1-1)*np.var(g1, ddof=1) +
                      (n2-1)*np.var(g2, ddof=1)) / (n1+n2-2))
    return 0.0 if pooled == 0 else (np.mean(g2) - np.mean(g1)) / pooled

def interpret_d(d):
    if pd.isna(d):      return 'N/A'
    if abs(d) < 0.2:    return 'Trivial'
    elif abs(d) < 0.5:  return 'Pequeño'
    elif abs(d) < 0.8:  return 'Mediano'
    else:               return 'Grande'

cohen_records = []
for model in MODELS:
    for pos in POSITIONS:
        sub  = df[(df['model_id'] == model) & (df['position_id'] == pos)]
        ctrl = sub[sub['cv_id'] == 'CV_CONTROL']
        for cv in TEST_CVS:
            test = sub[sub['cv_id'] == cv]
            for dim in DIMS:
                d = cohen_d(ctrl[dim].values, test[dim].values)
                cohen_records.append({
                    'model_id':    model,
                    'position_id': pos,
                    'cv_id':       cv,
                    'dimension':   dim,
                    'cohen_d':     d,
                    'magnitude':   interpret_d(d)
                })

cohen_df = pd.DataFrame(cohen_records)

for model in MODELS:
    for pos in POSITIONS:
        print(f"── {MODEL_LABELS[model]} — {POSITION_LABELS[pos]} ──")
        sub = cohen_df[(cohen_df['model_id'] == model) &
                       (cohen_df['position_id'] == pos)]
        pivot = sub.pivot(index='cv_id', columns='dimension',
                          values='cohen_d').reindex(TEST_CVS)[DIMS]
        pivot.index   = [CV_LABELS[c] for c in TEST_CVS]
        pivot.columns = DIM_SHORT
        print(pivot.round(3).to_string())
        print()

# Top 10 efectos más grandes
print("── Top 10 efectos más grandes (valor absoluto) ──")
top = cohen_df.assign(abs_d=cohen_df['cohen_d'].abs()).nlargest(10, 'abs_d')
top['model_id']    = top['model_id'].map(MODEL_LABELS)
top['position_id'] = top['position_id'].map(POSITION_LABELS)
top['cv_id']       = top['cv_id'].map(CV_LABELS)
print(top[['model_id','position_id','cv_id','dimension',
           'cohen_d','magnitude']].to_string(index=False))

# ── Figura 3: d de Cohen — barras horizontales por puesto ─────────────────
DIM_COLORS_BARS = ['#3B82F6', '#10B981', '#F59E0B', '#8B5CF6', '#EF4444']

for pi, pos in enumerate(POSITIONS):
    fig, axes = plt.subplots(1, 2, figsize=(16, 6), sharey=False)
    fig.suptitle(
        f'Figura 3.{pi+1} — d de Cohen | {POSITION_LABELS[pos]}\n'
        'Derecha = halo sube puntuación | Izquierda = la baja\n'
        'Líneas: -- 0.2 pequeño | : 0.5 mediano | -. 0.8 grande',
        fontsize=11, fontweight='bold'
    )
    y_pos   = np.arange(len(TEST_CVS))
    height  = 0.14
    offsets = [-2, -1, 0, 1, 2]

    for mi, (model, ax) in enumerate(zip(MODELS, axes)):
        sub = cohen_df[(cohen_df['model_id'] == model) &
                       (cohen_df['position_id'] == pos)]
        for di, (dim, dcolor) in enumerate(zip(DIMS, DIM_COLORS_BARS)):
            dvals = [sub[(sub['cv_id'] == cv) &
                         (sub['dimension'] == dim)]['cohen_d'].values[0]
                     for cv in TEST_CVS]
            bars = ax.barh(y_pos + offsets[di] * height, dvals,
                           height=height, color=dcolor, alpha=0.85,
                           label=DIM_LABELS[di])
            for bar, val in zip(bars, dvals):
                if abs(val) > 0.1:
                    ha  = 'left' if val >= 0 else 'right'
                    pad = 0.05   if val >= 0 else -0.05
                    ax.text(val + pad, bar.get_y() + bar.get_height()/2,
                            f'{val:.2f}', va='center', ha=ha,
                            fontsize=7, fontweight='bold')

        for xval, ls in [(0.2,'--'),(-0.2,'--'),(0.5,':'),(-.5,':'),(0.8,'-.'),(-.8,'-.')]:
            ax.axvline(xval, color='#6B7280', linewidth=0.8,
                       linestyle=ls, alpha=0.6)
        ax.axvline(0, color='black', linewidth=1.5)
        ax.set_yticks(y_pos)
        ax.set_yticklabels([CV_LABELS[c] for c in TEST_CVS], fontsize=10)
        ax.set_xlabel('d de Cohen', fontsize=10)
        ax.set_title(MODEL_LABELS[model], fontsize=11, fontweight='bold')
        ax.set_xlim(-2.5, 3.5)
        ax.grid(axis='x', alpha=0.25, linestyle='--')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

    legend_patches = [mpatches.Patch(color=c, alpha=0.85, label=l)
                      for c, l in zip(DIM_COLORS_BARS, DIM_LABELS)]
    fig.legend(handles=legend_patches, loc='lower center', ncol=5,
               fontsize=9, frameon=False, bbox_to_anchor=(0.5, -0.06))
    plt.tight_layout()
    fname = f'fig3_{pi+1}_cohen_{pos.lower()}.png'
    plt.savefig(fname, dpi=150, bbox_inches='tight', facecolor='white')
    plt.show()
    print(f"Figura 3.{pi+1} guardada: {fname}")


# =============================================================================
# BLOQUE 4 — TEST DE HIPÓTESIS (Mann-Whitney U)
# =============================================================================
# H0: no hay diferencia sistemática entre Control y versión Test
# H1: la versión Test puntúa sistemáticamente diferente al Control
# Mann-Whitney U: no asume normalidad, adecuado para escalas ordinales
# α = 0.05
# =============================================================================

print("\n" + "=" * 65)
print("BLOQUE 4 — TEST DE HIPÓTESIS (Mann-Whitney U, α = 0.05)")
print("=" * 65)

mw_records = []
for model in MODELS:
    for pos in POSITIONS:
        sub  = df[(df['model_id'] == model) & (df['position_id'] == pos)]
        ctrl = sub[sub['cv_id'] == 'CV_CONTROL']
        for cv in TEST_CVS:
            test = sub[sub['cv_id'] == cv]
            for dim in DIMS:
                if len(ctrl[dim].dropna()) < 2 or len(test[dim].dropna()) < 2:
                    continue
                stat, p = stats.mannwhitneyu(
                    ctrl[dim].values, test[dim].values,
                    alternative='two-sided'
                )
                mw_records.append({
                    'model_id':    model,
                    'position_id': pos,
                    'cv_id':       cv,
                    'dimension':   dim,
                    'U_stat':      round(stat, 1),
                    'p_value':     round(p, 4),
                    'significant': 'Sí ✓' if p < 0.05 else 'No'
                })

mw_df = pd.DataFrame(mw_records)

for model in MODELS:
    for pos in POSITIONS:
        print(f"── {MODEL_LABELS[model]} — {POSITION_LABELS[pos]} ──")
        sub = mw_df[(mw_df['model_id'] == model) &
                    (mw_df['position_id'] == pos)]
        for cv in TEST_CVS:
            print(f"\n  vs. {CV_LABELS[cv]}:")
            cv_sub = sub[sub['cv_id'] == cv][['dimension','p_value','significant']]
            cv_sub = cv_sub.set_index('dimension').reindex(DIMS)
            cv_sub.index = DIM_SHORT
            print(cv_sub.to_string())
        print()

# Resumen de significancias
print("── Resumen de tests significativos (p < 0.05) ──")
sig = mw_df[mw_df['p_value'] < 0.05]
for model in MODELS:
    for pos in POSITIONS:
        n = len(sig[(sig['model_id']==model) & (sig['position_id']==pos)])
        total = len(TEST_CVS) * len(DIMS)
        print(f"  {MODEL_LABELS[model]} — {POSITION_LABELS[pos]}: "
              f"{n} de {total} comparaciones significativas")

# ── Figura 4: p-valores heatmap — 2x2 ────────────────────────────────────
fig, axes = plt.subplots(2, 2, figsize=(16, 10))
fig.suptitle(
    'Figura 4 — p-valores Mann-Whitney U (Control vs versión Test)\n'
    'Borde negro = diferencia estadísticamente significativa (p < 0.05)',
    fontsize=12, fontweight='bold'
)
for mi, model in enumerate(MODELS):
    for pi, pos in enumerate(POSITIONS):
        ax = axes[mi, pi]
        sub = mw_df[(mw_df['model_id'] == model) &
                    (mw_df['position_id'] == pos)]
        pivot = sub.pivot(index='cv_id', columns='dimension',
                          values='p_value').reindex(TEST_CVS)[DIMS]
        pivot.index   = [CV_LABELS[c] for c in TEST_CVS]
        pivot.columns = DIM_SHORT
        sns.heatmap(pivot, ax=ax, annot=True, fmt='.3f',
                    cmap='RdYlGn_r', vmin=0, vmax=0.5,
                    linewidths=0.5, linecolor='white',
                    cbar_kws={'label': 'p-valor'})
        for i in range(pivot.shape[0]):
            for j in range(pivot.shape[1]):
                if not pd.isna(pivot.iloc[i, j]) and pivot.iloc[i, j] < 0.05:
                    ax.add_patch(plt.Rectangle((j, i), 1, 1,
                                 fill=False, edgecolor='black', lw=2.5))
        ax.set_title(f"{MODEL_LABELS[model]}\n{POSITION_LABELS[pos]}",
                     fontsize=10, fontweight='bold')
        ax.set_xlabel('Dimensión', fontsize=9)
        ax.set_ylabel('Versión CV', fontsize=9)
        plt.setp(ax.get_xticklabels(), rotation=0, fontsize=8)
        plt.setp(ax.get_yticklabels(), rotation=0, fontsize=9)
plt.tight_layout()
plt.savefig('fig4_pvalues.png', dpi=150, bbox_inches='tight', facecolor='white')
plt.show()
print("Figura 4 guardada: fig4_pvalues.png")


# =============================================================================
# BLOQUE 5 — CORRELACIÓN INTER-DIMENSIONAL (Pearson)
# =============================================================================
# Objetivo: verificar el mecanismo de Thorndike — cuando aparece un atributo
# halo, todas las dimensiones se mueven juntas (correlación artificial),
# aunque sean conceptualmente independientes.
# Si la correlación media sube de Control a Test, eso es evidencia del
# mecanismo de contaminación del efecto halo.
# =============================================================================

print("\n" + "=" * 65)
print("BLOQUE 5 — CORRELACIÓN INTER-DIMENSIONAL (Pearson)")
print("=" * 65)
print("Si el halo actúa: correlación media entre dimensiones > en Test que en Control\n")

corr_records = []
for model in MODELS:
    for pos in POSITIONS:
        sub = df[(df['model_id'] == model) & (df['position_id'] == pos)]
        for cv in CV_ORDER:
            cv_sub = sub[sub['cv_id'] == cv][DIMS]
            corr   = cv_sub.corr()
            upper  = corr.values[np.triu_indices_from(corr.values, k=1)]
            valid  = upper[~np.isnan(upper)]
            mean_corr = valid.mean() if len(valid) > 0 else np.nan
            corr_records.append({
                'model_id':    model,
                'position_id': pos,
                'cv_id':       cv,
                'mean_corr':   mean_corr
            })

corr_summary = pd.DataFrame(corr_records)

for model in MODELS:
    for pos in POSITIONS:
        sub = corr_summary[(corr_summary['model_id'] == model) &
                           (corr_summary['position_id'] == pos)]
        print(f"{MODEL_LABELS[model]} — {POSITION_LABELS[pos]}:")
        for _, row in sub.iterrows():
            print(f"  {CV_LABELS[row['cv_id']]:28} correlación media: {row['mean_corr']:.3f}")
        print()

# ── Figura 5: Matrices de correlación Control vs Award ────────────────────
fig, axes = plt.subplots(2, 4, figsize=(20, 10))
fig.suptitle(
    'Figura 5 — Matrices de correlación inter-dimensional\n'
    'Control vs Test C (Award) — por modelo y puesto',
    fontsize=13, fontweight='bold'
)
plot_pairs = [
    (0, 0, 'claude-sonnet-4-6', 'BACKEND_DEV',       'CV_CONTROL', 'Claude — Backend — Control'),
    (0, 1, 'claude-sonnet-4-6', 'BACKEND_DEV',       'CV_AWARD',   'Claude — Backend — Award'),
    (0, 2, 'claude-sonnet-4-6', 'MARKETING_ANALYST', 'CV_CONTROL', 'Claude — Marketing — Control'),
    (0, 3, 'claude-sonnet-4-6', 'MARKETING_ANALYST', 'CV_AWARD',   'Claude — Marketing — Award'),
    (1, 0, 'gpt-4o',            'BACKEND_DEV',       'CV_CONTROL', 'GPT-4o — Backend — Control'),
    (1, 1, 'gpt-4o',            'BACKEND_DEV',       'CV_AWARD',   'GPT-4o — Backend — Award'),
    (1, 2, 'gpt-4o',            'MARKETING_ANALYST', 'CV_CONTROL', 'GPT-4o — Marketing — Control'),
    (1, 3, 'gpt-4o',            'MARKETING_ANALYST', 'CV_AWARD',   'GPT-4o — Marketing — Award'),
]
for row, col, model, pos, cv, title in plot_pairs:
    ax = axes[row, col]
    sub  = df[(df['model_id'] == model) & (df['position_id'] == pos) &
              (df['cv_id'] == cv)][DIMS]
    corr = sub.corr()
    corr.index   = DIM_SHORT
    corr.columns = DIM_SHORT
    sns.heatmap(corr, ax=ax, annot=True, fmt='.2f',
                cmap='coolwarm', vmin=-1, vmax=1,
                square=True, linewidths=0.5,
                cbar_kws={'shrink': 0.7}, annot_kws={'size': 7})
    ax.set_title(title, fontsize=8, fontweight='bold')
    plt.setp(ax.get_xticklabels(), fontsize=7)
    plt.setp(ax.get_yticklabels(), fontsize=7)
plt.tight_layout()
plt.savefig('fig5_correlations.png', dpi=150, bbox_inches='tight', facecolor='white')
plt.show()
print("Figura 5 guardada: fig5_correlations.png")


# =============================================================================
# BLOQUE 6 — COMPARACIÓN ENTRE MODELOS, PUESTOS Y ROLES
# =============================================================================
# Objetivo: ¿qué modelo muestra mayor efecto halo? ¿en qué puesto es más
# pronunciado? ¿qué rol evaluador es más susceptible al sesgo?
# =============================================================================

print("\n" + "=" * 65)
print("BLOQUE 6 — COMPARACIÓN ENTRE MODELOS, PUESTOS Y ROLES")
print("=" * 65)

# Diferencia global media por modelo y puesto
print("── Diferencia global media (Test − Control, promedio dimensiones) ──")
for model in MODELS:
    for pos in POSITIONS:
        sub = df[(df['model_id'] == model) & (df['position_id'] == pos)]
        ctrl_m = sub[sub['cv_id'] == 'CV_CONTROL'][DIMS].mean().mean()
        print(f"\n{MODEL_LABELS[model]} — {POSITION_LABELS[pos]}:")
        for cv in TEST_CVS:
            test_m = sub[sub['cv_id'] == cv][DIMS].mean().mean()
            print(f"  {CV_LABELS[cv]:28} Δ = {test_m - ctrl_m:+.3f}")

# ── Figura 6: Comparación Claude vs GPT-4o por puesto y versión test ──────
fig, axes = plt.subplots(2, 3, figsize=(18, 10))
fig.suptitle(
    'Figura 6 — Diferencia (Test − Control) por versión de CV\n'
    'Comparación entre Claude y GPT-4o, separado por puesto',
    fontsize=12, fontweight='bold'
)
x      = np.arange(len(DIMS))
width  = 0.35

for pi, pos in enumerate(POSITIONS):
    for ti, cv in enumerate(TEST_CVS):
        ax = axes[pi, ti]
        for mi, (model, color) in enumerate(zip(MODELS, ['#6366F1','#F97316'])):
            sub    = df[(df['model_id'] == model) & (df['position_id'] == pos)]
            ctrl_m = sub[sub['cv_id'] == 'CV_CONTROL'][DIMS].mean()
            test_m = sub[sub['cv_id'] == cv][DIMS].mean()
            diffs  = test_m - ctrl_m
            ax.bar(x + (mi - 0.5) * width, diffs, width=width,
                   color=color, alpha=0.85, label=MODEL_LABELS[model])
        ax.axhline(0, color='black', linewidth=1)
        ax.axhline( 0.5, color='gray', lw=0.8, ls='--', alpha=0.5)
        ax.axhline(-0.5, color='gray', lw=0.8, ls='--', alpha=0.5)
        ax.set_title(f"{POSITION_LABELS[pos]}\n{CV_LABELS[cv]}",
                     fontsize=9, fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels(DIM_SHORT, fontsize=8)
        ax.set_ylabel('Δ (Test − Control)' if ti == 0 else '', fontsize=9)
        ax.grid(axis='y', alpha=0.3, ls='--')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        if pi == 0 and ti == 0:
            ax.legend(fontsize=9, frameon=False)
plt.tight_layout()
plt.savefig('fig6_model_comparison.png', dpi=150, bbox_inches='tight',
            facecolor='white')
plt.show()
print("Figura 6 guardada: fig6_model_comparison.png")

# ── Figura 7: Diferencia media por rol evaluador ───────────────────────────
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle(
    'Figura 7 — Diferencia media (Test − Control) por rol evaluador\n'
    'Promedio de todas las versiones test y todas las dimensiones',
    fontsize=12, fontweight='bold'
)
for mi, model in enumerate(MODELS):
    for pi, pos in enumerate(POSITIONS):
        ax = axes[mi, pi]
        sub = df[(df['model_id'] == model) & (df['position_id'] == pos)]
        role_diffs = {}
        for role in ROLE_ORDER:
            ctrl_m = sub[(sub['cv_id']=='CV_CONTROL') &
                         (sub['role_id']==role)][DIMS].mean().mean()
            test_vals = [
                sub[(sub['cv_id']==cv) &
                    (sub['role_id']==role)][DIMS].mean().mean() - ctrl_m
                for cv in TEST_CVS
            ]
            role_diffs[role] = np.mean(test_vals)

        roles  = list(role_diffs.keys())
        diffs  = list(role_diffs.values())
        colors = ['#059669' if d > 0 else '#DC2626' for d in diffs]
        bars   = ax.barh([ROLE_LABELS[r] for r in roles], diffs,
                         color=colors, alpha=0.8)
        ax.axvline(0, color='black', linewidth=1)
        ax.set_xlabel('Diferencia media (Test − Control)', fontsize=9)
        ax.set_title(f"{MODEL_LABELS[model]}\n{POSITION_LABELS[pos]}",
                     fontsize=10, fontweight='bold')
        ax.grid(axis='x', alpha=0.3, ls='--')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        for bar, val in zip(bars, diffs):
            ax.text(val + (0.01 if val >= 0 else -0.01),
                    bar.get_y() + bar.get_height()/2,
                    f'{val:+.3f}', va='center',
                    ha='left' if val >= 0 else 'right',
                    fontsize=9, fontweight='bold')
plt.tight_layout()
plt.savefig('fig7_role_comparison.png', dpi=150, bbox_inches='tight',
            facecolor='white')
plt.show()
print("Figura 7 guardada: fig7_role_comparison.png")


# =============================================================================
# RESUMEN FINAL
# =============================================================================

print("\n" + "=" * 65)
print("RESUMEN FINAL DEL ANÁLISIS")
print("=" * 65)

print("\n1. CONSISTENCIA (Bloque 1B — varianza intra-perfil)")
intra_all = df.groupby(['model_id','position_id','cv_id','role_id'])[DIMS].std()
print(f"   Mediana global de la SD intra-perfil: {intra_all.median().median():.4f}")
print("   → Sesgo detectado es sistemático, no ruido aleatorio\n")

print("2. DIFERENCIAS MÁS GRANDES (Bloque 2)")
for model in MODELS:
    for pos in POSITIONS:
        sub = df[(df['model_id']==model) & (df['position_id']==pos)]
        max_diff = 0
        max_label = ''
        for cv in TEST_CVS:
            for dim in DIMS:
                ctrl_m = sub[sub['cv_id']=='CV_CONTROL'][dim].mean()
                test_m = sub[sub['cv_id']==cv][dim].mean()
                d = test_m - ctrl_m
                if abs(d) > abs(max_diff):
                    max_diff  = d
                    max_label = f"{CV_LABELS[cv]} × {dim}"
        print(f"   {MODEL_LABELS[model]} — {POSITION_LABELS[pos]}:")
        print(f"   Mayor diferencia: {max_label} (Δ = {max_diff:+.3f})")

print("\n3. d DE COHEN MÁS GRANDES (Bloque 3)")
top5 = cohen_df.assign(abs_d=cohen_df['cohen_d'].abs()).nlargest(5,'abs_d')
for _, row in top5.iterrows():
    print(f"   {MODEL_LABELS[row['model_id']]} | {POSITION_LABELS[row['position_id']]} | "
          f"{CV_LABELS[row['cv_id']]} | {row['dimension']}: "
          f"d = {row['cohen_d']:.3f} ({row['magnitude']})")

print("\n4. TESTS SIGNIFICATIVOS (Bloque 4, p < 0.05)")
for model in MODELS:
    for pos in POSITIONS:
        n = len(mw_df[(mw_df['model_id']==model) &
                      (mw_df['position_id']==pos) &
                      (mw_df['p_value']<0.05)])
        total = len(TEST_CVS) * len(DIMS)
        print(f"   {MODEL_LABELS[model]} — {POSITION_LABELS[pos]}: "
              f"{n} de {total} significativas")

print("\n5. CORRELACIÓN INTER-DIMENSIONAL (Bloque 5)")
