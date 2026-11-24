"""Integración con portales oficiales (APIs gubernamentales o RPA certificado).

Invisible para el cliente: el agente envía formularios y documentos.
"""

from dataclasses import dataclass


@dataclass
class PortalResult:
    success: bool
    tramite_number: str | None = None
    message: str = ""
    evidence: dict | None = None  # captura, fecha, etc.


class PortalClient:
    def __init__(self, base_url: str, credentials: dict, country: str = "AR"):
        self.base_url = base_url
        self.credentials = credentials
        self.country = country

    async def submit_form(self, form_data: dict, documents: list[dict]) -> PortalResult:
        # Stub: en producción usa API oficial o RPA certificado
        return PortalResult(success=True, tramite_number=f"TRM-{self.country}-0001", message="Enviado")

    async def check_status(self, tramite_number: str) -> str:
        return "en_proceso"


class PortalClientFactory:
    """Crea clientes de portal por país (V2: multi-país)."""

    def __init__(self, configs: dict[str, dict]):
        # configs: {"AR": {"base_url": "...", "credentials": {...}}, ...}
        self.configs = configs

    def get_client(self, country: str) -> PortalClient:
        if country not in self.configs:
            raise ValueError(f"No portal config for country: {country}")
        cfg = self.configs[country]
        return PortalClient(base_url=cfg["base_url"], credentials=cfg["credentials"], country=country)

    def supported_countries(self) -> list[str]:
        return sorted(self.configs.keys())