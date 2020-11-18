# Run in Standard sql
CREATE OR REPLACE FUNCTION
general.bq_adaptive
 (message string)
 RETURNS int64
AS (
# Model language based on commit: b7618c31efc5f3ae85f5300239c7bade872ad212
# Adaptive
# Adaptive :build_adaptive_regex()
(LENGTH(REGEXP_REPLACE(lower(message),'(((((\\s|\\.|\\?|\\!|\\[|\\]|\\(|\\)|\\:|^|$|\\,|\'|"|/|#|\\$|\\%|&|\\*|\\+|=|`|;|<|>|@|~|{|}|_|\\|)((un)?hid(e|es|den)|allow(s|ed|ing)?|buil(t|ds|ing)|calibirat(e|es|ed|ing)|configure|deferr(ed|s|ing)?|enhanc(e|es|ed|ing)|extend(s|ed|ing)?|form(ed|s|ing)?|report(s|ed|ing)?|support(s|ed|ing)?|add(s|ed|ing)?|creat(e|es|ing)|disabl(e|es|ed|ing)|implement(ed|s|ing)?|import(s|ed|ing)?|introduc(e|es|ed|ing)|port(s|ed|ing)?|provid(e|es|ed|ing)|updat(e|es|ed|ing)|upgrad(e|es|ed|ing)))\\s[\\s\\S]{0,50}(ability|configuration|conversion|debug|new|possibility|support|test(s)?|tweak(s)?|mode|option|assertion(s)?|assignment(s)?|code|conditional(s)?|control|definition(s)?|delegate|delegation|design pattern(s)?|error(-| )?code(s)?|exception(s)?|flag(s)?|getter(s)?|guard clause(s)?|hierarch(y|ies)|implementation(s)?|inheritance|inline|internal|macro(s)?|magic number(s)?|modifier(s)?|null object(s)?|object(s)?|patch(es)?|pointer(s)?|polymorphism|quer(y|ies)|reference(s)?|ref(s)?|return type|setter(s)?|static|sub(-| )?class(es)?|super(-| )?class(es)?|(sub)?(-| )?system(s)?|uninline|variable(s)?|handler|plugin|contravariant|covariant|action(s)?|queue(s)?|stack(s)?|driver(s)?|storage|tool(s)?|log(s)?|setting(s)?|fall( |-)back(s)?|memory|param(s)?|volatile|file(s)?|generic(s)?|initialization(s)?|public|protected|private|framework|singelton|declaration(s)?|init|destructor(s)?|instances(s)?|primitive(s)?|algorithm(s)?|class(es)?|collection(s)?|constant(s)?|constructor(s)?|field(s)?|function(s)?|interface(s)?|member(s)?|method(s)?|parameter(s)?|structure(s)?|template(s)?|type(s)?|unit(s)?|module(s)?)(\\s|\\.|\\?|\\!|\\[|\\]|\\(|\\)|\\:|^|$|\\,|\'|"|/|#|\\$|\\%|&|\\*|\\+|=|`|;|<|>|@|~|{|}|_|\\|)))|(^(feat|build|chore|ci|test|perf)(\\(.*\\))?(!)?:))', '@'))-LENGTH(REGEXP_REPLACE(lower(message),'(((((\\s|\\.|\\?|\\!|\\[|\\]|\\(|\\)|\\:|^|$|\\,|\'|"|/|#|\\$|\\%|&|\\*|\\+|=|`|;|<|>|@|~|{|}|_|\\|)((un)?hid(e|es|den)|allow(s|ed|ing)?|buil(t|ds|ing)|calibirat(e|es|ed|ing)|configure|deferr(ed|s|ing)?|enhanc(e|es|ed|ing)|extend(s|ed|ing)?|form(ed|s|ing)?|report(s|ed|ing)?|support(s|ed|ing)?|add(s|ed|ing)?|creat(e|es|ing)|disabl(e|es|ed|ing)|implement(ed|s|ing)?|import(s|ed|ing)?|introduc(e|es|ed|ing)|port(s|ed|ing)?|provid(e|es|ed|ing)|updat(e|es|ed|ing)|upgrad(e|es|ed|ing)))\\s[\\s\\S]{0,50}(ability|configuration|conversion|debug|new|possibility|support|test(s)?|tweak(s)?|mode|option|assertion(s)?|assignment(s)?|code|conditional(s)?|control|definition(s)?|delegate|delegation|design pattern(s)?|error(-| )?code(s)?|exception(s)?|flag(s)?|getter(s)?|guard clause(s)?|hierarch(y|ies)|implementation(s)?|inheritance|inline|internal|macro(s)?|magic number(s)?|modifier(s)?|null object(s)?|object(s)?|patch(es)?|pointer(s)?|polymorphism|quer(y|ies)|reference(s)?|ref(s)?|return type|setter(s)?|static|sub(-| )?class(es)?|super(-| )?class(es)?|(sub)?(-| )?system(s)?|uninline|variable(s)?|handler|plugin|contravariant|covariant|action(s)?|queue(s)?|stack(s)?|driver(s)?|storage|tool(s)?|log(s)?|setting(s)?|fall( |-)back(s)?|memory|param(s)?|volatile|file(s)?|generic(s)?|initialization(s)?|public|protected|private|framework|singelton|declaration(s)?|init|destructor(s)?|instances(s)?|primitive(s)?|algorithm(s)?|class(es)?|collection(s)?|constant(s)?|constructor(s)?|field(s)?|function(s)?|interface(s)?|member(s)?|method(s)?|parameter(s)?|structure(s)?|template(s)?|type(s)?|unit(s)?|module(s)?)(\\s|\\.|\\?|\\!|\\[|\\]|\\(|\\)|\\:|^|$|\\,|\'|"|/|#|\\$|\\%|&|\\*|\\+|=|`|;|<|>|@|~|{|}|_|\\|)))|(^(feat|build|chore|ci|test|perf)(\\(.*\\))?(!)?:))', '')))
#Adaptive :build_adaptive_action_regex()
+
(LENGTH(REGEXP_REPLACE(lower(message),'(add(s|ed|ing)?[\\s\\S]{1,50}(version|v\\d|ver\\d)|(^|\\s)implement(ed|s|ing)?\\s|(make(s)?|made|making)[\\s\\S]{1,50}consitent|updat(e|es|ed|ing)[\\s\\S]{1,25}to[\\s\\S]{1,25}\\d+.\\d|updat(e|es|ed|ing)\\s+(to\\s+)?\\d+\\.\\d|(add(s|ed|ing)?|delet(e|es|ed|ing)|updat(e|es|ed|ing))\\s+([a-zA-Z0-9_\\*\\.])+\\.[a-zA-Z]{1,4}|(^|^[\\s\\S]{0,25}(\\s|\\.|\\?|\\!|\\[|\\]|\\(|\\)|\\:|^|$|\\,|\'|"|/|#|\\$|\\%|&|\\*|\\+|=|`|;|<|>|@|~|{|}|_|\\|))(upgrad(e|es|ed|ing)|configur(e|es|ed|ing)|chang(e|es|ed|ing)|(keep|change)\\s+(the\\s+)?default|new|merg(e|es|ed|ing)|clear(s|ed|ing)?|creat(e|es|ed|ing)|cast(s|et|ing)?[\\S\\s]{1,40}\\sas|add(s|ed|ing)?|Initial revision|(im)?port(s|ed|ing)?|(un)?hid(e|es|den)|updat(e|es|ed|ing)|upload(s|ed|ing)?|disabl(e|es|ed|ing)|delet(e|es|ed|ing)|enabl(e|es|ed|ing)|quirk(s|ed|ing)?|skip(s|ed|ing)?|switch(s|ed|ing)?|allow(s|ed|ing)?|provid(e|es|ed|ing)|remov(e|es|ed|ing)|refresh(s|ed|ing)?|no message|wip|work in progress|message|change(-|\\s)?set|commit)(\\s|\\.|\\?|\\!|\\[|\\]|\\(|\\)|\\:|^|$|\\,|\'|"|/|#|\\$|\\%|&|\\*|\\+|=|`|;|<|>|@|~|{|}|_|\\|)|^\\[(IMP|imp)\\]|support(s|ed|ing)?\\sfor\\s|show(es|ed|ing)?[\\s\\S]instead|scal(e|es|ed|ing)?\\s(up|down)|(cr|pr)(s)?(-)?(d+)?\\sfix(es)?|fix(ing|es|ed)?\\s(cr|pr|code review|code-review|review))', '@'))-LENGTH(REGEXP_REPLACE(lower(message),'(add(s|ed|ing)?[\\s\\S]{1,50}(version|v\\d|ver\\d)|(^|\\s)implement(ed|s|ing)?\\s|(make(s)?|made|making)[\\s\\S]{1,50}consitent|updat(e|es|ed|ing)[\\s\\S]{1,25}to[\\s\\S]{1,25}\\d+.\\d|updat(e|es|ed|ing)\\s+(to\\s+)?\\d+\\.\\d|(add(s|ed|ing)?|delet(e|es|ed|ing)|updat(e|es|ed|ing))\\s+([a-zA-Z0-9_\\*\\.])+\\.[a-zA-Z]{1,4}|(^|^[\\s\\S]{0,25}(\\s|\\.|\\?|\\!|\\[|\\]|\\(|\\)|\\:|^|$|\\,|\'|"|/|#|\\$|\\%|&|\\*|\\+|=|`|;|<|>|@|~|{|}|_|\\|))(upgrad(e|es|ed|ing)|configur(e|es|ed|ing)|chang(e|es|ed|ing)|(keep|change)\\s+(the\\s+)?default|new|merg(e|es|ed|ing)|clear(s|ed|ing)?|creat(e|es|ed|ing)|cast(s|et|ing)?[\\S\\s]{1,40}\\sas|add(s|ed|ing)?|Initial revision|(im)?port(s|ed|ing)?|(un)?hid(e|es|den)|updat(e|es|ed|ing)|upload(s|ed|ing)?|disabl(e|es|ed|ing)|delet(e|es|ed|ing)|enabl(e|es|ed|ing)|quirk(s|ed|ing)?|skip(s|ed|ing)?|switch(s|ed|ing)?|allow(s|ed|ing)?|provid(e|es|ed|ing)|remov(e|es|ed|ing)|refresh(s|ed|ing)?|no message|wip|work in progress|message|change(-|\\s)?set|commit)(\\s|\\.|\\?|\\!|\\[|\\]|\\(|\\)|\\:|^|$|\\,|\'|"|/|#|\\$|\\%|&|\\*|\\+|=|`|;|<|>|@|~|{|}|_|\\|)|^\\[(IMP|imp)\\]|support(s|ed|ing)?\\sfor\\s|show(es|ed|ing)?[\\s\\S]instead|scal(e|es|ed|ing)?\\s(up|down)|(cr|pr)(s)?(-)?(d+)?\\sfix(es)?|fix(ing|es|ed)?\\s(cr|pr|code review|code-review|review))', '')))
# Adaptive :build_non_adaptive_context()
-
(LENGTH(REGEXP_REPLACE(lower(message),'(((\\s|\\.|\\?|\\!|\\[|\\]|\\(|\\)|\\:|^|$|\\,|\'|"|/|#|\\$|\\%|&|\\*|\\+|=|`|;|<|>|@|~|{|}|_|\\|)((un)?hid(e|es|den)|allow(s|ed|ing)?|buil(t|ds|ing)|calibirat(e|es|ed|ing)|configure|deferr(ed|s|ing)?|enhanc(e|es|ed|ing)|extend(s|ed|ing)?|form(ed|s|ing)?|report(s|ed|ing)?|support(s|ed|ing)?|add(s|ed|ing)?|creat(e|es|ing)|disabl(e|es|ed|ing)|implement(ed|s|ing)?|import(s|ed|ing)?|introduc(e|es|ed|ing)|port(s|ed|ing)?|provid(e|es|ed|ing)|updat(e|es|ed|ing)|upgrad(e|es|ed|ing)))\\s[\\s\\S]{0,50}(change( |-)?log|comment(s)?|copy( |-)?right(s)?|doc(s)?|documentation|explanation(s)?|man( |-)?page(s)?|manual|note(s)?|readme(.md)?|[-a-z\\d_/\\\\]*.(md|txt)|translation(s)?|java( |-)?doc(s)?|java( |-)?documentation|example(s)?|diagram(s)?|guide(s)?|gitignore|icon(s)?|doc( |-)?string(s)?|tutorials(s)?|help|man|doc( |-)?string(s)?|desc(ription)?(s)?|copy( |-)?right(s)?|explanation(s)?|release notes|tag(s)?|bug|helper|miss(ing|ed)|to( |-)?do(s)?|warning(s)?)|^[\\s\\S]{0,50}(transla(tion|et|eted|ets|ting)|readme(.md)?)|((\\s|\\.|\\?|\\!|\\[|\\]|\\(|\\)|\\:|^|$|\\,|\'|"|/|#|\\$|\\%|&|\\*|\\+|=|`|;|<|>|@|~|{|}|_|\\|)(remov(e|es|ed|ing)))\\s[\\s\\S]{0,50}(change( |-)?log|comment(s)?|copy( |-)?right(s)?|doc(s)?|documentation|explanation(s)?|man( |-)?page(s)?|manual|note(s)?|readme(.md)?|[-a-z\\d_/\\\\]*.(md|txt)|translation(s)?|java( |-)?doc(s)?|java( |-)?documentation|example(s)?|diagram(s)?|guide(s)?|gitignore|icon(s)?|doc( |-)?string(s)?|tutorials(s)?|help|man|doc( |-)?string(s)?|desc(ription)?(s)?|copy( |-)?right(s)?|explanation(s)?|release notes|tag(s)?|assertion(s)?|assignment(s)?|code|conditional(s)?|control|definition(s)?|delegate|delegation|design pattern(s)?|error(-| )?code(s)?|exception(s)?|flag(s)?|getter(s)?|guard clause(s)?|hierarch(y|ies)|implementation(s)?|inheritance|inline|internal|macro(s)?|magic number(s)?|modifier(s)?|null object(s)?|object(s)?|patch(es)?|pointer(s)?|polymorphism|quer(y|ies)|reference(s)?|ref(s)?|return type|setter(s)?|static|sub(-| )?class(es)?|super(-| )?class(es)?|(sub)?(-| )?system(s)?|uninline|variable(s)?|handler|plugin|contravariant|covariant|action(s)?|queue(s)?|stack(s)?|driver(s)?|storage|tool(s)?|log(s)?|setting(s)?|fall( |-)back(s)?|memory|param(s)?|volatile|file(s)?|generic(s)?|initialization(s)?|public|protected|private|framework|singelton|declaration(s)?|init|destructor(s)?|instances(s)?|primitive(s)?|algorithm(s)?|class(es)?|collection(s)?|constant(s)?|constructor(s)?|field(s)?|function(s)?|interface(s)?|member(s)?|method(s)?|parameter(s)?|structure(s)?|template(s)?|type(s)?|unit(s)?|module(s)?|unnecessary|unneeded|unused|(not|never|no longer) used|no longer needed|redundant|useless|duplicate(d)?|deprecated|obsolete(d)?|commented|([a-zA-Z0-9_\\*\\.])+\\.[a-zA-Z]{1,4}))', '@'))-LENGTH(REGEXP_REPLACE(lower(message),'(((\\s|\\.|\\?|\\!|\\[|\\]|\\(|\\)|\\:|^|$|\\,|\'|"|/|#|\\$|\\%|&|\\*|\\+|=|`|;|<|>|@|~|{|}|_|\\|)((un)?hid(e|es|den)|allow(s|ed|ing)?|buil(t|ds|ing)|calibirat(e|es|ed|ing)|configure|deferr(ed|s|ing)?|enhanc(e|es|ed|ing)|extend(s|ed|ing)?|form(ed|s|ing)?|report(s|ed|ing)?|support(s|ed|ing)?|add(s|ed|ing)?|creat(e|es|ing)|disabl(e|es|ed|ing)|implement(ed|s|ing)?|import(s|ed|ing)?|introduc(e|es|ed|ing)|port(s|ed|ing)?|provid(e|es|ed|ing)|updat(e|es|ed|ing)|upgrad(e|es|ed|ing)))\\s[\\s\\S]{0,50}(change( |-)?log|comment(s)?|copy( |-)?right(s)?|doc(s)?|documentation|explanation(s)?|man( |-)?page(s)?|manual|note(s)?|readme(.md)?|[-a-z\\d_/\\\\]*.(md|txt)|translation(s)?|java( |-)?doc(s)?|java( |-)?documentation|example(s)?|diagram(s)?|guide(s)?|gitignore|icon(s)?|doc( |-)?string(s)?|tutorials(s)?|help|man|doc( |-)?string(s)?|desc(ription)?(s)?|copy( |-)?right(s)?|explanation(s)?|release notes|tag(s)?|bug|helper|miss(ing|ed)|to( |-)?do(s)?|warning(s)?)|^[\\s\\S]{0,50}(transla(tion|et|eted|ets|ting)|readme(.md)?)|((\\s|\\.|\\?|\\!|\\[|\\]|\\(|\\)|\\:|^|$|\\,|\'|"|/|#|\\$|\\%|&|\\*|\\+|=|`|;|<|>|@|~|{|}|_|\\|)(remov(e|es|ed|ing)))\\s[\\s\\S]{0,50}(change( |-)?log|comment(s)?|copy( |-)?right(s)?|doc(s)?|documentation|explanation(s)?|man( |-)?page(s)?|manual|note(s)?|readme(.md)?|[-a-z\\d_/\\\\]*.(md|txt)|translation(s)?|java( |-)?doc(s)?|java( |-)?documentation|example(s)?|diagram(s)?|guide(s)?|gitignore|icon(s)?|doc( |-)?string(s)?|tutorials(s)?|help|man|doc( |-)?string(s)?|desc(ription)?(s)?|copy( |-)?right(s)?|explanation(s)?|release notes|tag(s)?|assertion(s)?|assignment(s)?|code|conditional(s)?|control|definition(s)?|delegate|delegation|design pattern(s)?|error(-| )?code(s)?|exception(s)?|flag(s)?|getter(s)?|guard clause(s)?|hierarch(y|ies)|implementation(s)?|inheritance|inline|internal|macro(s)?|magic number(s)?|modifier(s)?|null object(s)?|object(s)?|patch(es)?|pointer(s)?|polymorphism|quer(y|ies)|reference(s)?|ref(s)?|return type|setter(s)?|static|sub(-| )?class(es)?|super(-| )?class(es)?|(sub)?(-| )?system(s)?|uninline|variable(s)?|handler|plugin|contravariant|covariant|action(s)?|queue(s)?|stack(s)?|driver(s)?|storage|tool(s)?|log(s)?|setting(s)?|fall( |-)back(s)?|memory|param(s)?|volatile|file(s)?|generic(s)?|initialization(s)?|public|protected|private|framework|singelton|declaration(s)?|init|destructor(s)?|instances(s)?|primitive(s)?|algorithm(s)?|class(es)?|collection(s)?|constant(s)?|constructor(s)?|field(s)?|function(s)?|interface(s)?|member(s)?|method(s)?|parameter(s)?|structure(s)?|template(s)?|type(s)?|unit(s)?|module(s)?|unnecessary|unneeded|unused|(not|never|no longer) used|no longer needed|redundant|useless|duplicate(d)?|deprecated|obsolete(d)?|commented|([a-zA-Z0-9_\\*\\.])+\\.[a-zA-Z]{1,4}))', '')))
# Adaptive :build_non_adaptive_linguistic()
-
(LENGTH(REGEXP_REPLACE(lower(message),'(((\\s|\\.|\\?|\\!|\\[|\\]|\\(|\\)|\\:|^|$|\\,|\'|"|/|#|\\$|\\%|&|\\*|\\+|=|`|;|<|>|@|~|{|}|_|\\|)(can|could|ha(ve|s|d)|may|might|must|need|ought|shall|should|will|would))[\\s\\S]{0,10}((((\\s|\\.|\\?|\\!|\\[|\\]|\\(|\\)|\\:|^|$|\\,|\'|"|/|#|\\$|\\%|&|\\*|\\+|=|`|;|<|>|@|~|{|}|_|\\|)((un)?hid(e|es|den)|allow(s|ed|ing)?|buil(t|ds|ing)|calibirat(e|es|ed|ing)|configure|deferr(ed|s|ing)?|enhanc(e|es|ed|ing)|extend(s|ed|ing)?|form(ed|s|ing)?|report(s|ed|ing)?|support(s|ed|ing)?|add(s|ed|ing)?|creat(e|es|ing)|disabl(e|es|ed|ing)|implement(ed|s|ing)?|import(s|ed|ing)?|introduc(e|es|ed|ing)|port(s|ed|ing)?|provid(e|es|ed|ing)|updat(e|es|ed|ing)|upgrad(e|es|ed|ing)))\\s[\\s\\S]{0,50}(ability|configuration|conversion|debug|new|possibility|support|test(s)?|tweak(s)?|mode|option|assertion(s)?|assignment(s)?|code|conditional(s)?|control|definition(s)?|delegate|delegation|design pattern(s)?|error(-| )?code(s)?|exception(s)?|flag(s)?|getter(s)?|guard clause(s)?|hierarch(y|ies)|implementation(s)?|inheritance|inline|internal|macro(s)?|magic number(s)?|modifier(s)?|null object(s)?|object(s)?|patch(es)?|pointer(s)?|polymorphism|quer(y|ies)|reference(s)?|ref(s)?|return type|setter(s)?|static|sub(-| )?class(es)?|super(-| )?class(es)?|(sub)?(-| )?system(s)?|uninline|variable(s)?|handler|plugin|contravariant|covariant|action(s)?|queue(s)?|stack(s)?|driver(s)?|storage|tool(s)?|log(s)?|setting(s)?|fall( |-)back(s)?|memory|param(s)?|volatile|file(s)?|generic(s)?|initialization(s)?|public|protected|private|framework|singelton|declaration(s)?|init|destructor(s)?|instances(s)?|primitive(s)?|algorithm(s)?|class(es)?|collection(s)?|constant(s)?|constructor(s)?|field(s)?|function(s)?|interface(s)?|member(s)?|method(s)?|parameter(s)?|structure(s)?|template(s)?|type(s)?|unit(s)?|module(s)?)(\\s|\\.|\\?|\\!|\\[|\\]|\\(|\\)|\\:|^|$|\\,|\'|"|/|#|\\$|\\%|&|\\*|\\+|=|`|;|<|>|@|~|{|}|_|\\|)))|((\\s|\\.|\\?|\\!|\\[|\\]|\\(|\\)|\\:|^|$|\\,|\'|"|/|#|\\$|\\%|&|\\*|\\+|=|`|;|<|>|@|~|{|}|_|\\|)(aren\'t|didn\'t|don\'t|doesn\'t|isn\'t|lack|n\'t|never|no|nobody|none|not|nothing|weren\'t|without|won\'t))[\\s\\S]{0,10}((((\\s|\\.|\\?|\\!|\\[|\\]|\\(|\\)|\\:|^|$|\\,|\'|"|/|#|\\$|\\%|&|\\*|\\+|=|`|;|<|>|@|~|{|}|_|\\|)((un)?hid(e|es|den)|allow(s|ed|ing)?|buil(t|ds|ing)|calibirat(e|es|ed|ing)|configure|deferr(ed|s|ing)?|enhanc(e|es|ed|ing)|extend(s|ed|ing)?|form(ed|s|ing)?|report(s|ed|ing)?|support(s|ed|ing)?|add(s|ed|ing)?|creat(e|es|ing)|disabl(e|es|ed|ing)|implement(ed|s|ing)?|import(s|ed|ing)?|introduc(e|es|ed|ing)|port(s|ed|ing)?|provid(e|es|ed|ing)|updat(e|es|ed|ing)|upgrad(e|es|ed|ing)))\\s[\\s\\S]{0,50}(ability|configuration|conversion|debug|new|possibility|support|test(s)?|tweak(s)?|mode|option|assertion(s)?|assignment(s)?|code|conditional(s)?|control|definition(s)?|delegate|delegation|design pattern(s)?|error(-| )?code(s)?|exception(s)?|flag(s)?|getter(s)?|guard clause(s)?|hierarch(y|ies)|implementation(s)?|inheritance|inline|internal|macro(s)?|magic number(s)?|modifier(s)?|null object(s)?|object(s)?|patch(es)?|pointer(s)?|polymorphism|quer(y|ies)|reference(s)?|ref(s)?|return type|setter(s)?|static|sub(-| )?class(es)?|super(-| )?class(es)?|(sub)?(-| )?system(s)?|uninline|variable(s)?|handler|plugin|contravariant|covariant|action(s)?|queue(s)?|stack(s)?|driver(s)?|storage|tool(s)?|log(s)?|setting(s)?|fall( |-)back(s)?|memory|param(s)?|volatile|file(s)?|generic(s)?|initialization(s)?|public|protected|private|framework|singelton|declaration(s)?|init|destructor(s)?|instances(s)?|primitive(s)?|algorithm(s)?|class(es)?|collection(s)?|constant(s)?|constructor(s)?|field(s)?|function(s)?|interface(s)?|member(s)?|method(s)?|parameter(s)?|structure(s)?|template(s)?|type(s)?|unit(s)?|module(s)?)(\\s|\\.|\\?|\\!|\\[|\\]|\\(|\\)|\\:|^|$|\\,|\'|"|/|#|\\$|\\%|&|\\*|\\+|=|`|;|<|>|@|~|{|}|_|\\|)))|((\\s|\\.|\\?|\\!|\\[|\\]|\\(|\\)|\\:|^|$|\\,|\'|"|/|#|\\$|\\%|&|\\*|\\+|=|`|;|<|>|@|~|{|}|_|\\|)(for(get|gets|got|geting)|allow(s|ed|ing)?))[\\s\\S]{0,10}((((\\s|\\.|\\?|\\!|\\[|\\]|\\(|\\)|\\:|^|$|\\,|\'|"|/|#|\\$|\\%|&|\\*|\\+|=|`|;|<|>|@|~|{|}|_|\\|)((un)?hid(e|es|den)|allow(s|ed|ing)?|buil(t|ds|ing)|calibirat(e|es|ed|ing)|configure|deferr(ed|s|ing)?|enhanc(e|es|ed|ing)|extend(s|ed|ing)?|form(ed|s|ing)?|report(s|ed|ing)?|support(s|ed|ing)?|add(s|ed|ing)?|creat(e|es|ing)|disabl(e|es|ed|ing)|implement(ed|s|ing)?|import(s|ed|ing)?|introduc(e|es|ed|ing)|port(s|ed|ing)?|provid(e|es|ed|ing)|updat(e|es|ed|ing)|upgrad(e|es|ed|ing)))\\s[\\s\\S]{0,50}(ability|configuration|conversion|debug|new|possibility|support|test(s)?|tweak(s)?|mode|option|assertion(s)?|assignment(s)?|code|conditional(s)?|control|definition(s)?|delegate|delegation|design pattern(s)?|error(-| )?code(s)?|exception(s)?|flag(s)?|getter(s)?|guard clause(s)?|hierarch(y|ies)|implementation(s)?|inheritance|inline|internal|macro(s)?|magic number(s)?|modifier(s)?|null object(s)?|object(s)?|patch(es)?|pointer(s)?|polymorphism|quer(y|ies)|reference(s)?|ref(s)?|return type|setter(s)?|static|sub(-| )?class(es)?|super(-| )?class(es)?|(sub)?(-| )?system(s)?|uninline|variable(s)?|handler|plugin|contravariant|covariant|action(s)?|queue(s)?|stack(s)?|driver(s)?|storage|tool(s)?|log(s)?|setting(s)?|fall( |-)back(s)?|memory|param(s)?|volatile|file(s)?|generic(s)?|initialization(s)?|public|protected|private|framework|singelton|declaration(s)?|init|destructor(s)?|instances(s)?|primitive(s)?|algorithm(s)?|class(es)?|collection(s)?|constant(s)?|constructor(s)?|field(s)?|function(s)?|interface(s)?|member(s)?|method(s)?|parameter(s)?|structure(s)?|template(s)?|type(s)?|unit(s)?|module(s)?)(\\s|\\.|\\?|\\!|\\[|\\]|\\(|\\)|\\:|^|$|\\,|\'|"|/|#|\\$|\\%|&|\\*|\\+|=|`|;|<|>|@|~|{|}|_|\\|))))', '@'))-LENGTH(REGEXP_REPLACE(lower(message),'(((\\s|\\.|\\?|\\!|\\[|\\]|\\(|\\)|\\:|^|$|\\,|\'|"|/|#|\\$|\\%|&|\\*|\\+|=|`|;|<|>|@|~|{|}|_|\\|)(can|could|ha(ve|s|d)|may|might|must|need|ought|shall|should|will|would))[\\s\\S]{0,10}((((\\s|\\.|\\?|\\!|\\[|\\]|\\(|\\)|\\:|^|$|\\,|\'|"|/|#|\\$|\\%|&|\\*|\\+|=|`|;|<|>|@|~|{|}|_|\\|)((un)?hid(e|es|den)|allow(s|ed|ing)?|buil(t|ds|ing)|calibirat(e|es|ed|ing)|configure|deferr(ed|s|ing)?|enhanc(e|es|ed|ing)|extend(s|ed|ing)?|form(ed|s|ing)?|report(s|ed|ing)?|support(s|ed|ing)?|add(s|ed|ing)?|creat(e|es|ing)|disabl(e|es|ed|ing)|implement(ed|s|ing)?|import(s|ed|ing)?|introduc(e|es|ed|ing)|port(s|ed|ing)?|provid(e|es|ed|ing)|updat(e|es|ed|ing)|upgrad(e|es|ed|ing)))\\s[\\s\\S]{0,50}(ability|configuration|conversion|debug|new|possibility|support|test(s)?|tweak(s)?|mode|option|assertion(s)?|assignment(s)?|code|conditional(s)?|control|definition(s)?|delegate|delegation|design pattern(s)?|error(-| )?code(s)?|exception(s)?|flag(s)?|getter(s)?|guard clause(s)?|hierarch(y|ies)|implementation(s)?|inheritance|inline|internal|macro(s)?|magic number(s)?|modifier(s)?|null object(s)?|object(s)?|patch(es)?|pointer(s)?|polymorphism|quer(y|ies)|reference(s)?|ref(s)?|return type|setter(s)?|static|sub(-| )?class(es)?|super(-| )?class(es)?|(sub)?(-| )?system(s)?|uninline|variable(s)?|handler|plugin|contravariant|covariant|action(s)?|queue(s)?|stack(s)?|driver(s)?|storage|tool(s)?|log(s)?|setting(s)?|fall( |-)back(s)?|memory|param(s)?|volatile|file(s)?|generic(s)?|initialization(s)?|public|protected|private|framework|singelton|declaration(s)?|init|destructor(s)?|instances(s)?|primitive(s)?|algorithm(s)?|class(es)?|collection(s)?|constant(s)?|constructor(s)?|field(s)?|function(s)?|interface(s)?|member(s)?|method(s)?|parameter(s)?|structure(s)?|template(s)?|type(s)?|unit(s)?|module(s)?)(\\s|\\.|\\?|\\!|\\[|\\]|\\(|\\)|\\:|^|$|\\,|\'|"|/|#|\\$|\\%|&|\\*|\\+|=|`|;|<|>|@|~|{|}|_|\\|)))|((\\s|\\.|\\?|\\!|\\[|\\]|\\(|\\)|\\:|^|$|\\,|\'|"|/|#|\\$|\\%|&|\\*|\\+|=|`|;|<|>|@|~|{|}|_|\\|)(aren\'t|didn\'t|don\'t|doesn\'t|isn\'t|lack|n\'t|never|no|nobody|none|not|nothing|weren\'t|without|won\'t))[\\s\\S]{0,10}((((\\s|\\.|\\?|\\!|\\[|\\]|\\(|\\)|\\:|^|$|\\,|\'|"|/|#|\\$|\\%|&|\\*|\\+|=|`|;|<|>|@|~|{|}|_|\\|)((un)?hid(e|es|den)|allow(s|ed|ing)?|buil(t|ds|ing)|calibirat(e|es|ed|ing)|configure|deferr(ed|s|ing)?|enhanc(e|es|ed|ing)|extend(s|ed|ing)?|form(ed|s|ing)?|report(s|ed|ing)?|support(s|ed|ing)?|add(s|ed|ing)?|creat(e|es|ing)|disabl(e|es|ed|ing)|implement(ed|s|ing)?|import(s|ed|ing)?|introduc(e|es|ed|ing)|port(s|ed|ing)?|provid(e|es|ed|ing)|updat(e|es|ed|ing)|upgrad(e|es|ed|ing)))\\s[\\s\\S]{0,50}(ability|configuration|conversion|debug|new|possibility|support|test(s)?|tweak(s)?|mode|option|assertion(s)?|assignment(s)?|code|conditional(s)?|control|definition(s)?|delegate|delegation|design pattern(s)?|error(-| )?code(s)?|exception(s)?|flag(s)?|getter(s)?|guard clause(s)?|hierarch(y|ies)|implementation(s)?|inheritance|inline|internal|macro(s)?|magic number(s)?|modifier(s)?|null object(s)?|object(s)?|patch(es)?|pointer(s)?|polymorphism|quer(y|ies)|reference(s)?|ref(s)?|return type|setter(s)?|static|sub(-| )?class(es)?|super(-| )?class(es)?|(sub)?(-| )?system(s)?|uninline|variable(s)?|handler|plugin|contravariant|covariant|action(s)?|queue(s)?|stack(s)?|driver(s)?|storage|tool(s)?|log(s)?|setting(s)?|fall( |-)back(s)?|memory|param(s)?|volatile|file(s)?|generic(s)?|initialization(s)?|public|protected|private|framework|singelton|declaration(s)?|init|destructor(s)?|instances(s)?|primitive(s)?|algorithm(s)?|class(es)?|collection(s)?|constant(s)?|constructor(s)?|field(s)?|function(s)?|interface(s)?|member(s)?|method(s)?|parameter(s)?|structure(s)?|template(s)?|type(s)?|unit(s)?|module(s)?)(\\s|\\.|\\?|\\!|\\[|\\]|\\(|\\)|\\:|^|$|\\,|\'|"|/|#|\\$|\\%|&|\\*|\\+|=|`|;|<|>|@|~|{|}|_|\\|)))|((\\s|\\.|\\?|\\!|\\[|\\]|\\(|\\)|\\:|^|$|\\,|\'|"|/|#|\\$|\\%|&|\\*|\\+|=|`|;|<|>|@|~|{|}|_|\\|)(for(get|gets|got|geting)|allow(s|ed|ing)?))[\\s\\S]{0,10}((((\\s|\\.|\\?|\\!|\\[|\\]|\\(|\\)|\\:|^|$|\\,|\'|"|/|#|\\$|\\%|&|\\*|\\+|=|`|;|<|>|@|~|{|}|_|\\|)((un)?hid(e|es|den)|allow(s|ed|ing)?|buil(t|ds|ing)|calibirat(e|es|ed|ing)|configure|deferr(ed|s|ing)?|enhanc(e|es|ed|ing)|extend(s|ed|ing)?|form(ed|s|ing)?|report(s|ed|ing)?|support(s|ed|ing)?|add(s|ed|ing)?|creat(e|es|ing)|disabl(e|es|ed|ing)|implement(ed|s|ing)?|import(s|ed|ing)?|introduc(e|es|ed|ing)|port(s|ed|ing)?|provid(e|es|ed|ing)|updat(e|es|ed|ing)|upgrad(e|es|ed|ing)))\\s[\\s\\S]{0,50}(ability|configuration|conversion|debug|new|possibility|support|test(s)?|tweak(s)?|mode|option|assertion(s)?|assignment(s)?|code|conditional(s)?|control|definition(s)?|delegate|delegation|design pattern(s)?|error(-| )?code(s)?|exception(s)?|flag(s)?|getter(s)?|guard clause(s)?|hierarch(y|ies)|implementation(s)?|inheritance|inline|internal|macro(s)?|magic number(s)?|modifier(s)?|null object(s)?|object(s)?|patch(es)?|pointer(s)?|polymorphism|quer(y|ies)|reference(s)?|ref(s)?|return type|setter(s)?|static|sub(-| )?class(es)?|super(-| )?class(es)?|(sub)?(-| )?system(s)?|uninline|variable(s)?|handler|plugin|contravariant|covariant|action(s)?|queue(s)?|stack(s)?|driver(s)?|storage|tool(s)?|log(s)?|setting(s)?|fall( |-)back(s)?|memory|param(s)?|volatile|file(s)?|generic(s)?|initialization(s)?|public|protected|private|framework|singelton|declaration(s)?|init|destructor(s)?|instances(s)?|primitive(s)?|algorithm(s)?|class(es)?|collection(s)?|constant(s)?|constructor(s)?|field(s)?|function(s)?|interface(s)?|member(s)?|method(s)?|parameter(s)?|structure(s)?|template(s)?|type(s)?|unit(s)?|module(s)?)(\\s|\\.|\\?|\\!|\\[|\\]|\\(|\\)|\\:|^|$|\\,|\'|"|/|#|\\$|\\%|&|\\*|\\+|=|`|;|<|>|@|~|{|}|_|\\|))))', '')))
# Adaptive - end
 )
 ;


# Run in Standard sql
CREATE OR REPLACE FUNCTION
general.bq_core_adaptive
 (message string)
 RETURNS int64
AS (
# Model language based on commit: b7618c31efc5f3ae85f5300239c7bade872ad212
# Core Adaptive Term
(LENGTH(REGEXP_REPLACE(lower(message),'((\\s|\\.|\\?|\\!|\\[|\\]|\\(|\\)|\\:|^|$|\\,|\'|"|/|#|\\$|\\%|&|\\*|\\+|=|`|;|<|>|@|~|{|}|_|\\|)(add(s|ed|ing)?|creat(e|es|ing)|disabl(e|es|ed|ing)|implement(ed|s|ing)?|import(s|ed|ing)?|introduc(e|es|ed|ing)|port(s|ed|ing)?|provid(e|es|ed|ing)|updat(e|es|ed|ing)|upgrad(e|es|ed|ing))(\\s|\\.|\\?|\\!|\\[|\\]|\\(|\\)|\\:|^|$|\\,|\'|"|/|#|\\$|\\%|&|\\*|\\+|=|`|;|<|>|@|~|{|}|_|\\|))', '@'))-LENGTH(REGEXP_REPLACE(lower(message),'((\\s|\\.|\\?|\\!|\\[|\\]|\\(|\\)|\\:|^|$|\\,|\'|"|/|#|\\$|\\%|&|\\*|\\+|=|`|;|<|>|@|~|{|}|_|\\|)(add(s|ed|ing)?|creat(e|es|ing)|disabl(e|es|ed|ing)|implement(ed|s|ing)?|import(s|ed|ing)?|introduc(e|es|ed|ing)|port(s|ed|ing)?|provid(e|es|ed|ing)|updat(e|es|ed|ing)|upgrad(e|es|ed|ing))(\\s|\\.|\\?|\\!|\\[|\\]|\\(|\\)|\\:|^|$|\\,|\'|"|/|#|\\$|\\%|&|\\*|\\+|=|`|;|<|>|@|~|{|}|_|\\|))', '')))
#Core Adaptive Term - end
 )
 ;