from unittest import TestCase

from pygls import uris
from pygls.lsp import methods
from pygls.lsp.types import (
    ClientCapabilities,
    CompletionItem,
    CompletionParams,
    Hover,
    HoverParams,
    InitializeParams,
    Position,
)

from aac.lang.active_context_lifecycle_manager import get_active_context

from tests.lang.LspTestClient import LspTestClient


class TestLspServer(TestCase):
    def setUp(self):
        self.client = LspTestClient()
        self.client.start()
        res = self.client.send_request(
            methods.INITIALIZE,
            InitializeParams(process_id=12345, root_uri="file://", capabilities=ClientCapabilities()),
        )

        self.assertIn("capabilities", res)

    def tearDown(self):
        self.client.stop()

    def test_handles_hover_request(self):
        res: Hover = self.client.send_request(
            methods.HOVER,
            HoverParams(text_document={"uri": TEST_DOCUMENT_URI}, position=Position(line=0, character=0)),
        )

        self.assertSequenceEqual(list(res.keys()), ["contents"])
        self.assertIn("LSP server", res.get("contents"))

    def test_handles_completion_request(self):
        active_context = get_active_context(reload_context=True)

        res: list[CompletionItem] = self.client.send_request(
            methods.COMPLETION,
            CompletionParams(text_document={"uri": TEST_DOCUMENT_URI}, position=Position(line=0, character=0)),
        )

        self.assertSequenceEqual(list(res.keys()), ["isIncomplete", "items"])
        self.assertSequenceEqual([i.get("label") for i in res.get("items")], active_context.get_root_keys())
        self.assertFalse(res.get("isIncomplete"))


TEST_DOCUMENT_URI = uris.from_fs_path(__file__)