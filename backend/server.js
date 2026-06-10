const http = require("http");

const PORT = process.env.PORT || 3000;
const MAX_BODY_BYTES = 1_000_000;

function sendJson(res, statusCode, body) {
  res.writeHead(statusCode, {
    "Content-Type": "application/json; charset=utf-8",
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type"
  });
  res.end(JSON.stringify(body));
}

function computeGapPercentual(nivel) {
  const normalized = String(nivel || "").toLowerCase();
  if (normalized.includes("pleno")) return 20;
  if (normalized.includes("senior")) return 15;
  return 30;
}

function buildOrientarResponse(payload) {
  const gapPercentual = computeGapPercentual(payload.nivel);
  const aderenciaBase = Math.max(0, 100 - gapPercentual);

  return {
    gap_percentual: gapPercentual,
    gap_itens: [
      "Prática em projetos reais",
      "Networking com mentores",
      "Fortalecer inglês técnico"
    ],
    trilha_sugerida: [
      "Trilha cloud fundamentals",
      "Projeto guiado de portfólio",
      "Mentoria quinzenal de carreira"
    ],
    vagas_compativeis: [
      {
        titulo: "Estágio em Desenvolvimento",
        empresa: "Parceira BiT",
        aderencia_percentual: aderenciaBase
      },
      {
        titulo: "Pessoa Desenvolvedora Júnior",
        empresa: "Comunidade Tech Inclusiva",
        aderencia_percentual: Math.max(0, aderenciaBase - 2)
      }
    ],
    confianca: 0.82
  };
}

const server = http.createServer((req, res) => {
  if (req.method === "OPTIONS") {
    return sendJson(res, 204, {});
  }

  if (req.method === "POST" && req.url === "/orientar") {
    const contentType = req.headers["content-type"] || "";
    if (!contentType.includes("application/json")) {
      return sendJson(res, 415, { error: "Content-Type deve ser application/json" });
    }

    let body = "";
    let total = 0;

    req.on("data", (chunk) => {
      total += chunk.length;
      if (total > MAX_BODY_BYTES) {
        req.destroy();
      } else {
        body += chunk.toString("utf8");
      }
    });

    req.on("error", () => sendJson(res, 400, { error: "Requisição inválida" }));

    req.on("end", () => {
      try {
        const payload = JSON.parse(body || "{}");
        const required = ["usuario_id", "perfil", "nivel", "regiao", "idioma", "lat", "lng"];
        const missing = required.filter((key) => payload[key] === undefined || payload[key] === null || payload[key] === "");

        if (missing.length > 0) {
          return sendJson(res, 400, { error: `Campos obrigatórios ausentes: ${missing.join(", ")}` });
        }

        return sendJson(res, 200, buildOrientarResponse(payload));
      } catch {
        return sendJson(res, 400, { error: "JSON inválido" });
      }
    });
    return;
  }

  sendJson(res, 404, { error: "Rota não encontrada" });
});

server.listen(PORT, () => {
  console.log(`App BiT backend em http://localhost:${PORT}`);
});
