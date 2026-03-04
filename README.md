🛠️ Sistema de Chamados TI - Prefeitura de Delta
Este sistema foi desenvolvido pela Delta Cyber Security LTDA para gerenciar e centralizar as demandas técnicas de uma prefeitura, abrangendo setores como Administração, Educação e Saúde. O projeto foca em integridade de dados, transparência e comunicação em tempo real.

🛡️ Segurança e Integridade (Core Cybersec)
Como um projeto focado em Cibersegurança, o sistema possui camadas de proteção críticas no Firebase Firestore:

Bloqueio de Deleção: Implementamos a regra allow delete: if false, garantindo que nenhum chamado possa ser apagado, mantendo um histórico auditável e imutável para a prefeitura.

Validação de Identidade: Todos os formulários possuem validação obrigatória de Nome e Sobrenome, garantindo a rastreabilidade de quem abriu o chamado.

Proteção Global: Regras de segurança que restringem o acesso apenas às coleções autorizadas, prevenindo vazamentos de informações.

🚀 Funcionalidades Principais
Painel Administrativo: Visualização clara de chamados com exibição imediata da descrição detalhada do problema.

Chat em Tempo Real: Sistema de mensagens entre técnico e usuário com notificações visuais de mensagens não lidas.

Relatórios em PDF: Geração de relatórios mensais automáticos contendo o histórico detalhado de todas as soluções aplicadas.

Filtros Inteligentes: Organização por urgência (Alta, Média, Baixa) e status de atendimento.

👥 Equipe de Desenvolvimento (Delta Cyber Security)
Lucas - Lead Cybersecurity & Backend Architecture

Ramon - Fullstack Developer

Ezequias - Estudante de Sistemas de Informação pela Uniube     

Jean - Developer

Gustavo - Ultimo periodo em Engenharia Da Computação (Uniube)

💻 Tecnologias Utilizadas
Frontend: HTML5, CSS3 (Glassmorphism UI) e Bootstrap 5.

Backend: Firebase Firestore (NoSQL) para sincronização em tempo real.

Bibliotecas: jsPDF e jspdf-autotable para a geração de documentos PDF oficiais.
