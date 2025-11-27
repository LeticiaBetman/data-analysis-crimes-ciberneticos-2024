import os
import pandas as pd
from unidecode import unidecode

INPUT = "data/dados-de-crimes-ciberneticos-jan-a-dez-de-2024.xlsx"
OUTPUT = "outputs/crimes_2024_clean.parquet"

def main():
    # 1. Verifica se o arquivo existe
    if not os.path.exists(INPUT):
        raise FileNotFoundError(f"Arquivo não encontrado: {INPUT}")
    print("✅ Arquivo encontrado!")

    # 2. Lê o arquivo Excel (primeira aba)
    excel_file = pd.ExcelFile(INPUT)
    print("📄 Abas:", excel_file.sheet_names)
    aba = excel_file.sheet_names[0]
    df = pd.read_excel(INPUT, sheet_name=aba)

    # 3. Mostra informações básicas
    print("\n📏 Formato:", df.shape)
    print("\n📋 Colunas:", df.columns.tolist())
    print("\n🔍 Primeiras linhas:")
    print(df.head())

    # 4. Padroniza nomes das colunas
    df.columns = [unidecode(col).strip().lower().replace(" ", "_") for col in df.columns]
    print("\n📑 Novos nomes de colunas:", df.columns.tolist())

    # 5. Verifica valores nulos
    print("\n❓ Valores nulos por coluna:")
    print(df.isna().sum())

    # 6. Converte colunas numéricas
    colunas_numericas = [
        "qtd_de_operacoes",
        "prisoes_em_flagrante",
        "qtd_de_vitimas_de_abuso_sexual_infantojuvenil_resgatadas",
        "mbas_expedidos",
        "prisoes_preventivas_expedidas",
        "prisoes_temporarias_expedidas",
    ]
    for col in colunas_numericas:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # 7. Padroniza meses
    df["mes"] = df["mes"].str.strip().str.capitalize()
    
    # 8. Remove linhas sem UF (registros vazios)
    linhas_antes = len(df)
    df = df.dropna(subset=["uf"])
    linhas_depois = len(df)
    print(f"\n🧹 Linhas removidas: {linhas_antes - linhas_depois}")
    
    # 9. Padroniza UF e área
    df["uf"] = df["uf"].str.strip().str.upper()
    df["area_de_atribuicao"] = df["area_de_atribuicao"].str.strip().str.title()

    # 10. Remove duplicadas
    duplicadas = df.duplicated().sum()
    print(f"🔁 Linhas duplicadas: {duplicadas}")
    if duplicadas > 0:
        df = df.drop_duplicates()

    # 11. Salva o resultado limpo
    df.to_parquet(OUTPUT, index=False)
    print(f"\n💾 Arquivo limpo salvo em: {OUTPUT}")

if __name__ == "__main__":
    main()


