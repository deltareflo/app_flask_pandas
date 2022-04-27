import bisect
from flask import abort
import pandas as pd
import numpy as np


def convertir_pickle(archivo):
    excel = f"{archivo}.xlsx"
    dfs = pd.read_excel(excel)
    dfs.to_pickle(f"{archivo}.pkl")


# Función para obtener el baremo adecusado según el sexo y la edad del sujeto
def get_dataframe_p1(baremo, edad):
    if baremo == "General" and edad < 5:
        df2 = pd.read_pickle('baremos/P1_Gral_3_4.pkl')

    elif baremo == "Mujeres" and edad < 5:
        df2 = pd.read_pickle('baremos/P1_Muj_3_4.pkl')

    elif baremo == "Varones" and edad < 5:
        df2 = pd.read_pickle('baremos/P1_Var_3_4.pkl')

    elif baremo == "General" and edad < 7:
        df2 = pd.read_pickle('baremos/P1_Gral_5_6.pkl')

    elif baremo == "Varones" and edad < 7:
        df2 = pd.read_pickle('baremos/P1_Var_5_6.pkl')

    elif baremo == "Mujeres" and edad < 7:
        df2 = pd.read_pickle('baremos/P1_Muj_5_6.pkl')

    return df2


def transforma_a_numero(x):
    if x == "Nunca":
        return 0
    elif x == "Alguna vez":
        return 1
    elif x == "Frecuentemente":
        return 2
    elif x == "Casi siempre":
        return 3
    else:
        return 0


# De acuerdo a la nota T de la persona se obtienen los niveles
def get_niveles(df_final, dimension):
    opciones_niveles_adapta = ['Clínicamente significativo', 'En riesgo', 'Medio', 'Alto', 'Muy alto']
    opciones_niveles_clinico = ['Muy bajo', 'Bajo', 'Medio', 'En riesgo', 'Clínicamente significativo']
    clinico = ["Agresividad", "Ansiedad", "Atipicidad", "Depresion", "Hiperactividad", "Problemas de atencion",
               "Retraimiento", "Somatizacion", "Problemas de conducta", "Problemas de aprendizaje",
               "Actitud negativa hacia el colegio", "Actitud negativa hacia los profesores", "Locus de control",
               "Estres social", "Sentido de incapacidad", "Busqueda de sensaciones"]
    adaptable = ["Adaptabilidad", "Habilidades sociales"]
    condiciones = [df_final[f'T {dimension}'] <= 30, df_final[f'T {dimension}'] <= 40, df_final[f'T {dimension}'] <= 59,
                   df_final[f'T {dimension}'] <= 69, df_final[f'T {dimension}'] <= 129]
    if dimension in clinico:
        df_final[f'Nivel {dimension}'] = np.select(condiciones, opciones_niveles_clinico)
    else:
        df_final[f'Nivel {dimension}'] = np.select(condiciones, opciones_niveles_adapta)

    return df_final[f'Nivel {dimension}']


# De una lista de dimensiones se obtienen todos los niveles aplicando la funcion get_niveles
def niveles_all(df_final, prueba="P1"):
    dimensiones_p1 = ["Adaptabilidad", "Agresividad", "Atipicidad", "Ansiedad", "Depresion", "Hiperactividad",
                      "Habilidades sociales", "Problemas de atencion", "Retraimiento", "Somatizacion"]
    dimensiones_p2 = ["Adaptabilidad", "Agresividad", "Atipicidad", "Ansiedad", "Depresion", "Hiperactividad",
                      "Habilidades sociales", "Problemas de atencion", "Retraimiento", "Somatizacion",
                      "Problemas de conducta", "Liderazgo"]
    dimensiones_p3 = ["Agresividad", "Atipicidad", "Ansiedad", "Depresion", "Hiperactividad",
                      "Habilidades sociales", "Problemas de atencion", "Retraimiento", "Somatizacion",
                      "Problemas de conducta", "Liderazgo"]
    dimensiones_t1 = ["Adaptabilidad", "Agresividad", "Atipicidad", "Ansiedad", "Depresion", "Hiperactividad",
                      "Habilidades sociales", "Problemas de atencion", "Retraimiento", "Somatizacion"]
    dimensiones_t2 = ["Adaptabilidad", "Agresividad", "Atipicidad", "Ansiedad", "Depresion", "Hiperactividad",
                      "Habilidades sociales", "Problemas de atencion", "Retraimiento", "Somatizacion",
                      "Problemas de conducta", "Liderazgo", "Problemas de aprendizaje", "Habilidades para el estudio"]
    dimensiones_t3 = ["Agresividad", "Atipicidad", "Ansiedad", "Depresion", "Hiperactividad",
                      "Habilidades sociales", "Problemas de atencion", "Retraimiento", "Somatizacion",
                      "Problemas de conducta", "Liderazgo", "Problemas de aprendizaje", "Habilidades para el estudio"]
    dimensiones_s2 = ["Locus de control", "Atipicidad", "Ansiedad", "Depresion", "Estres social",
                      "Sentido de incapacidad","Relaciones interpersonales", "Relaciones con los padres",
                      "Autoestima", "Confianza en si mismo", "Actitud negativa hacia el colegio",
                      "Actitud negativa hacia los profesores"]
    dimensiones_s3 = ["Locus de control", "Somatizacion", "Atipicidad", "Ansiedad", "Depresion", "Estres social",
                      "Sentido de incapacidad","Relaciones interpersonales", "Relaciones con los padres",
                      "Autoestima", "Confianza en si mismo", "Actitud negativa hacia el colegio",
                      "Actitud negativa hacia los profesores", "Busqueda de sensaciones"]
    if prueba == "P1":
        for x in dimensiones_p1:
            get_niveles(df_final, x)
    elif prueba == "P2":
        for x in dimensiones_p2:
            get_niveles(df_final, x)
    elif prueba == "P3":
        for x in dimensiones_p3:
            get_niveles(df_final, x)
    elif prueba == "T1":
        for x in dimensiones_t1:
            get_niveles(df_final, x)
    elif prueba == "T2":
        for x in dimensiones_t2:
            get_niveles(df_final, x)
    elif prueba == "T3":
        for x in dimensiones_t3:
            get_niveles(df_final, x)
    elif prueba == "S2":
        for x in dimensiones_s2:
            get_niveles(df_final, x)
    elif prueba == "S3":
        for x in dimensiones_s3:
            get_niveles(df_final, x)


# Se obtiene la nota T de las personas de acuerdo a su puntaje en una dimensión
def puntaje_p1(valores, edades, baremos, columna_comparar, columna_recuperar):
    resultado = []

    for j in range(len(valores)):
        #df2 = pd.read_pickle('baremos/P1_Gral_3_4.pkl')
        if baremos[j] == "General" and edades[j] < 5:
            df2 = pd.read_pickle('baremos/P1_Gral_3_4.pkl')

        elif baremos[j] == "Mujeres" and edades[j] < 5:
            df2 = pd.read_pickle('baremos/P1_Muj_3_4.pkl')

        elif baremos[j] == "Varones" and edades[j] < 5:
            df2 = pd.read_pickle('baremos/P1_Var_3_4.pkl')

        elif baremos[j] == "General" and edades[j] < 7:
            df2 = pd.read_pickle('baremos/P1_Gral_5_6.pkl')

        elif baremos[j] == "Varones" and edades[j] < 7:
            df2 = pd.read_pickle('baremos/P1_Var_5_6.pkl')

        elif baremos[j] == "Mujeres" and edades[j] < 7:
            df2 = pd.read_pickle('baremos/P1_Muj_5_6.pkl')

        df2 = df2.loc[:, [columna_recuperar, columna_comparar]]
        df2 = df2.dropna()
        sintomas = df2.loc[:, columna_comparar].values.tolist()
        sintomas = sorted(sintomas)
        pc = df2.loc[:, columna_recuperar].values.tolist()
        pc = sorted(pc)
        i = bisect.bisect_left(sintomas, valores[j])
        resultado.append(int(pc[i]))
    return resultado


def puntaje_p2(valores, edades, baremos, columna_comparar, columna_recuperar):
    resultado = []
    for j in range(len(valores)):

        if baremos[j] == "General" and edades[j] < 9:
            df2 = pd.read_pickle('baremos/P2_Gral_6_8.pkl')

        elif baremos[j] == "Mujeres" and edades[j] < 9:
            df2 = pd.read_pickle('baremos/P2_Muj_6_8.pkl')

        elif baremos[j] == "Varones" and edades[j] < 9:
            df2 = pd.read_pickle('baremos/P2_Var_6_8.pkl')

        elif baremos[j] == "General" and edades[j] < 13:
            df2 = pd.read_pickle('baremos/P2_Gral_8_12.pkl')

        elif baremos[j] == "Varones" and edades[j] < 13:
            df2 = pd.read_pickle('baremos/P2_Var_9_12.pkl')

        elif baremos[j] == "Mujeres" and edades[j] < 13:
            df2 = pd.read_pickle('baremos/P2_Muj_9_12.pkl')

        df2 = df2.loc[:, [columna_recuperar, columna_comparar]]
        df2 = df2.dropna()
        sintomas = df2.loc[:, columna_comparar].values.tolist()
        sintomas = sorted(sintomas)
        pc = df2.loc[:, columna_recuperar].values.tolist()
        pc = sorted(pc)
        i = bisect.bisect_left(sintomas, valores[j])
        resultado.append(int(pc[i]))
    return resultado


def puntaje_p3(valores, edades, baremos, columna_comparar, columna_recuperar):
    resultado = []
    for j in range(len(valores)):

        if baremos[j] == "General" and edades[j] < 15:
            df2 = pd.read_pickle('baremos/P3_Gral_12_14.pkl')

        elif baremos[j] == "Mujeres" and edades[j] < 15:
            df2 = pd.read_pickle('baremos/P3_Muj_12_14.pkl')

        elif baremos[j] == "Varones" and edades[j] < 15:
            df2 = pd.read_pickle('baremos/P3_Var_12_14.pkl')

        elif baremos[j] == "General" and edades[j] < 17:
            df2 = pd.read_pickle('baremos/P3_Gral_15_16.pkl')

        elif baremos[j] == "Varones" and edades[j] < 17:
            df2 = pd.read_pickle('baremos/P3_Var_15_16.pkl')

        elif baremos[j] == "Mujeres" and edades[j] < 17:
            df2 = pd.read_pickle('baremos/P3_Muj_15_16.pkl')

        elif baremos[j] == "General" and edades[j] < 19:
            df2 = pd.read_pickle('baremos/P3_Gral_17_18.pkl')

        elif baremos[j] == "Varones" and edades[j] < 19:
            df2 = pd.read_pickle('baremos/P3_Var_17_18.pkl')

        elif baremos[j] == "Mujeres" and edades[j] < 19:
            df2 = pd.read_pickle('baremos/P3_Muj_17_18.pkl')

        df2 = df2.loc[:, [columna_recuperar, columna_comparar]]
        df2 = df2.dropna()
        sintomas = df2.loc[:, columna_comparar].values.tolist()
        sintomas = sorted(sintomas)
        pc = df2.loc[:, columna_recuperar].values.tolist()
        pc = sorted(pc)
        i = bisect.bisect_left(sintomas, valores[j])
        resultado.append(int(pc[i]))
    return resultado


def puntaje_s2(valores, edades, baremos, columna_comparar, columna_recuperar):
    resultado = []
    for j in range(len(valores)):

        if baremos[j] == "General" and edades[j] < 11:
            df2 = pd.read_pickle('baremos/S2_Gral_8_10.pkl')

        elif baremos[j] == "Mujeres" and edades[j] < 11:
            df2 = pd.read_pickle('baremos/S2_Muj_8_10.pkl')

        elif baremos[j] == "Varones" and edades[j] < 11:
            df2 = pd.read_pickle('baremos/S2_Var_8_10.pkl')

        elif baremos[j] == "General" and edades[j] < 13:
            df2 = pd.read_pickle('baremos/S2_Gral_11_12.pkl')

        elif baremos[j] == "Varones" and edades[j] < 13:
            df2 = pd.read_pickle('baremos/S2_Var_11_12.pkl')

        elif baremos[j] == "Mujeres" and edades[j] < 13:
            df2 = pd.read_pickle('baremos/S2_Muj_11_12.pkl')

        df2 = df2.loc[:, [columna_recuperar, columna_comparar]]
        df2 = df2.dropna()
        sintomas = df2.loc[:, columna_comparar].values.tolist()
        sintomas = sorted(sintomas)
        pc = df2.loc[:, columna_recuperar].values.tolist()
        pc = sorted(pc)
        i = bisect.bisect_left(sintomas, valores[j])
        resultado.append(int(pc[i]))
    return resultado


def puntaje_s3(valores, edades, baremos, columna_comparar, columna_recuperar):
    resultado = []
    for j in range(len(valores)):

        if baremos[j] == "General" and edades[j] < 15:
            df2 = pd.read_pickle('baremos/S3_Gral_12_14.pkl')

        elif baremos[j] == "Mujeres" and edades[j] < 15:
            df2 = pd.read_pickle('baremos/S3_Muj_12_14.pkl')

        elif baremos[j] == "Varones" and edades[j] < 15:
            df2 = pd.read_pickle('baremos/S3_Var_12_14.pkl')

        elif baremos[j] == "General" and edades[j] < 17:
            df2 = pd.read_pickle('baremos/S3_Gral_15_16.pkl')

        elif baremos[j] == "Varones" and edades[j] < 17:
            df2 = pd.read_pickle('baremos/S3_Var_15_16.pkl')

        elif baremos[j] == "Mujeres" and edades[j] < 17:
            df2 = pd.read_pickle('baremos/S3_Muj_15_16.pkl')

        elif baremos[j] == "General" and edades[j] < 19:
            df2 = pd.read_pickle('baremos/S3_Gral_17_18.pkl')

        elif baremos[j] == "Varones" and edades[j] < 19:
            df2 = pd.read_pickle('baremos/S3_Var_17_18.pkl')

        elif baremos[j] == "Mujeres" and edades[j] < 19:
            df2 = pd.read_pickle('baremos/S3_Muj_17_18.pkl')

        df2 = df2.loc[:, [columna_recuperar, columna_comparar]]
        df2 = df2.dropna()
        sintomas = df2.loc[:, columna_comparar].values.tolist()
        sintomas = sorted(sintomas)
        pc = df2.loc[:, columna_recuperar].values.tolist()
        pc = sorted(pc)
        i = bisect.bisect_left(sintomas, valores[j])
        resultado.append(int(pc[i]))
    return resultado


def puntaje_T1(valores, edades, baremos, columna_comparar, columna_recuperar):
    resultado = []
    for j in range(len(valores)):

        if baremos[j] == "General" and edades[j] < 5:
            df2 = pd.read_pickle('baremos/T1_Gral_3_4.pkl')

        elif baremos[j] == "Mujeres" and edades[j] < 5:
            df2 = pd.read_pickle('baremos/T1_Muj_3_4.pkl')

        elif baremos[j] == "Varones" and edades[j] < 5:
            df2 = pd.read_pickle('baremos/T1_Var_3_4.pkl')

        elif baremos[j] == "General" and edades[j] < 7:
            df2 = pd.read_pickle('baremos/T1_Gral_5_6.pkl')

        elif baremos[j] == "Varones" and edades[j] < 7:
            df2 = pd.read_pickle('baremos/T1_Var_5_6.pkl')

        elif baremos[j] == "Mujeres" and edades[j] < 7:
            df2 = pd.read_pickle('baremos/T1_Muj_5_6.pkl')

        df2 = df2.loc[:, [columna_recuperar, columna_comparar]]
        df2 = df2.dropna()
        sintomas = df2.loc[:, columna_comparar].values.tolist()
        sintomas = sorted(sintomas)
        pc = df2.loc[:, columna_recuperar].values.tolist()
        pc = sorted(pc)
        i = bisect.bisect_left(sintomas, valores[j])
        resultado.append(int(pc[i]))
    return resultado


def puntaje_t2(valores, edades, baremos, columna_comparar, columna_recuperar):
    resultado = []
    for j in range(len(valores)):

        if baremos[j] == "General" and edades[j] < 9:
            df2 = pd.read_pickle('baremos/T2_Gral_6_8.pkl')

        elif baremos[j] == "Mujeres" and edades[j] < 9:
            df2 = pd.read_pickle('baremos/T2_Muj_6_8.pkl')

        elif baremos[j] == "Varones" and edades[j] < 9:
            df2 = pd.read_pickle('baremos/T2_Var_6_8.pkl')

        elif baremos[j] == "General" and edades[j] < 13:
            df2 = pd.read_pickle('baremos/T2_Gral_9_12.pkl')

        elif baremos[j] == "Varones" and edades[j] < 13:
            df2 = pd.read_pickle('baremos/T2_Var_9_12.pkl')

        elif baremos[j] == "Mujeres" and edades[j] < 13:
            df2 = pd.read_pickle('baremos/T2_Muj_9_12.pkl')

        df2 = df2.loc[:, [columna_recuperar, columna_comparar]]
        df2 = df2.dropna()
        sintomas = df2.loc[:, columna_comparar].values.tolist()
        sintomas = sorted(sintomas)
        pc = df2.loc[:, columna_recuperar].values.tolist()
        pc = sorted(pc)
        i = bisect.bisect_left(sintomas, valores[j])
        resultado.append(int(pc[i]))
    return resultado


def puntaje_t3(valores, edades, baremos, columna_comparar, columna_recuperar):
    resultado = []
    for j in range(len(valores)):

        if baremos[j] == "General" and edades[j] < 15:
            df2 = pd.read_pickle('baremos/T3_Gral_12_14.pkl')

        elif baremos[j] == "Mujeres" and edades[j] < 15:
            df2 = pd.read_pickle('baremos/T3_Muj_12_14.pkl')

        elif baremos[j] == "Varones" and edades[j] < 15:
            df2 = pd.read_pickle('baremos/T3_Var_12_14.pkl')

        elif baremos[j] == "General" and edades[j] < 17:
            df2 = pd.read_pickle('baremos/T3_Gral_15_16.pkl')

        elif baremos[j] == "Varones" and edades[j] < 17:
            df2 = pd.read_pickle('baremos/T3_Var_15_16.pkl')

        elif baremos[j] == "Mujeres" and edades[j] < 17:
            df2 = pd.read_pickle('baremos/T3_Muj_15_16.pkl')

        elif baremos[j] == "General" and edades[j] < 19:
            df2 = pd.read_pickle('baremos/T3_Gral_17_18.pkl')

        elif baremos[j] == "Varones" and edades[j] < 19:
            df2 = pd.read_pickle('baremos/T3_Var_17_18.pkl')

        elif baremos[j] == "Mujeres" and edades[j] < 19:
            df2 = pd.read_pickle('baremos/T3_Muj_17_18.pkl')

        df2 = df2.loc[:, [columna_recuperar, columna_comparar]]
        df2 = df2.dropna()
        sintomas = df2.loc[:, columna_comparar].values.tolist()
        sintomas = sorted(sintomas)
        pc = df2.loc[:, columna_recuperar].values.tolist()
        pc = sorted(pc)
        i = bisect.bisect_left(sintomas, valores[j])
        resultado.append(int(pc[i]))
    return resultado


def get_value_t(df, bare):
    edad1 = df.loc[:, 'Edad'].values.tolist()
    baremo1 = [bare, ]
    agresividad = df.loc[:, 'PD Agresividad'].values.tolist()
    adaptabilidad = df.loc[:, 'PD Adaptabilidad'].values.tolist()
    ansiedad = df.loc[:, 'PD Ansiedad'].values.tolist()
    atipicidad = df.loc[:, 'PD Atipicidad'].values.tolist()
    depresion = df.loc[:, 'PD Depresion'].values.tolist()
    hiperactividad = df.loc[:, 'PD Hiperactividad'].values.tolist()
    habilidades_sociales = df.loc[:, 'PD Habilidades sociales'].values.tolist()
    problemas_atencion = df.loc[:, 'PD Problemas de atencion'].values.tolist()
    retraimiento = df.loc[:, 'PD Retraimiento'].values.tolist()
    somatizacion = df.loc[:, 'PD Somatizacion'].values.tolist()

    puntaje_t = {
        "T Agresividad": puntaje_p1(agresividad, edades=edad1, baremos=baremo1, columna_comparar='PD',
                                    columna_recuperar='T Agresividad'),
        "T Adaptabilidad": puntaje_p1(adaptabilidad, edades=edad1, baremos=baremo1, columna_comparar='PD',
                                      columna_recuperar='T Adaptabilidad'),
        "T Ansiedad": puntaje_p1(ansiedad, edades=edad1, baremos=baremo1, columna_comparar='PD',
                                 columna_recuperar='T Ansiedad'),
        "T Atipicidad": puntaje_p1(atipicidad, edades=edad1, baremos=baremo1, columna_comparar='PD',
                                   columna_recuperar='T Atipicidad'),
        "T Depresion": puntaje_p1(depresion, edades=edad1, baremos=baremo1, columna_comparar='PD',
                                  columna_recuperar='T Depresión'),
        "T Hiperactividad": puntaje_p1(hiperactividad, edades=edad1, baremos=baremo1, columna_comparar='PD',
                                       columna_recuperar='T Hiperactividad'),
        "T Habilidades sociales": puntaje_p1(habilidades_sociales, edades=edad1, baremos=baremo1, columna_comparar='PD',
                                             columna_recuperar='T Habilidades sociales'),
        "T Problemas de atencion": puntaje_p1(problemas_atencion, edades=edad1, baremos=baremo1, columna_comparar='PD',
                                              columna_recuperar='T Problemas de atención'),
        "T Retraimiento": puntaje_p1(retraimiento, edades=edad1, baremos=baremo1, columna_comparar='PD',
                                     columna_recuperar='T Retraimiento'),
        "T Somatizacion": puntaje_p1(somatizacion, edades=edad1, baremos=baremo1, columna_comparar='PD',
                                     columna_recuperar='T Somatización'),
    }
    df_t = pd.DataFrame(puntaje_t)
    return df_t


# Transforma los valores de texto a numeros (se podría cambiar por la función map
"""
def recodifica_var(df_columns):
    # print(df.iloc[:,1].map({"Nunca":0, "Alguna vez":1, "Frecuentemente":2,"Casi siempre":3}))
    for i in range(df_columns):
        df.iloc[:, i] = df.iloc[:, i].apply(transforma_a_numero)
    return df
"""


# Se obtiene la edad de una persona según el calendario gregoriano
def date_diff(date1, date2):
    return (date1 - date2).days / 365.2425


def cargar_dataframe(url1):
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRrEpOBKtTnticMTM5BSb2MbsMpkU9hkaAVIjNhUz" \
          "-cWbMEvAINexTz7aL1ql0rfYGBcT0PQxh88MyC/pubhtml?gid=74737359&single=true "

    # Se lee la página web, el argumento header=1 indica que el nombre de las columnas está en la segunda fila
    # El encoding="UTF-8" asegura que se reconozca los acentos y la ñ
    tablas = pd.read_html(url1, header=1, encoding="UTF-8")
    df = tablas[0]
    return df


def dataframe_calculos_iniciales(url2):
    # Se declara la url de la cual se va a leer los datos
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRrEpOBKtTnticMTM5BSb2MbsMpkU9hkaAVIjNhUz" \
          "-cWbMEvAINexTz7aL1ql0rfYGBcT0PQxh88MyC/pubhtml?gid=74737359&single=true "
    df = cargar_dataframe(url2)
    df_info = df.iloc[1:, :8]

    # Convertir a formato datetime

    df_info['Fecha de nacimiento'] = pd.to_datetime(df_info['Fecha de nacimiento'], infer_datetime_format=True)
    df_info['Fecha'] = pd.to_datetime(df_info['Fecha'], infer_datetime_format=True)

    df_info['Fecha de nacimiento'] = pd.to_datetime(df_info['Fecha de nacimiento'], infer_datetime_format=True)
    df_info['Fecha'] = pd.to_datetime(df_info['Fecha'], infer_datetime_format=True)

    # Calculamos la edad
    df_info['dias'] = (df_info['Fecha'] - df_info['Fecha de nacimiento']).dt.days
    df_info['Edad'] = df_info['dias'] / 365.2425
    df_info['Edad'] = df_info['Edad'].astype(int)

    # Añadimos la columna baremo en función del sexo de la persona mediante map
    df_info['Baremo'] = df_info['Sexo'].map({'Varón': 'Varones',
                                             'Mujer': 'Mujeres'})

    # Se selecciona solo las columnas de los items
    df = df.iloc[1:, 8:]

    # Se recodifican todas las columnas
    for i in range(len(df.columns)):
        df.iloc[:, i] = df.iloc[:, i].apply(transforma_a_numero)
    # df = recodifica_var(len(df.columns))

    df1 = pd.concat([df_info, df], axis=1)
    return df1


def dataframe_p2():
    # Se declara la url de la cual se va a leer los datos

    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQ7vGtlwPr73WmlOAKR3lK4223ytE9mQzodJJtABdyewRjeLpc91aJv" \
          "-9MeGPEzIsJoBfYFG1h_HXJG/pubhtml "
    df = dataframe_calculos_iniciales(url)
    # df = recodifica_var(len(df.columns))
    df_info = df.iloc[:, :11]
    df = df.iloc[:, 11:]
    # Se calculan los puntajes directos
    puntaje_directo = {
        "PD Agresividad": df.iloc[:, 1] + df.iloc[:, 20] + df.iloc[:, 28] + df.iloc[:, 31] + df.iloc[:, 42] \
                          + df.iloc[:, 53] + df.iloc[:, 65] + df.iloc[:, 77] + df.iloc[:, 88] + df.iloc[:, 98]
                          + df.iloc[:, 110] + df.iloc[:, 121] + df.iloc[:, 130],
        "PD Adaptabilidad": df.iloc[:, 0] + df.iloc[:, 30] + (3 - df.iloc[:, 41]) + df.iloc[:, 64] + \
                            df.iloc[:, 76] + df.iloc[:, 97] + df.iloc[:, 109] + df.iloc[:, 129],
        "PD Ansiedad": df.iloc[:, 2] + df.iloc[:, 43] + df.iloc[:, 54] + df.iloc[:, 66] + df.iloc[:, 78] \
                       + df.iloc[:, 99] + df.iloc[:, 111],
        "PD Atipicidad": df.iloc[:, 4] + df.iloc[:, 12] + df.iloc[:, 22] + df.iloc[:, 33] + df.iloc[:, 45] \
                         + df.iloc[:, 55] + df.iloc[:, 68] + df.iloc[:, 80] + df.iloc[:, 89] + df.iloc[:, 101]
                         + df.iloc[:, 113] + df.iloc[:, 122],
        "PD Depresion": df.iloc[:, 5] + df.iloc[:, 14] + df.iloc[:, 23] + df.iloc[:, 35] + df.iloc[:, 47] \
                        + df.iloc[:, 57] + df.iloc[:, 70] + df.iloc[:, 82] + df.iloc[:, 91] + df.iloc[:, 103]
                        + df.iloc[:, 115] + df.iloc[:, 124],
        "PD Hiperactividad": df.iloc[:, 15] + df.iloc[:, 36] + df.iloc[:, 48] + df.iloc[:, 58] + df.iloc[:,71] \
                             + df.iloc[:, 83] + df.iloc[:, 104] + df.iloc[:, 116] + df.iloc[:, 132],
        "PD Habilidades sociales": df.iloc[:, 7] + df.iloc[:, 17] + df.iloc[:, 26] + df.iloc[:, 38] + df.iloc[:, 50]\
                                   + df.iloc[:, 60] + df.iloc[:, 73] + df.iloc[:, 85] + df.iloc[:, 94] + df.iloc[:, 96]
                                   + df.iloc[:, 106] + df.iloc[:, 118] + df.iloc[:, 126] + df.iloc[:, 128],
        "PD Problemas de atencion": (3 - df.iloc[:, 3]) + df.iloc[:, 32] + df.iloc[:, 44] + df.iloc[:, 67] + \
                                    (3 - df.iloc[:, 79]) + (3 -df.iloc[:, 100]) + (3 -df.iloc[:, 112]),
        "PD Retraimiento": (3 -df.iloc[:, 9]) + df.iloc[:, 19] + df.iloc[:, 40] + df.iloc[:, 52] + df.iloc[:, 75]\
                           + df.iloc[:, 87] + df.iloc[:, 108] + df.iloc[:, 120] + df.iloc[:, 133],
        "PD Somatizacion": df.iloc[:, 8] + df.iloc[:, 18] + df.iloc[:, 27] + df.iloc[:, 39] + df.iloc[:, 51] \
                           + df.iloc[:, 61] + df.iloc[:, 63] + df.iloc[:, 74] + df.iloc[:, 86] + df.iloc[:, 95]
                           + df.iloc[:, 107] + df.iloc[:, 119] + df.iloc[:, 127],
        "PD Problemas de conducta": df.iloc[:, 13] + df.iloc[:, 34] + df.iloc[:, 46] + df.iloc[:, 102] + df.iloc[:, 56] \
                           + df.iloc[:, 69] + df.iloc[:, 81] + df.iloc[:, 90] + df.iloc[:, 114] + df.iloc[:, 131],
        "PD Liderazgo": df.iloc[:, 6] + df.iloc[:, 16] + df.iloc[:, 37] + df.iloc[:, 49] + df.iloc[:, 59] \
                           + df.iloc[:, 72] + df.iloc[:, 84] + df.iloc[:, 93] + df.iloc[:, 105] + df.iloc[:, 117],

    }

    # inicio=time.time()
    # Convertir a lista los baremos, edad y los puntajes directos de cada dimensión
    baremo1 = df_info['Baremo'].values.tolist()
    edad1 = df_info['Edad'].values.tolist()

    df_puntaje = pd.DataFrame(puntaje_directo)
    adaptabilidad = df_puntaje['PD Adaptabilidad'].values.tolist()
    agresividad = df_puntaje['PD Agresividad'].values.tolist()
    ansiedad = df_puntaje['PD Ansiedad'].values.tolist()
    atipicidad = df_puntaje['PD Atipicidad'].values.tolist()
    depresion = df_puntaje['PD Depresion'].values.tolist()
    hiperactividad = df_puntaje['PD Hiperactividad'].values.tolist()
    habilidades_sociales = df_puntaje['PD Habilidades sociales'].values.tolist()
    problemas_atencion = df_puntaje['PD Problemas de atencion'].values.tolist()
    retraimiento = df_puntaje['PD Retraimiento'].values.tolist()
    somatizacion = df_puntaje['PD Somatizacion'].values.tolist()
    problemas_conducta = df_puntaje['PD Problemas de conducta'].values.tolist()
    liderazgo = df_puntaje['PD Liderazgo'].values.tolist()

    # Declarar una variable para los valores de una columna en base a la funcion puntaje_p1
    somatizacion_valores = puntaje_p2(somatizacion, edades=edad1, baremos=baremo1, columna_comparar='PD',
                                      columna_recuperar='T Somatización')

    # Crear un diccionario con el nombre de las columnas y los puntajes T
    puntaje_T = {
        "T Agresividad": puntaje_p2(agresividad, edades=edad1, baremos=baremo1, columna_comparar='PD',
                                    columna_recuperar='T Agresividad'),
        "T Adaptabilidad": puntaje_p2(adaptabilidad, edades=edad1, baremos=baremo1, columna_comparar='PD',
                                      columna_recuperar='T Adaptabilidad'),
        "T Ansiedad": puntaje_p2(ansiedad, edades=edad1, baremos=baremo1, columna_comparar='PD',
                                 columna_recuperar='T Ansiedad'),
        "T Atipicidad": puntaje_p2(atipicidad, edades=edad1, baremos=baremo1, columna_comparar='PD',
                                   columna_recuperar='T Atipicidad'),
        "T Depresion": puntaje_p2(depresion, edades=edad1, baremos=baremo1, columna_comparar='PD',
                                  columna_recuperar='T Depresión'),
        "T Hiperactividad": puntaje_p2(hiperactividad, edades=edad1, baremos=baremo1, columna_comparar='PD',
                                       columna_recuperar='T Hiperactividad'),
        "T Habilidades sociales": puntaje_p2(habilidades_sociales, edades=edad1, baremos=baremo1, columna_comparar='PD',
                                             columna_recuperar='T Habilidades sociales'),
        "T Problemas de atencion": puntaje_p2(problemas_atencion, edades=edad1, baremos=baremo1, columna_comparar='PD',
                                              columna_recuperar='T Problemas de atención'),
        "T Retraimiento": puntaje_p2(retraimiento, edades=edad1, baremos=baremo1, columna_comparar='PD',
                                     columna_recuperar='T Retraimiento'),
        "T Somatizacion": somatizacion_valores,
        "T Problemas de conducta": puntaje_p2(problemas_conducta, edades=edad1, baremos=baremo1, columna_comparar='PD',
                                     columna_recuperar='T Problemas de conducta'),
        "T Liderazgo": puntaje_p2(liderazgo, edades=edad1, baremos=baremo1, columna_comparar='PD',
                                     columna_recuperar='T Liderazgo'),
    }
    # Se convierte a dataframe el diccionario creado anteriormente
    df_T = pd.DataFrame(puntaje_T)
    # print(time.time()-inicio)

    # Se resetea los indices de todos los dataframes
    df_info = df_info.reset_index(drop=True)
    df = df.reset_index(drop=True)
    df_puntaje = df_puntaje.reset_index(drop=True)
    df_T = df_T.reset_index(drop=True)
    df_info_filtrado = df_info.loc[:, ['1', 'Nombre y apellido', 'Edad', 'Baremo']]
    # Se unen todos los dataframes
    df_final = pd.concat([df_info_filtrado, df_puntaje, df_T], axis=1)
    prueba = "P2"
    # Se generan las columnas de los niveles basados en el puntaje T con la funcion niveles_all()
    niveles_all(df_final, prueba="P2")
    df_final.iloc[:, 0] = df_final.iloc[:, 0].map(int)
    df_final.rename(columns={'1': 'Id'}, inplace=True)
    df_final = df_final.reindex(columns=['Id', 'Nombre y apellido', 'Edad', 'Baremo',
                                         'PD Agresividad', 'T Agresividad', 'Nivel Agresividad',
                                         'PD Adaptabilidad', 'T Adaptabilidad', 'Nivel Adaptabilidad',
                                         'PD Ansiedad', 'T Ansiedad', 'Nivel Ansiedad',
                                         'PD Atipicidad', 'T Atipicidad', 'Nivel Atipicidad',
                                         'PD Depresion', 'T Depresion', 'Nivel Depresion',
                                         'PD Hiperactividad', 'T Hiperactividad', 'Nivel Hiperactividad',
                                         'PD Habilidades sociales', 'T Habilidades sociales',
                                         'Nivel Habilidades sociales',
                                         'PD Problemas de atencion', 'T Problemas de atencion',
                                         'Nivel Problemas de atencion',
                                         'PD Retraimiento', 'T Retraimiento', 'Nivel Retraimiento',
                                         'PD Somatizacion', 'T Somatizacion', 'Nivel Somatizacion',
                                         'PD Problemas de conducta', 'T Problemas de conducta', 'Nivel Problemas de conducta',
                                         'PD Liderazgo', 'T Liderazgo', 'Nivel Liderazgo'])
    # Guardar en csv
    # df_final.to_csv('resultados1.csv', encoding='utf-8')
    return df_final


def dataframe_p1():
    # Se declara la url de la cual se va a leer los datos
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRrEpOBKtTnticMTM5BSb2MbsMpkU9hkaAVIjNhUz" \
          "-cWbMEvAINexTz7aL1ql0rfYGBcT0PQxh88MyC/pubhtml?gid=74737359&single=true "
    df = dataframe_calculos_iniciales(url)
    # df = recodifica_var(len(df.columns))
    df_info = df.iloc[:, :11]
    df = df.iloc[:, 11:]
    # Se calculan los puntajes directos
    puntaje_directo = {
        "PD Agresividad": df.iloc[:, 1] + df.iloc[:, 11] + df.iloc[:, 19] + df.iloc[:, 27] + df.iloc[:, 31]\
                          + df.iloc[:,42] + df.iloc[:,52] + df.iloc[:,64] + df.iloc[:,75] + df.iloc[:,85] \
                          + df.iloc[:,96] + df.iloc[:,105] + df.iloc[:,115],
        "PD Adaptabilidad": df.iloc[:, 0] + (3 - df.iloc[:, 10]) + (3 - df.iloc[:, 30]) + df.iloc[:, 41]\
                            + df.iloc[:,63] + df.iloc[:,74] + df.iloc[:,84] + (3 - df.iloc[:, 95]) + df.iloc[:, 104]\
                            + df.iloc[:, 114] + df.iloc[:, 125],
        "PD Ansiedad": df.iloc[:, 20] + df.iloc[:, 32] + df.iloc[:, 43] + df.iloc[:, 53] + df.iloc[:, 65] \
                       + df.iloc[:,76] + df.iloc[:, 86] + df.iloc[:, 106] + df.iloc[:, 116],
        "PD Atipicidad": df.iloc[:, 3] + df.iloc[:, 13] + df.iloc[:, 21] + df.iloc[:, 34] + df.iloc[:, 45] \
                         + df.iloc[:, 54] + df.iloc[:, 67] + df.iloc[:, 78] + df.iloc[:, 87] + df.iloc[:, 108] \
                         + df.iloc[:, 117],
        "PD Depresion": df.iloc[:, 4] + df.iloc[:, 14] + df.iloc[:, 22] + df.iloc[:, 35] + df.iloc[:, 46]\
                        + df.iloc[:,55] + df.iloc[:, 60] + df.iloc[:, 68] + df.iloc[:, 79] + df.iloc[:, 88] \
                        + df.iloc[:, 98] + df.iloc[:, 109] + df.iloc[:, 118],
        "PD Hiperactividad": df.iloc[:, 5] + df.iloc[:, 15] + df.iloc[:, 23] + df.iloc[:, 28] + df.iloc[:, 36] \
                             + df.iloc[:, 47] + df.iloc[:, 56] + df.iloc[:, 61] + df.iloc[:, 69] + df.iloc[:, 80]\
                             + df.iloc[:, 93] + df.iloc[:, 99] + df.iloc[:, 110] + df.iloc[:, 119] + df.iloc[:, 124]\
                             + df.iloc[:, 127],
        "PD Habilidades sociales": df.iloc[:, 6] + df.iloc[:, 16] + df.iloc[:, 24] + df.iloc[:, 37] + df.iloc[:, 48]\
                                   + df.iloc[:, 57] + df.iloc[:, 70] + df.iloc[:, 81] + df.iloc[:, 90]\
                                   + df.iloc[:, 100]+ df.iloc[:, 111] + df.iloc[:, 120] + df.iloc[:, 123]\
                                   + df.iloc[:, 129],
        "PD Problemas de atencion": df.iloc[:, 2] + (3 - df.iloc[:, 33]) + df.iloc[:, 44] + df.iloc[:, 66]\
                                    + df.iloc[:, 77] + df.iloc[:, 97] + df.iloc[:, 107] + df.iloc[:, 126],
        "PD Retraimiento": df.iloc[:, 8] + df.iloc[:, 39] + df.iloc[:, 50] + df.iloc[:, 59] + df.iloc[:, 72]\
                           + df.iloc[:, 83] + df.iloc[:, 92] + (3 - df.iloc[:, 102]) + df.iloc[:, 113] + \
                           df.iloc[:, 122] + df.iloc[:, 128],
        "PD Somatizacion": df.iloc[:, 7] + df.iloc[:, 17] + df.iloc[:, 25] + df.iloc[:, 29] + df.iloc[:, 38] \
                           + df.iloc[:, 49] + df.iloc[:, 58] + df.iloc[:, 62] + df.iloc[:, 71] + df.iloc[:, 82]\
                           + df.iloc[:, 91] + df.iloc[:, 101] + df.iloc[:, 112] + df.iloc[:, 121],

    }

    # inicio=time.time()
    # Convertir a lista los baremos, edad y los puntajes directos de cada dimensión
    baremo1 = df_info['Baremo'].values.tolist()
    edad1 = df_info['Edad'].values.tolist()
    df_puntaje = pd.DataFrame(puntaje_directo)
    adaptabilidad = df_puntaje['PD Adaptabilidad'].values.tolist()
    agresividad = df_puntaje['PD Agresividad'].values.tolist()
    ansiedad = df_puntaje['PD Ansiedad'].values.tolist()
    atipicidad = df_puntaje['PD Atipicidad'].values.tolist()
    depresion = df_puntaje['PD Depresion'].values.tolist()
    hiperactividad = df_puntaje['PD Hiperactividad'].values.tolist()
    habilidades_sociales = df_puntaje['PD Habilidades sociales'].values.tolist()
    problemas_atencion = df_puntaje['PD Problemas de atencion'].values.tolist()
    retraimiento = df_puntaje['PD Retraimiento'].values.tolist()
    somatizacion = df_puntaje['PD Somatizacion'].values.tolist()

    # Declarar una variable para los valores de una columna en base a la funcion puntaje_p1
    somatizacion_valores = puntaje_p1(somatizacion, edades=edad1, baremos=baremo1, columna_comparar='PD',
                                      columna_recuperar='T Somatización')

    # Crear un diccionario con el nombre de las columnas y los puntajes T
    puntaje_T = {
        "T Agresividad": puntaje_p1(agresividad, edades=edad1, baremos=baremo1, columna_comparar='PD',
                                    columna_recuperar='T Agresividad'),
        "T Adaptabilidad": puntaje_p1(adaptabilidad, edades=edad1, baremos=baremo1, columna_comparar='PD',
                                      columna_recuperar='T Adaptabilidad'),
        "T Ansiedad": puntaje_p1(ansiedad, edades=edad1, baremos=baremo1, columna_comparar='PD',
                                 columna_recuperar='T Ansiedad'),
        "T Atipicidad": puntaje_p1(atipicidad, edades=edad1, baremos=baremo1, columna_comparar='PD',
                                   columna_recuperar='T Atipicidad'),
        "T Depresion": puntaje_p1(depresion, edades=edad1, baremos=baremo1, columna_comparar='PD',
                                  columna_recuperar='T Depresión'),
        "T Hiperactividad": puntaje_p1(hiperactividad, edades=edad1, baremos=baremo1, columna_comparar='PD',
                                       columna_recuperar='T Hiperactividad'),
        "T Habilidades sociales": puntaje_p1(habilidades_sociales, edades=edad1, baremos=baremo1, columna_comparar='PD',
                                             columna_recuperar='T Habilidades sociales'),
        "T Problemas de atencion": puntaje_p1(problemas_atencion, edades=edad1, baremos=baremo1, columna_comparar='PD',
                                              columna_recuperar='T Problemas de atención'),
        "T Retraimiento": puntaje_p1(retraimiento, edades=edad1, baremos=baremo1, columna_comparar='PD',
                                     columna_recuperar='T Retraimiento'),
        "T Somatizacion": somatizacion_valores,
    }
    # Se convierte a dataframe el diccionario creado anteriormente
    df_T = pd.DataFrame(puntaje_T)
    # print(time.time()-inicio)

    # Se resetea los indices de todos los dataframes
    df_info = df_info.reset_index(drop=True)
    df = df.reset_index(drop=True)
    df_puntaje = df_puntaje.reset_index(drop=True)
    df_T = df_T.reset_index(drop=True)
    df_info_filtrado = df_info.loc[:, ['1', 'Nombre y apellido', 'Edad', 'Baremo']]
    # Se unen todos los dataframes
    df_final = pd.concat([df_info_filtrado, df_puntaje, df_T], axis=1)
    prueba = "P1"
    # Se generan las columnas de los niveles basados en el puntaje T con la funcion niveles_all()
    niveles_all(df_final)
    df_final.iloc[:, 0] = df_final.iloc[:, 0].map(int)
    df_final.rename(columns={'1': 'Id'}, inplace=True)
    df_final = df_final.reindex(columns=['Id', 'Nombre y apellido', 'Edad', 'Baremo',
                                         'PD Agresividad', 'T Agresividad', 'Nivel Agresividad',
                                         'PD Adaptabilidad', 'T Adaptabilidad', 'Nivel Adaptabilidad',
                                         'PD Ansiedad', 'T Ansiedad', 'Nivel Ansiedad',
                                         'PD Atipicidad', 'T Atipicidad', 'Nivel Atipicidad',
                                         'PD Depresion', 'T Depresion', 'Nivel Depresion',
                                         'PD Hiperactividad', 'T Hiperactividad', 'Nivel Hiperactividad',
                                         'PD Habilidades sociales', 'T Habilidades sociales',
                                         'Nivel Habilidades sociales',
                                         'PD Problemas de atencion', 'T Problemas de atencion',
                                         'Nivel Problemas de atencion',
                                         'PD Retraimiento', 'T Retraimiento', 'Nivel Retraimiento',
                                         'PD Somatizacion', 'T Somatizacion', 'Nivel Somatizacion'])
    # Guardar en csv
    # df_final.to_csv('resultados1.csv', encoding='utf-8')
    return df_final


def cambio_baremo_one_p1(df3, p1_id, baremo_p1):
    datos = df3['Id'] == p1_id
    dato_filtrado = df3[datos]
    if len(dato_filtrado) > 0:
        dat_valor_t = get_value_t(dato_filtrado, bare=baremo_p1)
        niveles_all(dat_valor_t)
        datos_gral = dato_filtrado.loc[:, ['Id', 'Nombre y apellido', 'Edad', 'Baremo',
                                           'PD Agresividad', 'PD Adaptabilidad',
                                           'PD Ansiedad', 'PD Atipicidad', 'PD Depresion',
                                           'PD Hiperactividad', 'PD Habilidades sociales',
                                           'PD Problemas de atencion', 'PD Retraimiento',
                                           'PD Somatizacion']]
        datos_gral = datos_gral.reset_index(drop=True)
        dat_valor_t = dat_valor_t.reset_index(drop=True)
        df_final_p1 = pd.concat([datos_gral, dat_valor_t], axis=1)

        df_final_p1.iloc[0, 3] = baremo_p1
        df_final_p1 = df_final_p1.reindex(columns=['Id', 'Nombre y apellido', 'Edad', 'Baremo',
                                                   'PD Agresividad', 'T Agresividad', 'Nivel Agresividad',
                                                   'PD Adaptabilidad', 'T Adaptabilidad', 'Nivel Adaptabilidad',
                                                   'PD Ansiedad', 'T Ansiedad', 'Nivel Ansiedad',
                                                   'PD Atipicidad', 'T Atipicidad', 'Nivel Atipicidad',
                                                   'PD Depresion', 'T Depresion', 'Nivel Depresion',
                                                   'PD Hiperactividad', 'T Hiperactividad', 'Nivel Hiperactividad',
                                                   'PD Habilidades sociales', 'T Habilidades sociales',
                                                   'Nivel Habilidades sociales',
                                                   'PD Problemas de atencion', 'T Problemas de atencion',
                                                   'Nivel Problemas de atencion',
                                                   'PD Retraimiento', 'T Retraimiento', 'Nivel Retraimiento',
                                                   'PD Somatizacion', 'T Somatizacion', 'Nivel Somatizacion'])

        df3.iloc[p1_id - 2, :] = df_final_p1.iloc[0, :]
    return df3


def p1_dict_one(df_gral, datos_cambiados, p1_id):
    datos = datos_cambiados['Id'] == p1_id
    dato_filtrado = df_gral[datos]
    if len(dato_filtrado) == 0:
        abort(404, description="Upss! Parece que hubo un error")
    dato_filtrado.columns = dato_filtrado.columns.str.replace(" ", "_")
    dato_dict = dato_filtrado.to_dict('records')
    return dato_dict


if __name__ == '__main__':
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQ7vGtlwPr73WmlOAKR3lK4223ytE9mQzodJJtABdyewRjeLpc91aJv-9MeGPEzIsJoBfYFG1h_HXJG/pubhtml "
    #df = cargar_dataframe(url)
    #df = dataframe_calculos_iniciales(url)
    #df = df.iloc[:, 11:]
    frame_p2 = dataframe_p1()
    """id_p1 = 3
    barem_p1 = "General"
    datos_finales = cambio_baremo_one_p1(frame_p1,id_p1, barem_p1)
    diccionario= p1_dict_one(frame_p1, datos_finales, id_p1)
    dato_filtrados.columns = dato_filtrados.columns.str.replace(" ", "_")
    dato_dict = dato_filtrados.to_dict('records')
    # print(datos_finales)
    # df_pic = pd.read_pickle("baremos/P1_Gral_3_4.pkl")
    # print(df_pic)"""
    print(frame_p2.columns)
    print(frame_p2.iloc[:, [3,4]])

