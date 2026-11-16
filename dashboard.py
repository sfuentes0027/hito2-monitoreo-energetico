"""Dashboard local basado en exportación CSV de Google Sheets."""
import streamlit as st,pandas as pd
st.set_page_config(page_title='Monitoreo energético | Hito 2',layout='wide')
st.title('Monitoreo energético · Hito 2')
st.caption('Sebastian Fuentes · Felipe Ruiz · Magdalena Gomez')
file=st.file_uploader('Sube el CSV exportado desde la hoja de registros de n8n',type=['csv'])
if not file:
    st.info('Para visualizar datos reales, exporta la hoja de Google Sheets como CSV y súbela aquí. Este dashboard aún no está publicado.')
    st.stop()
df=pd.read_csv(file)
if df.empty:st.warning('El archivo no tiene filas');st.stop()
cols=st.columns(3)
cols[0].metric('Registros',len(df))
if 'prioridad' in df:cols[1].metric('Alertas altas',int(df.prioridad.astype(str).str.lower().eq('alta').sum()))
if 'requiere_revision_humana' in df:cols[2].metric('Revisiones solicitadas',int(df.requiere_revision_humana.astype(str).str.lower().isin(['true','si','sí','1']).sum()))
if 'fecha' in df:
    df['fecha']=pd.to_datetime(df['fecha'],errors='coerce')
    df=df.sort_values('fecha')
for k in ['energia_kwh','potencia_kw','voltaje_v','corriente_a']:
    if k in df:
        df[k]=pd.to_numeric(df[k],errors='coerce')
        if df[k].notna().any():st.subheader(k);st.line_chart(df.set_index('fecha')[k] if 'fecha' in df else df[k])
if 'prioridad' in df:st.subheader('Distribución de prioridades');st.bar_chart(df.prioridad.value_counts())
st.subheader('Historial de diagnósticos y recomendaciones')
st.dataframe(df,use_container_width=True)
