# Função para categorizar os preços com base na moda
import pandas as pd


def cr_val_alert(preco, moda):
    limite_inferior = moda * 0.7
    limite_superior = moda * 1.3

    if preco > limite_superior:
        return r"30% acima da moda"
    elif preco < limite_inferior:
        return r"30% abaixo da moda"
    return r"Dentro da faixa"

def boxplot_df(df: pd.DataFrame, group, aggs):
    agg_df = df.groupby(group)['Qual_o_preco_deste_produto'].agg(aggs)
    agg_df['preco_minimo'] = agg_df['mean'] - agg_df['std']
    agg_df['preco_maximo'] = agg_df['mean'] + agg_df['std']
    merged_df = df.merge(agg_df, on=group, how='left', left_index=False, right_index=False)

    def verifica_margem(row):
        if pd.isna(row['preco_minimo']) or pd.isna(row['preco_maximo']):
            return None
        return row['preco_minimo'] <= row['Qual_o_preco_deste_produto'] <= row['preco_maximo']

    merged_df['fora_intervalo'] = merged_df.apply(verifica_margem, axis=1)
    merged_df = merged_df.set_index(df.index)

    return merged_df