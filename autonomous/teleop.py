import magicbot, wpilib


class TeleopSandstorm:
  MODE_NAME = "Teleop"
  DEFAULT = False
  VERBOSE_LOGGING = True
  robot: magicbot.MagicRobot

  def on_enable(self): pass
  def on_disable(self): pass

  timer = wpilib.Timer()
  timer.reset()
  timer.start()

  def on_iteration(self, _time_elapsed):
    print(self.timer.get())
    self.robot.teleopPeriodic()