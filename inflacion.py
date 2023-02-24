# -----------------------------------------------Librerias------------------------------------------------

import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import geopandas as gpd
import plotly.express as px
from PIL import Image
import plotly.graph_objects as go


# --------------------------------------------Titulos----------------------------------------------------
APP_title = "INFLACIÓN ARGENTINA"
APP_sub_title = "origen: datos.gob.ar"
st.set_page_config(APP_title)
st.title(APP_title)
st.caption(APP_sub_title)
#Imagen
st.image("https://img.freepik.com/vector-premium/bandera-acuarela-argentina-ilustracion-trazo-pincel_97886-10157.jpg", width=800)


# ---------------------------------------Load DATA------------------------------------------------------

mundial= pd.read_csv(r"mundial.csv")
geomund = gpd.read_file(r"countries.geojson")
inflacion = pd.read_csv(r"indice-precios-al-consumidor-nivel-general-base-diciembre-2016-mensual.csv")
salarios = pd.read_csv(r"salarios.csv")
tipo_de_cambio = pd.read_csv(r"tipo_de_cambio.csv")
balanza_comercial = pd.read_excel(r"balanmensual.xls")
balanza_pagos = pd.read_csv(r"balanza_pagos.csv")
ipc = pd.read_csv(r"IPC2.csv",sep=",")

# Creamos las pestañas que dividen nuestra app

tabs = st.tabs(['ARG y el mundo','Argentina',"Variables influyentes", "Serie temporal"])



#------------------------------------------------------------------------Primer PESTAÑA: Arg y el mundo---------------------------------------------------------------------
tab_plots = tabs[0]

with tab_plots:
    st.write("""En este análisis vamos a tomar los datos a partir del 2016,
     y ver la relación entre algunas variables importantes y la inflación.""")
    
    st.markdown("""La inflación es el aumento generalizado del nivel de precios de una economía, 
    medida como la variación porcentual de dichos precios.""")


    def mapa_mundial(df,fecha):
        fig = px.choropleth(
            df, geojson=geomund, color=fecha,
            featureidkey="properties.ISO_A3", locations='Country Code',
            color_continuous_scale="Viridis",
            # range_color=(0,200),
            labels={fecha:"Inflacion anual(en %)", "Country Code":""},
            hover_name = 'Country Name',
            width=700,
            height=450,
        )
        return fig

    col=mundial.columns[5:]
    fecha = st.selectbox(
        'Selecciona el año a visualizar',
        col, 
        len(col)-1
        )

    st.plotly_chart(mapa_mundial(mundial,fecha))

    st.write("2022")

    image = Image.open('Arg_y_el_mundo_top.jpg')
    st.image(image, caption='Fuente : https://datosmacro.expansion.com/')



#-------------------------------------------------------------------------------SEGUNDA PESTAÑA: Argentina------------------------------------------------------------------------------------
tab_plots = tabs[1]

with tab_plots:

    # Colocamos el grafico de la evolucion de la inflacion
    fig = px.line(inflacion, x="indice_tiempo", y=inflacion["ipc_ng_nacional"]-100, markers=True, title='Evolucion de la inflación en Argentina (Base dic 2016)', 
                         labels={"indice_tiempo":"","y":"Inflación"}, template="plotly_dark")
    annotations = []
    # Source
    annotations.append(dict(xref='paper', yref='paper', x=0.5, y=-0.1,
                              xanchor='center', yanchor='top',
                              text='Fuente: datos.gob.ar',
                              font=dict(family='Arial',
                                        size=12,
                                        color='rgb(150,150,150)'),
                              showarrow=False))
    fig.update_layout(annotations=annotations)
    st.plotly_chart(fig)

    st.write("""La inflación en Argentina ha evidenciado una tendencia ascendente a lo largo de los últimos veinte años,
     llegando a niveles por encima del 90 % anual. En cambio, la gran mayoría de los países del mundo ha logrado mantener
      tasas relativamente bajas y estables. Así, Argentina permaneció catorce de los últimos dieciséis años entre las diez
       economías con mayor inflación y está a punto de unirse al pequeño club que enfrentó tasas superiores al 100 % en al 
       menos un año de la última década (Burkina Faso, Líbano, Sudán del Sur, Sudán del Norte, Venezuela y Zimbabue)""")
    # Grafico de la inflacion mes a mes
    fig2 = px.line(inflacion, x="indice_tiempo", y=inflacion["ipc_ng_nacional_tasa_variacion_mensual"]*100, title='Inflación mensual en %',  
                    markers=True,
                    labels={"indice_tiempo":"","ipc_ng_nacional_tasa_variacion_mensual":"Inflación var mensual"}, 
                    template="plotly_dark")
    annotations = []
    # Source
    annotations.append(dict(xref='paper', yref='paper', x=0.5, y=-0.1,
                              xanchor='center', yanchor='top',
                              text='Fuente: datos.gob.ar',
                              font=dict(family='Arial',
                                        size=12,
                                        color='rgb(150,150,150)'),
                              showarrow=False))
    fig2.update_layout(annotations=annotations)


    st.plotly_chart(fig2)

    st.write("""En este caso podemos ver como la inflación mensual en argentina fue aumentando poco a poco 
                llegando a extremos en los cuales se tiene una inflación mensual igual a la que tiene otro país en un año""")

    # Colocamos la tabla
    def tabla(df,fecha):
        df=df.round(2)
        df=df[["Regiones",fecha]].transpose()
        st.write("Inflacion Anual")
        st.write(df)

    def display_map(df,fecha):
        html = open("map.html","r",encoding="utf-8").read()
        st.components.v1.html(html,width=700, height=450)
        
#         map = folium.Map(location=[-36.375962, -65.287933], zoom_start = 3  )
#         choropleth = folium.Choropleth(
#             geo_data=gpd.read_file(r"RegionesArgentina.geojson"),
#             data = df,
#             columns = ("Regiones","2017","2018","2019","2020","2021","2022"),
#             key_on= "feature.properties.index",
#             line_opacity=0.8,
#             highlight=True
#         )
#         choropleth.geojson.add_to(map)

#         for feature in choropleth.geojson.data["features"]:
#             Regiones = feature["properties"]["index"]
#             feature["properties"]["IPC"] = "IPC acumulado: " + str(df.loc[df["Regiones"]==Regiones,fecha])

#         choropleth.geojson.add_child(
#             folium.features.GeoJsonTooltip(["index"], labels=False)
#         )
#         st_map = st_folium(map,width=700, height=450)
    



    def main():

        #Load DATA
        geo = gpd.read_file(r"RegionesArgentina.geojson")
        inflacionmap = pd.read_csv(r"inflacionTT.csv")
        inflacionmes = pd.read_csv(r"inflacionnoac.csv")

        a = inflacionmap.columns[1:]
        fecha = st.selectbox("Año",a,len(a)-1)
        


        # Funciones
        tabla(inflacionmes,fecha)

        display_map(inflacionmes,fecha)
    

    if __name__ == "__main__":
        main()



#-------------------------------------------------------------------------------TERCERA PESTAÑA:Variables influyentes ------------------------------------------------------------------------------------
tab_plots = tabs[2]

with tab_plots:

# --------------------------------------------------------Salarios-----------------------------------------------------
    st.title("Salarios")
    st.write("""Cuando suben los precios, sube la presión para que se incrementen los salarios, ya que los trabajadores 
    no desean perder poder adquisitivo. No obstante, muchas empresas no tienen capacidad para poder 
    afrontar una subida generalizada del salario de sus trabajadores, que determinaría una nueva subida de sus costes.
    Entrando asi en un espiral precios-salarios que no para de crecer.""")
    # Grafico 1 salarios
    fig3 = px.line(salarios, x="indice_tiempo", y=salarios.columns[2:5], title='Evolución de los salarios',  markers=True,
                    labels={"indice_tiempo":"","value":"Valores"}, template="plotly_dark")
    annotations = []
    # Source
    annotations.append(dict(xref='paper', yref='paper', x=0.5, y=-0.1,
                              xanchor='center', yanchor='top',
                              text='Fuente: datos.gob.ar',
                              font=dict(family='Arial',
                                        size=12,
                                        color='rgb(150,150,150)'),
                              showarrow=False))
    fig3.update_layout(annotations=annotations)
    fig3.update_xaxes(
        rangeslider_visible=True
    )
    st.plotly_chart(fig3)

    # Grafico 2 salarios
    fig4 = px.line(salarios, x="indice_tiempo", y=salarios.columns[5:8], 
                    title='Evolución de los salarios(en porcentaje de aumento mensual)',  markers=True,
                    labels={"indice_tiempo":"","value":"Valores"}, template="plotly_dark")
    annotations = []
    # Source
    annotations.append(dict(xref='paper', yref='paper', x=0.5, y=-0.1,
                              xanchor='center', yanchor='top',
                              text='Fuente: datos.gob.ar',
                              font=dict(family='Arial',
                                        size=12,
                                        color='rgb(150,150,150)'),
                              showarrow=False))
    fig4.update_layout(annotations=annotations)
    fig4.update_xaxes(
        rangeslider_visible=True
    )
    st.plotly_chart(fig4)
    st.write("""Aquí podemos ver como el salario general sigue al salario registrado, 
    mientras el que más muestra picos diferenciados es el salario no registrado.""")

    # Grafico salarios vs inflación
    fig5 = px.histogram(salarios, x="indice_tiempo", y="Salarios general", histfunc="avg",
                    title="Comparación evolución salarios vs IPC",
                    template="plotly_dark",labels={"indice_tiempo":"","avg of Salarios general":"Valores"})
    fig5.update_traces(xbins_size="M1", hovertemplate=None)
    fig5.update_xaxes(showgrid=True)
    fig5.update_layout(bargap=0.1)
    fig5.add_trace(go.Scatter(x=salarios["indice_tiempo"], y=salarios["IPC general"], name="IPC"))
    fig5.update_layout(hovermode="x unified")
    annotations = []
    # Source
    annotations.append(dict(xref='paper', yref='paper', x=0.5, y=-0.1,
                                xanchor='center', yanchor='top',
                                text='Fuente: datos.gob.ar',
                                font=dict(family='Arial',
                                            size=12,
                                            color='rgb(150,150,150)'),
                                showarrow=False))
    fig5.update_layout(annotations=annotations)

    st.plotly_chart(fig5)

    st.write("""En este grafico podemos ver como el aumento de salarios potencia el aumento de la inflación""")

# ---------------------------------------------------------------------Tipo de cambio real------------------------------------------
    st.title("Tipo de cambio real")
    st.write("""El tipo de cambio real entre las monedas de dos países es un indicador de los precios de una cesta 
    de bienes y servicios de un país con respecto a los de otro país.
    Indica la relación a la que podemos intercambiar los bienes de un país por los de otro país.
    """)

    st.write("""Entre inflación y tipo de cambio existe una correspondencia inversa, es decir, 
    que un aumento en la inflación terminaría depreciando la moneda, pues el aumento en los 
    precios locales debe llevar un aumento en el tipo de cambio para mantener los precios reales 
    y alineados con los globales.""")

    st.write("""Si al aguien le interesa profundizar en el tema puede leer este articulo
    https://observatorio.unr.edu.ar/10-preguntas-para-entender-las-variaciones-del-tipo-de-cambio/""")

    # Grafico de tipo de cambio vs IPC  (Variacion )
    fig6 = px.histogram(tipo_de_cambio, x="indice_tiempo", y="Tipo de cambio real multilateral(Var %)", title="Comparación evolución tipo de cambio vs IPC (Variacion)",
                    template="plotly_dark",labels={"indice_tiempo":""})
    fig6.update_traces(xbins_size="M1", hovertemplate=None)
    fig6.update_xaxes(showgrid=True)
    fig6.update_layout(bargap=0.1)
    fig6.add_trace(go.Scatter(x=tipo_de_cambio["indice_tiempo"], y=tipo_de_cambio["IPC general(Var %)"], name="IPC"))
    fig6.update_layout(hovermode="x unified")
    annotations = []
    # Source
    annotations.append(dict(xref='paper', yref='paper', x=0.5, y=-0.1,
                                xanchor='center', yanchor='top',
                                text='Fuente: datos.gob.ar',
                                font=dict(family='Arial',
                                            size=12,
                                            color='rgb(150,150,150)'),
                                showarrow=False))
    fig.update_layout(annotations=annotations)

    st.plotly_chart(fig6)
    

# ----------------------------------------------------------Balanza comercial-------------------------------------------------------------------
    st.title("Balanza comercial")
    st.write("""La balanza comercial es un indicador que mide la relación entre las exportaciones y las importaciones 
            de un país en un determinado periodo. La balanza comercial no incluye los servicios prestados a o desde 
            otros países ni tampoco los movimientos de capitales.""")
    
    gr = balanza_comercial[["Mes","Total mensual exp","Total mensual imp"]]

    #Grafico evolución de la balanza comercial 
    fig7 = px.line(gr, x="Mes", y=gr.columns[1:3], 
                    title='Evolución de la balanza comercial(en millones de dolares)',  markers=True,
                    labels={"Mes":"","value":"Valores","variable":""}, template="plotly_dark")
    annotations = []
    # Source
    annotations.append(dict(xref='paper', yref='paper', x=0.5, y=-0.1,
                                xanchor='center', yanchor='top',
                                text='Fuente: Indec',
                                font=dict(family='Arial',
                                            size=12,
                                            color='rgb(150,150,150)'),
                                showarrow=False))
    fig7.update_layout(annotations=annotations)
    fig7.update_layout(hovermode="x unified")
    newnames = {'Total mensual exp':'Exportación', 'Total mensual imp': 'Importación'}
    fig7.for_each_trace(lambda t: t.update(name = newnames[t.name],
                                        legendgroup = newnames[t.name],
                                        hovertemplate = None)
                                        )
    st.plotly_chart(fig7)
# -------------------------------------------------------Balanza de pagos-------------------------------------------------
    st.title("Balanza de pagos")
    st.write("""La balanza de pagos comprende la cuenta corriente, la cuenta de capital y la cuenta financiera.""")
    st.write("La cuenta corriente brinda información de:")
    st.markdown("""
    • El comercio de bienes y servicios, tanto exportaciones como importaciones.

    • El ingreso primario, o los ingresos y egresos devengados provenientes de rentas (por ejemplo, cobros y pagos de intereses o remisión de utilidades).
    
    • El ingreso secundario, o las transferencias corrientes (tales como las remesas).
    
    Cuando la cuenta corriente arroja un resultado positivo se está en presencia de un superávit, mientras
    que un saldo negativo constituye un déficit.

    Por su parte, la cuenta de capital abarca las transferencias de capital (una donación de activos de
    capital o las condonaciones o quitas de deuda, por ejemplo) y la adquisición o disposición de activos
    no financieros no producidos.

    Por último, la cuenta financiera comprende las transacciones de activos y pasivos financieros con
    extranjeros (no residentes), distinguiendo el tipo funcional de inversión, es decir, inversión directa, de
    cartera, derivados financieros, otra inversión y activos de reserva """)
    # Grafico evolucion balanza de pagos
    fig8 = px.histogram(balanza_pagos, x=balanza_pagos.columns[0], y='Capacidad/Necesidad de financiamiento', 
                    title="Balanza de pagos",
                        template="plotly_dark",labels={"Unnamed: 0":"","Capacidad/Necesidad de financiamiento":"Valores"})
    fig8.update_traces(xbins_size="M1", hovertemplate=None)
    fig8.update_xaxes(showgrid=True)
    fig8.update_layout(bargap=0.1)
    annotations = []
    # Source
    annotations.append(dict(xref='paper', yref='paper', x=0.5, y=-0.1,
                                xanchor='center', yanchor='top',
                                text='Fuente: datos.gob.ar',
                                font=dict(family='Arial',
                                            size=12,
                                            color='rgb(150,150,150)'),
                                showarrow=False))
    fig8.update_layout(annotations=annotations)
    st.plotly_chart(fig8)

    st.write("""La importancia de la balanza de pagos radica en que nos permite conocer si el país está en déficit o superávit. 
            Este último lo definimos cuando el saldo de la balanza es positivo, que significa que el estado obtuvo más 
            ingresos que egresos""")

# ------------------------------------------------------Serie temporal----------------------------------------------------
tab_plots = tabs[3]

with tab_plots:
    st.title("ARIMA")
    st.write("""En principio mostramos la distribución de la inflación a lo largo de los años""")

    fig9= px.line(ipc, x="Periodo", y=' Nacional ',template="plotly_dark",
             labels={"Periodo":""," Nacional ":"IPC"})
    annotations = []

    # Source
    annotations.append(dict(xref='paper', yref='paper', x=0.5, y=-0.1,
                                xanchor='center', yanchor='top',
                                text='Fuente: INDEC',
                                font=dict(family='Arial',
                                            size=12,
                                            color='rgb(150,150,150)'),
                                showarrow=False))
    fig9.update_layout(annotations=annotations)

    st.plotly_chart(fig9)

    st.write("Utilizamos la prueba de Dickey-Fuller aumentada (ADF) para chequear si la serie es estacionaria o no.")

    st.write("""**¿Cuáles son nuestras hipótesis?**""")
    st.markdown("$H_{0}$: tiene una raíz unitaria (serie no estacionaria).")
    st.markdown("$H_{1}$: no tiene una raíz unitaria (serie estacionaria).")

    st.code("""from statsmodels.tsa.stattools import adfuller
    data = ipc2.values
    stat, p, lags, obs, crit, t = adfuller(data)
    print('stat=%.3f, p=%.3f' % (stat, p))
    if p > 0.05:
        print('Probablemente no estacionaria')
    else:
        print('Probablemente estacionaria')""")
    
    image= Image.open('ad_fuller.png')
    st.image(image)

    st.write("""Una vez que sabemos que la serie probablemente es estacionaria, aplicamos la siguiente función para ver 
    cuáles son los mejores hiperparametros del modelo ARIMA.""")

    st.code("""# evaluate an ARIMA model for a given order (p,d,q)
    def evaluate_arima_model(X, arima_order):
    # prepare training dataset
    train_size = int(len(X) * 0.66)
    train, test = X[0:train_size], X[train_size:]
    history = [x for x in train]
    # make predictions
    predictions = list()
    for t in range(len(test)):
    model = ARIMA(history, order=arima_order)
    model_fit = model.fit()
    yhat = model_fit.forecast()[0]
    predictions.append(yhat)
    history.append(test[t])
    # calculate out of sample error
    rmse = sqrt(mean_squared_error(test, predictions))
    return rmse""")
    st.code("""# evaluate combinations of p, d and q values for an ARIMA model
    def evaluate_models(dataset, p_values, d_values, q_values):
    dataset = dataset.astype('float32')
    best_score, best_cfg = float("inf"), None
    for p in p_values:
    for d in d_values:
        for q in q_values:
        order = (p,d,q)
        try:
            rmse = evaluate_arima_model(dataset, order)
            if rmse < best_score:
            best_score, best_cfg = rmse, order
            print('ARIMA%s RMSE=%.3f' % (order,rmse))
        except:
            continue
    print('Best ARIMA%s RMSE=%.3f' % (best_cfg, best_score))""")

    image= Image.open('evaluate_parameters.png')
    st.image(image)

    st.write("Como vemos en la imagen anterior, los mejores hiperparametros son (8,1,1), por ende, vamos a utilizar esos.")
    
    st.write("""Aplicamos ARIMA(8,1,1) y vemos su resultado""")

    image= Image.open('arima.png')
    st.image(image)
    
    st.markdown("Con la siguiente grafica podemos ver lo siguiente:")
    st.markdown("Arriba a la izquierda: los errores residuales parecen fluctuar alrededor de una media de cero y tienen una varianza uniforme.")
    st.markdown("Arriba a la derecha: el gráfico de densidad sugiere una distribución normal con media cero.")
    st.write("""Abajo a la izquierda: Todos los puntos deben estar perfectamente alineados con la línea roja. 
                Cualquier desviación significativa implicaría que la distribución está sesgada.""")
    st.write("""Abajo a la derecha: El gráfico Correlogram, también conocido como ACF, muestra que los errores residuales no están auto correlacionados.
    Cualquier auto correlación implicaría que existe algún patrón en los errores residuales que no se explican en el modelo.
    Por lo tanto, deberá buscar más X (predictores) para el modelo.""")

    image= Image.open('arimaa.png')
    st.image(image)

    
    st.write("En el siguiente grafico vemos la predicción vs la serie original, si bien se acerca, vemos que no es perfecto")
    image= Image.open('arimab.png')
    st.image(image)
    

    st.write("""Para comprobar la calidad del ajuste del modelo entrenado a los datos de la serie temporal proporcionados, 
        podemos usar el método `predict` del modelo ARIMA entrenado para trazar los valores reales y pronosticados 
        uno encima del otro. Verifiquemos qué tan bien funciona la predicción:""")
    
    
    image= Image.open('arimac.png')
    st.image(image)
    st.write("Test MAPE: 0.526")
    
    st.write("""MAPE: Mean Absolute Percent Error (Media del Error Absoluto en Porcentaje) mide el promedio del error en porcentaje.""")

    st.write("""52,6 % de MAPE que implica que el modelo tiene una precisión de alrededor del 47.4 % para predecir. No es un buen valor, pero seguimos con la prediccion final""")

    st.write("""Por último, hacemos el pronóstico de 12 meses (1 año) con el modelo entrenado, obteniendo la siguiente gráfica:""")

    image= Image.open('arimad.png')
    st.image(image)

    st.markdown("""Valores pronosticados por el modelo:""")
    st.markdown("- Enero : 5.26825204")
    st.markdown("- Febrero : 4.90362904") 
    st.markdown("- Marzo : 5.0569651")
    st.markdown("- Abril : 4.81403047")
    st.markdown("- Mayo : 4.96768265")
    st.markdown("- Junio : 5.4474125")
    st.markdown("- Julio : 5.46244198")
    st.markdown("- Agosto : 5.37474489")
    st.markdown("- Septiembre : 5.48295512") 
    st.markdown("- Octubre : 5.43303108")
    st.markdown("- Noviembre : 5.44979314")
    st.markdown("- Diciembre :  5.58631082")
    

























