# -*- coding: utf-8 -*-

#################################################################################
# Author      : Luis Felipe Paternina                                           #
#################################################################################

{

  "name"                 :  "Website Form",
  "summary"              :  """Add a mandatory field""",
  "category"             :  "Website",
  "version"              :  "13.0",
  "sequence"             :  1,
  "author"               :  "Luis Felipe Paternina",
  "depends"              :  ['auth_signup'],
  "data"                 :  [
                             'views/res_partner_view.xml',
                             #'views/account_details_template.xml',
                            ],
 
  "application"          :  True,
  "installable"          :  True,
  "auto_install"         :  False,

}
