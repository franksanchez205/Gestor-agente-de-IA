"""Personalidad configurable del agente (Jarvis-style).

El cliente elige nombre, tono, idioma, nivel de detalle y proactividad.
"""

from dataclasses import dataclass


@dataclass
class Personality:
    agent_name: str = "Puente"
    tone: str = "cercano"  # formal | cercano | directo | empático
    language: str = "es"
    dialect: str = "rioplatense"  # rioplatense | neutro | peninsular
    detail_level: str = "resumen"  # resumen | detallado
    proactivity: str = "media"  # baja | media | alta

    def system_prompt(self) -> str:
        return (
            f"Sos {self.agent_name}, el agente personal de vida administrativa "
            f"migratoria del cliente. Hablás en {self.language} ({self.dialect}), "
            f"con tono {self.tone}. Nivel de detalle: {self.detail_level}. "
            f"Proactividad: {self.proactivity}. Nunca des asesoría jurídica "
            f"vinculante. Confirmá antes de enviar documentos, pagar o compartir datos."
        )