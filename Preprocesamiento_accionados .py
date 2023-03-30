#!/usr/bin/env python
# coding: utf-8

# # Preprocesamiento

# In[1]:


import re
import spacy
import pandas as pd 
from unidecode import unidecode
from collections import Counter

nlp = spacy.load("es_core_news_md")
nlp = spacy.load("es_core_news_sm")


# In[2]:


def Limpiar_texto2(texto):
    texto = unidecode(texto)
    # Eliminar cualquier signo de puntuación
    puntuación = r'[.,;:¡!¿?@#$%&[\](){}<>~=+\-*/|\\_^`"\']'
    #puntuación = r'[^\w\s]|(?<=\w)\.(?=[a-zA-Z])'
    texto = re.sub(puntuación, '', texto)

    # Eliminar cualquier carácter que no sea una letra o un número
    alfanumérico = r'\w+(?:-\w+)*'
    texto = re.sub(alfanumérico, lambda x: x.group(0).replace('-', ' '), texto)

    # Eliminar cualquier caracter que no sea una letra o un número o un espacio en blanco
    texto = re.sub(r'[^a-zA-Z0-9\s]', '', texto)

    doc = nlp(texto.lower())

    return " ".join(unidecode(token.norm_) for token in doc if not token.is_punct)


# In[3]:


accionados = pd.read_excel('Demandado.xlsx')
accionados.shape


# In[4]:


accionados['texto_limpio'] = accionados['Demandado'].apply(Limpiar_texto2)    
accionados.head(20)


# # Etiqueta Otros

# In[5]:


otros = r'\botro\b|\byotros\b|\byotro\b|\botros\b|y\botro\b|y\botros\b|y\botrs\b|y\botrosm\b|y\botroos\b'
accionados = accionados.assign(otros=accionados['Demandado'].astype(str).str.contains(otros, flags=re.IGNORECASE).astype(int))
accionados['texto_limpio'] = accionados['texto_limpio'].str.replace(otros, ' ', regex=True)


# In[6]:


accionados.loc[accionados.otros ==1]


# # Stop Words

# In[7]:


stop_words = ["sa", "sas", "ltda", "y", "e", "ni", "que", "pero", "si", "porque", "cuando", "pues", "sino",
            "aunque","el","los","las","lo","la", "un","una","unos","unas","al","del",
            "a","ante","bajo","cabe","con","contra","de","desde",
            "en","entre","hacia","hasta","para",
            "por" ,"segun" ,"sin" ,"so" ,"sobre" ,"tras"]
letras_solas = r'\b[a-zA-Z]\b'
accionados['texto_limpio'] = accionados['texto_limpio'].apply(lambda x: re.sub(letras_solas, '', x))
patron = r"\b(" + "|".join(stop_words) + r")\b"
accionados['texto_limpio'] = accionados['texto_limpio'].apply(lambda x: re.sub(patron,"",x))
accionados['texto_limpio'] = accionados['texto_limpio'].apply(lambda x: re.sub(' +', ' ', x))


# In[8]:


accionados.head(20)


# # Tokens

# In[9]:


def tokenizar(texto):
    doc = nlp(texto)
    return [token.text for token in doc]


# In[10]:


accionados["tokens"] = accionados["texto_limpio"].apply(tokenizar)
accionados.head(20)


# In[11]:


all_tokens = [token for lista_tokens in accionados["tokens"] for token in lista_tokens]
conteo_tokens = Counter(all_tokens)
conteo_tokens_ordenado = dict(sorted(conteo_tokens.items(), key=lambda x: x[1], reverse=True))
for token, conteo in conteo_tokens_ordenado.items():
    print(f"{token}: {conteo}")


# # Pensiones 

# In[12]:


Pensiones = r"porvenir|colfondos|colfondo|skandia|proteccion|colpensiones|pension|pensiones|afp"
accionados["pensiones"] = accionados["texto_limpio"].str.contains(Pensiones).astype(int)
accionados.loc[accionados.pensiones == 1]


# # EPS

# In[13]:


lista_eps = ["asmet","entidad promotora salud","empresa promotora salud", "eps", "epss" "epsi", "sos","aliansalud", "ambuq","cajacopi", "cafam", "capital salud", "capresoca", "colsubsidio", "comfandi", 'comfachocó', 'comfaoriente', 'comfamiliar', 'comfenalco', "compensar", "coomeva", "coosalud", "cruz blanca", "sanitas", "sura", "famisanar", "medimas", "mutual ser", "nueva eps", "salud total","savia", "anas wayuu", "asociacion indigena cauca","aic", "asociacion mutual ser", "mutualser", "cooperativa salud"]

regex = "|".join([re.escape(eps) for eps in lista_eps])
eps = re.compile(regex, flags=re.IGNORECASE)
accionados["eps"] = accionados["texto_limpio"].str.contains(eps).astype(int)


# In[14]:


accionados.loc[accionados.eps ==1]


# # Judiciales 

# In[15]:


judicial = r"juzgado|juzgados|juez|judicial"
accionados["judicial"] = accionados["texto_limpio"].str.contains(judicial).astype(int)
accionados.loc[accionados.judicial == 1]


# # UARIV

# In[16]:


UARIV = r"(?:(?:\bunidad\b.*\bvictimas\b)|(?:\bvictimas\b.*\bunidad\b)|\buariv\b)"
accionados["uariv"] = accionados["texto_limpio"].str.contains(UARIV).astype(int)
accionados.loc[accionados.uariv == 1]


# # Ministerios y Secretarias 

# In[17]:


ministerios = r"\bministerio\b"
accionados["ministerios"] = accionados["texto_limpio"].str.contains(ministerios).astype(int)
accionados.loc[accionados.ministerios == 1]


# In[18]:


secretarias = r"\bsecretaria\b"
accionados["secretarias"] = accionados["texto_limpio"].str.contains(secretarias).astype(int)
accionados.loc[accionados.secretarias == 1]


# # Alcaldias

# In[19]:


alcaldia = r"\balcaldia\b"
accionados["alcaldias"] = accionados["texto_limpio"].str.contains(alcaldia).astype(int)
accionados.loc[accionados.alcaldias == 1]


# # Movilidad-Transito

# In[20]:


movilidad = r"\bmovilidad\b|\btransito\b"
accionados["movilidad"] = accionados["texto_limpio"].str.contains(movilidad).astype(int)
accionados.loc[accionados.movilidad == 1]


# # Entidades Carcelarias 

# In[21]:


carcelario = r"\bpenitenciario\b|\bcarcelario\b|\binpec\b|(?:\binstituto\b.*\bpenitenciario\b)"
accionados["carcelario"] = accionados["texto_limpio"].str.contains(carcelario).astype(int)
accionados.loc[accionados.carcelario == 1]


# # Sin etiqueta

# In[22]:


filtro = (accionados[['pensiones', 'eps', 'judicial', 'uariv', 'alcaldias', 'ministerios', 'secretarias', 'movilidad', 'carcelario']] == 0).all(axis=1)
sin_etiqueta = accionados[filtro]
sin_etiqueta


# In[23]:


porcentaje_sin_etiquetar = len(sin_etiqueta) / len(accionados) * 100
print(porcentaje_sin_etiquetar, "%")


# In[24]:


all_tokens2 = [token for lista_tokens in sin_etiqueta["tokens"] for token in lista_tokens]
conteo_tokens2 = Counter(all_tokens2)
conteo_tokens_ordenado2 = dict(sorted(conteo_tokens2.items(), key=lambda x: x[1], reverse=True))
for token, conteo in conteo_tokens_ordenado2.items():
    print(f"{token}: {conteo}")

