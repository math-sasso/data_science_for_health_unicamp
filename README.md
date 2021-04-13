# data_science_for_health_unicamp

# Projeto `Perfil de morbidade e mortalidade de recém-nascido com anomalias congênitas no Brasil entre 2005 a 2019.`

# Project `<Title in English>`

# Apresentação

O presente projeto foi originado no contexto das atividades da disciplina de pós-graduação [_Ciência e Visualização de Dados em Saúde_](https://github.com/datasci4health/home), oferecida no primeiro semestre de 2021, na Unicamp.

| Nome                             | RA     | Especialização |
| -------------------------------- | ------ | -------------- |
| Matheus Gustavo Alves Sasso      | 158257 | Computação     |
| Giancarlo Schaffer Torres Junior | 263890 | Computação     |
| Maria Estela de Oliveira Paiva   | 263885 | Computação     |
| Kedma Teixeira Montedori         | 098182 | Saúde          |

# Descrição Resumida do Projeto

Projeto é motivada pela especialidade da Kedma na área de desenvolvimento infantil. Sabendo que as malformações congênitas representam importante problema de saúde pública, tendo em vista suas repercussões no crescimento e desenvolvimento infantil nosso projeto contempla os pontos a seguir:

- Interface a qual seja possível verificar as causas de disfunções de malformação de nascidos vivos podendo ser consultadas por estado/microrregião.

- Sistema de inteligência artificial que retornará o impacto de cada variável de entrada para que seja predita uma classe de anomalia na saída.

[Vídeo de Apresentação](https://youtu.be/DN1tSBkntmY)

# Perguntas de Pesquisa

Qual o perfil de morbidade e mortalidade dos recém-nascidos com anomalias congênitas de acordo com os estados brasileiros no período entre 2005 a 2019?

# Bases de Dados

A base de dados utilizada no problema em questão é o SINASC do datasus, o qual, possui dados a respeito de nascidos vivos estão separados por estado, e com temporalidade de 1994 a 2019.

# Metodologia

Análise descritiva dos dados presentes no banco dos SINASC investigando as correlações e projeções.

# Ferramentas

Python e libs (Pysus, pandas…) para tratar dados e criar modelo, React para desenvolver interface front-end, Fast API.

# Cronograma

| Etapas                                                  | Semanas   |
| ------------------------------------------------------- | --------- |
| Seleção inicial dos dados e Pré-processamento dos dados | 4 semanas |
| Data mining                                             | 3 semanas |
| Interface web                                           | 2 semanas |
| Criação de apis                                         | 1 semana  |
| Integração com interface e deploy                       | 1 semana  |
| Relatório                                               | 3 semanas |
| Testes e correções                                      | 2 semanas |

|                                                         | 1   | 2   | 3   | 4   | 5   | 6   | 7   | 8   | 9   | 10  |
| ------------------------------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Seleção inicial dos dados e Pré-processamento dos dados | X   | X   | X   | X   |     |     |     |     |     |     |
| Data mining                                             |     |     |     |     | X   | X   | X   |     |     |     |
| Interface web                                           |     |     |     |     | X   | X   |     |     |     |     |
| Criação de apis                                         |     |     |     |     |     |     | X   |     |     |     |
| Integração com interface e deploy                       |     |     |     |     |     |     |     | X   |     |     |
| Relatório                                               |     |     |     | X   |     |     |     | X   |     | X   |
| Testes e correções                                      |     |     |     |     |     |     |     |     | X   | X   |

# Project Organization

---

    ├── LICENSE
    ├── Makefile           <- Makefile with commands like `make data` or `make train`
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── external       <- Data from third party sources.
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── docs               <- A default Sphinx project; see sphinx-doc.org for details
    │
    ├── models             <- Trained and serialized models, model predictions, or model summaries
    │
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                         the creator's initials, and a short `-` delimited description, e.g.
    │                         `1.0-jqp-initial-data-exploration`.
    │
    ├── references         <- Data dictionaries, manuals, and all other explanatory materials.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    ├── setup.py           <- makes project pip installable (pip install -e .) so src can be imported
    ├── src                <- Source code for use in this project.
    │   ├── __init__.py    <- Makes src a Python module
    │   │
    │   ├── data           <- Scripts to download or generate data
    │   │   └── make_dataset.py
    │   │
    │   ├── features       <- Scripts to turn raw data into features for modeling
    │   │   └── build_features.py
    │   │
    │   ├── models         <- Scripts to train models and then use trained models to make
    │   │   │                 predictions
    │   │   ├── predict_model.py
    │   │   └── train_model.py
    │   │
    │   └── visualization  <- Scripts to create exploratory and results oriented visualizations
    │       └── visualize.py
    │
    └── tox.ini            <- tox file with settings for running tox; see tox.readthedocs.io

---

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
