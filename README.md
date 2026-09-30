# 🏥 Dashboard Executivo - Gestão Clínica & Análise de Absenteísmo
![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![Power BI](https://img.shields.io/badge/Power_BI-Analytics-F2C94C?style=for-the-badge&logo=powerbi&logoColor=black)

## 📌 Visão Geral do Projeto

Este projeto consiste na construção de uma **solução end-to-end de Business Intelligence** voltada para a gestão operacional e financeira de uma rede clínica. O objetivo principal foi mapear o impacto financeiro do **absenteísmo de pacientes (Taxa de No-Show / Faltas)** sobre o faturamento total da instituição.

A solução cobre todo o ciclo de vida dos dados: da geração sintética e persistência relacional até a modelagem dimensional e construção de um painel executivo interativo.

---

## 🖼️ Preview do Dashboard
![Dashboard Executivo de Gestão Clínica](dashboard)
---

## 🏗️ Arquitetura da Solução
1. **Geração de Dados Sintéticos (Python):** Simulação de 1.500 atendimentos clínicos reais mantendo uma taxa média de 18% de absenteísmo, dados demográficos de pacientes e distribuição por especialidades e cidades.
2. **Armazenamento Relacional (SQLite):** Estruturação das tabelas relacionais no banco `clinica.db`.
3. **Modelagem de Dados (Power BI):** Construção de um esquema em estrela (*Star Schema*) otimizado para alta performance de filtragem.
4. **Métricas Avançadas (DAX):** Cálculo dinâmico de indicadores chave de desempenho (KPIs) de faturamento e taxas operacionais.

---

## 📊 Modelagem de Dados & Esquema Dimensional

A modelagem segue o padrão **Star Schema**, garantindo relacionamentos limpos de 1 : N (*um para muitos*):

* **Tabela Fato:**
  * `consultas` (ID, Data/Hora, Valor, Status, ID_Paciente, ID_Profissional)
* **Tabelas Dimensão:**
  * `pacientes` (ID_Paciente, Nome, Cidade, Idade)
  * `profissionais` (ID_Profissional, Nome, Especialidade)

---

## 📐 Principais Medidas DAX Desenvolvidas

* **Faturamento Total:**
  ```dax
  Faturamento Total = SUM(consultas[valor])
  Consultas Não Comparecidas (%) = 
DIVIDE(
    CALCULATE(COUNT(consultas[id_consulta]), consultas[status] = "Faltou"),
    COUNT(consultas[id_consulta])
)
