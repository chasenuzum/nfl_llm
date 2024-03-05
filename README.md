# NFL Large Language Model (LLM) Project

## Overview
This project aims to analyze NFL (National Football League) data from the year 2008 to the present using Python and Llama-2. The project involves processing, analyzing, and visualizing various aspects of NFL data to derive insights and patterns for fantasy football.

## Features
- **SQL Database:** SQL Lite database ready for use of NFL data.
- **Data Analysis:** Performing exploratory data analysis (EDA) to understand trends, patterns, and relationships within the dataset.
- **Chroma DB:** Creation of Chroma DB and embeddings for use in RAG.
- **Visualization:** Creating informative visualizations such as plots, charts, and graphs to illustrate findings in a intuitive front end.
- **RAG and SQL agent duo:** Utilize a comboination of RAG and SQL agents in Langchain to balance precision of data (SQL) and semantic understanding of unstructured data (RAG) in responses.
- **LLM Interface in Streamlit:** Spin up streamlit QA chat bot to discuss roster formation.
- **API Integration from Major Fantasy Providers:** ESPN and Sleeper Roster ingestion in front end interface.

## Requirements
- Python 3.x
- Pandas
- NumPy
- Langchain
- Chromadb
- Ollama

## Installation
1. Clone the repository:
`git clone https://github.com/chasenuzum/nfl_llm.git`

2. Install the required Python packages:
`pip install -r requirements.txt`


## Usage
1. Spin up Ollama and Llama2 https://ollama.com/download
2. Run the python file:
`python run.py`
3. Wait until download, embeddings, finish
4. Open local port listed in terminal

## Contributing
Contributions are welcome! If you'd like to contribute to this project, please follow these steps:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature/new-feature`).
3. Make your changes.
4. Commit your changes (`git commit -am 'Add new feature'`).
5. Push to the branch (`git push origin feature/new-feature`).
6. Create a new Pull Request.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments
- The [nfl-data-py](https://pypi.org/project/nfl-data-py/) team for providing the dataset.
- Contributors to libraries used in this project