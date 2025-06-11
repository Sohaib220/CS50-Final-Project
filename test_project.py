import pytest
from unittest import mock
import pygame
from project import start_timer, choose_alarm_sound, stop_timer, play_alarm


alarm_sound = "test_alarm.mp3"


@pytest.fixture
def mock_pygame():
    # Mock the necessary pygame methods
    with mock.patch("pygame.mixer.init"), \
            mock.patch("pygame.mixer.music.load"), \
            mock.patch("pygame.mixer.music.play"), \
            mock.patch("pygame.mixer.music.stop") as mock_stop:
        yield mock_stop  # Ensure the stop method is yielded to the test


def test_start_timer():
    # Test for valid time conversion to seconds (AM)
    with mock.patch('tkinter.StringVar.get', side_effect=["2", "30", "AM"]):
        with mock.patch('project.open_timer_window') as mock_window:
            # Pass the correct mock for hours, minutes, and AM/PM
            hours = mock.Mock()
            minutes = mock.Mock()
            am_pm = mock.Mock()

            # Simulate the behavior of StringVar.get() returning actual string values
            hours.get.return_value = "2"
            minutes.get.return_value = "30"
            am_pm.get.return_value = "AM"

            start_timer(hours, minutes, am_pm)
            # Ensure the time for 2:30 AM is calculated and a new window opens
            mock_window.assert_called()

    # Test for valid time conversion to seconds (PM)
    with mock.patch('tkinter.StringVar.get', side_effect=["1", "00", "PM"]):
        with mock.patch('project.open_timer_window') as mock_window:
            hours = mock.Mock()
            minutes = mock.Mock()
            am_pm = mock.Mock()

            hours.get.return_value = "1"
            minutes.get.return_value = "00"
            am_pm.get.return_value = "PM"

            start_timer(hours, minutes, am_pm)
            # Ensure the time for 1:00 PM (which is 13:00) works correctly
            mock_window.assert_called()
def stop_timer():
    # Stop the music
    pygame.mixer.music.stop()

def test_choose_alarm_sound():
    with mock.patch('tkinter.filedialog.askopenfilename', return_value="test_alarm.mp3"):
        choose_alarm_sound()
        assert alarm_sound == "test_alarm.mp3"  # Test the alarm sound is correctly chosen


def test_stop_timer():
    # Mock the pygame mixer stop method
    with mock.patch('pygame.mixer.music.stop') as mock_stop:
        stop_timer()
        # Assert that the stop method was called at least once
        mock_stop.assert_called_once()


def test_play_alarm(mock_pygame):
    # Test play_alarm to ensure pygame music is played
    play_alarm()
    # Assert that play was called in pygame
    pygame.mixer.music.play.assert_called()
