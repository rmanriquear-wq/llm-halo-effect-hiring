# =============================================================================
# ANÁLISIS DE VARIABILIDAD POR ROL EVALUADOR
# PFG TECNUN — ¿Simulan los LLMs el efecto halo en selección de personal?
# =============================================================================
# Objetivo: examinar cómo cada rol evaluador (HR Officer, Head of HR, CTO, CEO)
# puntúa diferente el mismo CV. Esto responde a dos preguntas:
# 1. ¿Los prompts funcionan como se diseñaron? (cada rol debería tener
#    criterios distintos y por tanto puntuaciones distintas)
# 2. ¿El efecto halo es más pronunciado en unos roles que en otros?
#    (algunos evaluadores pueden ser más susceptibles al sesgo de prestigio)
# =============================================================================



# -----------------------------------------------------------------------------
# CARGA DE DATOS
# -----------------------------------------------------------------------------

df = pd.read_excel(FILE_PATH)
df['error'] = df['error'].astype(str).str.upper().isin(['TRUE', '1'])
df = df[df['error'] == False].copy()

# -----------------------------------------------------------------------------
# CONFIGURACIÓN
# -----------------------------------------------------------------------------
DIMS       = ['technical_skills', 'communication', 'leadership_potential',
              'teamwork', 'cultural_fit']
DIM_LABELS = ['Technical Skills', 'Communication', 'Leadership Potential',
              'Teamwork', 'Cultural Fit']
DIM_SHORT  = ['Tech.', 'Comm.', 'Leadership', 'Teamwork', 'Cult. Fit']

MODELS       = ['claude-sonnet-4-6', 'gpt-4o']
MODEL_LABELS = {'claude-sonnet-4-6': 'Claude Sonnet 4.6', 'gpt-4o': 'GPT-4o'}

POSITIONS = ['BACKEND_DEV', 'MARKETING_ANALYST']
POSITION_LABELS = {
    'BACKEND_DEV':       'Backend Developer (James Mitchell)',
    'MARKETING_ANALYST': 'Digital Marketing Analyst (Laura Sánchez)'
}

CV_ORDER  = ['CV_CONTROL', 'CV_ELITE_UNI', 'CV_PRESTIGE_EMPLOYER', 'CV_AWARD']
CV_LABELS = {
    'CV_CONTROL':           'Control\n(Zaragoza / Complutense)',
    'CV_ELITE_UNI':         'Test A\n(MIT / LSE)',
    'CV_PRESTIGE_EMPLOYER': 'Test B\n(Google / Unilever)',
    'CV_AWARD':             'Test C\n(Award)'
}
CV_LABELS_SHORT = {
    'CV_CONTROL':           'Control',
    'CV_ELITE_UNI':         'MIT/LSE',
    'CV_PRESTIGE_EMPLOYER': 'Google/Unilever',
    'CV_AWARD':             'Award'
}

ROLE_ORDER  = ['HR_OFFICER', 'HEAD_HR', 'CTO', 'CEO']
ROLE_LABELS = {
    'HR_OFFICER': 'HR Officer',
    'HEAD_HR':    'Head of HR',
    'CTO':        'CTO',
    'CEO':        'CEO'
}
ROLE_COLORS = ['#3B82F6', '#10B981', '#F59E0B', '#EF4444']


# =============================================================================
# ANÁLISIS 1 — Medias por rol en cada versión de CV
# =============================================================================
# Muestra cómo puntúa cada evaluador el mismo candidato.
# Si los prompts funcionan bien, HR Officer y CTO deberían diferir en Tech,
# CEO y Head HR deberían diferir en Cultural Fit y Leadership.
# =============================================================================

print("=" * 70)
print("ANÁLISIS DE VARIABILIDAD POR ROL EVALUADOR")
print("=" * 70)

print("\n── Medias por rol evaluador (promedio de las 5 iteraciones) ──\n")
for model in MODELS:
    for pos in POSITIONS:
        sub = df[(df['model_id'] == model) & (df['position_id'] == pos)]
        print(f"{MODEL_LABELS[model]} — {POSITION_LABELS[pos]}:")
        print(f"  {'':20} {'Tech':>6} {'Comm':>6} {'Lead':>6} {'Team':>6} {'Cult':>6}")
        print("  " + "-" * 55)
        for cv in CV_ORDER:
            label = CV_LABELS_SHORT[cv]
            cv_sub = sub[sub['cv_id'] == cv]
            print(f"  [{label}]")
            for role in ROLE_ORDER:
                role_sub = cv_sub[cv_sub['role_id'] == role][DIMS].mean()
                print(f"    {ROLE_LABELS[role]:18} "
                      f"{role_sub['technical_skills']:>5.2f}  "
                      f"{role_sub['communication']:>5.2f}  "
                      f"{role_sub['leadership_potential']:>5.2f}  "
                      f"{role_sub['teamwork']:>5.2f}  "
                      f"{role_sub['cultural_fit']:>5.2f}")
        print()


# =============================================================================
# ANÁLISIS 2 — Diferencia del halo por rol (Test − Control para cada rol)
# =============================================================================
# Pregunta clave: ¿qué rol es más susceptible al efecto halo?
# Si el CEO sube más sus puntuaciones con el Award que el CTO, significa
# que la visión estratégica es más vulnerable al sesgo de prestigio.
# =============================================================================

print("=" * 70)
print("DIFERENCIA (Test − Control) POR ROL EVALUADOR")
print("=" * 70)
print("Identifica qué evaluador es más susceptible al efecto halo\n")

halo_by_role = []
for model in MODELS:
    for pos in POSITIONS:
        sub = df[(df['model_id'] == model) & (df['position_id'] == pos)]
        for role in ROLE_ORDER:
            role_sub = sub[sub['role_id'] == role]
            ctrl_mean = role_sub[role_sub['cv_id'] == 'CV_CONTROL'][DIMS].mean()
            for cv in ['CV_ELITE_UNI', 'CV_PRESTIGE_EMPLOYER', 'CV_AWARD']:
                test_mean = role_sub[role_sub['cv_id'] == cv][DIMS].mean()
                diff = test_mean - ctrl_mean
                halo_by_role.append({
                    'model_id':    model,
                    'position_id': pos,
                    'role_id':     role,
                    'cv_id':       cv,
                    'mean_diff':   diff.mean(),  # media de todas las dimensiones
                    **{dim: diff[dim] for dim in DIMS}
                })

halo_role_df = pd.DataFrame(halo_by_role)

for model in MODELS:
    for pos in POSITIONS:
        sub = halo_role_df[(halo_role_df['model_id'] == model) &
                           (halo_role_df['position_id'] == pos)]
        print(f"{MODEL_LABELS[model]} — {POSITION_LABELS[pos]}:")
        pivot = sub.groupby(['role_id', 'cv_id'])['mean_diff'].mean().unstack()
        pivot = pivot.reindex(ROLE_ORDER)[['CV_ELITE_UNI',
                                           'CV_PRESTIGE_EMPLOYER', 'CV_AWARD']]
        pivot.index   = [ROLE_LABELS[r] for r in ROLE_ORDER]
        pivot.columns = ['MIT/LSE', 'Google/Unilever', 'Award']
        print(pivot.round(3).to_string())
        print()


# =============================================================================
# FIGURAS
# =============================================================================

# ── FIGURA A: Radar/líneas por rol — un gráfico por modelo × puesto ─────────
# Muestra el perfil de puntuación de cada rol en el CV control.
# Si los 4 roles producen perfiles distintos, los prompts funcionan bien.

fig, axes = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle(
    'Figura A — Perfil de puntuación por rol evaluador (CV Control)\n'
    'Si los roles difieren entre sí, los prompts capturan criterios distintos',
    fontsize=13, fontweight='bold'
)

x = np.arange(len(DIMS))
width = 0.18
offsets = [-1.5, -0.5, 0.5, 1.5]

for mi, model in enumerate(MODELS):
    for pi, pos in enumerate(POSITIONS):
        ax = axes[mi, pi]
        sub = df[(df['model_id'] == model) &
                 (df['position_id'] == pos) &
                 (df['cv_id'] == 'CV_CONTROL')]

        for i, (role, color) in enumerate(zip(ROLE_ORDER, ROLE_COLORS)):
            role_means = sub[sub['role_id'] == role][DIMS].mean()
            role_stds  = sub[sub['role_id'] == role][DIMS].std()
            bars = ax.bar(x + offsets[i] * width, role_means,
                          width=width, color=color, alpha=0.85,
                          label=ROLE_LABELS[role],
                          yerr=role_stds, capsize=3,
                          error_kw={'linewidth': 1.1, 'ecolor': '#374151'})
            for bar, val in zip(bars, role_means):
                ax.text(bar.get_x() + bar.get_width() / 2,
                        val + 0.15, f'{val:.1f}',
                        ha='center', va='bottom', fontsize=6,
                        color='#374151', fontweight='bold')

        ax.set_title(f"{MODEL_LABELS[model]}\n{POSITION_LABELS[pos]}",
                     fontsize=10, fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels(DIM_SHORT, fontsize=10)
        ax.set_ylabel('Media (± SD)', fontsize=10)
        ax.set_ylim(0, 12)
        ax.set_yticks([0, 2, 4, 6, 8, 10])
        ax.grid(axis='y', alpha=0.3, linestyle='--')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        if mi == 0 and pi == 0:
            ax.legend(fontsize=9, frameon=False, ncol=2,
                      loc='upper left')

plt.tight_layout()
plt.savefig('figA_perfil_rol_control.png', dpi=150, bbox_inches='tight',
            facecolor='white')
plt.show()
print("Figura A guardada: figA_perfil_rol_control.png")


# ── FIGURA B: Heatmap de diferencias (Test−Control) por rol ─────────────────
# 4 heatmaps (modelo × puesto), filas = roles, columnas = versiones test
# Color = magnitud del sesgo medio sobre todas las dimensiones

fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle(
    'Figura B — Susceptibilidad al efecto halo por rol evaluador\n'
    'Diferencia media (Test − Control) promediando todas las dimensiones\n'
    'Verde = halo positivo | Rojo = efecto cuerno',
    fontsize=12, fontweight='bold'
)

for mi, model in enumerate(MODELS):
    for pi, pos in enumerate(POSITIONS):
        ax = axes[mi, pi]
        sub = halo_role_df[(halo_role_df['model_id'] == model) &
                           (halo_role_df['position_id'] == pos)]
        pivot = sub.groupby(['role_id', 'cv_id'])['mean_diff'].mean().unstack()
        pivot = pivot.reindex(ROLE_ORDER)[['CV_ELITE_UNI',
                                           'CV_PRESTIGE_EMPLOYER', 'CV_AWARD']]
        pivot.index   = [ROLE_LABELS[r] for r in ROLE_ORDER]
        pivot.columns = ['Test A\n(MIT/LSE)', 'Test B\n(Google/Unilever)',
                         'Test C\n(Award)']
        sns.heatmap(pivot, ax=ax, annot=True, fmt='.2f',
                    cmap='RdYlGn', center=0, vmin=-1.5, vmax=1.5,
                    linewidths=0.5, linecolor='white',
                    cbar_kws={'label': 'Δ medio'}, annot_kws={'size': 10})
        ax.set_title(f"{MODEL_LABELS[model]}\n{POSITION_LABELS[pos]}",
                     fontsize=10, fontweight='bold')
        ax.set_xlabel('Versión CV', fontsize=9)
        ax.set_ylabel('Rol evaluador', fontsize=9)
        plt.setp(ax.get_xticklabels(), rotation=0, fontsize=9)
        plt.setp(ax.get_yticklabels(), rotation=0, fontsize=10)

plt.tight_layout()
plt.savefig('figB_halo_por_rol.png', dpi=150, bbox_inches='tight',
            facecolor='white')
plt.show()
print("Figura B guardada: figB_halo_por_rol.png")


# ── FIGURA C: Evolución del halo por rol — líneas por CV ─────────────────────
# Para cada modelo y puesto, muestra cómo la diferencia (Test−Control) varía
# entre roles. Si una línea sube mucho en un rol, ese rol es más susceptible.
# Separado por dimensión de evaluación para ver en qué aspectos opera el halo.

for dim, dim_label in zip(DIMS, DIM_LABELS):
    fig, axes = plt.subplots(2, 2, figsize=(16, 10))
    fig.suptitle(
        f'Figura C — Diferencia (Test − Control) por rol evaluador\n'
        f'Dimensión: {dim_label}',
        fontsize=13, fontweight='bold'
    )

    cv_colors_test = {'CV_ELITE_UNI': '#3B82F6',
                      'CV_PRESTIGE_EMPLOYER': '#10B981',
                      'CV_AWARD': '#F59E0B'}
    cv_labels_test = {'CV_ELITE_UNI': 'Test A (MIT/LSE)',
                      'CV_PRESTIGE_EMPLOYER': 'Test B (Google/Unilever)',
                      'CV_AWARD': 'Test C (Award)'}

    for mi, model in enumerate(MODELS):
        for pi, pos in enumerate(POSITIONS):
            ax = axes[mi, pi]
            sub_halo = halo_role_df[(halo_role_df['model_id'] == model) &
                                    (halo_role_df['position_id'] == pos)]

            for cv in ['CV_ELITE_UNI', 'CV_PRESTIGE_EMPLOYER', 'CV_AWARD']:
                cv_sub = sub_halo[sub_halo['cv_id'] == cv]
                vals = [cv_sub[cv_sub['role_id'] == role][dim].values[0]
                        for role in ROLE_ORDER]
                ax.plot([ROLE_LABELS[r] for r in ROLE_ORDER], vals,
                        marker='o', linewidth=2, markersize=8,
                        color=cv_colors_test[cv],
                        label=cv_labels_test[cv])
                for j, val in enumerate(vals):
                    ax.annotate(f'{val:.2f}',
                                (ROLE_LABELS[ROLE_ORDER[j]], val),
                                textcoords='offset points',
                                xytext=(0, 8), ha='center',
                                fontsize=8, fontweight='bold',
                                color=cv_colors_test[cv])

            ax.axhline(0, color='black', linewidth=1, linestyle='-')
            ax.axhline( 0.5, color='gray', lw=0.8, ls='--', alpha=0.5)
            ax.axhline(-0.5, color='gray', lw=0.8, ls='--', alpha=0.5)
            ax.set_title(f"{MODEL_LABELS[model]}\n{POSITION_LABELS[pos]}",
                         fontsize=10, fontweight='bold')
            ax.set_ylabel(f'Δ {dim_label} (Test − Control)', fontsize=9)
            ax.set_ylim(-2.5, 3.5)
            ax.grid(axis='y', alpha=0.3, linestyle='--')
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            if mi == 0 and pi == 0:
                ax.legend(fontsize=9, frameon=False, loc='upper right')

    plt.tight_layout()
    fname = f'figC_{dim}_por_rol.png'
    plt.savefig(fname, dpi=150, bbox_inches='tight', facecolor='white')
    plt.show()
    print(f"Figura C ({dim_label}) guardada: {fname}")


# ── FIGURA D: Varianza entre roles por CV ─────────────────────────────────────
# Para cada versión de CV, muestra la desviación típica entre los 4 roles.
# Alta varianza = los roles evalúan muy diferente (prompts bien diferenciados).
# Si la varianza entre roles sube con el halo, el halo también dispersa juicios.

print("\n── Varianza entre roles por versión de CV ──")
print("Alta SD = los roles evalúan muy diferente el mismo candidato\n")

var_records = []
for model in MODELS:
    for pos in POSITIONS:
        sub = df[(df['model_id'] == model) & (df['position_id'] == pos)]
        for cv in CV_ORDER:
            cv_sub = sub[sub['cv_id'] == cv]
            role_means = cv_sub.groupby('role_id')[DIMS].mean()
            between_role_std = role_means.std()
            var_records.append({
                'model_id':    model,
                'position_id': pos,
                'cv_id':       cv,
                **{f'std_{dim}': between_role_std[dim] for dim in DIMS},
                'mean_std':    between_role_std.mean()
            })

var_df = pd.DataFrame(var_records)

for model in MODELS:
    for pos in POSITIONS:
        sub = var_df[(var_df['model_id'] == model) &
                     (var_df['position_id'] == pos)]
        print(f"{MODEL_LABELS[model]} — {POSITION_LABELS[pos]}:")
        print(f"  {'':20} {'Tech':>6} {'Comm':>6} {'Lead':>6} {'Team':>6} {'Cult':>6} {'Media':>6}")
        for _, row in sub.iterrows():
            print(f"  {CV_LABELS_SHORT[row['cv_id']]:20} "
                  f"{row['std_technical_skills']:>5.3f}  "
                  f"{row['std_communication']:>5.3f}  "
                  f"{row['std_leadership_potential']:>5.3f}  "
                  f"{row['std_teamwork']:>5.3f}  "
                  f"{row['std_cultural_fit']:>5.3f}  "
                  f"{row['mean_std']:>5.3f}")
        print()

fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle(
    'Figura D — Varianza entre roles evaluadores por versión de CV\n'
    'SD entre los 4 roles para cada dimensión — mayor SD = roles más divergentes',
    fontsize=12, fontweight='bold'
)

x = np.arange(len(DIMS))
width = 0.18
offsets_cv = [-1.5, -0.5, 0.5, 1.5]
cv_colors = ['#6B7280', '#3B82F6', '#10B981', '#F59E0B']

for mi, model in enumerate(MODELS):
    for pi, pos in enumerate(POSITIONS):
        ax = axes[mi, pi]
        sub = var_df[(var_df['model_id'] == model) &
                     (var_df['position_id'] == pos)]

        for i, cv in enumerate(CV_ORDER):
            row = sub[sub['cv_id'] == cv].iloc[0]
            vals = [row[f'std_{dim}'] for dim in DIMS]
            ax.bar(x + offsets_cv[i] * width, vals,
                   width=width, color=cv_colors[i], alpha=0.85,
                   label=CV_LABELS_SHORT[cv])
            for j, (bar_x, val) in enumerate(
                    zip(x + offsets_cv[i] * width, vals)):
                if val > 0.05:
                    ax.text(bar_x, val + 0.02, f'{val:.2f}',
                            ha='center', va='bottom',
                            fontsize=6.5, fontweight='bold', color='#374151')

        ax.set_title(f"{MODEL_LABELS[model]}\n{POSITION_LABELS[pos]}",
                     fontsize=10, fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels(DIM_SHORT, fontsize=10)
        ax.set_ylabel('SD entre roles evaluadores', fontsize=10)
        ax.set_ylim(0, 3.5)
        ax.grid(axis='y', alpha=0.3, linestyle='--')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        if mi == 0 and pi == 0:
            legend_patches = [mpatches.Patch(color=c, alpha=0.85, label=l)
                              for c, l in zip(cv_colors,
                                              CV_LABELS_SHORT.values())]
            ax.legend(handles=legend_patches, fontsize=9, frameon=False,
                      ncol=2, loc='upper right')

plt.tight_layout()
plt.savefig('figD_varianza_entre_roles.png', dpi=150,
            bbox_inches='tight', facecolor='white')
plt.show()
print("Figura D guardada: figD_varianza_entre_roles.png")

print("\nAnálisis de variabilidad por rol completado.")
print("Figuras generadas: figA, figB, figC (×5 dimensiones), figD")
