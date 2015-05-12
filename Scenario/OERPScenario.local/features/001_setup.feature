@setup
Feature: install the required modules

Scenario: install modules
  Given I install the required modules with dependencies:
  | name          |
  | runbot_custom |
  | runbot-secure |
  | runbot-oca    |
 
