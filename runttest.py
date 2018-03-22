#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script run all unit tests in project.
"""
import unittest, sys

def main():
  all_tests = unittest.TestLoader().discover('.')
  unittest.TextTestRunner().run(all_tests)

if __name__ == "__main__":
  main()