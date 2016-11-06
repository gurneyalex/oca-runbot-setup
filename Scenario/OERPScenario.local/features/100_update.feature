@runbot_update1

Feature: update the instance
 @no_login
 Scenario: fix stuff in database
    Given I execute the SQL commands:
    """;
    UPDATE runbot_repo SET nginx=1;
    """

Scenario: install modules
  Given I install the required modules with dependencies:
  | name              |
  | runbot-oca        |
  | runbot_secure     |
  | runbot_skip_tests |
  | runbot            |


