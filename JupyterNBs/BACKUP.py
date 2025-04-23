import marimo

__generated_with = "0.13.0"
app = marimo.App()


@app.cell
def _():
    #!pip3 install fuzzywuzzy python-Levenshtein
    return


@app.cell
def _():
    import uuid
    import pandas as pd
    return pd, uuid


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        # Entidad y sector
        """
    )
    return


@app.cell
def _(pd):
    entidades=pd.read_excel('./input/entidades.xlsx')
    entidades.to_csv('./output/entidades.csv',index=False,sep='|',quotechar='"',escapechar="'")
    entidades.head()
    return (entidades,)


@app.cell
def _(pd):
    sectors=pd.read_excel('./input/sectores.xlsx')
    sectors.to_csv('./output/sectores.csv',index=False,sep='|',quotechar='"',escapechar="'")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        # Respuestas
        """
    )
    return


@app.cell
def _(pd):
    full_hierarchy=pd.read_excel('./input/full_hierarchy.xlsx')
    full_hierarchy[full_hierarchy['index_year']==2023].tail()
    return


@app.cell
def _(pd):
    resp_19=pd.read_excel('./input/resp_2019.xlsx')
    resp_21=pd.read_excel('./input/resp_2021.xlsx')
    resp_23=pd.read_excel('./input/resp_2023.xlsx')
    return resp_19, resp_21, resp_23


@app.cell
def _(resp_19, resp_21, resp_23):
    ans_2019 = resp_19.copy().drop(columns=['Dirección de correo electrónico']).dropna(axis=1, how='all')
    ans_2021 = resp_21.copy().dropna(axis=1, how='all')
    ans_2023 = resp_23.copy().drop(columns=['nombre_responde', 'dependencia_entidad', 'cargo_responde', 'correo_personal', 'correo_institucional', 'tel']).dropna(axis=1, how='all')
    return ans_2019, ans_2021, ans_2023


@app.cell
def _(ans_2019, ans_2021, ans_2023, entidades):
    # Assuming the 'entidades' DataFrame has the 'entidad' column with text and 'uuid' column with the corresponding UUIDs
    entidad_dict = dict(zip(entidades['name'], entidades['id']))

    # Apply the mapping to replace entidad text with uuid in each DataFrame
    ans_2019['entidad'] = ans_2019['entidad'].replace(entidad_dict)
    ans_2021['entidad'] = ans_2021['entidad'].replace(entidad_dict)
    ans_2023['entidad'] = ans_2023['entidad'].replace(entidad_dict)
    return


@app.cell
def _(ans_2019, ans_2021, ans_2023):
    df_19_melted = ans_2019.melt(id_vars=['entidad'], var_name='question', value_name='answer')
    df_21_melted = ans_2021.melt(id_vars=['entidad'], var_name='question', value_name='answer')
    df_23_melted = ans_2023.melt(id_vars=['entidad'], var_name='question', value_name='answer')
    return df_19_melted, df_21_melted, df_23_melted


@app.cell
def _(df_19_melted, df_21_melted, df_23_melted):
    ques_2019=df_19_melted['question'].unique()
    ques_2021=df_21_melted['question'].unique()
    ques_2023=df_23_melted['question'].unique()
    return ques_2019, ques_2021, ques_2023


@app.cell
def _(pd, ques_2019, ques_2021, ques_2023):
    df_2019 = pd.DataFrame(ques_2019.tolist(), columns=["questions"])
    df_2021 = pd.DataFrame(ques_2021.tolist(), columns=["questions"])
    df_2023 = pd.DataFrame(ques_2023.tolist(), columns=["questions"])
    return df_2019, df_2021, df_2023


@app.cell
def _(df_2019, df_2021, df_2023):
    df_2019.to_excel('./input/df_2019.xlsx',index=False)
    df_2021.to_excel('./input/df_2021.xlsx',index=False)
    df_2023.to_excel('./input/df_2023.xlsx',index=False)
    return


@app.cell
def _(df_19_melted, df_21_melted, df_23_melted):
    df_19_melted.to_excel('./input/df_19_melted.xlsx',index=False)
    df_21_melted.to_excel('./input/df_21_melted.xlsx',index=False)
    df_23_melted.to_excel('./input/df_23_melted.xlsx',index=False)
    return


@app.cell
def _(df_19_melted):
    print(df_19_melted.head())
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        # Personas
        """
    )
    return


@app.cell
def _(entidades, resp_23, uuid):
    persons = resp_23[['entidad', 'nombre_responde', 'dependencia_entidad', 'cargo_responde', 'correo_personal', 'correo_institucional', 'tel']].drop_duplicates().copy()

    persons = persons.rename(columns={
            "nombre_responde": "name",
            "entidad": "entity",
            "dependencia_entidad": "area",
            "cargo_responde": "job_title",
            "correo_personal": "email_per",
            "correo_institucional": "email_ent",
            "tel": "phone"
        }).reset_index(drop=True)

    persons["id"] = 0

    # Perform the merge and rename the relevant columns
    persons = persons.merge(
        entidades[['id', 'name']],  # Keep 'id' and 'name' from entidades
        left_on='entity',           # Matching entity name in persons
        right_on='name',            # Matching entity name in entidades
        how='left'
    )

    # Drop the redundant columns and rename the ones we want to keep
    persons = persons.drop(columns=['name_y', 'id_x'])  # Drop 'name_y' and 'id_x'
    persons = persons.rename(columns={'id_y': 'entity_id', 'name_x': 'name'})  # Rename columns as needed

    persons["id"] = [uuid.uuid4() for _ in range(len(persons))]

    persons = persons[['id', 'name', 'email_per', 'email_ent', 'phone', 'area', 'job_title', 'entity_id']].drop_duplicates().copy()

    persons.to_csv('./output/persons.csv', index=False, sep='|', quotechar='"', escapechar="'")

    # Check the final result
    persons.head()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        # Indices
        """
    )
    return


@app.cell
def _(pd):
    data = {
        'id': [
            2019,
            2021,
            2023
            ],
        'description': [
            'El Índice de Innovación del 2019 contó con la participación de 39 entidades y generó la linea base del Distrito en innovación.',
            'El Índice de Innovación del 2019 contó con la participación de 68 entidades y añadió a todas las Alcaldías Locales',
            'El Índice de Innovación del 2019 contó con la participación de 69 entidades y amplió drásticamente la información al incorporar búcles con información descriptiva.',
        ]
        }
    indices = pd.DataFrame(data)
    indices.to_csv('./output/indices.csv',index=False,sep='|',quotechar='"',escapechar="'")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        # Jerarquia
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ## 19
        """
    )
    return


@app.cell
def _(pd):
    j_2019=pd.read_excel('./input/pre_2019.xlsx')
    j_2019['index_edition_id']='2019'
    j_2019['weight']=0
    j_2019['question_type']="0"

    j_2019 = j_2019.drop(columns=['T'])
    return (j_2019,)


@app.cell
def _(j_2019, uuid):
    c_2019 = j_2019[['Componente', 'index_edition_id', 'weight']].drop_duplicates().copy()
    v_2019 = j_2019[['Componente', 'Variable', 'index_edition_id', 'weight']].drop_duplicates().copy()
    i_2019 = j_2019[['Variable', 'Indicador', 'index_edition_id', 'weight']].drop_duplicates().copy()
    p_2019 = j_2019[['Indicador', 'Pregunta', 'index_edition_id', 'weight']].drop_duplicates().copy()
    s_2019 = j_2019[['Pregunta', 'SubPregunta', 'index_edition_id', 'weight']].drop_duplicates().copy()

    c_2019["componente_id"] = [uuid.uuid4() for _ in range(len(c_2019))]
    v_2019["variable_id"] = [uuid.uuid4() for _ in range(len(v_2019))]
    i_2019["indicador_id"] = [uuid.uuid4() for _ in range(len(i_2019))]
    p_2019["pregunta_id"] = [uuid.uuid4() for _ in range(len(p_2019))]
    s_2019["subpregunta_id"] = [uuid.uuid4() for _ in range(len(s_2019))]

    v_2019 = v_2019.merge(
        c_2019[['Componente', 'componente_id']], 
        on='Componente', 
        how='left'
    )

    i_2019 = i_2019.merge(
        v_2019[['Variable', 'variable_id']], 
        on='Variable', 
        how='left'
    )

    p_2019 = p_2019.merge(
        i_2019[['Indicador', 'indicador_id']], 
        on='Indicador', 
        how='left'
    )

    s_2019 = s_2019.merge(
        p_2019[['Pregunta', 'pregunta_id']], 
        on='Pregunta', 
        how='left'
    )
    return c_2019, i_2019, p_2019, s_2019, v_2019


@app.cell
def _(c_2019, i_2019, p_2019, s_2019, v_2019):
    c_2019_1 = c_2019.rename(columns={'componente_id': 'id'})
    v_2019_1 = v_2019.rename(columns={'componente_id': 'parent_id', 'variable_id': 'id', 'Componente': 'parent_text', 'Variable': 'text'})
    i_2019_1 = i_2019.rename(columns={'variable_id': 'parent_id', 'indicador_id': 'id', 'Variable': 'parent_text', 'Indicador': 'text'})
    p_2019_1 = p_2019.rename(columns={'indicador_id': 'parent_id', 'pregunta_id': 'id', 'Indicador': 'parent_text', 'Pregunta': 'text'})
    s_2019_1 = s_2019.rename(columns={'pregunta_id': 'parent_id', 'subpregunta_id': 'id', 'Pregunta': 'parent_text', 'SubPregunta': 'text'})
    return c_2019_1, i_2019_1, p_2019_1, s_2019_1, v_2019_1


@app.cell
def _(c_2019_1, i_2019_1, p_2019_1, s_2019_1, v_2019_1):
    c_2019_1['text'] = c_2019_1['Componente']
    c_2019_2 = c_2019_1[['index_edition_id', 'id', 'text', 'weight']]
    v_2019_2 = v_2019_1[['index_edition_id', 'id', 'parent_id', 'parent_text', 'text', 'weight']]
    i_2019_2 = i_2019_1[['index_edition_id', 'id', 'parent_id', 'parent_text', 'text', 'weight']]
    p_2019_2 = p_2019_1[['index_edition_id', 'id', 'parent_id', 'parent_text', 'text', 'weight']]
    s_2019_2 = s_2019_1[['index_edition_id', 'id', 'parent_id', 'parent_text', 'text', 'weight']]
    return c_2019_2, i_2019_2, p_2019_2, s_2019_2, v_2019_2


@app.cell
def _(i_2019_2, p_2019_2, s_2019_2, v_2019_2):
    v_2019_2.head()
    v_2019_2.head()
    i_2019_2.head()
    p_2019_2.head()
    s_2019_2.head()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ## 21
        """
    )
    return


@app.cell
def _(pd, uuid):
    j_2021=pd.read_excel('./input/pre_2021.xlsx')
    j_2021['index_edition_id']='2021'
    j_2021['weight']=0
    j_2021['question_type']="0"

    j_2021 = j_2021.drop(columns=['T'])




    c_2021 = j_2021[['Componente','index_edition_id', 'weight']].drop_duplicates().copy()

    c_2021 = c_2021.rename(columns={"Componente": "name"})
    c_2021["id"] = [uuid.uuid4() for _ in range(len(c_2021))]

    c_2021 = c_2021[['id', 'index_edition_id', 'name', 'weight']]



    v_2021 = j_2021[['Componente', 'Variable', 'index_edition_id', 'weight']].drop_duplicates().copy()

    v_2021 = v_2021.rename(columns={"Variable": "name"})
    v_2021["id"] = [uuid.uuid4() for _ in range(len(v_2021))]

    v_2021 = v_2021.merge(
        c_2021[['name', 'id']], 
        left_on='Componente', 
        right_on='name', 
        how='left'
    ).rename(columns={'id_y': 'component_id', 'name_x': 'name', 'id_x': 'id'}).drop(columns=['Componente', 'name_y'])

    v_2021 = v_2021[['id', 'index_edition_id', 'component_id', 'name', 'weight']]



    i_2021 = j_2021[['Variable', 'Indicador', 'index_edition_id', 'weight']].drop_duplicates().copy()

    i_2021 = i_2021.rename(columns={"Indicador": "name"})
    i_2021["id"] = [uuid.uuid4() for _ in range(len(i_2021))]

    i_2021 = i_2021.merge(
        v_2021[['name', 'id']], 
        left_on='Variable', 
        right_on='name', 
        how='left'
    ).rename(columns={'id_y': 'variable_id', 'name_x': 'name', 'id_x': 'id'}).drop(columns=['Variable', 'name_y'])

    i_2021 = i_2021[['id', 'index_edition_id', 'variable_id', 'name', 'weight']]



    p_2021 = j_2021[['Indicador', 'Pregunta', 'index_edition_id', 'weight', 'question_type']].drop_duplicates().copy()

    p_2021 = p_2021.rename(columns={"Pregunta": "name"})
    p_2021["id"] = [uuid.uuid4() for _ in range(len(p_2021))]

    p_2021 = p_2021.merge(
        i_2021[['name', 'id']], 
        left_on='Indicador', 
        right_on='name', 
        how='left'
    ).rename(columns={'id_y': 'indicador_id', 'name_x': 'name', 'id_x': 'id'}).drop(columns=['Indicador', 'name_y'])

    p_2021 = p_2021[['id', 'index_edition_id', 'indicador_id', 'name', 'weight', 'question_type']]
    return c_2021, i_2021, p_2021, v_2021


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ## 23
        """
    )
    return


@app.cell
def _(pd, uuid):
    j_2023=pd.read_excel('./input/pre_2023.xlsx')
    j_2023['index_edition_id']='2023'
    j_2023['weight']=0
    j_2023['question_type']="0"

    j_2023 = j_2023.drop(columns=['T'])




    c_2023 = j_2023[['Componente','index_edition_id', 'weight']].drop_duplicates().copy()

    c_2023 = c_2023.rename(columns={"Componente": "name"})
    c_2023["id"] = [uuid.uuid4() for _ in range(len(c_2023))]

    c_2023 = c_2023[['id', 'index_edition_id', 'name', 'weight']]



    v_2023 = j_2023[['Componente', 'Variable', 'index_edition_id', 'weight']].drop_duplicates().copy()

    v_2023 = v_2023.rename(columns={"Variable": "name"})
    v_2023["id"] = [uuid.uuid4() for _ in range(len(v_2023))]

    v_2023 = v_2023.merge(
        c_2023[['name', 'id']], 
        left_on='Componente', 
        right_on='name', 
        how='left'
    ).rename(columns={'id_y': 'component_id', 'name_x': 'name', 'id_x': 'id'}).drop(columns=['Componente', 'name_y'])

    v_2023 = v_2023[['id', 'index_edition_id', 'component_id', 'name', 'weight']]



    i_2023 = j_2023[['Variable', 'Indicador', 'index_edition_id', 'weight']].drop_duplicates().copy()

    i_2023 = i_2023.rename(columns={"Indicador": "name"})
    i_2023["id"] = [uuid.uuid4() for _ in range(len(i_2023))]

    i_2023 = i_2023.merge(
        v_2023[['name', 'id']], 
        left_on='Variable', 
        right_on='name', 
        how='left'
    ).rename(columns={'id_y': 'variable_id', 'name_x': 'name', 'id_x': 'id'}).drop(columns=['Variable', 'name_y'])

    i_2023 = i_2023[['id', 'index_edition_id', 'variable_id', 'name', 'weight']]



    p_2023 = j_2023[['Indicador', 'Pregunta', 'index_edition_id', 'weight', 'question_type']].drop_duplicates().copy()

    p_2023 = p_2023.rename(columns={"Pregunta": "name"})
    p_2023["id"] = [uuid.uuid4() for _ in range(len(p_2023))]

    p_2023 = p_2023.merge(
        i_2023[['name', 'id']], 
        left_on='Indicador', 
        right_on='name', 
        how='left'
    ).rename(columns={'id_y': 'indicador_id', 'name_x': 'name', 'id_x': 'id'}).drop(columns=['Indicador', 'name_y'])

    p_2023 = p_2023[['id', 'index_edition_id', 'indicador_id', 'name', 'weight', 'question_type']]
    return c_2023, i_2023, p_2023, v_2023


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ## Unificado
        """
    )
    return


@app.cell
def _(c_2019_2, c_2021, c_2023, pd):
    c = pd.concat([c_2019_2, c_2021, c_2023])
    return (c,)


@app.cell
def _(pd, v_2019_2, v_2021, v_2023):
    v = pd.concat([v_2019_2, v_2021, v_2023])
    return (v,)


@app.cell
def _(i_2019_2, i_2021, i_2023, pd):
    i = pd.concat([i_2019_2, i_2021, i_2023])
    return (i,)


@app.cell
def _(p_2019_2, p_2021, p_2023, pd):
    p = pd.concat([p_2019_2, p_2021, p_2023])
    return (p,)


@app.cell
def _(c, i, p, v):
    c.to_csv('./output/componentes.csv',index=False,sep='|',quotechar='"',escapechar="'")
    v.to_csv('./output/variables.csv',index=False,sep='|',quotechar='"',escapechar="'")
    i.to_csv('./output/indicadores.csv',index=False,sep='|',quotechar='"',escapechar="'")
    p.to_csv('./output/preguntas.csv',index=False,sep='|',quotechar='"',escapechar="'")
    return


@app.cell
def _():
    import marimo as mo
    return (mo,)


if __name__ == "__main__":
    app.run()
