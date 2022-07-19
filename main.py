import datetime
import pandas as pd


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


"""formato='%m/%d/%Y'
fecha = "04/04/2021"
fecha_creada = datetime.datetime.strptime(fecha, formato).date()
url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQ7vGtlwPr73WmlOAKR3lK4223ytE9mQzodJJtABdyewRjeLpc91aJv-9MeGPEzIsJoBfYFG1h_HXJG/pubhtml"
tablas = pd.read_html(url, header=1, encoding="UTF-8")
df = tablas[0]
df_info = df.iloc[1:, :8]
df_info.loc[df_info.iloc[:, 2] == 'Avril Napout', 'Fecha de nacimiento']='04/17/2015'
df_info['Fecha de nacimiento'] = pd.to_datetime(df_info['Fecha de nacimiento'], infer_datetime_format=True)
df_info['Fecha'] = pd.to_datetime(df_info['Fecha'], infer_datetime_format=True)

try:
    df_info['dias'] = (df_info['Fecha'] - df_info['Fecha de nacimiento']).dt.days
    df_info['Edad'] = df_info['dias'] / 365.2425
    df_info['Edad'] = df_info['Edad'].astype(int)

except:
    print("Hubo un error")"""
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print(datetime.datetime.now())

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
