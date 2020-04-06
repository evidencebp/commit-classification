# Run in Starndad sql
CREATE OR REPLACE FUNCTION
ccp.bq_non_positive_linguistic_refactor
 (message string)
 RETURNS int64
AS (
# Model language based on commit: 5cd4738202154452854991b2714ce49459316371
# Refactor :build_non_positive_linguistic(build_refactor_regex())
-
(LENGTH(REGEXP_REPLACE(lower(message),'(((\\s|\\.|\\?|\\!|\\[|\\]|\\(|\\)|\\:|^|$|\\,|\'|"|/|#|\\$|\\%|&|\\*|\\+|=|`|;|<|>|@|~|{|}|\\|)(can|could|ha(ve|s|d)|may|might|must|need|ought|shall|should|will|would))[\\s\\S]{0,10}(((\\s|\\.|\\?|\\!|\\[|\\]|\\(|\\)|\\:|^|$|\\,|\'|"|/|#|\\$|\\%|&|\\*|\\+|=|`|;|<|>|@|~|{|}|\\|)(clean(ing)?(-| )?up(s)?|call(s|ed|ing)?[\\s\\S]{1,50}instead|collaps(e|es|ed|ing)|consolidat(e|es|ed|ing)|decompos(e|es|ed|ing)|drop(ed|s|ing)?( back)|encapsulat(e|es|ed|ing)|gereneliz(e|es|ed|ing)|optimiz(e|es|ed|ing|ation|ations)|pull(ed|s|ing)? (up|down)|re(-)?(write|wrote)|re(-| )?factor(ed|s|ing|ings)?|re(-)?implement(ed|s|ing)?|renam(e|es|ed|ing|ings)|better nam(e|es|ing)|re(-)?organiz(e|es|ed|ing)|re(-)?organization|re(-)?work(ed|s|ing|ings)?|reorg|simplif(y|es|ied|ying|ication)|suppress(es|ed|ing)? warning(s)?|unif(y|ies|ied|ing)|uninline|beef(ed|s|ing)? up|refactor(ing)?(s)?|code improvement(s)?|revis(e|es|ed|ing)|re(-)?construct(s|ed|ing)?|re(-)?(write|write|wrote|writing)|re(-)?cod(e|ed|es|ing)|factor(ed|s|ing)? out|re(-| )?packag(e|es|ed|ing))(\\s|\\.|\\?|\\!|\\[|\\]|\\(|\\)|\\:|^|$|\\,|\'|"|/|#|\\$|\\%|&|\\*|\\+|=|`|;|<|>|@|~|{|}|\\|))|((((\\s|\\.|\\?|\\!|\\[|\\]|\\(|\\)|\\:|^|$|\\,|\'|"|/|#|\\$|\\%|&|\\*|\\+|=|`|;|<|>|@|~|{|}|\\|)(clean(ing|s|ed)?clean(ing)?(-| )?up(s)?|combin(e|es|ed|ing)|compos(e|es|ed|ing)|de(-| )?compos(e|es|ed|ing)|convert(ed|s|ing)?|dead|deprecat(e|es|ed|ing)|drop(ed|s|ing)?|duplicat(e|es|ed|ing)|extract(ed|s|ing)?|improv(e|es|ed|ing)|increas(e|es|ed|ing)|(make|makes|made|making)|mov(e|es|ed|ing)|rebuil(d|ds|ding|t)|replac(e|es|ed|ing)|redundant|re(-|)?organiz(e|es|ed|ing)|re(-|)?structur(e|es|ed|ing)|separat(e|e s|ed|ing)|split(s|ing)?|subsitut(e|es|ed|ing)|tid(y|ying|ied)|short(:?en|er|ing|s)?|polish(ed|es|ing)?|(get|got|getting) rid|encapsulate|hide(e|es|ed|ing)|un(-| )?hid(e|es|ed|ing)|parameteriz(e|es|ed|ing)|substitut(e|es|ed|ing)|unnecessary|unneeded|unused|(not|never|no longer) used|no longer needed|redundant|useless|duplicate(d)?|deprecated|obsolete(d)?|commented))((\\s|\\.|\\?|\\!|\\[|\\]|\\(|\\)|\\:|^|$|\\,|\'|"|/|#|\\$|\\%|&|\\*|\\+|=|`|;|<|>|@|~|{|}|\\|)|(\\s|\\.|\\?|\\!|\\[|\\]|\\(|\\)|\\:|^|$|\\,|\'|"|/|#|\\$|\\%|&|\\*|\\+|=|`|;|<|>|@|~|{|}|\\|)[\\s\\S]{0,50}(\\s|\\.|\\?|\\!|\\[|\\]|\\(|\\)|\\:|^|$|\\,|\'|"|/|#|\\$|\\%|&|\\*|\\+|=|`|;|<|>|@|~|{|}|\\|))(algorithm(s)?|assertion(s)?|assignment(s)?|class(es)?|code|collection(s)?|conditional(s)?|constant(s)?|constructor(s)?|control|definition(s)?|delegate|delegation|design pattern(s)?|error(-| )?code(s)?|exception(s)?|field(s)?|flag(s)?|function(s)?|getter(s)?|guard clause(s)?|hierarch(y|ies)|implementation(s)?|inheritance|inline|interface(s)?|internal|macro(s)?|magic number(s)?|member(s)?|method(s)?|modifier(s)?|null object(s)?|object(s)?|parameter(s)?|patch(es)?|pointer(s)?|polymorphism|quer(y|ies)|reference(s)?|ref(s)?|return type|setter(s)?|static|structure(s)?|sub(-| )?class(es)?|super(-| )?class(es)?|(sub)?(-| )?system(s)?|template(s)?|type(s)?|uninline|variable(s)?|handler|plugin|unit(s)?|contravariant|covariant|action(s)?|queue(s)?|stack(s)?|driver(s)?|storage|tool(s)?|module(s)?|log(s)?|setting(s)?|fall( |-)back(s)?|memory|param(s)?|volatile|file(s)?|generic(s)?|initialization(s)?|public|protected|private|framework|singelton|declaration(s)?|init|destructor(s)?|instances(s)?|primitive(s)?|(helper|utility|auxiliary) function(s)?)(\\s|\\.|\\?|\\!|\\[|\\]|\\(|\\)|\\:|^|$|\\,|\'|"|/|#|\\$|\\%|&|\\*|\\+|=|`|;|<|>|@|~|{|}|\\|)))|((^|^[\\s\\S]{0,25}(\\s|\\.|\\?|\\!|\\[|\\]|\\(|\\)|\\:|^|$|\\,|\'|"|/|#|\\$|\\%|&|\\*|\\+|=|`|;|<|>|@|~|{|}|\\|))(clean(ing|s|ed)?(-| )?up(s)?|cleaner|deprecat(e|es|ed|ing)|extract(ed|s|ing)?|re(-|)?organiz(e|es|ed|ing)|re(-|)?structur(e|es|ed|ing)|tid(y|ying|ied) up|improv(e|ed|es|ing|ement|ements)|re(-|)?organiz(e|es|ed|ing)|re(-|)?structur(e|es|ed|ing)|(helper|utility|auxiliary) function(s)?|(move|moved|moves|moving) to|separat(e|es|ed|ing)|split(s|ing)?|->)(\\s|\\.|\\?|\\!|\\[|\\]|\\(|\\)|\\:|^|$|\\,|\'|"|/|#|\\$|\\%|&|\\*|\\+|=|`|;|<|>|@|~|{|}|\\|)))|((\\s|\\.|\\?|\\!|\\[|\\]|\\(|\\)|\\:|^|$|\\,|\'|"|/|#|\\$|\\%|&|\\*|\\+|=|`|;|<|>|@|~|{|}|\\|)(aren\'t|didn\'t|don\'t|doesn\'t|isn\'t|lack|n\'t|never|no|nobody|none|not|nothing|weren\'t|without|won\'t))[\\s\\S]{0,10}(((\\s|\\.|\\?|\\!|\\[|\\]|\\(|\\)|\\:|^|$|\\,|\'|"|/|#|\\$|\\%|&|\\*|\\+|=|`|;|<|>|@|~|{|}|\\|)(clean(ing)?(-| )?up(s)?|call(s|ed|ing)?[\\s\\S]{1,50}instead|collaps(e|es|ed|ing)|consolidat(e|es|ed|ing)|decompos(e|es|ed|ing)|drop(ed|s|ing)?( back)|encapsulat(e|es|ed|ing)|gereneliz(e|es|ed|ing)|optimiz(e|es|ed|ing|ation|ations)|pull(ed|s|ing)? (up|down)|re(-)?(write|wrote)|re(-| )?factor(ed|s|ing|ings)?|re(-)?implement(ed|s|ing)?|renam(e|es|ed|ing|ings)|better nam(e|es|ing)|re(-)?organiz(e|es|ed|ing)|re(-)?organization|re(-)?work(ed|s|ing|ings)?|reorg|simplif(y|es|ied|ying|ication)|suppress(es|ed|ing)? warning(s)?|unif(y|ies|ied|ing)|uninline|beef(ed|s|ing)? up|refactor(ing)?(s)?|code improvement(s)?|revis(e|es|ed|ing)|re(-)?construct(s|ed|ing)?|re(-)?(write|write|wrote|writing)|re(-)?cod(e|ed|es|ing)|factor(ed|s|ing)? out|re(-| )?packag(e|es|ed|ing))(\\s|\\.|\\?|\\!|\\[|\\]|\\(|\\)|\\:|^|$|\\,|\'|"|/|#|\\$|\\%|&|\\*|\\+|=|`|;|<|>|@|~|{|}|\\|))|((((\\s|\\.|\\?|\\!|\\[|\\]|\\(|\\)|\\:|^|$|\\,|\'|"|/|#|\\$|\\%|&|\\*|\\+|=|`|;|<|>|@|~|{|}|\\|)(clean(ing|s|ed)?clean(ing)?(-| )?up(s)?|combin(e|es|ed|ing)|compos(e|es|ed|ing)|de(-| )?compos(e|es|ed|ing)|convert(ed|s|ing)?|dead|deprecat(e|es|ed|ing)|drop(ed|s|ing)?|duplicat(e|es|ed|ing)|extract(ed|s|ing)?|improv(e|es|ed|ing)|increas(e|es|ed|ing)|(make|makes|made|making)|mov(e|es|ed|ing)|rebuil(d|ds|ding|t)|replac(e|es|ed|ing)|redundant|re(-|)?organiz(e|es|ed|ing)|re(-|)?structur(e|es|ed|ing)|separat(e|e s|ed|ing)|split(s|ing)?|subsitut(e|es|ed|ing)|tid(y|ying|ied)|short(:?en|er|ing|s)?|polish(ed|es|ing)?|(get|got|getting) rid|encapsulate|hide(e|es|ed|ing)|un(-| )?hid(e|es|ed|ing)|parameteriz(e|es|ed|ing)|substitut(e|es|ed|ing)|unnecessary|unneeded|unused|(not|never|no longer) used|no longer needed|redundant|useless|duplicate(d)?|deprecated|obsolete(d)?|commented))((\\s|\\.|\\?|\\!|\\[|\\]|\\(|\\)|\\:|^|$|\\,|\'|"|/|#|\\$|\\%|&|\\*|\\+|=|`|;|<|>|@|~|{|}|\\|)|(\\s|\\.|\\?|\\!|\\[|\\]|\\(|\\)|\\:|^|$|\\,|\'|"|/|#|\\$|\\%|&|\\*|\\+|=|`|;|<|>|@|~|{|}|\\|)[\\s\\S]{0,50}(\\s|\\.|\\?|\\!|\\[|\\]|\\(|\\)|\\:|^|$|\\,|\'|"|/|#|\\$|\\%|&|\\*|\\+|=|`|;|<|>|@|~|{|}|\\|))(algorithm(s)?|assertion(s)?|assignment(s)?|class(es)?|code|collection(s)?|conditional(s)?|constant(s)?|constructor(s)?|control|definition(s)?|delegate|delegation|design pattern(s)?|error(-| )?code(s)?|exception(s)?|field(s)?|flag(s)?|function(s)?|getter(s)?|guard clause(s)?|hierarch(y|ies)|implementation(s)?|inheritance|inline|interface(s)?|internal|macro(s)?|magic number(s)?|member(s)?|method(s)?|modifier(s)?|null object(s)?|object(s)?|parameter(s)?|patch(es)?|pointer(s)?|polymorphism|quer(y|ies)|reference(s)?|ref(s)?|return type|setter(s)?|static|structure(s)?|sub(-| )?class(es)?|super(-| )?class(es)?|(sub)?(-| )?system(s)?|template(s)?|type(s)?|uninline|variable(s)?|handler|plugin|unit(s)?|contravariant|covariant|action(s)?|queue(s)?|stack(s)?|driver(s)?|storage|tool(s)?|module(s)?|log(s)?|setting(s)?|fall( |-)back(s)?|memory|param(s)?|volatile|file(s)?|generic(s)?|initialization(s)?|public|protected|private|framework|singelton|declaration(s)?|init|destructor(s)?|instances(s)?|primitive(s)?|(helper|utility|auxiliary) function(s)?)(\\s|\\.|\\?|\\!|\\[|\\]|\\(|\\)|\\:|^|$|\\,|\'|"|/|#|\\$|\\%|&|\\*|\\+|=|`|;|<|>|@|~|{|}|\\|)))|((^|^[\\s\\S]{0,25}(\\s|\\.|\\?|\\!|\\[|\\]|\\(|\\)|\\:|^|$|\\,|\'|"|/|#|\\$|\\%|&|\\*|\\+|=|`|;|<|>|@|~|{|}|\\|))(clean(ing|s|ed)?(-| )?up(s)?|cleaner|deprecat(e|es|ed|ing)|extract(ed|s|ing)?|re(-|)?organiz(e|es|ed|ing)|re(-|)?structur(e|es|ed|ing)|tid(y|ying|ied) up|improv(e|ed|es|ing|ement|ements)|re(-|)?organiz(e|es|ed|ing)|re(-|)?structur(e|es|ed|ing)|(helper|utility|auxiliary) function(s)?|(move|moved|moves|moving) to|separat(e|es|ed|ing)|split(s|ing)?|->)(\\s|\\.|\\?|\\!|\\[|\\]|\\(|\\)|\\:|^|$|\\,|\'|"|/|#|\\$|\\%|&|\\*|\\+|=|`|;|<|>|@|~|{|}|\\|)))|((\\s|\\.|\\?|\\!|\\[|\\]|\\(|\\)|\\:|^|$|\\,|\'|"|/|#|\\$|\\%|&|\\*|\\+|=|`|;|<|>|@|~|{|}|\\|)(for(get|gets|got|geting)|allow(s|ed|ing)?))[\\s\\S]{0,10}(((\\s|\\.|\\?|\\!|\\[|\\]|\\(|\\)|\\:|^|$|\\,|\'|"|/|#|\\$|\\%|&|\\*|\\+|=|`|;|<|>|@|~|{|}|\\|)(clean(ing)?(-| )?up(s)?|call(s|ed|ing)?[\\s\\S]{1,50}instead|collaps(e|es|ed|ing)|consolidat(e|es|ed|ing)|decompos(e|es|ed|ing)|drop(ed|s|ing)?( back)|encapsulat(e|es|ed|ing)|gereneliz(e|es|ed|ing)|optimiz(e|es|ed|ing|ation|ations)|pull(ed|s|ing)? (up|down)|re(-)?(write|wrote)|re(-| )?factor(ed|s|ing|ings)?|re(-)?implement(ed|s|ing)?|renam(e|es|ed|ing|ings)|better nam(e|es|ing)|re(-)?organiz(e|es|ed|ing)|re(-)?organization|re(-)?work(ed|s|ing|ings)?|reorg|simplif(y|es|ied|ying|ication)|suppress(es|ed|ing)? warning(s)?|unif(y|ies|ied|ing)|uninline|beef(ed|s|ing)? up|refactor(ing)?(s)?|code improvement(s)?|revis(e|es|ed|ing)|re(-)?construct(s|ed|ing)?|re(-)?(write|write|wrote|writing)|re(-)?cod(e|ed|es|ing)|factor(ed|s|ing)? out|re(-| )?packag(e|es|ed|ing))(\\s|\\.|\\?|\\!|\\[|\\]|\\(|\\)|\\:|^|$|\\,|\'|"|/|#|\\$|\\%|&|\\*|\\+|=|`|;|<|>|@|~|{|}|\\|))|((((\\s|\\.|\\?|\\!|\\[|\\]|\\(|\\)|\\:|^|$|\\,|\'|"|/|#|\\$|\\%|&|\\*|\\+|=|`|;|<|>|@|~|{|}|\\|)(clean(ing|s|ed)?clean(ing)?(-| )?up(s)?|combin(e|es|ed|ing)|compos(e|es|ed|ing)|de(-| )?compos(e|es|ed|ing)|convert(ed|s|ing)?|dead|deprecat(e|es|ed|ing)|drop(ed|s|ing)?|duplicat(e|es|ed|ing)|extract(ed|s|ing)?|improv(e|es|ed|ing)|increas(e|es|ed|ing)|(make|makes|made|making)|mov(e|es|ed|ing)|rebuil(d|ds|ding|t)|replac(e|es|ed|ing)|redundant|re(-|)?organiz(e|es|ed|ing)|re(-|)?structur(e|es|ed|ing)|separat(e|e s|ed|ing)|split(s|ing)?|subsitut(e|es|ed|ing)|tid(y|ying|ied)|short(:?en|er|ing|s)?|polish(ed|es|ing)?|(get|got|getting) rid|encapsulate|hide(e|es|ed|ing)|un(-| )?hid(e|es|ed|ing)|parameteriz(e|es|ed|ing)|substitut(e|es|ed|ing)|unnecessary|unneeded|unused|(not|never|no longer) used|no longer needed|redundant|useless|duplicate(d)?|deprecated|obsolete(d)?|commented))((\\s|\\.|\\?|\\!|\\[|\\]|\\(|\\)|\\:|^|$|\\,|\'|"|/|#|\\$|\\%|&|\\*|\\+|=|`|;|<|>|@|~|{|}|\\|)|(\\s|\\.|\\?|\\!|\\[|\\]|\\(|\\)|\\:|^|$|\\,|\'|"|/|#|\\$|\\%|&|\\*|\\+|=|`|;|<|>|@|~|{|}|\\|)[\\s\\S]{0,50}(\\s|\\.|\\?|\\!|\\[|\\]|\\(|\\)|\\:|^|$|\\,|\'|"|/|#|\\$|\\%|&|\\*|\\+|=|`|;|<|>|@|~|{|}|\\|))(algorithm(s)?|assertion(s)?|assignment(s)?|class(es)?|code|collection(s)?|conditional(s)?|constant(s)?|constructor(s)?|control|definition(s)?|delegate|delegation|design pattern(s)?|error(-| )?code(s)?|exception(s)?|field(s)?|flag(s)?|function(s)?|getter(s)?|guard clause(s)?|hierarch(y|ies)|implementation(s)?|inheritance|inline|interface(s)?|internal|macro(s)?|magic number(s)?|member(s)?|method(s)?|modifier(s)?|null object(s)?|object(s)?|parameter(s)?|patch(es)?|pointer(s)?|polymorphism|quer(y|ies)|reference(s)?|ref(s)?|return type|setter(s)?|static|structure(s)?|sub(-| )?class(es)?|super(-| )?class(es)?|(sub)?(-| )?system(s)?|template(s)?|type(s)?|uninline|variable(s)?|handler|plugin|unit(s)?|contravariant|covariant|action(s)?|queue(s)?|stack(s)?|driver(s)?|storage|tool(s)?|module(s)?|log(s)?|setting(s)?|fall( |-)back(s)?|memory|param(s)?|volatile|file(s)?|generic(s)?|initialization(s)?|public|protected|private|framework|singelton|declaration(s)?|init|destructor(s)?|instances(s)?|primitive(s)?|(helper|utility|auxiliary) function(s)?)(\\s|\\.|\\?|\\!|\\[|\\]|\\(|\\)|\\:|^|$|\\,|\'|"|/|#|\\$|\\%|&|\\*|\\+|=|`|;|<|>|@|~|{|}|\\|)))|((^|^[\\s\\S]{0,25}(\\s|\\.|\\?|\\!|\\[|\\]|\\(|\\)|\\:|^|$|\\,|\'|"|/|#|\\$|\\%|&|\\*|\\+|=|`|;|<|>|@|~|{|}|\\|))(clean(ing|s|ed)?(-| )?up(s)?|cleaner|deprecat(e|es|ed|ing)|extract(ed|s|ing)?|re(-|)?organiz(e|es|ed|ing)|re(-|)?structur(e|es|ed|ing)|tid(y|ying|ied) up|improv(e|ed|es|ing|ement|ements)|re(-|)?organiz(e|es|ed|ing)|re(-|)?structur(e|es|ed|ing)|(helper|utility|auxiliary) function(s)?|(move|moved|moves|moving) to|separat(e|es|ed|ing)|split(s|ing)?|->)(\\s|\\.|\\?|\\!|\\[|\\]|\\(|\\)|\\:|^|$|\\,|\'|"|/|#|\\$|\\%|&|\\*|\\+|=|`|;|<|>|@|~|{|}|\\|))))', '@'))-LENGTH(REGEXP_REPLACE(lower(message),'(((\\s|\\.|\\?|\\!|\\[|\\]|\\(|\\)|\\:|^|$|\\,|\'|"|/|#|\\$|\\%|&|\\*|\\+|=|`|;|<|>|@|~|{|}|\\|)(can|could|ha(ve|s|d)|may|might|must|need|ought|shall|should|will|would))[\\s\\S]{0,10}(((\\s|\\.|\\?|\\!|\\[|\\]|\\(|\\)|\\:|^|$|\\,|\'|"|/|#|\\$|\\%|&|\\*|\\+|=|`|;|<|>|@|~|{|}|\\|)(clean(ing)?(-| )?up(s)?|call(s|ed|ing)?[\\s\\S]{1,50}instead|collaps(e|es|ed|ing)|consolidat(e|es|ed|ing)|decompos(e|es|ed|ing)|drop(ed|s|ing)?( back)|encapsulat(e|es|ed|ing)|gereneliz(e|es|ed|ing)|optimiz(e|es|ed|ing|ation|ations)|pull(ed|s|ing)? (up|down)|re(-)?(write|wrote)|re(-| )?factor(ed|s|ing|ings)?|re(-)?implement(ed|s|ing)?|renam(e|es|ed|ing|ings)|better nam(e|es|ing)|re(-)?organiz(e|es|ed|ing)|re(-)?organization|re(-)?work(ed|s|ing|ings)?|reorg|simplif(y|es|ied|ying|ication)|suppress(es|ed|ing)? warning(s)?|unif(y|ies|ied|ing)|uninline|beef(ed|s|ing)? up|refactor(ing)?(s)?|code improvement(s)?|revis(e|es|ed|ing)|re(-)?construct(s|ed|ing)?|re(-)?(write|write|wrote|writing)|re(-)?cod(e|ed|es|ing)|factor(ed|s|ing)? out|re(-| )?packag(e|es|ed|ing))(\\s|\\.|\\?|\\!|\\[|\\]|\\(|\\)|\\:|^|$|\\,|\'|"|/|#|\\$|\\%|&|\\*|\\+|=|`|;|<|>|@|~|{|}|\\|))|((((\\s|\\.|\\?|\\!|\\[|\\]|\\(|\\)|\\:|^|$|\\,|\'|"|/|#|\\$|\\%|&|\\*|\\+|=|`|;|<|>|@|~|{|}|\\|)(clean(ing|s|ed)?clean(ing)?(-| )?up(s)?|combin(e|es|ed|ing)|compos(e|es|ed|ing)|de(-| )?compos(e|es|ed|ing)|convert(ed|s|ing)?|dead|deprecat(e|es|ed|ing)|drop(ed|s|ing)?|duplicat(e|es|ed|ing)|extract(ed|s|ing)?|improv(e|es|ed|ing)|increas(e|es|ed|ing)|(make|makes|made|making)|mov(e|es|ed|ing)|rebuil(d|ds|ding|t)|replac(e|es|ed|ing)|redundant|re(-|)?organiz(e|es|ed|ing)|re(-|)?structur(e|es|ed|ing)|separat(e|e s|ed|ing)|split(s|ing)?|subsitut(e|es|ed|ing)|tid(y|ying|ied)|short(:?en|er|ing|s)?|polish(ed|es|ing)?|(get|got|getting) rid|encapsulate|hide(e|es|ed|ing)|un(-| )?hid(e|es|ed|ing)|parameteriz(e|es|ed|ing)|substitut(e|es|ed|ing)|unnecessary|unneeded|unused|(not|never|no longer) used|no longer needed|redundant|useless|duplicate(d)?|deprecated|obsolete(d)?|commented))((\\s|\\.|\\?|\\!|\\[|\\]|\\(|\\)|\\:|^|$|\\,|\'|"|/|#|\\$|\\%|&|\\*|\\+|=|`|;|<|>|@|~|{|}|\\|)|(\\s|\\.|\\?|\\!|\\[|\\]|\\(|\\)|\\:|^|$|\\,|\'|"|/|#|\\$|\\%|&|\\*|\\+|=|`|;|<|>|@|~|{|}|\\|)[\\s\\S]{0,50}(\\s|\\.|\\?|\\!|\\[|\\]|\\(|\\)|\\:|^|$|\\,|\'|"|/|#|\\$|\\%|&|\\*|\\+|=|`|;|<|>|@|~|{|}|\\|))(algorithm(s)?|assertion(s)?|assignment(s)?|class(es)?|code|collection(s)?|conditional(s)?|constant(s)?|constructor(s)?|control|definition(s)?|delegate|delegation|design pattern(s)?|error(-| )?code(s)?|exception(s)?|field(s)?|flag(s)?|function(s)?|getter(s)?|guard clause(s)?|hierarch(y|ies)|implementation(s)?|inheritance|inline|interface(s)?|internal|macro(s)?|magic number(s)?|member(s)?|method(s)?|modifier(s)?|null object(s)?|object(s)?|parameter(s)?|patch(es)?|pointer(s)?|polymorphism|quer(y|ies)|reference(s)?|ref(s)?|return type|setter(s)?|static|structure(s)?|sub(-| )?class(es)?|super(-| )?class(es)?|(sub)?(-| )?system(s)?|template(s)?|type(s)?|uninline|variable(s)?|handler|plugin|unit(s)?|contravariant|covariant|action(s)?|queue(s)?|stack(s)?|driver(s)?|storage|tool(s)?|module(s)?|log(s)?|setting(s)?|fall( |-)back(s)?|memory|param(s)?|volatile|file(s)?|generic(s)?|initialization(s)?|public|protected|private|framework|singelton|declaration(s)?|init|destructor(s)?|instances(s)?|primitive(s)?|(helper|utility|auxiliary) function(s)?)(\\s|\\.|\\?|\\!|\\[|\\]|\\(|\\)|\\:|^|$|\\,|\'|"|/|#|\\$|\\%|&|\\*|\\+|=|`|;|<|>|@|~|{|}|\\|)))|((^|^[\\s\\S]{0,25}(\\s|\\.|\\?|\\!|\\[|\\]|\\(|\\)|\\:|^|$|\\,|\'|"|/|#|\\$|\\%|&|\\*|\\+|=|`|;|<|>|@|~|{|}|\\|))(clean(ing|s|ed)?(-| )?up(s)?|cleaner|deprecat(e|es|ed|ing)|extract(ed|s|ing)?|re(-|)?organiz(e|es|ed|ing)|re(-|)?structur(e|es|ed|ing)|tid(y|ying|ied) up|improv(e|ed|es|ing|ement|ements)|re(-|)?organiz(e|es|ed|ing)|re(-|)?structur(e|es|ed|ing)|(helper|utility|auxiliary) function(s)?|(move|moved|moves|moving) to|separat(e|es|ed|ing)|split(s|ing)?|->)(\\s|\\.|\\?|\\!|\\[|\\]|\\(|\\)|\\:|^|$|\\,|\'|"|/|#|\\$|\\%|&|\\*|\\+|=|`|;|<|>|@|~|{|}|\\|)))|((\\s|\\.|\\?|\\!|\\[|\\]|\\(|\\)|\\:|^|$|\\,|\'|"|/|#|\\$|\\%|&|\\*|\\+|=|`|;|<|>|@|~|{|}|\\|)(aren\'t|didn\'t|don\'t|doesn\'t|isn\'t|lack|n\'t|never|no|nobody|none|not|nothing|weren\'t|without|won\'t))[\\s\\S]{0,10}(((\\s|\\.|\\?|\\!|\\[|\\]|\\(|\\)|\\:|^|$|\\,|\'|"|/|#|\\$|\\%|&|\\*|\\+|=|`|;|<|>|@|~|{|}|\\|)(clean(ing)?(-| )?up(s)?|call(s|ed|ing)?[\\s\\S]{1,50}instead|collaps(e|es|ed|ing)|consolidat(e|es|ed|ing)|decompos(e|es|ed|ing)|drop(ed|s|ing)?( back)|encapsulat(e|es|ed|ing)|gereneliz(e|es|ed|ing)|optimiz(e|es|ed|ing|ation|ations)|pull(ed|s|ing)? (up|down)|re(-)?(write|wrote)|re(-| )?factor(ed|s|ing|ings)?|re(-)?implement(ed|s|ing)?|renam(e|es|ed|ing|ings)|better nam(e|es|ing)|re(-)?organiz(e|es|ed|ing)|re(-)?organization|re(-)?work(ed|s|ing|ings)?|reorg|simplif(y|es|ied|ying|ication)|suppress(es|ed|ing)? warning(s)?|unif(y|ies|ied|ing)|uninline|beef(ed|s|ing)? up|refactor(ing)?(s)?|code improvement(s)?|revis(e|es|ed|ing)|re(-)?construct(s|ed|ing)?|re(-)?(write|write|wrote|writing)|re(-)?cod(e|ed|es|ing)|factor(ed|s|ing)? out|re(-| )?packag(e|es|ed|ing))(\\s|\\.|\\?|\\!|\\[|\\]|\\(|\\)|\\:|^|$|\\,|\'|"|/|#|\\$|\\%|&|\\*|\\+|=|`|;|<|>|@|~|{|}|\\|))|((((\\s|\\.|\\?|\\!|\\[|\\]|\\(|\\)|\\:|^|$|\\,|\'|"|/|#|\\$|\\%|&|\\*|\\+|=|`|;|<|>|@|~|{|}|\\|)(clean(ing|s|ed)?clean(ing)?(-| )?up(s)?|combin(e|es|ed|ing)|compos(e|es|ed|ing)|de(-| )?compos(e|es|ed|ing)|convert(ed|s|ing)?|dead|deprecat(e|es|ed|ing)|drop(ed|s|ing)?|duplicat(e|es|ed|ing)|extract(ed|s|ing)?|improv(e|es|ed|ing)|increas(e|es|ed|ing)|(make|makes|made|making)|mov(e|es|ed|ing)|rebuil(d|ds|ding|t)|replac(e|es|ed|ing)|redundant|re(-|)?organiz(e|es|ed|ing)|re(-|)?structur(e|es|ed|ing)|separat(e|e s|ed|ing)|split(s|ing)?|subsitut(e|es|ed|ing)|tid(y|ying|ied)|short(:?en|er|ing|s)?|polish(ed|es|ing)?|(get|got|getting) rid|encapsulate|hide(e|es|ed|ing)|un(-| )?hid(e|es|ed|ing)|parameteriz(e|es|ed|ing)|substitut(e|es|ed|ing)|unnecessary|unneeded|unused|(not|never|no longer) used|no longer needed|redundant|useless|duplicate(d)?|deprecated|obsolete(d)?|commented))((\\s|\\.|\\?|\\!|\\[|\\]|\\(|\\)|\\:|^|$|\\,|\'|"|/|#|\\$|\\%|&|\\*|\\+|=|`|;|<|>|@|~|{|}|\\|)|(\\s|\\.|\\?|\\!|\\[|\\]|\\(|\\)|\\:|^|$|\\,|\'|"|/|#|\\$|\\%|&|\\*|\\+|=|`|;|<|>|@|~|{|}|\\|)[\\s\\S]{0,50}(\\s|\\.|\\?|\\!|\\[|\\]|\\(|\\)|\\:|^|$|\\,|\'|"|/|#|\\$|\\%|&|\\*|\\+|=|`|;|<|>|@|~|{|}|\\|))(algorithm(s)?|assertion(s)?|assignment(s)?|class(es)?|code|collection(s)?|conditional(s)?|constant(s)?|constructor(s)?|control|definition(s)?|delegate|delegation|design pattern(s)?|error(-| )?code(s)?|exception(s)?|field(s)?|flag(s)?|function(s)?|getter(s)?|guard clause(s)?|hierarch(y|ies)|implementation(s)?|inheritance|inline|interface(s)?|internal|macro(s)?|magic number(s)?|member(s)?|method(s)?|modifier(s)?|null object(s)?|object(s)?|parameter(s)?|patch(es)?|pointer(s)?|polymorphism|quer(y|ies)|reference(s)?|ref(s)?|return type|setter(s)?|static|structure(s)?|sub(-| )?class(es)?|super(-| )?class(es)?|(sub)?(-| )?system(s)?|template(s)?|type(s)?|uninline|variable(s)?|handler|plugin|unit(s)?|contravariant|covariant|action(s)?|queue(s)?|stack(s)?|driver(s)?|storage|tool(s)?|module(s)?|log(s)?|setting(s)?|fall( |-)back(s)?|memory|param(s)?|volatile|file(s)?|generic(s)?|initialization(s)?|public|protected|private|framework|singelton|declaration(s)?|init|destructor(s)?|instances(s)?|primitive(s)?|(helper|utility|auxiliary) function(s)?)(\\s|\\.|\\?|\\!|\\[|\\]|\\(|\\)|\\:|^|$|\\,|\'|"|/|#|\\$|\\%|&|\\*|\\+|=|`|;|<|>|@|~|{|}|\\|)))|((^|^[\\s\\S]{0,25}(\\s|\\.|\\?|\\!|\\[|\\]|\\(|\\)|\\:|^|$|\\,|\'|"|/|#|\\$|\\%|&|\\*|\\+|=|`|;|<|>|@|~|{|}|\\|))(clean(ing|s|ed)?(-| )?up(s)?|cleaner|deprecat(e|es|ed|ing)|extract(ed|s|ing)?|re(-|)?organiz(e|es|ed|ing)|re(-|)?structur(e|es|ed|ing)|tid(y|ying|ied) up|improv(e|ed|es|ing|ement|ements)|re(-|)?organiz(e|es|ed|ing)|re(-|)?structur(e|es|ed|ing)|(helper|utility|auxiliary) function(s)?|(move|moved|moves|moving) to|separat(e|es|ed|ing)|split(s|ing)?|->)(\\s|\\.|\\?|\\!|\\[|\\]|\\(|\\)|\\:|^|$|\\,|\'|"|/|#|\\$|\\%|&|\\*|\\+|=|`|;|<|>|@|~|{|}|\\|)))|((\\s|\\.|\\?|\\!|\\[|\\]|\\(|\\)|\\:|^|$|\\,|\'|"|/|#|\\$|\\%|&|\\*|\\+|=|`|;|<|>|@|~|{|}|\\|)(for(get|gets|got|geting)|allow(s|ed|ing)?))[\\s\\S]{0,10}(((\\s|\\.|\\?|\\!|\\[|\\]|\\(|\\)|\\:|^|$|\\,|\'|"|/|#|\\$|\\%|&|\\*|\\+|=|`|;|<|>|@|~|{|}|\\|)(clean(ing)?(-| )?up(s)?|call(s|ed|ing)?[\\s\\S]{1,50}instead|collaps(e|es|ed|ing)|consolidat(e|es|ed|ing)|decompos(e|es|ed|ing)|drop(ed|s|ing)?( back)|encapsulat(e|es|ed|ing)|gereneliz(e|es|ed|ing)|optimiz(e|es|ed|ing|ation|ations)|pull(ed|s|ing)? (up|down)|re(-)?(write|wrote)|re(-| )?factor(ed|s|ing|ings)?|re(-)?implement(ed|s|ing)?|renam(e|es|ed|ing|ings)|better nam(e|es|ing)|re(-)?organiz(e|es|ed|ing)|re(-)?organization|re(-)?work(ed|s|ing|ings)?|reorg|simplif(y|es|ied|ying|ication)|suppress(es|ed|ing)? warning(s)?|unif(y|ies|ied|ing)|uninline|beef(ed|s|ing)? up|refactor(ing)?(s)?|code improvement(s)?|revis(e|es|ed|ing)|re(-)?construct(s|ed|ing)?|re(-)?(write|write|wrote|writing)|re(-)?cod(e|ed|es|ing)|factor(ed|s|ing)? out|re(-| )?packag(e|es|ed|ing))(\\s|\\.|\\?|\\!|\\[|\\]|\\(|\\)|\\:|^|$|\\,|\'|"|/|#|\\$|\\%|&|\\*|\\+|=|`|;|<|>|@|~|{|}|\\|))|((((\\s|\\.|\\?|\\!|\\[|\\]|\\(|\\)|\\:|^|$|\\,|\'|"|/|#|\\$|\\%|&|\\*|\\+|=|`|;|<|>|@|~|{|}|\\|)(clean(ing|s|ed)?clean(ing)?(-| )?up(s)?|combin(e|es|ed|ing)|compos(e|es|ed|ing)|de(-| )?compos(e|es|ed|ing)|convert(ed|s|ing)?|dead|deprecat(e|es|ed|ing)|drop(ed|s|ing)?|duplicat(e|es|ed|ing)|extract(ed|s|ing)?|improv(e|es|ed|ing)|increas(e|es|ed|ing)|(make|makes|made|making)|mov(e|es|ed|ing)|rebuil(d|ds|ding|t)|replac(e|es|ed|ing)|redundant|re(-|)?organiz(e|es|ed|ing)|re(-|)?structur(e|es|ed|ing)|separat(e|e s|ed|ing)|split(s|ing)?|subsitut(e|es|ed|ing)|tid(y|ying|ied)|short(:?en|er|ing|s)?|polish(ed|es|ing)?|(get|got|getting) rid|encapsulate|hide(e|es|ed|ing)|un(-| )?hid(e|es|ed|ing)|parameteriz(e|es|ed|ing)|substitut(e|es|ed|ing)|unnecessary|unneeded|unused|(not|never|no longer) used|no longer needed|redundant|useless|duplicate(d)?|deprecated|obsolete(d)?|commented))((\\s|\\.|\\?|\\!|\\[|\\]|\\(|\\)|\\:|^|$|\\,|\'|"|/|#|\\$|\\%|&|\\*|\\+|=|`|;|<|>|@|~|{|}|\\|)|(\\s|\\.|\\?|\\!|\\[|\\]|\\(|\\)|\\:|^|$|\\,|\'|"|/|#|\\$|\\%|&|\\*|\\+|=|`|;|<|>|@|~|{|}|\\|)[\\s\\S]{0,50}(\\s|\\.|\\?|\\!|\\[|\\]|\\(|\\)|\\:|^|$|\\,|\'|"|/|#|\\$|\\%|&|\\*|\\+|=|`|;|<|>|@|~|{|}|\\|))(algorithm(s)?|assertion(s)?|assignment(s)?|class(es)?|code|collection(s)?|conditional(s)?|constant(s)?|constructor(s)?|control|definition(s)?|delegate|delegation|design pattern(s)?|error(-| )?code(s)?|exception(s)?|field(s)?|flag(s)?|function(s)?|getter(s)?|guard clause(s)?|hierarch(y|ies)|implementation(s)?|inheritance|inline|interface(s)?|internal|macro(s)?|magic number(s)?|member(s)?|method(s)?|modifier(s)?|null object(s)?|object(s)?|parameter(s)?|patch(es)?|pointer(s)?|polymorphism|quer(y|ies)|reference(s)?|ref(s)?|return type|setter(s)?|static|structure(s)?|sub(-| )?class(es)?|super(-| )?class(es)?|(sub)?(-| )?system(s)?|template(s)?|type(s)?|uninline|variable(s)?|handler|plugin|unit(s)?|contravariant|covariant|action(s)?|queue(s)?|stack(s)?|driver(s)?|storage|tool(s)?|module(s)?|log(s)?|setting(s)?|fall( |-)back(s)?|memory|param(s)?|volatile|file(s)?|generic(s)?|initialization(s)?|public|protected|private|framework|singelton|declaration(s)?|init|destructor(s)?|instances(s)?|primitive(s)?|(helper|utility|auxiliary) function(s)?)(\\s|\\.|\\?|\\!|\\[|\\]|\\(|\\)|\\:|^|$|\\,|\'|"|/|#|\\$|\\%|&|\\*|\\+|=|`|;|<|>|@|~|{|}|\\|)))|((^|^[\\s\\S]{0,25}(\\s|\\.|\\?|\\!|\\[|\\]|\\(|\\)|\\:|^|$|\\,|\'|"|/|#|\\$|\\%|&|\\*|\\+|=|`|;|<|>|@|~|{|}|\\|))(clean(ing|s|ed)?(-| )?up(s)?|cleaner|deprecat(e|es|ed|ing)|extract(ed|s|ing)?|re(-|)?organiz(e|es|ed|ing)|re(-|)?structur(e|es|ed|ing)|tid(y|ying|ied) up|improv(e|ed|es|ing|ement|ements)|re(-|)?organiz(e|es|ed|ing)|re(-|)?structur(e|es|ed|ing)|(helper|utility|auxiliary) function(s)?|(move|moved|moves|moving) to|separat(e|es|ed|ing)|split(s|ing)?|->)(\\s|\\.|\\?|\\!|\\[|\\]|\\(|\\)|\\:|^|$|\\,|\'|"|/|#|\\$|\\%|&|\\*|\\+|=|`|;|<|>|@|~|{|}|\\|))))', '')))
 )

