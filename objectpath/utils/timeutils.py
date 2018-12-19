#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of ObjectPath released under MIT license.
# Copyright (C) 2008-2010 Adrian Kalbarczyk

import datetime
import sys, os
try:
  import pytz
  TIMEZONE_CACHE = {"UTC": pytz.utc}
except ImportError:
  pass

from objectpath.core import STR_TYPES,ITER_TYPES

HOURS_IN_DAY = 24

now = datetime.datetime.now

def round9_10(n):
  i = int(n)
  if n - i > 0.9:
    return i + 1
  return i

# TODO its 31 minuta, should be 31 minut - probably done

def age(arg):
  date = arg[0]

  try:
    reference = arg[1]
  except:
    reference = None

  try:
    lang = arg[2]
  except:
    lang = 'en'

  if reference is None:
    reference = now()
  td = reference - date  #TimeDelta

  days = float(td.days)
  if days:
    years = round9_10(days/365)
    if years:
      if lang == "pl":
        return [years, years is 1 and "rok" or years < 5 and "lata" or "lat"]
      elif lang == "en":
        return [years, years is 1 and "year" or "years"]
      else:
        return years

    months = round9_10(days/30)
    if months:
      if lang == "pl":
        return [
            months, months is 1 and "miesiąc" or 1 < months < 5 and "miesiące"
            or "miesięcy"
        ]
      elif lang == "en":
        return [months, months is 1 and "month" or "months"]
      else:
        return months

    weeks = round9_10(days/7)
    if weeks:
      if lang == "pl":
        return [
            weeks, weeks is 1 and "tydzień"
            or weeks % 10 in [0, 1, 5, 6, 7, 8, 9] and "tygodni" or "tygodnie"
        ]
      elif lang == "en":
        return [weeks, weeks is 1 and "week" or "weeks"]
      else:
        return weeks

    days = int(days)
    if lang == "pl":
      return [days, days is 1 and "dzień" or "dni"]
    elif lang == "en":
      return [days, days is 1 and "day" or "days"]
    else:
      return days

  seconds = float(td.seconds)
  if seconds is not None:
    hours = round9_10(seconds/3600)
    if hours:
      if lang == "pl":
        return [
            hours, hours is 1 and "godzina" or 1 < hours < 5 and "godziny"
            or "godzin"
        ]
      elif lang == "en":
        return [hours, hours is 1 and "hour" or "hours"]
      else:
        return hours

    minutes = round9_10(seconds/60)
    if minutes:
      if lang == "pl":
        return [
            minutes, minutes is 1 and "minuta" or 1 < minutes < 5 and "minuty"
            or "minut"
        ]
      elif lang == "en":
        return [minutes, minutes is 1 and "minute" or "minutes"]
      else:
        return minutes

    seconds = int(seconds)
    if lang == "pl":
      return [
          seconds, seconds is 1 and "sekunda" or 1 < seconds < 5 and "sekundy"
          or "sekund"
      ]
    elif lang == "en":
      return [seconds, seconds is 1 and "second" or "seconds"]
    else:
      return seconds
  # return (0,"seconds")

def date(d):
  if d:
    d = d[0]
    t = type(d)
    if t is datetime.datetime:
      return datetime.date(d.year, d.month, d.day)
    if t in (tuple, list):
      return datetime.date(*d)
  return datetime.date.today()

def date2list(d):
  return [d.year, d.month, d.day]

def time(d):
  if not d or not d[0]:
    d = now()
  else:
    d = d[0]
    t = type(d)
    if t in (tuple, list):
      return datetime.time(*d)
  return datetime.time(d.hour, d.minute, d.second, d.microsecond)

def time2list(t):
  return [t.hour, t.minute, t.second, t.microsecond]

def addTimes(fst, snd):
  l1 = time2list(fst)
  l2 = time2list(snd)
  t = [l1[0] + l2[0], l1[1] + l2[1], l1[2] + l2[2], l1[3] + l2[3]]
  t2 = []
  one = 0
  ms = t[3]
  if ms >= 1000000:
    t2.append(ms - 1000000)
    one = 1
  else:
    t2.append(ms)
  for i in (t[2], t[1]):
    i = i + one
    one = 0
    if i >= 60:
      t2.append(i - 60)
      one = 1
    # elif i==60:
    # 	t2.append(0)
    # 	one=1
    else:
      t2.append(i)
  hour = t[0] + one
  if hour >= HOURS_IN_DAY:
    t2.append(hour - HOURS_IN_DAY)
  else:
    t2.append(hour)
  return datetime.time(*reversed(t2))

def subTimes(fst, snd):
  l1 = time2list(fst)
  l2 = time2list(snd)
  t = [l1[0] - l2[0], l1[1] - l2[1], l1[2] - l2[2], l1[3] - l2[3]]
  t2 = []
  one = 0
  ms = t[3]
  if ms < 0:
    t2.append(1000000 + ms)
    one = 1
  else:
    t2.append(ms)
  for i in (t[2], t[1]):
    i = i - one
    one = 0
    if i >= 0:
      t2.append(i)
    else:
      t2.append(60 + i)
      one = 1
  hour = t[0] - one
  if hour < 0:
    t2.append(HOURS_IN_DAY + hour)
  else:
    t2.append(hour)
  return datetime.time(*reversed(t2))

def dateTime(arg):
  """
	d may be:
		- datetime()
		- [y,m,d,h[,m[,ms]]]
		- [date(),time()]
		- [[y,m,d],[h,m,s,ms]]
		and permutations of above
	"""
  l = len(arg)
  if l is 1:
    dt = arg[0]
    typed = type(dt)
    if typed is datetime.datetime:
      return dt
    if typed in (tuple, list) and len(dt) in [5, 6, 7]:
      return datetime.datetime(*dt)
    if type(arg) in ITER_TYPES:
      arg = list(arg[0])
      l = len(arg)
  if l is 2:
    date = time = None
    typeArg0 = type(arg[0])
    typeArg1 = type(arg[1])
    if typeArg0 in STR_TYPES:
      return datetime.datetime.strptime(arg[0], arg[1])
    if typeArg0 is datetime.date:
      d = arg[0]
      date = [d.year, d.month, d.day]
    if typeArg0 in (tuple, list):
      date = arg[0]
    if typeArg1 is datetime.time:
      t = arg[1]
      time = [t.hour, t.minute, t.second, t.microsecond]
    if typeArg1 in (tuple, list):
      time = arg[1]
    return datetime.datetime(*date + time)

# dt - dateTime, tzName is e.g. 'Europe/Warsaw'
def UTC2local(dt, tzName="UTC"):
  try:
    if tzName in TIMEZONE_CACHE:
      tz = TIMEZONE_CACHE[tzName]
    else:
      tz = TIMEZONE_CACHE[tzName] = pytz.timezone(tzName)
    return TIMEZONE_CACHE["UTC"].localize(dt).astimezone(tz)
  except Exception:
    return dt
