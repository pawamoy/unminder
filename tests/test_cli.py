"""Tests for the `cli` module."""

import pytest

from unminder import cli


def test_show_queue_help(capsys):
    """Shows help."""
    with pytest.raises(SystemExit):
        cli.queue(["-h"])
    captured = capsys.readouterr()
    assert "queue" in captured.out


def test_show_review_help(capsys):
    """Shows help."""
    with pytest.raises(SystemExit):
        cli.review(["-h"])
    captured = capsys.readouterr()
    assert "review" in captured.out
