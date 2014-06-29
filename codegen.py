#!/usr/bin/python
# -*- coding: utf-8 -*-

from datetime import date
from datetime import timedelta
from random import randint

class CodeGenerator(object):
  DELIMITER = '  '
  DATE_FORMAT = '%Y-%m-%d'
  VALID_FOR = timedelta(days=1)

  def __init__(self, code, last_generated_at):
    self.last_generated_at = last_generated_at
    self.code = code

  def generate_code_if_expired():
    today = date.today()
    if self.last_generated_at and (self.last_generated_at + self.VALID_FOR) < today:
      self.code = randint(0, 9999)
      self.last_generated_at = today
      return self.code
    else:
      return None

  def write_file(self, path):
    with open(path, 'w') as f: f.write(self.to_line())

  def to_line(self):
    return str(self.code) \
            + self.DELIMITER \
            + self.last_generated_at.strftime(self.DATE_FORMAT) \
            + "\n"

  @classmethod
  def get_empty(klass):
    return klass(0, None)

  @classmethod
  def load_file(klass, path):
    try:
      with open(path, 'r') as f: return klass.parse_line(f.readline())
    except IOError:
      return klass.get_empty()

  @classmethod
  def parse_line(klass, line):
    cells = self.DELIMITER.split(line)
    if len(cells) >= 2:
      return klass(cells[0], date.strptime(cells[1], self.DATE_FORMAT))
    else:
      return klass.get_empty()

try:
  import android
except ImportError:
  import sys
  result_out = sys.stdout
  code_file_path = sys.argv[1]

  on_android = False
else:
  droid = android.Android()

  import StringIO
  result_out = StringIO.StringIO(u'')
  code_file_path = '/storage/emulated0/My/code.txt'

  on_android = True

code_generator = CodeGenerator.load_file(code_file_path)
print >>result_out, ("Last code: " + code_generator.code)
code_generator.generate_code_if_expired()
print >>result_out, ("New  code: " + code_generator.code)
code_generator.write_file(code_file_path)

if on_android:
  droid.dialogCreateAlert(
    "Code Generator",
    result_out.getvalue()
  )
  droid.dialogSetPositiveButtonText('OK')
  droid.dialogShow()
  result_out.close()
