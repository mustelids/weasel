import RPi.GPIO as gpio
import time
import Tkinter as tk
from subprocess import call

# own higher order function:
def sequence(*funcs):
  ''' Combines all functions to a higher function.
  The new input will be used to call every original
  function (given as parameters). The new output
  is the list of the respective function outputs.
 
  returns: higher order function
  '''
  return lambda *args: [f(*args) for f in funcs]


# Init
# ====

# set autorepeat off:
call(["xset", "-r"])

# use physical numbering of gpio-pins:
gpio.setmode(gpio.BOARD)

pins = {
 "F": 11,
 "B": 7,
 "L": 15,
 "R": 13
}

pins_old = {"F": 7,"B": 11,"L": 13,"R": 15,
 "GR": 12,"YE": 16,"RE": 18,"BL": 22}

# default all pins to False:
for p in pins.values():
  gpio.setup(p, gpio.OUT)
  gpio.output(p, False)


# Interactions
# ============

# Output functions:
def output_secure(pin, value, pin_to_reset):
  if value:
    gpio.output(pin_to_reset, False)
    while gpio.input(pin_to_reset):
      time.sleep(0.01)
  gpio.output(pin, value)

def left(value):
  output_secure(pins["L"], value, pins["R"])

def right(value):
  output_secure(pins["R"], value, pins["L"])

def forward(value):
  output_secure(pins["F"], value, pins["B"])

def backward(value):
  output_secure(pins["B"], value, pins["F"])

def red(value):
  gpio.output(pins["RE"], value)

def yellow(value):
  gpio.output(pins["YE"], value)

def green(value):
  gpio.output(pins["GR"], value)

def blue(value):
  gpio.output(pins["BL"], value)

do = {
  "w" : sequence(forward, green),
  "s" : sequence(backward, red),
  "a" : sequence(left, blue),
  "d" : sequence(right, yellow),
  "Up" : forward,
  "Down" : backward,
  "Left" : left,
  "Right" : right,
  "r" : red,
  "y" : yellow,
  "g" : green,
  "b" : blue
  }

def key_press(event):
  print "press", event.keysym
  if event.keysym in do: do[event.keysym](True)

def key_release(event):
  print "release", event.keysym
  if event.keysym in do: do[event.keysym](False)

def key_escape(event):
  root.destroy()


# GUI and Eventhandling
# =====================

root = tk.Tk()
root.bind_all('<KeyPress-Escape>', key_escape)
root.bind_all('<KeyPress>', key_press)
root.bind_all('<KeyRelease>', key_release)
print "Press w,a,s,d to drive car."
root.mainloop()


# Finally
# =======

# set autorepeat on again
call(["xset", "r"])