# 🔧 Environment Variables

NoteDiscovery supports environment variables to override configuration settings, allowing different behavior in different deployment environments (local, staging, production).

## 📋 Available Environment Variables

### Core Settings

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `PORT` | integer | `8000` | HTTP port for the application (Docker, run.py) |

> **Note**: Advanced server settings (CORS origins, debug mode) are configured via `config.yaml` only, not via environment variables. See [config.yaml](#advanced-server-configuration) for details.

### Authentication

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `AUTHENTICATION_ENABLED` | boolean | `config.yaml` | Enable/disable authentication |
| `AUTHENTICATION_PASSWORD_HASH` | string | `config.yaml` | Bcrypt password hash |
| `AUTHENTICATION_SECRET_KEY` | string | `config.yaml` | Session secret key (for session security) |

### Demo Mode

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `DEMO_MODE` | boolean | `false` | Enable demo mode (enables rate limiting and other demo restrictions) |

## 🎯 Configuration Priority

Configuration is loaded in this order (later overrides earlier):

1. **`config.yaml`** - Default configuration file
2. **Environment Variables** - Runtime overrides
3. **Command Line** - Highest priority (if applicable)

## 💡 Common Use Cases

### Use Case 1: Local Development (No Auth)

**Local setup:**
```bash
# No environment variables needed
# Uses config.yaml defaults (auth disabled)
python run.py
```

**`config.yaml`:**
```yaml
authentication:
  enabled: false
```

**Result:** ✅ No authentication, quick local testing

---

### Use Case 2: Public Demo (Auth + Rate Limiting)

**Render deployment:**
```yaml
# render.yaml
envVars:
  - key: DEMO_MODE
    value: "true"
  - key: AUTHENTICATION_ENABLED
    value: "true"
```

**`config.yaml`:**
```yaml
authentication:
  enabled: false  # Overridden by AUTHENTICATION_ENABLED=true
```

**Result:** ✅ Demo mode enabled (rate limiting + restrictions), authentication enabled

---

### Use Case 3: Private Demo (Custom Password & Secret Key)

**Generate password hash and secret key:**
```bash
# Generate password hash
python generate_password.py
# Enter password: mysecurepassword
# Generated hash: $2b$12$...

# Generate secret key
python -c "import secrets; print(secrets.token_hex(32))"
# Generated key: a1b2c3d4e5f6...
```

**Render deployment:**
```yaml
envVars:
  - key: AUTHENTICATION_ENABLED
    value: "true"
  - key: AUTHENTICATION_PASSWORD_HASH
    value: "$2b$12$..."  # Your generated hash
  - key: AUTHENTICATION_SECRET_KEY
    value: "a1b2c3d4e5f6..."  # Your generated key
```

**Result:** ✅ Custom password and secure session key for production demo

---

### Use Case 4: Docker Compose (Local Development)

**`docker-compose.yml`:**
```yaml
services:
  notediscovery:
    image: ghcr.io/gamosoft/notediscovery:latest
    ports:
      - "8000:8000"
    environment:
      - AUTHENTICATION_ENABLED=false
      - DEMO_MODE=false
    volumes:
      - ./data:/app/data
```

**Result:** ✅ Local deployment without restrictions (no auth, no rate limiting)

---

### Use Case 5: Custom Port

**Run on port 3000 instead of 8000:**

**Local (run.py):**
```bash
PORT=3000 python run.py
# → Runs on http://localhost:3000
```

**Docker:**
```bash
docker run -p 3000:3000 -e PORT=3000 ghcr.io/gamosoft/notediscovery:latest
```

**Docker Compose:**
```yaml
services:
  notediscovery:
    image: ghcr.io/gamosoft/notediscovery:latest
    ports:
      - "3000:3000"  # Host:Container
    environment:
      - PORT=3000
```

**Result:** ✅ App runs on custom port

---

## 🔐 Authentication Examples

### Example 1: Enable Auth via Environment

**Without environment variables:**
```bash
# Uses config.yaml defaults
🔐 Authentication DISABLED (from config.yaml)
✅ Production mode - Rate limiting disabled
```

**With environment variables (demo mode):**
```bash
export DEMO_MODE=true
export AUTHENTICATION_ENABLED=true
python run.py

# Output:
🎭 DEMO MODE enabled - Rate limiting active
🔐 Authentication ENABLED (from AUTHENTICATION_ENABLED env var)
```

### Example 2: Demo Deployment

**Public demo with restrictions:**
```bash
export DEMO_MODE=true
export AUTHENTICATION_ENABLED=true
export AUTHENTICATION_PASSWORD_HASH='$2b$12$custom_hash'
export AUTHENTICATION_SECRET_KEY='your_random_secret_key'
python run.py

# Output:
🎭 DEMO MODE enabled - Rate limiting active
🔐 Authentication ENABLED (from AUTHENTICATION_ENABLED env var)
🔑 Password hash loaded from AUTHENTICATION_PASSWORD_HASH env var
🔐 Secret key loaded from AUTHENTICATION_SECRET_KEY env var
```

**Private instance (no restrictions):**
```bash
# No environment variables needed
python run.py

# Output:
✅ Production mode - Rate limiting disabled
🔐 Authentication DISABLED (from config.yaml)
```

## 📝 Boolean Values

Environment variables accept multiple formats for boolean values:

**True values:**
- `true`, `True`, `TRUE`
- `1`
- `yes`, `Yes`, `YES`

**False values:**
- `false`, `False`, `FALSE`
- `0`
- `no`, `No`, `NO`
- Not set (uses config.yaml default)

**Examples:**
```bash
AUTHENTICATION_ENABLED=true    # ✅ Enabled
AUTHENTICATION_ENABLED=1       # ✅ Enabled
AUTHENTICATION_ENABLED=yes     # ✅ Enabled
AUTHENTICATION_ENABLED=false   # ❌ Disabled
AUTHENTICATION_ENABLED=0       # ❌ Disabled
# Not set          # Uses config.yaml
```

## 🚀 Deployment Scenarios

### Scenario 1: Same Codebase, Different Environments

**Repository structure:**
```
config.yaml          # Default: auth disabled (for local dev)
render.yaml          # Render: AUTHENTICATION_ENABLED=true
docker-compose.yml   # Docker: AUTHENTICATION_ENABLED=false (or not set)
```

**Benefits:**
- ✅ Single codebase
- ✅ No code changes between environments
- ✅ Environment-specific security

### Scenario 2: Team Collaboration

**Team workflow:**
```bash
# Developer 1 (local, no auth)
git clone repo
python run.py
# → No auth needed for local testing

# Developer 2 (local, testing auth)
AUTHENTICATION_ENABLED=true python run.py
# → Tests authentication locally

# Production (Render)
# → AUTHENTICATION_ENABLED=true in render.yaml
# → Always requires authentication
```

### Scenario 3: CI/CD Pipeline

**GitHub Actions:**
```yaml
- name: Test with auth disabled
  run: |
    export AUTHENTICATION_ENABLED=false
    pytest tests/

- name: Test with auth enabled
  run: |
    export AUTHENTICATION_ENABLED=true
    pytest tests/auth/
```

## 🔍 Checking Current Configuration

The application prints its configuration on startup:

```bash
python run.py

# Output:
🎭 DEMO MODE enabled - Rate limiting active
🔐 Authentication ENABLED (from AUTHENTICATION_ENABLED env var)
🔑 Password hash loaded from AUTHENTICATION_PASSWORD_HASH env var
🔐 Secret key loaded from AUTHENTICATION_SECRET_KEY env var
```

## ⚙️ Advanced: All Environment Variables

**Full demo deployment example:**
```bash
export PORT=8080
export DEMO_MODE=true
export AUTHENTICATION_ENABLED=true
export AUTHENTICATION_PASSWORD_HASH='$2b$12$...'
export AUTHENTICATION_SECRET_KEY='your_random_secret_key_here'

python run.py
```

**Docker example:**
```dockerfile
ENV PORT=8000
ENV DEMO_MODE=true
ENV AUTHENTICATION_ENABLED=true
ENV AUTHENTICATION_PASSWORD_HASH='$2b$12$...'
ENV AUTHENTICATION_SECRET_KEY='your_random_secret_key_here'
```

## 📊 Quick Reference Table

| Scenario | `DEMO_MODE` | `AUTHENTICATION_ENABLED` | Behavior |
|----------|-------------|---------------|----------|
| **Local Dev** | Not set | Not set | No restrictions, quick testing |
| **Local Auth Testing** | Not set | `true` | Auth only, no rate limits |
| **Public Demo** | `true` | `true` | Full restrictions + auth |
| **Private Instance** | Not set | `true` | Auth only, self-hosted |
| **Read-Only Demo** | `true` | Not set | Rate limited, no auth |

## 🆘 Troubleshooting

### "Authentication not working"

**Check startup logs:**
```
🔐 Authentication DISABLED (from config.yaml)
```

**Fix:** Set environment variable
```bash
export AUTHENTICATION_ENABLED=true
```

### "Wrong password accepted"

**Check if password hash is loaded:**
```
🔑 Password hash loaded from AUTHENTICATION_PASSWORD_HASH env var
```

**If not shown:** Environment variable not set, using `config.yaml`

### "Can't disable auth in Render"

**Option 1:** Remove from `render.yaml`
```yaml
# Remove or comment out:
# - key: AUTHENTICATION_ENABLED
#   value: "true"
```

**Option 2:** Explicitly disable
```yaml
- key: AUTHENTICATION_ENABLED
  value: "false"
```

## 🔧 Advanced Server Configuration

The following settings are available in `config.yaml` only (not via environment variables):

### CORS (Cross-Origin Resource Sharing)

```yaml
server:
  # List of allowed origins for CORS
  # Default: ["*"] allows all origins (fine for self-hosted)
  # Production: specify your domains
  allowed_origins: ["*"]
  
  # Examples for production:
  # allowed_origins: ["http://localhost:8000", "https://yourdomain.com"]
  # allowed_origins: ["https://*.yourdomain.com"]  # Wildcard subdomain
```

**Security Note:**
- `["*"]` is **safe for self-hosted** deployments on private networks
- For **public deployments**, specify exact origins to prevent unauthorized API access
- This prevents CSRF attacks when authentication is enabled

### Debug Mode

```yaml
server:
  # Enable detailed error messages in API responses
  # Default: false (production-safe)
  # Set to true for development/troubleshooting
  debug: false
```

**⚠️ CRITICAL**: Never enable `debug: true` in production!

When `debug: true`:
- Full error stack traces are returned to users
- Internal paths and system details are exposed
- Security vulnerabilities may be revealed

When `debug: false` (recommended):
- Generic error messages are returned
- Full error details are logged server-side only
- Production-safe error handling

---

## 📚 Related Documentation

- **Authentication**: [AUTHENTICATION.md](AUTHENTICATION.md)
- **Render Deployment**: [DEPLOYMENT_RENDER.md](DEPLOYMENT_RENDER.md)
- **API Rate Limiting**: [API.md](API.md#rate-limiting)

---

**Pro Tip:** Use environment variables for **deployment-specific** settings, and `config.yaml` for **application defaults**. This keeps your configuration flexible and maintainable! 🎯

