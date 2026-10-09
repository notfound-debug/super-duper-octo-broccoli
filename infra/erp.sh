#!/usr/bin/env bash
# Local ERPNext + India Compliance stack for Phase 0 (Docker, via vendor/frappe_docker).
# Usage: infra/erp.sh build | up | site | down | logs
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
FD="$ROOT/vendor/frappe_docker"
ENV="$ROOT/infra/.env.local"
COMPOSE="$ROOT/infra/compose.local.yaml"   # generated, gitignored (contains DB password)
SITE=merchant.localhost
dc() { docker compose -p merchant-erp -f "$COMPOSE" "$@"; }

case "${1:-}" in
  build)
    cd "$FD"
    docker build \
      --build-arg=FRAPPE_PATH=https://github.com/frappe/frappe \
      --build-arg=FRAPPE_BRANCH=version-16 \
      --secret=id=apps_json,src="$ROOT/infra/apps.json" \
      --tag=merchant-erp:16 \
      --file=images/layered/Containerfile .
    ;;
  up)
    cd "$FD"
    docker compose --env-file "$ENV" \
      -f compose.yaml \
      -f overrides/compose.mariadb.yaml \
      -f overrides/compose.redis.yaml \
      -f overrides/compose.noproxy.yaml \
      config > "$COMPOSE"
    dc up -d
    ;;
  site)
    set -a; . "$ENV"; set +a
    dc exec backend bench new-site "$SITE" \
      --mariadb-user-host-login-scope='172.%.%.%' \
      --db-root-password "$DB_PASSWORD" \
      --admin-password "$ADMIN_PASSWORD" \
      --install-app erpnext \
      --install-app india_compliance
    dc exec backend bench --site "$SITE" enable-scheduler
    echo "Open http://localhost:${HTTP_PUBLISH_PORT:-8080}  (user: Administrator, password: ADMIN_PASSWORD in infra/.env.local)"
    ;;
  down) dc down ;;
  logs) dc logs -f --tail=100 ;;
  *) echo "usage: $0 build|up|site|down|logs" >&2; exit 1 ;;
esac
