import marimo

__generated_with = "0.13.15"
app = marimo.App()


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _():
    import uuid
    import pandas as pd
    return pd, uuid


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""# Loads""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Entidades""")
    return


@app.cell
def _(pd):
    ori_ents= pd.read_excel('../entidades/entidades.xlsx')
    ori_ents.head()
    return (ori_ents,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Personas""")
    return


@app.cell
def _(pd):
    ori_per_2023= pd.read_excel('../respuestas/2023/2023.xlsx')
    ori_per_2023.head()
    return (ori_per_2023,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Jerarquia""")
    return


@app.cell
def _(pd):
    ori_jer_2019= pd.read_excel('../preguntas/estructura/2019.xlsx')
    ori_jer_2019.head()
    return (ori_jer_2019,)


@app.cell
def _(pd):
    ori_jer_2021= pd.read_excel('../preguntas/estructura/2021.xlsx')
    ori_jer_2021.head()
    return (ori_jer_2021,)


@app.cell
def _(pd):
    ori_jer_2023= pd.read_excel('../preguntas/estructura/2023.xlsx')
    ori_jer_2023.head()
    return (ori_jer_2023,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""# Preprocesado""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Jerarquia""")
    return


@app.cell
def _(ori_jer_2019, ori_jer_2021, ori_jer_2023, pd):
    ori_stacked = pd.concat([ori_jer_2019, ori_jer_2021, ori_jer_2023], axis=0, ignore_index=True)
    ori_stacked.head()
    return (ori_stacked,)


@app.cell
def _(ori_stacked, uuid):
    def generate_uuid_map(df, column):
        # Group by year and column
        pairs = df[['T', column]].drop_duplicates()
        pairs['id'] = [str(uuid.uuid4()) for _ in range(len(pairs))]
        return pairs

    # Apply to each column you want to normalize
    componente_map = generate_uuid_map(ori_stacked, 'Componente')
    variable_map   = generate_uuid_map(ori_stacked, 'Variable')
    indicador_map  = generate_uuid_map(ori_stacked, 'Indicador')
    pregunta_map   = generate_uuid_map(ori_stacked, 'Pregunta')
    subpregunta_map   = generate_uuid_map(ori_stacked, 'SubPregunta')
    return (
        componente_map,
        indicador_map,
        pregunta_map,
        subpregunta_map,
        variable_map,
    )


@app.cell
def _(
    componente_map,
    indicador_map,
    ori_stacked,
    pregunta_map,
    subpregunta_map,
    variable_map,
):
    stacked = (
        ori_stacked
        .merge(componente_map, on=['T', 'Componente'], how='left', suffixes=('', '_componente'))
        .merge(variable_map, on=['T', 'Variable'], how='left', suffixes=('', '_variable'))
        .merge(indicador_map, on=['T', 'Indicador'], how='left', suffixes=('', '_indicador'))
        .merge(pregunta_map, on=['T', 'Pregunta'], how='left', suffixes=('', '_pregunta'))
        .merge(subpregunta_map, on=['T', 'SubPregunta'], how='left', suffixes=('', '_subpregunta'))
    ).rename(columns={'id':'id_componente'})

    # Optional: drop the original columns and keep only UUIDs
    # stacked = stacked.drop(columns=['T', 'Componente', 'Variable', 'Indicador', 'Pregunta'])
    stacked
    return (stacked,)


@app.cell
def _(stacked):
    stacked[(stacked['T'] == 'IIP2023') & (stacked['Variable'] == 'Variable 6. Generación de ideas')]
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""# Nivel 0""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""## Sectores""")
    return


@app.cell
def _(ori_ents, uuid):
    sectores = ori_ents[['sector', 's_description']].drop_duplicates().copy()

    sectores['id'] = [str(uuid.uuid4()) for _ in range(len(sectores))]

    sectores = sectores[['id','sector','s_description']]

    sectores_out = sectores.rename(columns={'sector': 'name','s_description':'description'})

    sectores_out
    return sectores, sectores_out


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Usuarios""")
    return


@app.cell
def _(pd, uuid):
    import hashlib
    import random
    import string
    from datetime import datetime, timedelta

    def generate_hashed_password():
        random_password = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
        hashed = hashlib.sha256(random_password.encode()).hexdigest()
        return hashed

    def generate_user_row(username, name, email):
        now = datetime.now()
        return {
            "id": str(uuid.uuid4()),
            "username": username,
            "name": name,
            "email": email,
            "password_hash": generate_hashed_password(),
            "biography": f"{username} is a fictional user created for testing our pandas DataFrame.",
            "created_at": now,
            "updated_at": now + timedelta(minutes=5)
        }

    # Create the DataFrame
    usr = [
        generate_user_row("jmartinez", "Juan José Martínez Guerrero", "jmartinez@veeduriadistrital.gov.co"),
        generate_user_row("mramirez", "Miguel Andrés Ramírez Roa", "mramirez@veeduriadistrital.gov.co"),
    ]

    users = pd.DataFrame(usr)
    users
    return datetime, random, users


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Indices""")
    return


@app.cell
def _(pd):
    ind = {
        "id": [2019, 2021, 2023],
        "description": [
            "Primera medición del índice. En esta edición participaron exclusivamente las cabezas de sector, lo que resultó en un total de 39 entidades evaluadas.",
            "Segunda medición. Se amplía la convocatoria incluyendo alcaldías locales y entidades adscritas. Se incorpora una nueva variable enfocada en el uso de recursos digitales para la innovación.",
            "Tercera medición. Se implementa un sistema de retroalimentación (bucles) para comprender en profundidad los procesos de innovación institucional. Además, se ajusta el componente 2 conforme a la metodología de innovación del doble diamante."
        ]
    }

    indexes = pd.DataFrame(ind)
    indexes

    return (indexes,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## exports lvl 0""")
    return


@app.cell
def _(sectores_out):
    sectores_out.to_csv('./output/00_sectores.csv',index=False,sep='|',quotechar='"',escapechar="'")
    return


@app.cell
def _(users):
    users.to_csv('./output/00_usuarios.csv',index=False,sep='|',quotechar='"',escapechar="'")
    return


@app.cell
def _(indexes):
    indexes.to_csv('./output/00_indices.csv',index=False,sep='|',quotechar='"',escapechar="'")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""# Nivel 1""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Entidades""")
    return


@app.cell
def _(ori_ents, sectores):
    entidades = ori_ents[['_uuid', 'sector', 'entidad', 'description','mision', 'vision']].copy().rename(columns={'_uuid': 'id'})

    entidades = entidades.merge(
        sectores,
        on='sector',           # match by sector name
        how='left',
        suffixes=('', '_sector')
    )

    entidades['id_sector']

    entidades = entidades.rename(columns={'entidad': 'name','id_sector':'sector_id'})

    entidades= entidades[['id','name','description','mision','vision','sector_id']]
    entidades
    return (entidades,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Personas""")
    return


@app.cell
def _(ori_per_2023, uuid):
    personas = ori_per_2023[['entidad','nombre_responde','dependencia_entidad','cargo_responde','correo_personal','correo_institucional','tel']].copy()


    cols = ['dependencia_entidad','cargo_responde','correo_personal','correo_institucional']

    personas[cols] = personas[cols].apply(lambda col: col.str.capitalize())
    personas['nombre_responde'] = personas['nombre_responde'].str.title()

    personas['id'] = [str(uuid.uuid4()) for _ in range(len(personas))]
    personas['user_id'] = ''


    personas.rename(columns={'nombre_responde':'name','correo_personal':'email_per','correo_institucional':'email_ent','tel':'phone','dependencia_entidad':'area','cargo_responde':'job_title',}, inplace=True)

    personas_out = personas[['id','name','email_per','email_ent','phone','area','job_title','user_id']]

    personas_out
    return personas, personas_out


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Componentes""")
    return


@app.cell
def _(stacked):
    comps = stacked[['id_componente', 'T' , 'Componente', 'wc']].drop_duplicates().copy()
    comps.rename(columns={'id_componente':'id','T':'index_edition_id','Componente':'name','wc':'weight'}, inplace=True)
    comps
    return (comps,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## exports lvl 1""")
    return


@app.cell
def _(entidades):
    entidades.to_csv('./output/01_entidades.csv',index=False,sep='|',quotechar='"',escapechar="'")
    return


@app.cell
def _(personas_out):
    personas_out.to_csv('./output/01_personas.csv',index=False,sep='|',quotechar='"',escapechar="'")
    return


@app.cell
def _(comps):
    comps.to_csv('./output/01_componente.csv',index=False,sep='|',quotechar='"',escapechar="'")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""# Nivel 2""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Variables""")
    return


@app.cell
def _(stacked):
    vars = stacked[['id_variable', 'T' , 'id_componente', 'Variable', 'wv']].drop_duplicates().copy()
    vars.rename(columns={'id_variable':'id','T':'index_edition_id','Variable':'name','id_componente':'componente_id','wv':'weight'}, inplace=True)
    vars
    return (vars,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Asociación entidad-persona""")
    return


@app.cell
def _(entidades):
    entidades.info(verbose=True)
    return


@app.cell
def _(personas):
    personas.info(verbose=True)
    return


@app.cell
def _(personas):
    personas[personas['entidad']=='Secretaría Distrital De Integración Social']
    return


@app.cell
def _(entidades, personas):
    entidad_persona = personas.merge(entidades[['id', 'name']], 
                                left_on='entidad', right_on='name', 
                                how='left').rename(columns={'id_x':'person_id','id_y':'entity_id'})

    asociacion = entidad_persona[['entity_id','person_id']]
    asociacion
    return (asociacion,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Media""")
    return


@app.cell
def _(users):
    jmartinez = users[users['username']=='jmartinez']['id'].values[0]
    jmartinez
    return (jmartinez,)


@app.cell
def _(datetime, jmartinez, pd, random, uuid):
    from datetime import timezone


    # Possible enums
    media_types = ["image/png", "image/jpeg", "video/mp4"]
    parent_types = ["entity", "person", "user", "answer", "subanswer", "component", "variable", "indicator", "question", "subquestion"]

    # Generate mock data
    mock_data = []
    for _ in range(1):  # Change the number if you want more rows
        mock_data.append({
            "id": str(uuid.uuid4()),
            "user_id": str(jmartinez),
            "created_at": datetime.now(timezone.utc),
            "media_type": random.choice(media_types),
            "filename": f"file_{random.randint(1000, 9999)}.jpg",
            "file_size": random.randint(10000, 5000000),  # in bytes
            "parent_id": str(uuid.uuid4()),
            "parent_type": parent_types[1]
        })

    # Create DataFrame
    df_media = pd.DataFrame(mock_data)

    df_media
    return (df_media,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## exports lvl 2""")
    return


@app.cell
def _(vars):
    vars.to_csv('./output/02_variable.csv',index=False,sep='|',quotechar='"',escapechar="'")
    return


@app.cell
def _(asociacion):
    asociacion.to_csv('./output/02_asociacion.csv',index=False,sep='|',quotechar='"',escapechar="'")
    return


@app.cell
def _(df_media):
    df_media.to_csv('./output/02_archivos.csv',index=False,sep='|',quotechar='"',escapechar="'")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""# Nivel 3""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Indicadores""")
    return


@app.cell
def _(stacked):
    inds = stacked[['id_indicador', 'T' , 'id_variable', 'Indicador','wi']].drop_duplicates().copy()
    inds.rename(columns={'id_indicador':'id','T':'index_edition_id','Indicador':'name','id_variable':'variable_id','wi':'weight'}, inplace=True)
    inds
    return (inds,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## exports lvl 3""")
    return


@app.cell
def _(inds):
    inds.to_csv('./output/03_indicador.csv',index=False,sep='|',quotechar='"',escapechar="'")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""# Nivel 4""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Preguntas""")
    return


@app.cell
def _(stacked):
    pres = stacked[['id_pregunta', 'T' , 'id_indicador', 'Pregunta','tp','wp']].drop_duplicates().copy()
    pres.rename(columns={'id_pregunta':'id','T':'index_edition_id','Pregunta':'text','id_indicador':'indicator_id','wp':'weight','tp':'question_type'}, inplace=True)

    pres = pres[['id','index_edition_id','indicator_id','text','weight','question_type',]]
    pres
    return (pres,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## exports lvl 4""")
    return


@app.cell
def _(pres):
    pres.to_csv('./output/04_pregunta.csv',index=False,sep='|',quotechar='"',escapechar="'")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""# Nivel 5""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Subpreguntas""")
    return


@app.cell
def _(stacked):
    subpres = stacked[['id_subpregunta', 'T' , 'id_pregunta', 'SubPregunta','ts','ws']].drop_duplicates().copy()
    subpres.rename(columns={'id_subpregunta':'id','T':'index_edition_id','SubPregunta':'text','id_pregunta':'pregunta_id','ws':'weight','ts':'question_type'}, inplace=True)

    subpres = subpres[['id','index_edition_id','pregunta_id','text','weight',]]
    subpres
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Respuestas""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## exports lvl 5""")
    return


@app.cell
def _(pres):
    pres.to_csv('./output/05_subpregunta.csv',index=False,sep='|',quotechar='"',escapechar="'")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Respuestas""")
    return


@app.cell
def _():
    # resp_19=pd.read_excel('./input/resp_2019.xlsx')
    # resp_21=pd.read_excel('./input/resp_2021.xlsx')
    # resp_23=pd.read_excel('./input/resp_2023.xlsx')
    return


@app.cell
def _():
    # ans_2019 = resp_19.copy().drop(columns=['Dirección de correo electrónico']).dropna(axis=1, how='all')
    # ans_2021 = resp_21.copy().dropna(axis=1, how='all')
    # ans_2023 = resp_23.copy().drop(columns=['nombre_responde', 'dependencia_entidad', 'cargo_responde', 'correo_personal', 'correo_institucional', 'tel']).dropna(axis=1, how='all')
    return


@app.cell
def _():
    # # Assuming the 'entidades' DataFrame has the 'entidad' column with text and 'uuid' column with the corresponding UUIDs
    # entidad_dict = dict(zip(entidades['name'], entidades['id']))

    # # Apply the mapping to replace entidad text with uuid in each DataFrame
    # ans_2019['entidad'] = ans_2019['entidad'].replace(entidad_dict)
    # ans_2021['entidad'] = ans_2021['entidad'].replace(entidad_dict)
    # ans_2023['entidad'] = ans_2023['entidad'].replace(entidad_dict)
    return


@app.cell
def _():
    # df_19_melted = ans_2019.melt(id_vars=['entidad'], var_name='question', value_name='answer')
    # df_21_melted = ans_2021.melt(id_vars=['entidad'], var_name='question', value_name='answer')
    # df_23_melted = ans_2023.melt(id_vars=['entidad'], var_name='question', value_name='answer')
    return


@app.cell
def _():
    # ques_2019=df_19_melted['question'].unique()
    # ques_2021=df_21_melted['question'].unique()
    # ques_2023=df_23_melted['question'].unique()
    return


@app.cell
def _():
    # df_2019 = pd.DataFrame(ques_2019.tolist(), columns=["questions"])
    # df_2021 = pd.DataFrame(ques_2021.tolist(), columns=["questions"])
    # df_2023 = pd.DataFrame(ques_2023.tolist(), columns=["questions"])
    return


@app.cell
def _():
    # df_2019.to_excel('./input/df_2019.xlsx',index=False)
    # df_2021.to_excel('./input/df_2021.xlsx',index=False)
    # df_2023.to_excel('./input/df_2023.xlsx',index=False)
    return


@app.cell
def _():
    # df_19_melted.to_excel('./input/df_19_melted.xlsx',index=False)
    # df_21_melted.to_excel('./input/df_21_melted.xlsx',index=False)
    # df_23_melted.to_excel('./input/df_23_melted.xlsx',index=False)
    return


@app.cell
def _():
    # print(df_19_melted.head())
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""# Nivel 6""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Subrespuestas""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## exports lvl 6""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""# Jerarquia""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## 19""")
    return


@app.cell
def _():
    # j_2019=pd.read_excel('./input/pre_2019.xlsx')
    # j_2019['index_edition_id']='2019'
    # j_2019['weight']=0
    # j_2019['question_type']="0"

    # j_2019 = j_2019.drop(columns=['T'])
    return


@app.cell
def _():
    # c_2019 = j_2019[['Componente', 'index_edition_id', 'weight']].drop_duplicates().copy()
    # v_2019 = j_2019[['Componente', 'Variable', 'index_edition_id', 'weight']].drop_duplicates().copy()
    # i_2019 = j_2019[['Variable', 'Indicador', 'index_edition_id', 'weight']].drop_duplicates().copy()
    # p_2019 = j_2019[['Indicador', 'Pregunta', 'index_edition_id', 'weight']].drop_duplicates().copy()
    # s_2019 = j_2019[['Pregunta', 'SubPregunta', 'index_edition_id', 'weight']].drop_duplicates().copy()

    # c_2019["componente_id"] = [uuid.uuid4() for _ in range(len(c_2019))]
    # v_2019["variable_id"] = [uuid.uuid4() for _ in range(len(v_2019))]
    # i_2019["indicador_id"] = [uuid.uuid4() for _ in range(len(i_2019))]
    # p_2019["pregunta_id"] = [uuid.uuid4() for _ in range(len(p_2019))]
    # s_2019["subpregunta_id"] = [uuid.uuid4() for _ in range(len(s_2019))]

    # v_2019 = v_2019.merge(
    #     c_2019[['Componente', 'componente_id']], 
    #     on='Componente', 
    #     how='left'
    # )

    # i_2019 = i_2019.merge(
    #     v_2019[['Variable', 'variable_id']], 
    #     on='Variable', 
    #     how='left'
    # )

    # p_2019 = p_2019.merge(
    #     i_2019[['Indicador', 'indicador_id']], 
    #     on='Indicador', 
    #     how='left'
    # )

    # s_2019 = s_2019.merge(
    #     p_2019[['Pregunta', 'pregunta_id']], 
    #     on='Pregunta', 
    #     how='left'
    # )
    return


@app.cell
def _():
    # c_2019_1 = c_2019.rename(columns={'componente_id': 'id'})
    # v_2019_1 = v_2019.rename(columns={'componente_id': 'parent_id', 'variable_id': 'id', 'Componente': 'parent_text', 'Variable': 'text'})
    # i_2019_1 = i_2019.rename(columns={'variable_id': 'parent_id', 'indicador_id': 'id', 'Variable': 'parent_text', 'Indicador': 'text'})
    # p_2019_1 = p_2019.rename(columns={'indicador_id': 'parent_id', 'pregunta_id': 'id', 'Indicador': 'parent_text', 'Pregunta': 'text'})
    # s_2019_1 = s_2019.rename(columns={'pregunta_id': 'parent_id', 'subpregunta_id': 'id', 'Pregunta': 'parent_text', 'SubPregunta': 'text'})
    return


@app.cell
def _():
    # c_2019_1['text'] = c_2019_1['Componente']
    # c_2019_2 = c_2019_1[['index_edition_id', 'id', 'text', 'weight']]
    # v_2019_2 = v_2019_1[['index_edition_id', 'id', 'parent_id', 'parent_text', 'text', 'weight']]
    # i_2019_2 = i_2019_1[['index_edition_id', 'id', 'parent_id', 'parent_text', 'text', 'weight']]
    # p_2019_2 = p_2019_1[['index_edition_id', 'id', 'parent_id', 'parent_text', 'text', 'weight']]
    # s_2019_2 = s_2019_1[['index_edition_id', 'id', 'parent_id', 'parent_text', 'text', 'weight']]
    return


@app.cell
def _():
    # v_2019_2.head()
    # v_2019_2.head()
    # i_2019_2.head()
    # p_2019_2.head()
    # s_2019_2.head()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## 21""")
    return


@app.cell
def _():
    # j_2021=pd.read_excel('./input/pre_2021.xlsx')
    # j_2021['index_edition_id']='2021'
    # j_2021['weight']=0
    # j_2021['question_type']="0"

    # j_2021 = j_2021.drop(columns=['T'])




    # c_2021 = j_2021[['Componente','index_edition_id', 'weight']].drop_duplicates().copy()

    # c_2021 = c_2021.rename(columns={"Componente": "name"})
    # c_2021["id"] = [uuid.uuid4() for _ in range(len(c_2021))]

    # c_2021 = c_2021[['id', 'index_edition_id', 'name', 'weight']]



    # v_2021 = j_2021[['Componente', 'Variable', 'index_edition_id', 'weight']].drop_duplicates().copy()

    # v_2021 = v_2021.rename(columns={"Variable": "name"})
    # v_2021["id"] = [uuid.uuid4() for _ in range(len(v_2021))]

    # v_2021 = v_2021.merge(
    #     c_2021[['name', 'id']], 
    #     left_on='Componente', 
    #     right_on='name', 
    #     how='left'
    # ).rename(columns={'id_y': 'component_id', 'name_x': 'name', 'id_x': 'id'}).drop(columns=['Componente', 'name_y'])

    # v_2021 = v_2021[['id', 'index_edition_id', 'component_id', 'name', 'weight']]



    # i_2021 = j_2021[['Variable', 'Indicador', 'index_edition_id', 'weight']].drop_duplicates().copy()

    # i_2021 = i_2021.rename(columns={"Indicador": "name"})
    # i_2021["id"] = [uuid.uuid4() for _ in range(len(i_2021))]

    # i_2021 = i_2021.merge(
    #     v_2021[['name', 'id']], 
    #     left_on='Variable', 
    #     right_on='name', 
    #     how='left'
    # ).rename(columns={'id_y': 'variable_id', 'name_x': 'name', 'id_x': 'id'}).drop(columns=['Variable', 'name_y'])

    # i_2021 = i_2021[['id', 'index_edition_id', 'variable_id', 'name', 'weight']]



    # p_2021 = j_2021[['Indicador', 'Pregunta', 'index_edition_id', 'weight', 'question_type']].drop_duplicates().copy()

    # p_2021 = p_2021.rename(columns={"Pregunta": "name"})
    # p_2021["id"] = [uuid.uuid4() for _ in range(len(p_2021))]

    # p_2021 = p_2021.merge(
    #     i_2021[['name', 'id']], 
    #     left_on='Indicador', 
    #     right_on='name', 
    #     how='left'
    # ).rename(columns={'id_y': 'indicador_id', 'name_x': 'name', 'id_x': 'id'}).drop(columns=['Indicador', 'name_y'])

    # p_2021 = p_2021[['id', 'index_edition_id', 'indicador_id', 'name', 'weight', 'question_type']]
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## 23""")
    return


@app.cell
def _():
    # j_2023=pd.read_excel('./input/pre_2023.xlsx')
    # j_2023['index_edition_id']='2023'
    # j_2023['weight']=0
    # j_2023['question_type']="0"

    # j_2023 = j_2023.drop(columns=['T'])




    # c_2023 = j_2023[['Componente','index_edition_id', 'weight']].drop_duplicates().copy()

    # c_2023 = c_2023.rename(columns={"Componente": "name"})
    # c_2023["id"] = [uuid.uuid4() for _ in range(len(c_2023))]

    # c_2023 = c_2023[['id', 'index_edition_id', 'name', 'weight']]



    # v_2023 = j_2023[['Componente', 'Variable', 'index_edition_id', 'weight']].drop_duplicates().copy()

    # v_2023 = v_2023.rename(columns={"Variable": "name"})
    # v_2023["id"] = [uuid.uuid4() for _ in range(len(v_2023))]

    # v_2023 = v_2023.merge(
    #     c_2023[['name', 'id']], 
    #     left_on='Componente', 
    #     right_on='name', 
    #     how='left'
    # ).rename(columns={'id_y': 'component_id', 'name_x': 'name', 'id_x': 'id'}).drop(columns=['Componente', 'name_y'])

    # v_2023 = v_2023[['id', 'index_edition_id', 'component_id', 'name', 'weight']]



    # i_2023 = j_2023[['Variable', 'Indicador', 'index_edition_id', 'weight']].drop_duplicates().copy()

    # i_2023 = i_2023.rename(columns={"Indicador": "name"})
    # i_2023["id"] = [uuid.uuid4() for _ in range(len(i_2023))]

    # i_2023 = i_2023.merge(
    #     v_2023[['name', 'id']], 
    #     left_on='Variable', 
    #     right_on='name', 
    #     how='left'
    # ).rename(columns={'id_y': 'variable_id', 'name_x': 'name', 'id_x': 'id'}).drop(columns=['Variable', 'name_y'])

    # i_2023 = i_2023[['id', 'index_edition_id', 'variable_id', 'name', 'weight']]



    # p_2023 = j_2023[['Indicador', 'Pregunta', 'index_edition_id', 'weight', 'question_type']].drop_duplicates().copy()

    # p_2023 = p_2023.rename(columns={"Pregunta": "name"})
    # p_2023["id"] = [uuid.uuid4() for _ in range(len(p_2023))]

    # p_2023 = p_2023.merge(
    #     i_2023[['name', 'id']], 
    #     left_on='Indicador', 
    #     right_on='name', 
    #     how='left'
    # ).rename(columns={'id_y': 'indicador_id', 'name_x': 'name', 'id_x': 'id'}).drop(columns=['Indicador', 'name_y'])

    # p_2023 = p_2023[['id', 'index_edition_id', 'indicador_id', 'name', 'weight', 'question_type']]
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Unificado""")
    return


@app.cell
def _():
    # c = pd.concat([c_2019_2, c_2021, c_2023])
    return


@app.cell
def _():
    # v = pd.concat([v_2019_2, v_2021, v_2023])
    return


@app.cell
def _():
    # i = pd.concat([i_2019_2, i_2021, i_2023])
    return


@app.cell
def _():
    # p = pd.concat([p_2019_2, p_2021, p_2023])
    return


@app.cell
def _():
    # c.to_csv('./output/componentes.csv',index=False,sep='|',quotechar='"',escapechar="'")
    # v.to_csv('./output/variables.csv',index=False,sep='|',quotechar='"',escapechar="'")
    # i.to_csv('./output/indicadores.csv',index=False,sep='|',quotechar='"',escapechar="'")
    # p.to_csv('./output/preguntas.csv',index=False,sep='|',quotechar='"',escapechar="'")
    return


if __name__ == "__main__":
    app.run()
