.. Tahmatassu Telegram Bot documentation master file, created by
   sphinx-quickstart on Sat Mar 24 08:12:20 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Tahmatassu Telegram Bot's documentation!
===================================================

This is my introduction to the Tahmatassu Telegram Bot project. It's all about cooking recipes that I have tried and made by my self during the years.

Actual web page can be found from http://puumuki.game-server.cc

This bot uses web page REST API to fetch recipes from the server and 
servers them trough Telegram API to the end client at Telegram chat.

Project Structure
=================

* bot/* - Python module holding Python code of the project
* templates/* - Hold markdown templates used by the bot show static messages
* main.py - Tahmatassu Bot Runner, main executable
* setting.ini - Tahmatassu Telgeram Bot Settings

Poject is provided under MIT license.

.. toctree::
   :maxdepth: 3
   :caption: Contents: 

.. automodule:: bot

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
