#!/bin/bash

# =============================================================================
# App BiT — Script de criação da estrutura do projecto
# Uso: bash setup_project.sh
# =============================================================================

set -e  # Para imediatamente se algum comando falhar

PROJECT_NAME="appbit-backend"

echo "🚀 A criar estrutura do projecto: $PROJECT_NAME"

# -----------------------------------------------------------------------------
# Raiz do projecto
# -----------------------------------------------------------------------------
mkdir -p $PROJECT_NAME
cd $PROJECT_NAME

# -----------------------------------------------------------------------------
# Aplicação principal
# -----------------------------------------------------------------------------
mkdir -p app/core
mkdir -p app/models
mkdir -p app/schemas
mkdir -p app/repositories
mkdir -p app/services
mkdir -p app/agents
mkdir -p app/api/v1/routes

# -----------------------------------------------------------------------------
# Testes (espelham a estrutura de app/)
# -----------------------------------------------------------------------------
mkdir -p tests/unit/services
mkdir -p tests/unit/repositories
mkdir -p tests/integration/routes

# -----------------------------------------------------------------------------
# Alembic (migrations)
# -----------------------------------------------------------------------------
mkdir -p alembic/versions

# -----------------------------------------------------------------------------
# Ficheiros Python — app/
# -----------------------------------------------------------------------------
touch app/__init__.py
touch app/main.py

# -----------------------------------------------------------------------------
# Ficheiros Python — app/core/
# -----------------------------------------------------------------------------
touch app/core/__init__.py
touch app/core/config.py       # Settings via pydantic-settings
touch app/core/database.py     # Engine + SessionLocal + get_db
touch app/core/security.py     # JWT + hashing
touch app/core/exceptions.py   # Excepções de domínio (AppBitException, etc.)
touch app/core/logger.py       # Configuração de logging

# -----------------------------------------------------------------------------
# Ficheiros Python — app/models/
# -----------------------------------------------------------------------------
touch app/models/__init__.py        # Exporta todos os models para o Alembic
touch app/models/base.py            # DeclarativeBase + timestamps
touch app/models/user.py            # User + UserProfile
touch app/models/job.py             # Job + JobApplication
touch app/models/course.py          # Course + UserCourse
touch app/models/mentorship.py      # Mentor + MentorshipSession
touch app/models/mental_health.py   # CheckIn + CrisisAlert
touch app/models/event.py           # Event + EventRegistration

# -----------------------------------------------------------------------------
# Ficheiros Python — app/schemas/
# -----------------------------------------------------------------------------
touch app/schemas/__init__.py
touch app/schemas/user.py           # UserCreate, UserResponse, UserProfileUpdate
touch app/schemas/auth.py           # TokenResponse, LoginRequest
touch app/schemas/orientar.py       # OrientarRequest, OrientarResponse
touch app/schemas/saude.py          # SaudeRequest, SaudeResponse
touch app/schemas/job.py            # JobResponse, JobApplicationResponse
touch app/schemas/course.py         # CourseResponse, UserCourseResponse
touch app/schemas/mentorship.py     # MentorResponse, SessionRequest
touch app/schemas/event.py          # EventResponse, EventRegistrationResponse

# -----------------------------------------------------------------------------
# Ficheiros Python — app/repositories/
# -----------------------------------------------------------------------------
touch app/repositories/__init__.py
touch app/repositories/base_repo.py        # CRUD genérico reutilizável
touch app/repositories/user_repo.py        # Queries de User + UserProfile
touch app/repositories/job_repo.py         # Queries de Job + match por perfil
touch app/repositories/course_repo.py      # Queries de Course + recomendação
touch app/repositories/checkin_repo.py     # Queries de CheckIn + CrisisAlert
touch app/repositories/mentorship_repo.py  # Queries de Mentor + Session
touch app/repositories/event_repo.py       # Queries de Event + geolocalização

# -----------------------------------------------------------------------------
# Ficheiros Python — app/services/
# -----------------------------------------------------------------------------
touch app/services/__init__.py
touch app/services/auth_service.py             # Login, register, JWT
touch app/services/user_service.py             # Gestão de perfil
touch app/services/orientation_service.py      # Lógica do /orientar + gap
touch app/services/mental_health_service.py    # Lógica do /saude + CVV
touch app/services/mentorship_service.py       # Agendamento de sessões
touch app/services/event_service.py            # Filtro por geolocalização CDRView

# -----------------------------------------------------------------------------
# Ficheiros Python — app/agents/
# -----------------------------------------------------------------------------
touch app/agents/__init__.py
touch app/agents/base_agent.py              # Classe base com chamada à API Anthropic
touch app/agents/orientation_agent.py       # Prompt de gap + trilha sugerida
touch app/agents/mental_health_agent.py     # Prompt de saúde mental + CVV

# -----------------------------------------------------------------------------
# Ficheiros Python — app/api/
# -----------------------------------------------------------------------------
touch app/api/__init__.py
touch app/api/v1/__init__.py
touch app/api/v1/router.py              # Agrega todas as routes de v1

touch app/api/v1/routes/__init__.py
touch app/api/v1/routes/auth.py         # POST /auth/register, POST /auth/login
touch app/api/v1/routes/users.py        # GET /users/me, PUT /users/me
touch app/api/v1/routes/orientar.py     # POST /orientar
touch app/api/v1/routes/saude.py        # POST /saude
touch app/api/v1/routes/jobs.py         # GET /jobs
touch app/api/v1/routes/courses.py      # GET /courses
touch app/api/v1/routes/mentorship.py   # GET /mentors, POST /sessions
touch app/api/v1/routes/events.py       # GET /events

# -----------------------------------------------------------------------------
# Ficheiros Python — tests/
# -----------------------------------------------------------------------------
touch tests/__init__.py
touch tests/conftest.py                             # Fixtures partilhadas (db, client)

touch tests/unit/__init__.py
touch tests/unit/services/__init__.py
touch tests/unit/services/test_orientation_service.py
touch tests/unit/services/test_mental_health_service.py

touch tests/unit/repositories/__init__.py
touch tests/unit/repositories/test_user_repo.py

touch tests/integration/__init__.py
touch tests/integration/routes/__init__.py
touch tests/integration/routes/test_orientar.py
touch tests/integration/routes/test_saude.py

# -----------------------------------------------------------------------------
# Alembic
# -----------------------------------------------------------------------------
touch alembic/env.py
touch alembic/script.py.mako
touch alembic.ini

# -----------------------------------------------------------------------------
# Raiz do projecto — ficheiros de configuração
# -----------------------------------------------------------------------------
touch .env.example
touch .gitignore
touch requirements.txt
touch README.md
touch Makefile

# -----------------------------------------------------------------------------
# Conteúdo inicial dos ficheiros principais
# -----------------------------------------------------------------------------

# .gitignore
cat > .gitignore << 'EOF'
# Ambiente virtual
.venv/
venv/

# Variáveis de ambiente — NUNCA subir para o repositório
.env

# Python
__pycache__/
*.pyc
*.pyo
*.pyd
.Python

# Testes
.pytest_cache/
.coverage
htmlcov/

# IDEs
.vscode/
.idea/

# Sistema operativo
.DS_Store
EOF

# .env.example — template sem valores reais
cat > .env.example << 'EOF'
DATABASE_URL=postgresql://user:password@localhost:5432/appbit
SECRET_KEY=your-secret-key-here
ANTHROPIC_API_KEY=your-anthropic-key-here
ENVIRONMENT=development
EOF

# Makefile — comandos úteis do dia a dia
cat > Makefile << 'EOF'
run:
	uvicorn app.main:app --reload

migrate:
	alembic upgrade head

migration:
	alembic revision --autogenerate -m "$(msg)"

test:
	pytest tests/ -v

install:
	pip install -r requirements.txt

freeze:
	pip freeze > requirements.txt
EOF

# requirements.txt — dependências do projecto
cat > requirements.txt << 'EOF'
fastapi
uvicorn[standard]
sqlalchemy
alembic
psycopg2-binary
pydantic-settings
python-jose[cryptography]
passlib[bcrypt]
python-dotenv
anthropic
httpx
pytest
pytest-asyncio
EOF

# -----------------------------------------------------------------------------
# Resultado final
# -----------------------------------------------------------------------------
echo ""
echo "✅ Estrutura criada com sucesso!"
echo ""
echo "Próximos passos:"
echo "  cd $PROJECT_NAME"
echo "  python -m venv .venv"
echo "  source .venv/bin/activate"
echo "  cp .env.example .env"
echo "  make install"
echo "  make run"
