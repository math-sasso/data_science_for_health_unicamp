# data_science_for_health_unicamp

# Projeto `Perfil de morbidade de recém-nascido com anomalias congênitas no Brasil entre 2010 a 2019.`

# Project `Morbidity profile of newborns with congenital anomalies in Brazil between 2010 and 2019.`

# Apresentação

O presente projeto foi originado no contexto das atividades da disciplina de pós-graduação \f, oferecida no primeiro semestre de 2021, na Unicamp.

| Nome                             | RA     | Especialização |
| -------------------------------- | ------ | -------------- |
| Matheus Gustavo Alves Sasso      | 158257 | Computação     |
| Giancarlo Schaffer Torres Junior | 263890 | Computação     |
| Maria Estela de Oliveira Paiva   | 263885 | Computação     |
| Kedma Teixeira Montedori         | 098182 | Saúde          |

# Descrição Resumida do Projeto

Projeto é motivado pela especialidade da Kedma na área de desenvolvimento infantil. Sabendo que as malformações congênitas representam importante problema de saúde pública, tendo em vista suas repercussões no crescimento e desenvolvimento infantil nosso projeto contempla os pontos a seguir:

- Interface a qual seja possível verificar o perfil de malformação de nascidos vivos podendo ser consultadas por macroregião no estado de São Paulo.

- Aplicaçãp de inteligência artificial que detectará anomalias a partir de cada variável de entrada.

- Estudo da influência das variáveis de entrada para a identificação de cada anomalia.

- Estudo dos modelos que mais se adequam para a classificação de cada tipo de anomalia.

**Aplicações**:

- Aplicação de predição de anomalias com dados do SINASC: [preditor-anomalias](https://datasus-app.herokuapp.com/)

- Aplicação para visualização de dados do SINASC: 
  - [Site](https://sinasc.netlify.app/#/)
  - [Repositório](https://github.com/schafferjrdev/datasci4health-frontend)
  - [Repositório API](https://github.com/Estela01/data_science_for_health_unicamp_backend)

# Perguntas de Pesquisa

Qual o perfil de morbidade dos recém-nascidos com anomalias congênitas no período entre 2010 a 2019 para o estado de São Paulo?

# Metodologia

Foram extraidos do SINASC , base do Datasus com dados de recém nascidos vivos, todos os dados correspontes ao intervalo de 2010 a 2019 para o Sudeste,dos quais dados foram extraídos aqueles de recém nascidos que possuiam anomalias referentes aos grupos do boletim epidemiológico publicado em 2021.

Rotulou-se com a classe 1 os recém nascidos que possuiam a anomalia e aleatoriamente escolhou-se o mesmo numero de recém nascidos que não possuiam a anomalia de interesse . Os dados categóricos foram codificados em one hot e após isso normalizou-se todos os dados dentro de um MinMax Scaler. Utilizou-se o AutoML para identificar o modelo com melhor performance para cada grupo de anomalia e ao comparar este o resultado do mesmo com a classificação  XGBOOST, selecionou-se aquele que possuia a maior acurácia.

Ademais, é importante ressaltar que primeiramente os modelos foram calculados apenas considerando os dados do Estado de São Paulo. Em seguida ao utilizar os dados referentes ao Sudeste verificou-se uma melhora signifitiva no resultado dos modelos por haver maior número de exemplares com anomalias.

Além disso, para visualização, construiu-se uma interface web para visualização dos dados brutos anuais de 2010 a 2019 destes grupos de anomalias para cada macrorregião no estado de São Paulo. O objetivo deste é facilitar a compreensão do problema a partir de uma visualização espacial e temporal das incidências de anomalia.


# Bases de Dados

A base de dados utilizada no problema em questão é o SINASC do DATASUS, o qual, possui dados a respeito de nascidos vivos estão separados por estado, e com temporalidade de 1994 a 2019. Entrtanto escolheu-se para a modelagem estatística apenas os estados do Sudeste (São Paulo, Rio de Janeiro, Espírito Santo e Minas Gerais) para limitar o contexto dos dados devido a grande quantidade e o periodo de 2010 a 2019, pois antes de 2010 menos dados eram oferecidos pela base.

É importante salientar que por o git não suportar uma grande quantidade de dados no projeto, utilizou-se a ferramenta [DVC](https://dvc.org/doc/start), a qual possibilita a colocar os dados do projeto no google drive apenas incluindo uma referência com extensão .dvc no github. Com esta referência e comandos da aplicação é possível baixar os dados na máquina local.

## Bases Estudadas e Adotadas

A base utilizada foi o SINASC, entrtanto para fazer a coleta dos dados utilizou-se o pacote PySUS.

Base de Dados | Endereço na Web | Resumo descritivo
----- | ----- | -----
SINASC | [http://tabnet.datasus.gov.br/cgi/deftohtm.exe?sinasc/cnv/nvuf.def](http://www2.datasus.gov.br/DATASUS/index.php?area=0205&id=6936&VObj=http://tabnet.datasus.gov.br/cgi/deftohtm.exe?sinasc/cnv/nv)| Base de dados do DATASUS sobre nascidos vivos.


- O que descobriu sobre esse banco?
É possível utilizar as colunas cruzadas com os estados uma a uma pelo site. O PySUS surgiu como altenativa para fazer a coleta automatizada.

- Quais as transformações e tratamentos (e.g., dados faltantes e limpeza) feitos?
Descoberta dos valores que correspondiam a valores nulos não intuitivos, através da leitura dos relatórios
Dados inputados em variáveis numéricas NaN com o Iterative Imputer do sklearn
Dados inputados em variáveis categóricas NaN pelo valor máximo
One Hot encoding das variáveis categóricas

- Por que este banco foi adotado?
Principal base de dados brasileira sobre nascidos vivos

- Apresente aqui uma Análise Exploratória (inicial) sobre esta base.
Visualização dos histogramas dos dados, valores faltantes e tipos dos dados. Além disso foi necessário entender o relatório do SINASC para saber o significado de cada uma das variáveis, que ja estavam codificadas na base.

## Bases Estudadas mas Não Adotadas

Desde o início, a única base analisada foi a base do SINASC


# Ferramentas

* Python e libs (PySUS, pandas…) para tratar dados e criar modelo
* DVC para fazer o storage dos dados 
* React para desenvolver interface front-end
* Fast API para servir os resultados para o front-end
* Streamlit para subir a aplicação de IA sem a necessidade de HTML
* Heroku para hospedar as aplicações e desta forma possuir uma URL Pública 

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
├── LICENSE <br>
├── README.md          <- apresentação do projeto <br>
│ <br>
│── data <br>
│   ├── external       <- dados de terceiros <br>
│   ├── interim        <- dados intermediários, e.g., resultado de transformação <br>
│   ├── processed      <- dados finais usados para a modelagem <br>
│   └── raw            <- dados originais sem modificações <br>
│ <br>
├── small_data         <- Dados que precisavam estar no GIT e não no DVC <br>
│  <br>
├── notebooks          <- Jupyter notebooks ou equivalentes <br>
│ <br>
├── src                <- fonte em linguagem de programação ou sistema (e.g., Orange) <br>
│   └── README.md      <- instruções básicas de instalação/execução <br>
│ <br>
└── assets             <- mídias usadas no projeto <br>

---


<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>

# Como rodar este projeto?

## Dockerfile (Sera utilizado na intragração do sistema)
Para garantir que é possível importar todas as bibliotecas basta buildar e rodar o dockerfile com os seguintes comandos na raiz do projeto.

Buildar docker image
```bash
sudo docker build -t ds_health_img .
```

Rodando o dockerfile
```bash
sudo docker run -it -p 8080:8080 --name ds_health -v $(pwd):/app ds_health_img
```


## Preparando para rodar Notebooks 

Para rodar o notebook, é necessário criar uma Virtual ENV e instalar as bibliotecas demandadas pelo projeto através do comando:
```bash
python3 venv -m .venv
source .venv/bin/activate
pip install -r requirements.txt
```

# Resultados

## Sindrome de Down

[sindrome_down](./notebooks/sindrome_down)

## Cardiopatias Congênitas

[cardiopatias_congenitas](./notebooks/cardiopatias_congenitas)

## Fendas Orais

[fendas_orais](./notebooks/fendas_orais)

## Anomalias em Membros

[anomalias_membros](./notebooks/membros)

## Microcefalia

[microcefalia](./notebooks/microcefalia)

## Anomalias nas Paredes Abdominais

[paredes_abdominais](./notebooks/paredes_abdominais)

## Anomalias no Tubo Neural

[tubo_neural](./notebooks/tubo_neural)


# Parecer Técnico

## Grupos de Anomalias Congênitas prioritárias

De acordo com o recente boletim epidemiológico aproximadamente 6% dos nascidos vivos (dados globais) foram diagnosticados com algum tipo de anomalia. Com cerca de 295 mil mortes nas primeiras quatro semanas de vida por ocasião de anomalia congênita. (Ministério da Saúde,2021)
No Brasil as anomalias congênitas representam a segunda principal causa de morte e embora anualmente aproximadamente 24 mil recém-nascidos sejam registrados com algum tipo de anomalia, sabe-se que tais valores possam ser superados visto que a subnotificação ainda é uma frequente realidade.
O MAPA RESULTANTE DESSE PROJETO conduz e amplia o olhar acerca de como as anomalias congênitas se distribuem no estado de São Paulo, com destaque para anomalias mais prevalentes para cada cidade. Vale, contudo, lembrar que este ainda represente um protótipo que passará por ajustes de ordem técnica, além disso a literatura já adverte que distribuição das anomalias congênitas ainda é subestimada em diversas cidades, o que inclusive pode representar um sinalizador para políticas públicas voltadas ao fortalecimento das notificações. 
Os achados obtidos, incluído as predições, não nos permitem estabelecer relações de causalidade, mas favorecem inferências robustas a exemplo notem a similaridade da distribuição das consultas pré-natal/mês em todas as anomalias prioritárias. Esses resultados provavelmente representem o não cumprimento das exigências do Ministério da Saúde relativos às consultas pré-natal (sendo a primeira consulta no primeiro trimestre e as demais distribuídas ao longo dos meses até a 34ºsemana – 7º mês sendo exigido um mínimo 6 consultas). À literatura inclusive adverte a importância de uma assistência pré-natal qualificada ao longo de todo o período gestacional na prevenção de anomalias congênitas a partir de ações de educação em saúde: planejamento familiar, gestação de risco por ocasião de idade, orientação a evitar exposição a agentes teratogênicos, histórico de recorrências familiares, além da suplementação adequada.
Com base nesses aspectos, uma análise exploratória por regiões favorece o levantamento de riscos mais sensíveis para ocorrências das anomalias por território. O que provavelmente permita formulação de estratégias mais eficazes dos desdobramentos decorrentes das disfunções instaladas para cada grupo de anomalia; de modo que haja um aprimoramento das políticas públicas de atenção à saúde do recém-nascido com e sem anomalias. A partir de uma qualificação das ações preventivas, desde o planejamento reprodutivo ao desenvolvimento gestacional, assim como no cuidado e reabilitação após o nascimento do sujeito acometido por anomalia, promovendo melhores condições de vida, crescimento e desenvolvimento dentro de cada território.

## Parecer ampliado para Síndrome de Down

O termo “síndrome” significa um conjunto de sinais e sintomas e “Down” designa o sobrenome do médico e pesquisador que primeiro descreveu a associação dos sinais característicos da pessoa com Síndrome de Down (SD)
A SD ou trissomia do 21 é uma condição humana geneticamente determinada, é a alteração cromossômica (cromossomopatia) mais comum em humanos e a principal causa de deficiência intelectual na população. A SD é um modo de estar no mundo que demonstra a diversidade humana. A presença do cromossomo 21 extra na constituição genética determina características físicas específicas e atraso no desenvolvimento. Sabe-se que as pessoas com SD quando atendidas e estimuladas adequadamente, têm potencial para uma vida saudável e plena inclusão social. No Brasil nasce uma criança com SD a cada 600 e 800 nascimentos, independente de etnia, gênero ou classe social.
As diferenças entre as pessoas com SD, tanto do aspecto físico quanto de desenvolvimento, decorrem de aspectos genéticos individuais, intercorrências clínicas, nutrição, estimulação, educação, contexto familiar, social e meio ambiente. Apesar dessas diferenças, há um consenso da comunidade científica de que não se atribuem graus à SD. Um dado importante recorrente e atualmente descrito no boletim epidemiológico de 2021 revela que nos nascidos com síndrome de Down, um alto percentual de mães com idade avançada foi identificado. Acrescenta-se também a importância do índice ou escore APGAR, um teste feito no recém-nascido logo após o nascimento que avalia seu estado geral e vitalidade, que auxilia na identificação da necessidade de qualquer tipo de tratamento ou cuidado médico extra após o nascimento. Embora o índice de Apgar seja uma avaliação rotineira da vitalidade do bebê tem ganhado destaque como uma ferramenta útil para prever condição de saúde da mãe, sugere um estudo publicado no “JAMA Pediatrics”. Contudo, o fato de o recém-nascido não ter “tirado” uma “nota” alta não significa que ele terá algum atraso no desenvolvimento, mas permite inferir que o bebê precisou de mais ajuda na adaptação à vida fora do conforto do útero. Apesar das informações e experiência acumulada nos últimos anos, não é possível prever qual o grau de autonomia que uma criança com SD terá na sua vida adulta. O potencial a ser desenvolvido é sempre uma fronteira a ser cruzada diariamente. No entanto, é consenso para as equipes que atuam no cuidado da pessoa com SD que todo investimento em saúde, educação e inclusão social resulta em uma melhor qualidade de vida e autonomia. Para tanto é importante um conhecimento das relações dos indicadores de risco para manifestações sindrômicas assim como compreensão das possíveis desordens já instaladas bem como a prevenção destas.
O aconselhamento Genético (AG) consiste em uma destas alternativas sendo o mais adotado o da American Society of Human Genetics (EPSTEIN, 1975). Segundo esta definição, trata-se do processo de comunicação que lida com problemas humanos associados com a ocorrência, ou risco de ocorrência, de uma doença genética em uma família, envolvendo a participação de uma ou mais pessoas treinadas para ajudar o indivíduo ou sua família a: 1) compreender os fatos médicos, incluindo o diagnóstico, provável curso da doença e as condutas disponíveis; 2) apreciar o modo como a hereditariedade contribui para a doença e o risco de recorrência para parentes específicos; 3) entender as alternativas para lidar com o risco de recorrência; 4) escolher o curso de ação que pareça apropriado em virtude do seu risco, objetivos familiares, padrões éticos e religiosos, atuando de acordo com essa decisão; 5) ajustar-se, da melhor maneira possível, à situação imposta pela ocorrência do distúrbio na família, bem como à perspectiva de recorrência do mesmo. No caso do AG as famílias com uma pessoa com SD, este processo é muitas vezes realizado pelo pediatra, médico assistente ou equipe aconselhamento dentro das normas estabelecidas pela comunidade médica, seguindo padrões éticos e técnicos adequados. Recomenda-se ainda que o cuidado com a saúde da pessoa com SD seja norteado pelas políticas públicas do Ministério da Saúde como a Política Nacional de Humanização, Política Nacional da Atenção Básica, Programas de Saúde da Criança e do Adolescente, Saúde da Mulher, do Homem, do Idoso, Saúde Mental e no Relatório Mundial sobre a Deficiência. Cada vez mais a sociedade está se conscientizando de como é importante valorizar a diversidade humana e de como é fundamental oferecer equidade de oportunidades para que as pessoas com deficiência exerçam seu direito em conviver em comunidade. A sociedade está mais preparada para receber pessoas com síndrome de Down e existem relatos de experiências muito bem-sucedidas de inclusão.
 
 
## Conclusão
Destacar as principais conclusões obtidas no desenvolvimento do projeto.

Destacar os principais desafios enfrentados.

Principais lições aprendidas.

## Trabalhos Futuros
O que poderia ser melhorado se houvesse mais tempo?

## Referências Bibliográficas

[1] Cabral, JVB; Guimarães, ALS; Sobral Filho, DC; Santos, ACO. Mortality due to congenital heart disease in Pernambuco from 1996 to 2016. Rev. assoc. med bras.2020; 66(7):931-936. <br>
[2] Kale, PL et al. Ameaça à vida ao nascer: uma análise das causas de morte e estimativa de sobrevida de menores de cinco anos em coortes de nascidos vivos. Cad. Saúde Pública 2019; 35(7). <br>
[3] Luz, G.S. et al. Anomalias congênitas no estado do Rio Grande do Sul: análise de série temporal. Rev bras epidemiol. 2019; 22. <br>
[4] Ministério da Saúde (BR). Secretaria de Vigilância em Saúde. Anomalias congênitas no Brasil, 2010 a 2019: análise dos dados de sistemas de informação para o fortalecimento da vigilância e atenção em saúde. Brasília, DF: MS; 2021 [acesso 22 de junho. 2021]. Boletim Epidemiológico. V.52, fev. 2021. Disponível em: Boletim Epidemiológico <br>
[5] Ministério da Saúde (BR). Como nascem os brasileiros: captação e prevalência das anomalias congênitas. In: Saúde Brasil 2018: uma análise da situação de saúde e das doenças e agravos crônicos: desafios e perspectivas. Brasília, 2019. <br>
[6] Reis LV. Anomalias congênitas, identificadas ao nascimento, em filhos de mulheres adolescentes [tese]. São Paulo: Escola Paulista de Medicina. Universidade Federal de São Paulo; 2005. <br>
[7] Chen, Tianqi, and Carlos Guestrin. "Xgboost: A scalable tree boosting system." Proceedings of the 22nd acm sigkdd international conference on knowledge discovery and data mining. 2016. <br>
[8] Feurer, Matthias, et al. "Auto-sklearn 2.0: The next generation." arXiv preprint arXiv:2007.04074 (2020). <br>
[9] Pedregosa, Fabian, et al. "Scikit-learn: Machine learning in Python." the Journal of machine Learning research 12 (2011): 2825-2830. <br>
 

