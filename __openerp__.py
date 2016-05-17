{
    'name': "Sale Contracts : information report list",
    'version': '1.0',
    'depends': ['account_analytic_account_improvements'],
    'author': "AbAKUS it-solutions SARL",
    'website': "http://www.abakusitsolutions.eu",
    'category': 'Sale',
    'description': 
    """
    Sale Contract List report

    This modules adds a report that prints the complete list of contract information for a given contract type.

    This module has been developed by AbAKUS it-solution.
    """,
    'data': ['wizard/contract_report_view.xml',
             'report/contract_list_report.xml',
            ],
}
