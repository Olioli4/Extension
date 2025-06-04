"""
Test for the popup form widget (inputbox) in form_widget.py
Requires pytest and pytest-qt (pip install pytest pytest-qt PyQt6)
"""
import sys
import os
import pytest
from PyQt6.QtWidgets import QApplication
import logging

logging.basicConfig(level=logging.DEBUG)

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from form_widget import inputbox

@pytest.mark.qt
def test_inputbox_popup(qtbot):
    logging.debug("Starting test_inputbox_popup")
    # Ensure QApplication exists
    app = QApplication.instance() or QApplication([])
    logging.debug(f"QApplication instance: {app}")
    # Simulate opening the inputbox dialog
    title = "Test Title"
    label = "Test Label"
    default_text = "Default Value"
    logging.debug(f"Calling inputbox with title={title}, label={label}, default_text={default_text}")
    result = inputbox(title, label, default_long_text=default_text)
    logging.debug(f"inputbox returned: {result}")
    # The dialog will block for user input, so we only test that it can be created
    # For full automation, you would need to simulate user input (advanced)
    assert isinstance(result, tuple)
    assert len(result) == 3
    # Optionally check types of returned values
    assert isinstance(result[0], str)
    assert isinstance(result[1], bool)
    assert isinstance(result[2], str)
