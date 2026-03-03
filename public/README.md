🛠️ Sistema de Chamados TI - Prefeitura de Delta
Este sistema foi desenvolvido pela Delta Cyber Security LTDA para centralizar e gerenciar chamados técnicos de diversos setores da prefeitura, como Saúde, Educação e Gabinete. O projeto prioriza a segurança da informação e a rastreabilidade das soluções.

🛡️ Segurança e Integridade (Cybersec)
O sistema utiliza o Firebase Firestore com regras de segurança rigorosas:

Bloqueio de Deleção: Implementamos allow delete: if false, garantindo que nenhum chamado seja apagado, preservando o histórico para auditoria.

Identificação Obrigatória: O sistema exige Nome e Sobrenome para a criação de novos chamados.

Proteção Global: Regras que impedem acessos não autorizados a outros documentos do banco de dados.

🚀 Funcionalidades Principais
Painel Administrativo: Visualização em tempo real de novos chamados com exibição da descrição detalhada do problema.

Chat Interno: Comunicação direta entre técnicos e usuários com notificações visuais para novas mensagens.

Relatórios PDF: Geração de documentos com o histórico completo dos atendimentos para fins gerenciais.

👥 Equipe de Desenvolvimento (Delta Cyber Security)
Lucas - Lead Cybersecurity & Backend Architecture

Ramon - Fullstack Developer

Ezequias - Developer & Systems Analyst

Jean - Developer

💻 Tecnologias Utilizadas
Frontend: HTML5, CSS3 (Glassmorphism design) e Bootstrap 5.

Backend: Firebase Firestore (NoSQL) para sincronização em tempo real.

Bibliotecas: jsPDF e jspdf-autotable para documentação.