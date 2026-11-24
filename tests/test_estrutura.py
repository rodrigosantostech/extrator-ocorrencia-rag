"""Diagnóstico da base modular sem API e sem dados pessoais reais."""

import contextlib
import hashlib
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from extrator_ocorrencia.cli import diagnosticar, main
from extrator_ocorrencia.config import Configuracao


class EstruturaTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.cfg = Configuracao.carregar(self.tmp.name)
        self.cfg.manual.parent.mkdir(parents=True)

    def preparar(self, texto):
        bruto = (
            "<!-- INICIO_CONTEUDO_ORIGINAL -->\n"
            + texto
            + "<!-- FIM_CONTEUDO_ORIGINAL -->\n"
        ).encode("utf-8")
        (self.cfg.manual.parent / "teste.md").write_bytes(bruto)
        manifesto = {
            "formato": "manual-modular-1",
            "versao": "2026.3",
            "documentos": [
                {
                    "arquivo": "teste.md",
                    "sha256": hashlib.sha256(bruto).hexdigest(),
                    "secoes_indexadas": [],
                    "anexo_rag": False,
                }
            ],
        }
        self.cfg.manual.write_text(json.dumps(manifesto), encoding="utf-8")

    def test_manual_ausente_retorna_erro(self):
        self.assertEqual(diagnosticar(self.cfg)["status"], "ERRO")

    def test_manual_vazio_retorna_erro(self):
        self.cfg.manual.write_text("  \n", encoding="utf-8")
        self.assertEqual(diagnosticar(self.cfg)["status"], "ERRO")

    def test_codificacao_invalida_retorna_erro(self):
        self.cfg.manual.write_bytes(b"\xff\xfe")
        self.assertEqual(diagnosticar(self.cfg)["status"], "ERRO")

    def test_cli_le_utf8_e_gera_relatorios(self):
        texto = "Manual sintético: ocorrência CRÍTICO e revisão humana."
        self.preparar(texto)
        saida = io.StringIO()
        with contextlib.redirect_stdout(saida):
            retorno = main(["diagnostico", "--raiz", str(self.cfg.raiz)])
        dados = json.loads(saida.getvalue())
        self.assertEqual(retorno, 0)
        self.assertEqual(dados["resultado"]["caracteres_manual"], len(texto))
        self.assertTrue(Path(dados["relatorio_html"]).exists())
        self.assertEqual(dados["resultado"]["manual_versao"], "2026.3")

    def test_cli_sinaliza_falha_no_codigo_de_saida(self):
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(main(["diagnostico", "--raiz", str(self.cfg.raiz)]), 1)

    def test_configuracao_resolve_caminho_informado(self):
        self.assertEqual(self.cfg.raiz, Path(self.tmp.name).resolve())

    def test_configuracao_localiza_base_incluida_no_executavel(self):
        executable = Path(self.tmp.name) / "dist" / "ExtratorOcorrencias.exe"
        bundle = Path(self.tmp.name) / "bundle"
        manual = bundle / "data" / "documents" / "manual_v2026_3"
        manual.mkdir(parents=True)

        with (
            patch("extrator_ocorrencia.config.sys.frozen", True, create=True),
            patch("extrator_ocorrencia.config.sys.executable", str(executable)),
            patch("extrator_ocorrencia.config.sys._MEIPASS", str(bundle), create=True),
        ):
            configuracao = Configuracao.carregar()
            caminho_manual = configuracao.manual

        self.assertEqual(configuracao.raiz, executable.parent.resolve())
        self.assertEqual(caminho_manual.resolve(), manual.resolve() / "manifesto.json")

    def test_falha_inesperada_nao_e_ocultada_pela_cli(self):
        with patch("extrator_ocorrencia.cli.diagnosticar", side_effect=RuntimeError):
            with self.assertRaises(RuntimeError):
                main(["diagnostico", "--raiz", str(self.cfg.raiz)])
