@runbot_update2

Feature: update the instance

Scenario: install modules
  Given I install the required modules with dependencies:
  | name              |
  | runbot-oca        |
  | runbot_secure     |
  | runbot_skip_tests |
  | runbot            |


