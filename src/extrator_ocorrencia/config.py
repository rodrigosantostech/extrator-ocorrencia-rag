"""Caminhos locais, independentes de credenciais e de serviços externos."""

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Configuracao:
    raiz: Path

    @classmethod
    def carregar(cls, raiz: Path | str | None = None) -> "Configuracao":
        return cls(Path(raiz if raiz is not None else Path.cwd()).resolve())

    @property
    def documentos(self) -> Path:
        return self.raiz / "data" / "documents"

    @property
    def manual(self) -> Path:
        return self.documentos / "manual_operacoes_saude_viva.md"

    @property
    def resultados(self) -> Path:
        return self.raiz / "results"
