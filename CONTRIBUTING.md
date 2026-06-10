# CONTRIBUTING.md

> Documento vivo. Todo o código submetido via Pull Request deve respeitar estas regras.  
> Qualquer excepção deve ser discutida e aprovada pelo lead antes de ser implementada.

---

## Índice

1. [Limites de Tamanho](#1-limites-de-tamanho)
2. [Nomenclatura](#2-nomenclatura)
3. [Estrutura de Funções](#3-estrutura-de-funções)
4. [Responsabilidade por Camada](#4-responsabilidade-por-camada)
5. [Tratamento de Erros](#5-tratamento-de-erros)
6. [Type Hints](#6-type-hints)
7. [Constantes](#7-constantes)
8. [Docstrings](#8-docstrings)
9. [Imports](#9-imports)
10. [Git & Pull Requests](#10-git--pull-requests)
11. [Checklist de PR](#11-checklist-de-pr)

---

## 1. Limites de Tamanho

| Unidade | Limite | Razão |
|---|---|---|
| Ficheiro `.py` | **200 linhas** | Acima disso, o ficheiro tem mais de uma responsabilidade |
| Função / método | **20 linhas** | Funções longas escondem lógica e dificultam testes |
| Classe | **150 linhas** | Classes grandes violam o princípio da responsabilidade única |
| Parâmetros por função | **4** | Acima disso, usar um schema ou dataclass |
| Níveis de indentação | **3** | Mais níveis indicam lógica que deve ser extraída |

---

## 2. Nomenclatura

**Regra geral:** o nome explica a intenção, não a implementação.

```python
# ❌
def calc(d, n):
    return d * n

# ✅
def calculate_gap_percentage(user_skills: list[str], required_skills: list[str]) -> float:
    ...
```

| Tipo | Convenção | Exemplo |
|---|---|---|
| Variável / parâmetro | `snake_case` | `user_profile`, `gap_percentage` |
| Função / método | `snake_case` — verbo + substantivo | `get_user`, `calculate_gap`, `send_alert` |
| Classe | `PascalCase` | `OrientationService`, `CheckInRepository` |
| Constante | `UPPER_SNAKE_CASE` | `CVV_THRESHOLD`, `MAX_RETRIES` |
| Ficheiro | `snake_case` | `mental_health_service.py` |
| Booleano | prefixo `is_` / `has_` / `can_` | `is_active`, `has_crisis`, `can_apply` |
| Enum value | `snake_case` | `GoalEnum.find_job` |

---

## 3. Estrutura de Funções

Toda a função segue o padrão: **validar → processar → retornar**.

```python
# ✅
async def apply_to_job(
    user_id: int,
    job_id: int,
    db: Session,
) -> JobApplicationResponse:
    # 1. Validar — guard clauses, falha cedo
    user = await user_repo.get_or_raise(user_id, db)
    job  = await job_repo.get_or_raise(job_id, db)

    # 2. Processar — lógica de negócio
    gap = calculate_gap(user.profile.skills, job.required_skills)

    # 3. Persistir e retornar
    application = await application_repo.create(user_id, job_id, gap, db)
    return JobApplicationResponse.model_validate(application)
```

### Guard Clauses — falha cedo, evita nesting

```python
# ❌ — nesting profundo
async def process_checkin(user_id, nota, db):
    user = db.get(User, user_id)
    if user:
        if user.is_active:
            if 0 <= nota <= 10:
                ...

# ✅ — guard clauses, lógica plana
async def process_checkin(user_id: int, nota: float, db: Session) -> CheckInResponse:
    user = await user_repo.get_or_raise(user_id, db)

    if not user.is_active:
        raise HTTPException(status_code=403, detail="User is inactive")

    if not (0 <= nota <= 10):
        raise ValueError("nota_semanal must be between 0 and 10")

    # lógica principal sem nesting
    ...
```

---

## 4. Responsabilidade por Camada

Cada camada faz exactamente uma coisa. Se uma função precisa de fazer duas, extrai uma.

| Camada | Responsabilidade |
|---|---|
| `routes/` | Recebe request, valida schema, chama service, devolve response |
| `services/` | Lógica de negócio pura — orquestra repositories e agents |
| `repositories/` | Acesso ao banco e queries SQL — sem lógica de negócio |
| `agents/` | Prompts e comunicação com IA — sem lógica de negócio |
| `models/` | Estrutura de dados — sem lógica de negócio |
| `schemas/` | Validação de I/O — sem lógica de negócio |

```python
# ❌ — route com lógica de negócio
@router.post("/orientar")
async def orientar(request: OrientarRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == request.usuario_id).first()
    skills_gap = list(set(job.required_skills) - set(user.profile.skills))
    gap_pct = len(skills_gap) / len(job.required_skills)
    ...

# ✅ — route delega ao service
@router.post("/orientar", response_model=OrientarResponse)
async def orientar(
    request: OrientarRequest,
    db: Session = Depends(get_db),
    service: OrientationService = Depends(get_orientation_service),
):
    return await service.orientar(request, db)
```

---

## 5. Tratamento de Erros

### Nunca silenciar erros

```python
# ❌
try:
    result = await agent.generate(prompt)
except Exception:
    pass

# ✅
try:
    result = await agent.generate(prompt)
except AnthropicAPIError as e:
    logger.error("AI agent failed: %s", e)
    raise HTTPException(status_code=503, detail="AI service temporarily unavailable")
```

### Excepções de domínio próprias

Definidas em `app/core/exceptions.py`:

```python
class AppBitException(Exception):
    """Base exception do projecto."""

class UserNotFoundException(AppBitException):
    def __init__(self, user_id: int):
        super().__init__(f"User {user_id} not found")

class CrisisDetectedException(AppBitException):
    def __init__(self, user_id: int, nota: float):
        super().__init__(f"Crisis detected for user {user_id} with nota {nota}")
```

---

## 6. Type Hints

Obrigatório em todas as funções — parâmetros e retorno.

```python
# ❌
def calculate_gap(user_skills, required_skills):
    missing = set(required_skills) - set(user_skills)
    return len(missing) / len(required_skills)

# ✅
def calculate_gap(
    user_skills: list[str],
    required_skills: list[str],
) -> float:
    if not required_skills:
        return 0.0
    missing = set(required_skills) - set(user_skills)
    return round(len(missing) / len(required_skills), 2)
```

---

## 7. Constantes

Nunca usar magic numbers. Toda a constante tem nome e vive no módulo onde faz sentido semanticamente.

```python
# ❌
if nota < 4:
    derivar_cvv = True

# ✅ — constante nomeada em app/models/mental_health.py
CVV_THRESHOLD = 4.0

if nota < CVV_THRESHOLD:
    derivar_cvv = True
```

---

## 8. Docstrings

Não documentes o óbvio. Documenta a **intenção** e as **decisões não óbvias**.

```python
# ❌ — inútil
def get_user(user_id: int, db: Session) -> User:
    """Gets a user."""
    ...

# ✅ — documenta a decisão de negócio
def calculate_gap(user_skills: list[str], required_skills: list[str]) -> float:
    """
    Calcula a percentagem de requisitos em falta.

    Retorna 0.0 se required_skills estiver vazio — vaga sem requisitos
    é considerada 100% compatível com qualquer perfil.
    """
    ...

# ✅ — documenta comportamento crítico e mandatório
async def process_checkin(user_id: int, nota: float, db: Session) -> CheckInResponse:
    """
    Processa check-in diário de saúde mental.

    Se nota < CVV_THRESHOLD (4.0), cria automaticamente um CrisisAlert
    e activa derivar_cvv=True na resposta. Este comportamento é mandatório
    e não deve ser alterado sem revisão do lead.
    """
    ...
```

---

## 9. Imports

Ordem obrigatória seguindo PEP 8:

```python
# 1. Biblioteca padrão
import enum
from datetime import datetime

# 2. Bibliotecas externas
from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session

# 3. Módulos internos do projecto
from app.core.config import settings
from app.models.user import User
from app.schemas.orientar import OrientarRequest, OrientarResponse
```

Import wildcard é proibido:

```python
# ❌
from app.models import *
```

---

## 10. Git & Pull Requests

### Branches

```
main
 └── develop
      ├── feature/orientar      ← backend lead
      └── feature/saude         ← programador 2
```

- Nenhum push directo para `main` ou `develop`
- Todo o trabalho parte de uma branch de feature
- Merge em `develop` apenas via Pull Request aprovado pelo lead

### Mensagens de Commit — Conventional Commits

```
feat: add /orientar endpoint with gap calculation
fix: correct CVV threshold to 4.0
refactor: extract gap logic to orientation_service
test: add unit tests for mental health service
docs: update README with local setup instructions
```

### Regras de Pull Request

- Mínimo **1 aprovação** do lead antes de mergir
- Máximo **200 linhas alteradas** por PR — PRs grandes não são revistos com qualidade
- Cada PR resolve **uma única coisa** — não misturar features com fixes

### O que nunca deve ser commitado

```
.env
__pycache__/
*.pyc
.venv/
```

Verifica o `.gitignore` antes do primeiro commit.

---

## 11. Checklist de PR

Antes de abrir um Pull Request, confirma cada ponto:

```
[ ] Ficheiro tem menos de 200 linhas?
[ ] Todas as funções têm type hints (parâmetros e retorno)?
[ ] Não há magic numbers — apenas constantes nomeadas?
[ ] Não há lógica de negócio nas routes?
[ ] Não há queries SQL nos services?
[ ] Erros são tratados explicitamente — nenhum except vazio?
[ ] A mensagem de commit segue o formato Conventional Commits?
[ ] O ficheiro .env não foi incluído no commit?
```
