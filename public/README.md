🛠️ Sistema de Chamados TI - Prefeitura de Delta
Este sistema foi desenvolvido pela Delta Cyber Security LTDA para gerenciar e centralizar as demandas técnicas de uma prefeitura, abrangendo setores como Administração, Educação e Saúde. O foco principal é a integridade dos dados e a rastreabilidade das soluções.

🛡️ Segurança e Integridade (Core Cybersec)
Como um projeto de Cibersegurança, o sistema possui camadas de proteção críticas no Firebase Firestore:

Bloqueio de Deleção: Implementamos a regra allow delete: if false, garantindo que nenhum chamado possa ser apagado, mantendo um histórico auditável e imutável para a prefeitura.

Validação de Dados: Todos os formulários possuem validação obrigatória de Nome e Sobre nome, seguindo as diretrizes de identificação do projeto.

Proteção Global: Regras de segurança que restringem o acesso apenas às coleções autorizadas, prevenindo vazamentos de informações.

🚀 Funcionalidades
Painel Administrativo Atualizado: Visualização imediata da descrição do problema enviada pelo usuário, facilitando o diagnóstico rápido.

Notificações em Tempo Real: Sistema de alertas visuais (bolinha pulsante) para novas mensagens não lidas no chat.

Relatórios em PDF: Geração de relatórios mensais automáticos contendo o histórico de interações e a solução final de cada chamado.

Filtros de Urgência: Organização automática por níveis de prioridade (Alta, Média e Baixa).

👥 Equipe de Desenvolvimento (Delta Cyber Security)
Lucas - Lead Cybersecurity & Backend Architecture

Ramon - Fullstack Developer

Ezequias - Developer & Systems Analyst

Jean - Developer

💻 Tecnologias
Frontend: HTML5, CSS3 (Glassmorphism UI) e Bootstrap 5.

Backend: Firebase Firestore (NoSQL) para sincronização em tempo real.

Bibliotecas: jsPDF e jspdf-autotable para documentação oficial.