import pytest

from textual.app import App, ComposeResult
from textual.widgets import OptionList, SelectionList
from textual.widgets.option_list import OptionDoesNotExist


class SelectionListApp(App[None]):
    """App for testing SelectionList event handling."""

    def compose(self) -> ComposeResult:
        yield SelectionList[int](
            ("Option 1", 1),
            ("Option 2", 2),
        )


async def test_stale_index_does_not_raise_option_does_not_exist() -> None:
    """Regression test: event handling with an invalid/stale index should not crash."""
    app = SelectionListApp()
    async with app.run_test() as pilot:
        selection_list = app.query_one(SelectionList)

        # 1. Set highlighted to an invalid/stale index
        selection_list.highlighted = 999

        # 2. Test _on_option_list_option_highlighted with an out-of-bounds index
        valid_option = selection_list.get_option_at_index(0)
        event = OptionList.OptionHighlighted(selection_list, valid_option, 999)

        try:
            selection_list._on_option_list_option_highlighted(event)
        except OptionDoesNotExist:
            pytest.fail(
                "_on_option_list_option_highlighted raised OptionDoesNotExist on stale index"
            )
