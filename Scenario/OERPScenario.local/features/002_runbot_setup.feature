@setup @config

Feature: configure the runbot
  Scenario: setup repo for OCB
  Given I need a "runbot.repo" with name: https://github.com/OCA/OCB
  And having:
  | name    |                      value |
  | name    | https://github.com/OCA/OCB |
  | testing |                          1 |
  | running |                          1 |
  | auto    |                          1 |

  Scenario Outline: setup the repositories
    Given I need a "runbot.repo" with name: https://github.com/OCA/<name>
    And having
    | name           |                               value |
    | name           |       https://github.com/OCA/<name> |
    | testing        |                                   1 |
    | running        |                                   1 |
    | auto           |                                   1 |
    | dependency_ids | by name: https://github.com/OCA/OCB |

    Examples:
    | name                        |
    | account-analytic            |
    | account-budgeting           |
    | account-closing             |
    | account-consolidation       |
    | account-financial-reporting |
    | account-financial-tools     |
    | account-fiscal-rule         |
    | account-invoice-reporting   |
    | account-invoicing           |
    | account-payment             |
    | banking                     |
    | bank-statement-reconcile    |
    | carrier-delivery            |
    | commission                  |
    | community-data-files        |
    | connector                   |
    | connector-accountedge       |
    | connector-cmis              |
    | connector-ecommerce         |
    | connector-lims              |
    | connector-magento           |
    | connector-prestashop        |
    | connector-sage-50           |
    | contract                    |
    | crm                         |
    | department                  |
    | e-commerce                  |
    | france                      |
    | geospatial                  |
    | hr                          |
    | hr-timesheet                |
    | knowledge                   |
    | l10n-belgium                |
    | l10n-canada                 |
    | l10n-france                 |
    | l10n-italy                  |
    | l10n-luxemburg              |
    | l10n-spain                  |
    | l10n-switzerland            |
    | maintainer-quality-tools    |
    | maintainers-tools           |
    | management-system           |
    | manufacture                 |
    | manufacture-mgmt            |
    | manufacture-reporting       |
    | margin-analysis             |
    | multi-company               |
    | partner-contact             |
    | product-attribute           |
    | product-kitting             |
    | product-variant             |
    | program                     |
    | project-reporting           |
    | project-service             |
    | purchase-reporting          |
    | purchase-workflow           |
    | reporting-engine            |
    | report-print-send           |
    | rma                         |
    | runbot-addons               |
    | sale-financial              |
    | sale-reporting              |
    | sale-workflow               |
    | server-tools                |
    | stock-logistics-barcode     |
    | stock-logistics-reporting   |
    | stock-logistics-tracking    |
    | stock-logistics-warehouse   |
    | stock-logistics-workflow    |
    | team_leaders.ods            |
    | vertical-construction       |
    | vertical-hotel              |
    | vertical-isp                |
    | vertical-medical            |
    | vertical-ngo                |
    | vertical-travel             |
    | web                         |
    | webkit-tools                |
    | webkit-utils                |
