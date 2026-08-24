// Módulo compartilhado de anexos (fotos/arquivos) dos chamados.
// Usado por painel.html (usuário) e admin.html (técnico) — mantém a lógica
// de seleção, upload e exibição em um único lugar.
//
// Os arquivos NÃO vão para o Firebase — ficam salvos em disco na própria VPS,
// através da API Flask em server/app.py. O Firestore continua guardando só
// os metadados do anexo (nome, tipo, tamanho, url) dentro do chamado.

// Se a API (server/app.py) estiver no mesmo domínio do site (Nginx fazendo
// proxy de /api e /uploads pro Flask), deixe "". Se ela rodar num
// domínio/porta diferente, troque para algo como "https://api.seudominio.com.br".
export const UPLOAD_API_ORIGIN = "";

export const ANEXO_ACCEPT = "image/*,application/pdf,.doc,.docx,.xls,.xlsx,.txt";
export const ANEXO_MAX_MB = 10;
export const ANEXO_MAX_FILES = 5;

export function iconeArquivo(tipo) {
    tipo = tipo || "";
    if (tipo.startsWith("image/")) return "bi-file-earmark-image";
    if (tipo === "application/pdf") return "bi-file-earmark-pdf";
    if (tipo.includes("word")) return "bi-file-earmark-word";
    if (tipo.includes("sheet") || tipo.includes("excel")) return "bi-file-earmark-excel";
    if (tipo.startsWith("text/")) return "bi-file-earmark-text";
    return "bi-file-earmark";
}

function formatarTamanho(bytes) {
    if (!bytes) return "";
    if (bytes < 1024) return bytes + " B";
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(0) + " KB";
    return (bytes / (1024 * 1024)).toFixed(1) + " MB";
}

/**
 * Mescla novos arquivos escolhidos com os já selecionados, validando
 * quantidade máxima e tamanho máximo por arquivo.
 * @returns {{arquivos: File[], erros: string[]}}
 */
export function adicionarArquivos(fileList, existentes) {
    const erros = [];
    const arquivos = [...existentes];
    for (const f of Array.from(fileList)) {
        if (arquivos.length >= ANEXO_MAX_FILES) {
            erros.push(`Máximo de ${ANEXO_MAX_FILES} anexos por envio.`);
            break;
        }
        if (f.size > ANEXO_MAX_MB * 1024 * 1024) {
            erros.push(`"${f.name}" excede ${ANEXO_MAX_MB}MB e foi ignorado.`);
            continue;
        }
        arquivos.push(f);
    }
    return { arquivos, erros };
}

/** HTML de pré-visualização (antes do envio). `onRemoveFn` é o nome global da função de remoção. */
export function renderPreview(arquivos, onRemoveFn) {
    if (!arquivos.length) return "";
    return arquivos.map((f, i) => {
        const isImg = f.type.startsWith("image/");
        const url = URL.createObjectURL(f);
        return `<div class="anexo-chip">
            ${isImg ? `<img src="${url}" class="anexo-thumb" alt="">` : `<i class="bi ${iconeArquivo(f.type)} anexo-file-ico"></i>`}
            <span class="anexo-nome" title="${f.name}">${f.name}</span>
            <span class="anexo-tam">${formatarTamanho(f.size)}</span>
            <button type="button" class="anexo-remove" onclick="${onRemoveFn}(${i})" aria-label="Remover anexo"><i class="bi bi-x"></i></button>
        </div>`;
    }).join("");
}

/**
 * Sobe os arquivos para a API de anexos (server/app.py), que salva em disco
 * na VPS dentro de `chamados/{chamadoId}/{pasta}/`.
 * @param {string} idToken - token do Firebase Auth do usuário logado (auth.currentUser.getIdToken()).
 * @param {string} chamadoId - id do documento do chamado no Firestore.
 * @param {"abertura"|"mensagens"} pasta
 * @param {File[]} arquivos
 * @returns {Promise<Array<{nome:string, tipo:string, tamanho:number, url:string, path:string}>>}
 */
export async function subirAnexos(idToken, chamadoId, pasta, arquivos) {
    const formData = new FormData();
    formData.append("pasta", pasta);
    arquivos.forEach(f => formData.append("arquivo", f));

    const resp = await fetch(`${UPLOAD_API_ORIGIN}/api/chamados/${encodeURIComponent(chamadoId)}/anexos`, {
        method: "POST",
        headers: { "Authorization": `Bearer ${idToken}` },
        body: formData
    });
    if (!resp.ok) {
        const corpo = await resp.json().catch(() => ({}));
        throw new Error(corpo.erro || `Falha ao enviar anexos (HTTP ${resp.status}).`);
    }
    const { anexos } = await resp.json();
    return anexos.map(a => ({ ...a, url: UPLOAD_API_ORIGIN + a.url }));
}

/** HTML dos anexos já enviados (cards/chat) — imagem clicável, demais arquivos como chip com ícone. */
export function renderAnexosEnviados(anexos) {
    if (!anexos || !anexos.length) return "";
    return `<div class="anexos-lista">${anexos.map(a => {
        const isImg = (a.tipo || "").startsWith("image/");
        return `<a href="${a.url}" target="_blank" rel="noopener" class="anexo-item" title="${a.nome}">
            ${isImg
                ? `<img src="${a.url}" class="anexo-thumb" alt="${a.nome}">`
                : `<i class="bi ${iconeArquivo(a.tipo)} anexo-file-ico"></i><span class="anexo-item-nome">${a.nome}</span>`}
        </a>`;
    }).join("")}</div>`;
}
