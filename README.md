### Descrição do Projeto

# ClaroTraining Insights

## Descrição

### Visão Geral
O projeto ClaroTraining Insights é um sistema de dashboard desenvolvido para a área de treinamento da Claro, que visa fornecer insights detalhados e visualizações interativas sobre os cursos oferecidos. Utilizando o framework Streamlit para a criação de visualizações dinâmicas, o sistema analisa dados de cursos e gera métricas quantitativas e qualitativas para apoiar a tomada de decisões na gestão de treinamentos.

### Componentes Principais

#### 1. Dados dos Cursos
Os dados dos cursos são armazenados em um arquivo Excel (`cursos_combined_matched.xlsx`) localizado no diretório `data`. Esse arquivo contém informações sobre os cursos oferecidos, categorizadas por tipo de habilidade (Hard Skill e Soft Skill) e distribuídas entre diferentes diretores.

#### 2. Configurações do Sistema
As configurações da aplicação, incluindo variáveis de ambiente e outras configurações gerais, estão definidas no arquivo `config/settings.py`. Variáveis de ambiente são usadas para carregar essas configurações de forma segura a partir do arquivo `.env`.

#### 3. Configuração de Logs
Os logs da aplicação são configurados no arquivo `config/log_config.py`. O sistema de logging utiliza um `RotatingFileHandler` para rotação de arquivos de log, e os logs são gravados tanto em arquivos quanto no console.




## Estrutura do Projeto

```plaintext
ClaroTrainingInsights/
│
├── config/
│   ├── log_config.py
│   └── settings.py
│
├── controllers/
│   └── course_controller.py
│
├── services/
│   └── course_service.py
│
├── data/
│   └── cursos_combined_matched.xlsx
│
├── main.py
└── .env
