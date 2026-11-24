# 004 - Credenciales verificables transfronterizas

## Objetivo

Implementar W3C Verifiable Credentials para el expediente digital del cliente, permitiendo que un documento emitido en un país sea verificable criptográficamente en otro sin pedir el original.

## Historias

- Como usuario, quiero que mis documentos (pasaporte, título, permiso) se guarden como credenciales verificables.
- Como usuario, quiero controlar qué comparto y con quién (self-sovereign identity).
- Como institución en otro país, quiero verificar un documento sin pedir el original.
- Como usuario, quiero exportar o eliminar mis datos en cualquier momento.

## Criterios de aceptación

- [ ] Los documentos se almacenan como W3C Verifiable Credentials (JWT-VC).
- [ ] El cliente puede verificar una credencial criptográficamente.
- [ ] El cliente controla el acceso (compartir/revocar).
- [ ] El cliente puede exportar o eliminar todos sus datos.
- [ ] Hay pruebas unitarias para emisión y verificación de credenciales.
- [ ] Cobertura de tests ≥ 80% en los módulos nuevos.

## Fuera de alcance

- Integración con autoridades emisoras reales (V2).
- Revocación on-chain (V3).
- ZKP (zero-knowledge proofs) (V3).