import l293d

motor = l293d.DC(22,18,16)

motor.clockwise()

l293d.cleanup()