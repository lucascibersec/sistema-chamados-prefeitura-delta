# 🛠️ Sistema de Chamados TI - Prefeitura de Delta

Este sistema foi desenvolvido pela **Delta Cyber Security LTDA** para gerenciar e centralizar as demandas técnicas de uma prefeitura, abrangendo setores como Administração, Educação e Saúde. O projeto prioriza a **integridade dos dados** e a **segurança da informação**.

## 🛡️ Segurança e Integridade (Core Cybersec)
Como um projeto focado em Cibersegurança, o sistema possui camadas de proteção críticas no Firebase Firestore:
* **Bloqueio de Deleção**: Implementamos a regra `allow delete: if false`, garantindo que nenhum chamado possa ser apagado, mantendo um histórico auditável e imutável.
* **Validação de Identidade**: O sistema exige Nome e Sobrenome para a criação de novos chamados, garantindo a rastreabilidade do solicitante.
* **Proteção Global**: Regras de segurança que restringem o acesso apenas às coleções autorizadas, prevenindo vazamentos de informações.

## 🚀 Funcionalidades Principais
* **Painel Administrativo**: Visualização em tempo real de novos chamados com exibição imediata da descrição do problema.
* **Chat em Tempo Real**: Sistema de mensagens entre técnico e usuário com notificações visuais de mensagens não lidas.
* **Relatórios em PDF**: Geração de relatórios mensais automáticos contendo o histórico detalhado de todas as soluções aplicadas.

## 👥 Equipe de Desenvolvimento (Delta Cyber Security)
* **Lucas** - Lead Cybersecurity & Backend Architecture
* **Ramon** - Fullstack Developer
* **Ezequias** - Developer & Systems Analyst
* **Jean** - Developer

## 💻 Tecnologias Utilizadas
* **Frontend**: HTML5, CSS3 (Glassmorphism UI) e Bootstrap 5.
* **Backend**: Firebase Firestore (NoSQL) para sincronização em tempo real.
* **Bibliotecas**: jsPDF e jspdf-autotable para documentação oficial.