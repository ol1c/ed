import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Zapewnienie istnienia folderu na wykresy
output_dir = 'wykresy'
os.makedirs(output_dir, exist_ok=True)

# Wczytanie danych
pokemon_df = pd.read_csv('dataset/pokemon.csv')
combats_df = pd.read_csv('dataset/combats.csv')

print("Generowanie oddzielnych histogramów i wykresów pudełkowych statystyk pokemonów...")
# Histogramy dla cech numerycznych
features = ['HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed']
features_num = features + ['Generation']
for feature in features_num:
    # Histogram
    plt.figure(figsize=(8, 6))
    pokemon_df[feature].hist(bins=20, color='teal', edgecolor='black')
    plt.title(f'Rozkład atrybutu: {feature}')
    plt.xlabel(feature)
    plt.ylabel('Liczebność')
    plt.tight_layout()
    safe_feature = feature.replace('. ', '_').replace(' ', '_')
    plt.savefig(f'{output_dir}/hist_{safe_feature}.png')
    plt.close()
    
    # Wykres pudełkowy (tylko dla głównych statystyk bojowych)
    if feature in features:
        plt.figure(figsize=(6, 4))
        sns.boxplot(y=pokemon_df[feature], color='lightblue')
        plt.title(f'Wykres pudełkowy: {feature}')
        plt.ylabel(feature) # Obrócona oś, z x na y
        plt.tight_layout()
        plt.savefig(f'{output_dir}/boxplot_{safe_feature}.png')
        plt.close()

print("Generowanie wykresów dla cech kategorycznych (Type 1, Type 2, Legendary)...")
cat_features = ['Type 1', 'Type 2', 'Legendary']
for feature in cat_features:
    plt.figure(figsize=(10, 6))
    sns.countplot(data=pokemon_df, y=feature, order=pokemon_df[feature].value_counts().index, palette='viridis', hue=pokemon_df[feature], legend=False)
    plt.title(f'Rozkład atrybutu: {feature}')
    plt.xlabel('Ilość')
    plt.ylabel(feature)
    plt.tight_layout()
    safe_feature = feature.replace('. ', '_').replace(' ', '_')
    plt.savefig(f'{output_dir}/hist_{safe_feature}.png')
    plt.close()

print("Generowanie macierzy korelacji (Spearman)...")
# Macierz korelacji cech numerycznych wg Spearmana
corr_matrix_spearman = pokemon_df[features + ['Generation', 'Legendary']].corr(method='spearman')

# Macierz bez współczynników
plt.figure(figsize=(10, 8))
sns.heatmap(corr_matrix_spearman, annot=False, cmap='coolwarm', vmin=-1, vmax=1)
plt.title('Macierz korelacji Spearmana statystyk Pokemonów')
plt.tight_layout()
plt.savefig(f'{output_dir}/macierz_korelacji_spearman.png')
plt.close()

# Macierz ze współczynnikami
plt.figure(figsize=(10, 8))
sns.heatmap(corr_matrix_spearman, annot=True, cmap='coolwarm', fmt='.2f', vmin=-1, vmax=1)
plt.title('Macierz korelacji Spearmana ze współczynnikami')
plt.tight_layout()
plt.savefig(f'{output_dir}/macierz_korelacji_spearman_annot.png')
plt.close()

print("Generowanie korelacji statystyk z wynikiem walki...")
# Dołączanie statystyk do wyników walk i obliczanie różnic
walki_df = combats_df.copy()
# Zmienna celu: 1 jeśli wygrał pierwszy pokemon, 0 jeśli drugi
walki_df['First_won'] = (walki_df['Winner'] == walki_df['First_pokemon']).astype(int)

# Podzbiór cech z pokemon_df do dołączenia
poke_stats = pokemon_df[['#'] + features]

# Dołączenie statystyk pierwszego
walki_df = walki_df.merge(poke_stats, left_on='First_pokemon', right_on='#', how='left')
walki_df = walki_df.rename(columns={f: f'{f}_1' for f in features}).drop(columns=['#'])

# Dołączenie statystyk drugiego
walki_df = walki_df.merge(poke_stats, left_on='Second_pokemon', right_on='#', how='left')
walki_df = walki_df.rename(columns={f: f'{f}_2' for f in features}).drop(columns=['#'])

# Wyliczenie różnic statystyk (Pokemon 1 - Pokemon 2)
for f in features:
    walki_df[f'Diff_{f}'] = walki_df[f'{f}_1'] - walki_df[f'{f}_2']

diff_cols = [f'Diff_{f}' for f in features] + ['First_won']

# Macierz korelacji z wynikiem walki
corr_walki_spearman = walki_df[diff_cols].corr(method='spearman')

plt.figure(figsize=(10, 8))
sns.heatmap(corr_walki_spearman, annot=True, cmap='RdYlGn', fmt='.2f', vmin=-1, vmax=1)
plt.title('Korelacja Spearmana (różnice cech vs. Zwycięstwo Pierwszego)')
plt.tight_layout()
plt.savefig(f'{output_dir}/korelacja_wynik_walki.png')
plt.close()

# Dodatkowy wykres słupkowy sortujący korelację z cechą wygranej
corr_with_target = corr_walki_spearman['First_won'].drop('First_won').sort_values(ascending=False)
plt.figure(figsize=(10, 6))
sns.barplot(x=corr_with_target.values, y=corr_with_target.index, palette='viridis')
plt.title('Korelacja atrybutów ze statusem zwycięstwa (Spearman)')
plt.xlabel('Współczynnik korelacji')
plt.ylabel('Różnica atrybutu (Pierwszy - Drugi)')
plt.tight_layout()
plt.savefig(f'{output_dir}/korelacja_z_wynikiem_bar.png')
plt.close()

print(f"Wykresy zostały pomyślnie wygenerowane i zapisane w folderze '{output_dir}'.")
