import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

INPUT = "outputs/crimes_2024_clean.parquet"
OUTPUT_DIR = "graficos"

def criar_pasta_saida():
    """Garante que a pasta de gráficos exista."""
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

def carregar_dados():
    """Carrega o arquivo parquet e valida existência."""
    if not os.path.exists(INPUT):
        raise FileNotFoundError(f"Arquivo não encontrado: {INPUT}")
    
    print("✅ Arquivo carregado!")
    return pd.read_parquet(INPUT)

def detectar_outliers(df, col):
    """Detecta outliers com método IQR."""
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1
    limite = Q3 + 1.5 * IQR
    return df[df[col] > limite][["uf", "mes", col]]

def salvar_grafico(nome):
    """Garante diretório e formata caminho completo."""
    return f"{OUTPUT_DIR}/{nome}"

# GRÁFICOS

def grafico_tendencia(df):
    """Gera gráfico de tendência com média móvel."""
    df["mes_num"] = df["mes"].map({
        "Jan":1,"Fev":2,"Mar":3,"Abr":4,"Mai":5,"Jun":6,
        "Jul":7,"Ago":8,"Set":9,"Out":10,"Nov":11,"Dez":12
    })

    tendencia = df.groupby("mes_num")["qtd_de_operacoes"].sum().sort_index()
    mm3 = tendencia.rolling(3).mean()

    plt.figure(figsize=(10,5))
    tendencia.plot(label="Operações")
    mm3.plot(label="Média Móvel (3M)")
    plt.legend()
    plt.xlabel("Mês")
    plt.ylabel("Quantidade")
    plt.title("Tendência Mensal de Operações — MM3")
    plt.tight_layout()
    plt.savefig(salvar_grafico("tendencia_mm3.png"))
    plt.close()

    print("\n📈 Tendência + Média móvel:")
    print(pd.DataFrame({"operacoes": tendencia, "MM3": mm3}))

def grafico_zscore(df):
    """Gráfico de Z-score por UF."""
    df["z_operacoes"] = (
        df["qtd_de_operacoes"] - df["qtd_de_operacoes"].mean()
    ) / df["qtd_de_operacoes"].std()

    ranking = df.groupby("uf")["z_operacoes"].mean().sort_values(ascending=False)
    print("\n📌 Ranking por Z-Score:")
    print(ranking)

    plt.figure(figsize=(12,5))
    ranking.sort_values().plot(kind="bar")
    plt.title("Z-Score Médio de Operações por UF")
    plt.xlabel("UF")
    plt.ylabel("Z-Score Médio")
    plt.tight_layout()
    plt.savefig(salvar_grafico("zscore_uf.png"))
    plt.close()

def grafico_eficiencia(df):
    """Eficiência média por estado."""
    plt.figure(figsize=(12,5))
    df.groupby("uf")["eficiencia"].mean().sort_values().plot(kind="bar")
    plt.title("Eficiência Média das Operações por UF")
    plt.xlabel("UF")
    plt.ylabel("Eficiência (Prisões / Operações)")
    plt.tight_layout()
    plt.savefig(salvar_grafico("eficiencia_uf.png"))
    plt.close()

def grafico_operacoes_por_uf(df):
    """Gráficos verticais e horizontais de operações por UF."""
    uf_counts = df.groupby("uf")["qtd_de_operacoes"].sum().sort_values(ascending=False)

    # Vertical
    plt.figure(figsize=(12,6))
    uf_counts.plot(kind="bar")
    plt.title("Total de Operações por UF")
    plt.xlabel("UF")
    plt.ylabel("Quantidade")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(salvar_grafico("operacoes_por_uf.png"))
    plt.close()

    # Horizontal
    plt.figure(figsize=(10,8))
    uf_counts.sort_values().plot(kind="barh")
    plt.title("Distribuição de Operações por UF (Horizontal)")
    plt.xlabel("Quantidade")
    plt.ylabel("UF")
    plt.tight_layout()
    plt.savefig(salvar_grafico("operacoes_por_uf_horizontal.png"))
    plt.close()

def main():
    criar_pasta_saida()

    df = carregar_dados()

    # Estatísticas gerais
    print("\n📊 Estatísticas descritivas:")
    print(df.describe(include="all"))

    # Outliers
    print("\n🚨 Detecção de Outliers:")
    for col in ["qtd_de_operacoes", "prisoes_em_flagrante", "mbas_expedidos"]:
        out = detectar_outliers(df, col)
        print(f"\n📌 Outliers em {col}:")
        print(out if not out.empty else "Nenhum outlier encontrado.")

    # Indicadores avançados
    df["eficiencia"] = df["prisoes_em_flagrante"] / df["qtd_de_operacoes"].replace(0, np.nan)
    df["vitimas_por_operacao"] = (
        df["qtd_de_vitimas_de_abuso_sexual_infantojuvenil_resgatadas"]
        / df["qtd_de_operacoes"].replace(0, np.nan)
    )

    print("\n⚙️ Indicadores avançados:")
    print(df[["uf", "mes", "eficiencia", "vitimas_por_operacao"]].head())

    # GRÁFICOS
    grafico_tendencia(df)
    grafico_zscore(df)
    grafico_eficiencia(df)
    grafico_operacoes_por_uf(df)

    print("\n🎉 Concluído! Gráficos salvos em /graficos/")

if __name__ == "__main__":
    main()
