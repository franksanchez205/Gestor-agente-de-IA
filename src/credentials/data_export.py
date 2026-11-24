"""Exportación y eliminación de datos del usuario (soberanía de datos).

Permite al cliente exportar todos sus datos o eliminarlos completamente.
"""

from typing import Any


class DataExporter:
    def __init__(self, session):
        self.session = session

    def export_user_data(self, user_id: str) -> dict[str, Any]:
        """Exporta todos los datos del usuario (perfil, documentos, casos, credenciales)."""
        from src.data.models import User, Document, Case, Credential

        user = self.session.query(User).filter(User.id == user_id).first()
        if user is None:
            return {}

        documents = self.session.query(Document).filter(Document.user_id == user_id).all()
        cases = self.session.query(Case).filter(Case.user_id == user_id).all()
        credentials = self.session.query(Credential).filter(Credential.user_id == user_id).all()

        return {
            "profile": {
                "id": user.id,
                "name": user.name,
                "nationality": user.nationality,
                "preferred_language": user.preferred_language,
                "preferred_channel": user.preferred_channel,
            },
            "documents": [
                {"id": d.id, "doc_type": d.doc_type, "issued_by": d.issued_by, "expires_at": str(d.expires_at)}
                for d in documents
            ],
            "cases": [
                {"id": c.id, "tramite": c.tramite, "country": c.country, "status": c.status}
                for c in cases
            ],
            "credentials": [
                {"id": cr.id, "issued_at": str(cr.issued_at), "revoked": cr.revoked}
                for cr in credentials
            ],
        }

    def delete_user_data(self, user_id: str) -> bool:
        """Elimina todos los datos del usuario (soberanía de datos)."""
        from src.data.models import User, Document, Case, Credential, Payment

        # Eliminar credenciales
        self.session.query(Credential).filter(Credential.user_id == user_id).delete()
        # Eliminar documentos
        self.session.query(Document).filter(Document.user_id == user_id).delete()
        # Eliminar casos (y pagos asociados)
        cases = self.session.query(Case).filter(Case.user_id == user_id).all()
        for case in cases:
            self.session.query(Payment).filter(Payment.case_id == case.id).delete()
        self.session.query(Case).filter(Case.user_id == user_id).delete()
        # Eliminar usuario
        self.session.query(User).filter(User.id == user_id).delete()
        self.session.commit()
        return True