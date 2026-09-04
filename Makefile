.PHONY: up down logs build
build: ; docker compose build
up:    ; docker compose build && docker compose up -d
down:  ; docker compose down
logs:  ; docker compose logs -f
