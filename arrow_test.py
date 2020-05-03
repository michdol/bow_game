from math import radians, degrees
from unittest import main, TestCase, mock

from arrow import Arrow
from colors import RED


class ArrowTest(TestCase):
  def _create_test_arrow(self, click_position):
    return Arrow(color=RED, screen=mock.Mock(), character=mock.Mock(), click_position=click_position)

  def test_get_release_angle(self):
    click_position = (10, 10)
    release_position = (0, 20)
    arrow = self._create_test_arrow(click_position)
    arrow.release_position = release_position
    adjacent, opposite = arrow.get_catheuses()
    angle = arrow.get_release_angle(adjacent, opposite)
    self.assertEqual(angle, radians(45))

  def test_get_catheuses(self):
    click_position = (10, 10)
    release_position = (0, 20)
    arrow = self._create_test_arrow(click_position)
    arrow.release_position = release_position
    adjacent, opposite = arrow.get_catheuses()
    self.assertEqual(adjacent, 10)
    self.assertEqual(opposite, 10)

    click_position = (0, 20)
    release_position = (10, 10)
    arrow = self._create_test_arrow(click_position)
    arrow.release_position = release_position
    adjacent, opposite = arrow.get_catheuses()
    self.assertEqual(adjacent, 10)
    self.assertEqual(opposite, 10)

    click_position = (0, 0)
    release_position = (10, 10)
    arrow = self._create_test_arrow(click_position)
    arrow.release_position = release_position
    adjacent, opposite = arrow.get_catheuses()
    self.assertEqual(adjacent, 10)
    self.assertEqual(opposite, 10)

  def test_adjust_angle_to_aim_direction(self):
    click_position = (10, 10)
    arrow = self._create_test_arrow(click_position)

    # First quater
    angle = arrow.adjust_angle_to_aim_direction(radians(45), aiming_down=False, is_moving_right=True)
    self.assertEqual(angle, radians(45))
    # Second quater
    angle = arrow.adjust_angle_to_aim_direction(radians(45), aiming_down=False, is_moving_right=False)
    self.assertEqual(angle, radians(135))
    # Third quater
    angle = arrow.adjust_angle_to_aim_direction(radians(45), aiming_down=True, is_moving_right=False)
    self.assertEqual(angle, radians(225))
    # Fourth quater
    angle = arrow.adjust_angle_to_aim_direction(radians(45), aiming_down=True, is_moving_right=True)
    self.assertEqual(angle, radians(315))

    # First quater
    angle = arrow.adjust_angle_to_aim_direction(radians(85), aiming_down=False, is_moving_right=True)
    self.assertEqual(angle, radians(85))
    # Second quater
    angle = arrow.adjust_angle_to_aim_direction(radians(85), aiming_down=False, is_moving_right=False)
    print("agn", degrees(angle))
    self.assertEqual(angle, radians(95))


if __name__ == "__main__":
  main()
