"""Verificações locais sem API e sem dados pessoais."""

import contextlib
import io
import json
from pathlib import Path
import tempfile
import unittest

from extrator_ocorrencia.cli import diagnosticar, main
from extrator_ocorrencia.config import Configuracao


class EstruturaTests(unittest.TestCase):
    def setUp(self):
        self.temporario = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporario.cleanup)
        self.configuracao = Configuracao.carregar(self.temporario.name)
        self.configuracao.documentos.mkdir(parents=True)

    def test_manual_ausente_retorna_erro(self):
        self.assertEqual(diagnosticar(self.configuracao)["status"], "ERRO")

    def test_manual_vazio_retorna_erro(self):
        self.configuracao.manual.write_text("  \n", encoding="utf-8")
        self.assertEqual(diagnosticar(self.configuracao)["status"], "ERRO")

    def test_codificacao_invalida_retorna_erro(self):
        self.configuracao.manual.write_bytes(b"\xff\xfe")
        self.assertEqual(diagnosticar(self.configuracao)["status"], "ERRO")

    def test_cli_le_utf8_sem_criar_resultados(self):
        texto = "Manual sintético: ocorrência CRÍTICO e revisão humana."
        self.configuracao.manual.write_text(texto, encoding="utf-8")
        saida = io.StringIO()
        with contextlib.redirect_stdout(saida):
            retorno = main(["diagnostico", "--raiz", str(self.configuracao.raiz)])
        resultado = json.loads(saida.getvalue())
        self.assertEqual(retorno, 0)
        self.assertEqual(resultado["caracteres_manual"], len(texto))
        self.assertEqual(resultado["recuperacao_rag"], "PENDENTE")
        self.assertFalse(self.configuracao.resultados.exists())

    def test_cli_sinaliza_falha_no_codigo_de_saida(self):
        with contextlib.redirect_stdout(io.StringIO()):
            retorno = main(["diagnostico", "--raiz", str(self.configuracao.raiz)])
        self.assertEqual(retorno, 1)

    def test_configuracao_resolve_caminho_informado(self):
        self.assertEqual(self.configuracao.raiz, Path(self.temporario.name).resolve())


if __name__ == "__main__":
    unittest.main()
