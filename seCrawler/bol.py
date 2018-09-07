# -*- coding: utf-8 -*-
from boilerpipe.extract import Extractor
extractor = Extractor(extractor='ArticleExtractor', url='http://www.baidu.com/link?url=_DaB_kMeHFFKecaTIyv-WwGj8FR88eAG_CmD9_ZNrGJancYF_oOwdy-o_9r1KmMSbFwemVmPVFp6SIWLrLz_La')
extracted_text = extractor.getText()
print  extracted_text
