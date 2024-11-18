import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

## ATENCION: Debe colocar la direccion en la que ha sido publicada la aplicacion en la siguiente linea\
# url = 'https://tp8-555555.streamlit.app/'

# Función para calcular y graficar evolución de ventas
def generar_grafico_evolucion(data, producto):
    ventas = data.groupby(["Año", "Mes"])["Unidades_vendidas"].sum().reset_index()
    fechas = range(len(ventas))
    
    # Crear gráfico de evolución
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(fechas, ventas["Unidades_vendidas"], label=f"{producto}", marker='o', linestyle='-', color='blue')
    
    # Calcular línea de tendencia
    x = np.arange(len(ventas))
    y = ventas["Unidades_vendidas"]
    coeficientes = np.polyfit(x, y, 1)
    tendencia = np.poly1d(coeficientes)
    ax.plot(x, tendencia(x), linestyle="--", color="red", label="Tendencia")
    
    # Configuración del gráfico
    ax.set_title(f"Evolución Mensual de Ventas - {producto}")
    ax.set_xlabel("Tiempo (Año-Mes)")
    ax.set_ylabel("Unidades Vendidas")
    ax.grid(True)
    ax.legend()
    
    # Configurar etiquetas para el eje x
    etiquetas = [f"{fila.Año}-{fila.Mes:02}" for fila in ventas.itertuples()]
    ax.set_xticks(fechas)
    ax.set_xticklabels(etiquetas, rotation=45, ha='right', fontsize=8)
    plt.tight_layout()
    
    return fig

# Función para mostrar métricas calculadas
def calcular_mostrar_metricas(data, producto):
    # Filtrar datos del producto
    data_producto = data[data["Producto"] == producto]
    
    # Cálculos principales
    data_producto["Precio_promedio"] = data_producto["Ingreso_total"] / data_producto["Unidades_vendidas"]
    data_producto["Margen"] = ((data_producto["Ingreso_total"] - data_producto["Costo_total"]) / data_producto["Ingreso_total"]) * 100
    data_producto["Ganancia"] = data_producto["Ingreso_total"] - data_producto["Costo_total"]
    
    # Resúmenes
    precio_promedio = data_producto["Precio_promedio"].mean()
    margen_promedio = data_producto["Margen"].mean()
    unidades_totales = data_producto["Unidades_vendidas"].sum()
    
    # Variaciones anuales
    precio_por_año = data_producto.groupby("Año")["Precio_promedio"].mean()
    margen_por_año = data_producto.groupby("Año")["Margen"].mean()
    unidades_por_año = data_producto.groupby("Año")["Unidades_vendidas"].sum()
    
    variacion_precio = precio_por_año.pct_change().mean() * 100
    variacion_margen = margen_por_año.pct_change().mean() * 100
    variacion_unidades = unidades_por_año.pct_change().mean() * 100
    
    # Mostrar métricas
    st.subheader(f"Producto: {producto}")  # Título del producto
    with st.container():
        col1, col2 = st.columns([1, 3])
        with col1:
            st.metric("Precio Promedio", f"${precio_promedio:,.2f}", f"{variacion_precio:+.2f}%")
            st.metric("Margen Promedio", f"{margen_promedio:.2f}%", f"{variacion_margen:+.2f}%")
            st.metric("Unidades Totales", f"{unidades_totales:,.0f}", f"{variacion_unidades:+.2f}%")
        with col2:
            fig = generar_grafico_evolucion(data_producto, producto)
            st.pyplot(fig)

# Información del alumno
def mostrar_informacion_alumno():
    with st.container():
        st.markdown('**Legajo:** 59154')
        st.markdown('**Nombre:** Garcia Maximo')
        st.markdown('**Comisión:** C5')

# Aplicación principal
def main():
    st.title("Análisis de Ventas - TP8")
    
    mostrar_informacion_alumno()
    
    # Subida de archivo
    archivo = st.sidebar.file_uploader("Cargar archivo CSV", type=["csv"])
    
    if archivo:
        data = pd.read_csv(archivo)
        
        # Filtro por sucursal
        sucursales = ["Todas"] + data["Sucursal"].unique().tolist()
        sucursal_elegida = st.sidebar.selectbox("Seleccionar Sucursal", sucursales)
        
        if sucursal_elegida != "Todas":
            data = data[data["Sucursal"] == sucursal_elegida]
            st.header(f"Datos de la Sucursal: {sucursal_elegida}")
        else:
            st.header("Datos de Todas las Sucursales")
        
        # Mostrar métricas y gráficos por producto
        for producto in data["Producto"].unique():
            st.divider()  # Agregar el separador antes de cada producto
            calcular_mostrar_metricas(data, producto)
    else:
        st.write("Sube un archivo CSV para comenzar.")

# Ejecutar la aplicación
if __name__ == "__main__":
    main()