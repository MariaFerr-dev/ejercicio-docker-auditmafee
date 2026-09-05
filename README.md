-- Auditoría

## Tabla de hallazgos

| ID | Hallazgo inicial | Riesgo | Evidencia | Corrección aplicada |
|---|---|---|---|---|
| AUD-001 | Credenciales de BD escritas en `app.py` | Alto | `DB_USER`/`DB_PASS` en código original | Variables de entorno mediante `.env` |
| AUD-002 | Consulta SQL concatenada con entrada del usuario | Crítico | `/buscar` en código original | Validación de entero + consulta parametrizada |
| AUD-003 | `/health` podía fallar aleatoriamente | Alto | `random` y división por cero | Endpoint determinista |
| AUD-004 | Python 3.8 en imagen base | Medio | `Dockerfile` original | Python 3.12-slim |
| AUD-005 | Dependencias antiguas | Medio | `Dockerfile` original | `requirements.txt` con versiones actuales del proyecto |
| AUD-006 | Ejecución como root en contenedor | Medio | `Dockerfile` original | Usuario sin privilegios |
| AUD-007 | Sin orquestación local | Medio | No existía Compose | `docker-compose.yml` |
| AUD-008 | Sin automatización de pruebas/seguridad | Alto | No existía workflow | GitHub Actions: Pytest, Bandit y Trivy |

## Resultado

Los hallazgos iniciales fueron corregidos y las comprobaciones quedan automatizadas en `.github/workflows/ci.yml`:

- Pytest valida los endpoints principales.
- Bandit analiza el código de aplicación y publica `auditoria_bandit.txt` como artefacto.
- Trivy bloquea imágenes con vulnerabilidades `HIGH` o `CRITICAL` corregibles.
- El despliegue a EC2 se ejecuta solo desde `main` y requiere secretos de GitHub.

La auditoría local debe excluir `.venv`, porque es una copia de dependencias de terceros:

```bash
bandit -r app.py -f txt -o auditoria_bandit.txt
```
- http://api-despliegueaudi.duckdns.org/
- http://dockerdespliegueaudi.duckdns.org/
- http://kumadespliegueaudi.duckdns.org/dashboard