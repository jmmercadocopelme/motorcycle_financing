{
    'name': 'Motorcycle Financing',
    'version': '18.0.0.0.1',
    'summary': 'Streamlines the loan application process for dealerships.',
    'category': 'Kawiil/Custom Modules',
    'author': 'jmmercadocopelme',
    'depends': ['sale', 'mail'],
    'data': [
        'security/motorcycle_financing_groups.xml',
        'security/ir.model.access.csv',
        'security/rules.xml',
        'data/loan_demo.xml',
    ],
    
    'views': [
        'views/loan_application_views.xml',
        'views/loan_application_tag_views.xml',
        'views/loan_application_document_views.xml',
        'views/loan_application_document_type_views.xml',
        'views/motorcycle_financing_menu.xml',
    ],

    'demo': [
        'data/loan_demo.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'OPL-1',
}
