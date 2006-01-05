# Zwiki/zwiki.org makefile

## misc

default: pot


## i18n
# remember: 
# 0f. you need zope 3's i18nextract with http://zopewiki.org/I18nextract patches
# 1. apply source updates 2. make pot 3. apply po updates 4. make po

LANGUAGES=fr en
I18NEXTRACT=/home/encolpe/zopes/zope-3.1/bin/i18nextract

pot: dtmlextract
	$(I18NEXTRACT) -d plone -p . -o ./i18n \
	    -x _darcs -x .old -x misc -x ftests  -x .doxygen  -x .svn
	tail +12 i18n/header.pot >>i18n/plone.pot
	python \
	-c "import re; \
	    t = open('i18n/CMFPlacefulWorkflow-plone.pot').read(); \
	    t = re.sub(r'(?s)^.*?msgid',r'msgid',t); \
	    t = re.sub(r'Zope 3 Developers <zope3-dev@zope.org>',\
	               r'<support@ingeniweb.com>', \
	               t); \
	    t = re.sub(r'(?s)(\"Generated-By:.*?\n)', \
	               r'\1\"Language-code: xx\\\n\"\n\"Language-name: X\\\n\"\n\"Preferred-encodings: utf-8 latin1\\\n\"\n\"Domain: plone\\\n\"\n', \
	               t); \
	    open('i18n/plone.pot','w').write(t)"
	mv i18n/plone.pot i18n/CMFPlacefulWorkflow-plone.pot
	rm -f skins/dtmlmessages.pt

# a dtml extraction hack, should integrate with i18nextract
dtmlextract: 
	echo '<div i18n:domain="plone">' >skins/dtmlmessages.pt
	find dtml -name "*.dtml" | xargs perl -n -e '/<dtml-translate domain="?plone"?>(.*?)<\/dtml-translate>/ and print "<span i18n:translate=\"\">$$1<\/span>\n";' >>skins/dtmlmessages.pt
	echo '</div>' >>skins/dtmlmessages.pt

po:
	cd i18n; \
	for L in $(LANGUAGES); do \
	 ls; \
	 msgmerge -U CMFPlacefulWorkflow-plone-$$L.po CMFPlacefulWorkflow-plone.pot; \
	 done

# PTS generates these, this is just for additional checking and stats
mo:
	cd i18n; \
	for L in $(LANGUAGES); do \
	 echo $$L; \
	 msgfmt --statistics CMFPlacefulWorkflow-plone-$$L.po -o CMFPlacefulWorkflow-plone-$$L.mo; \
	 done; \
	rm -f *.mo

i18n:
# sync po files with pot
	i18ndude sync --pot i18n/CMFPlacefulWorkflow-plone.pot \
        i18n/CMFPlacefulWorkflow-plone-[a-z][a-z].po \
        i18n/CMFPlacefulWorkflow-plone-[a-z][a-z]_[A-Z][A-Z].po

i18n-en:
# add untranslated msgstrs from the English translations
	for pofile in i18n/*.po; do \
        i18ndude admix $$pofile i18n/CMFPlacefulWorkflow-plone-en.po > i18n/temp-po; \
        mv -f i18n/temp-po $$pofile; \
    done

i18nchart:
# draw a chart
	i18ndude chart -o i18n/i18nchart.png --pot i18n/CMFPlacefulWorkflow-plone.pot \
        i18n/CMFPlacefulWorkflow-plone-[a-z][a-z].po \
        i18n/CMFPlacefulWorkflow-plone-[a-z][a-z]_[A-Z][A-Z].po
