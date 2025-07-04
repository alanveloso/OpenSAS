import pandas as pd

# Caminho do arquivo JTL do plano high
target_file = 'results/high_test_run_2.jtl'

df = pd.read_csv(target_file)

print(f'Total de requisições: {len(df)}')
print(f'Total de erros 403: {(df["responseCode"] == 403).sum()}')
print('\nContagem de 403 por label:')
print(df[df['responseCode'] == 403]['label'].value_counts())

print('\nExemplos de sequência de erro 403 por thread:')
for thread, group in df.groupby('threadName'):
    group = group.reset_index(drop=True)
    for idx, row in group.iterrows():
        if row['responseCode'] == 403:
            print(f'\nThread: {thread}, Linha: {idx}')
            if idx > 0:
                prev = group.loc[idx-1]
                print('Anterior:', prev[['label','responseCode','responseMessage']].to_dict())
            print('Atual:', row[['label','responseCode','responseMessage']].to_dict())
            print('-'*40)
    # Limitar a análise para as 3 primeiras threads
    if int(thread.split('-')[-1]) > 3:
        break 