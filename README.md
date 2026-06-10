# App BiT — MVP (backend + frontend)

Estrutura inicial para hackathon com:

- **Backend**: endpoint `POST /orientar` com retorno mockado e cálculo simples de gap.
- **Frontend**: interface responsiva com home + tela funcional de onboarding/orientação.

## Estrutura

```text
backend/
  package.json
  server.js
frontend/
  index.html
  styles.css
  app.js
```

## Requisitos

- Node.js 18+ (recomendado)

## Como executar localmente

### 1) Backend

```bash
cd /home/runner/work/S06-26-AB-EQUIPO-31-/S06-26-AB-EQUIPO-31-/No-Country-simulation/S06-26-AB-EQUIPO-31-/backend
npm start
```

Servidor padrão: `http://localhost:3000`

### 2) Frontend

Abra o arquivo abaixo no navegador:

`/home/runner/work/S06-26-AB-EQUIPO-31-/S06-26-AB-EQUIPO-31-/No-Country-simulation/S06-26-AB-EQUIPO-31-/frontend/index.html`

## Contrato principal implementado

### `POST /orientar`

Request (exemplo):

```json
{
  "usuario_id": "u-123",
  "perfil": "estudante",
  "nivel": "junior",
  "regiao": "Brasil/SP/São Paulo",
  "idioma": "pt-BR",
  "lat": -23.5505,
  "lng": -46.6333
}
```

Response (exemplo):

```json
{
  "gap_percentual": 30,
  "gap_itens": [
    "Prática em projetos reais",
    "Networking com mentores",
    "Fortalecer inglês técnico"
  ],
  "trilha_sugerida": [
    "Trilha cloud fundamentals",
    "Projeto guiado de portfólio",
    "Mentoria quinzenal de carreira"
  ],
  "vagas_compativeis": [
    {
      "titulo": "Estágio em Desenvolvimento",
      "empresa": "Parceira BiT",
      "aderencia_percentual": 70
    },
    {
      "titulo": "Pessoa Desenvolvedora Júnior",
      "empresa": "Comunidade Tech Inclusiva",
      "aderencia_percentual": 68
    }
  ],
  "confianca": 0.82
}
```

## Teste rápido com curl

```bash
curl -X POST http://localhost:3000/orientar \
  -H "Content-Type: application/json" \
  -d '{"usuario_id":"u-123","perfil":"estudante","nivel":"junior","regiao":"BR/SP","idioma":"pt-BR","lat":-23.55,"lng":-46.63}'
```