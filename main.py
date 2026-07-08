from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow browser checks
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Layer 1: defaults
config = {
    "port": 8000,
    "workers": 1,
    "debug": False,
    "log_level": "info",
    "api_key": "default-secret-000",
}

# Layer 2: config.development.yaml
config.update({
    "port": 8439,
    "workers": 6,
    "log_level": "error",
})

# Layer 3: .env
env_file = {
    "APP_LOG_LEVEL": "warning",
}

if "APP_LOG_LEVEL" in env_file:
    config["log_level"] = env_file["APP_LOG_LEVEL"]

# Layer 4: OS env vars (given assignment values)
os_env = {
    "APP_PORT": "8824",
    "APP_LOG_LEVEL": "warning",
    "APP_API_KEY": "key-7etvzhzi1i",
}

if "APP_PORT" in os_env:
    config["port"] = int(os_env["APP_PORT"])

if "APP_LOG_LEVEL" in os_env:
    config["log_level"] = os_env["APP_LOG_LEVEL"]

if "APP_API_KEY" in os_env:
    config["api_key"] = os_env["APP_API_KEY"]


def coerce(key, value):
    if key in ("port", "workers"):
        return int(value)

    if key == "debug":
        return str(value).lower() in ("true", "1", "yes", "on")

    return str(value)


@app.get("/effective-config")
def effective_config(set: list[str] = Query(default=[])):
    merged = config.copy()

    for item in set:
        if "=" not in item:
            continue

        k, v = item.split("=", 1)
        merged[k] = coerce(k, v)

    merged["api_key"] = "****"

    return merged
