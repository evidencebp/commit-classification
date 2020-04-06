# Run in Starndad sql
CREATE OR REPLACE FUNCTION
ccp.bq_non_positive_linguistic_refactor_goals
 (message string)
 RETURNS int64
AS (
# Model language based on commit: 5cd4738202154452854991b2714ce49459316371
# Refactor :build_non_positive_linguistic(build_refactor_goals_regex())
(LENGTH(REGEXP_REPLACE(lower(message),'(((\\s|\\.|\\?|\\!|\\[|\\]|\\(|\\)|\\:|^|$|\\,|\'|"|/|#|\\$|\\%|&|\\*|\\+|=|`|;|<|>|@|~|{|}|\\|)(can|could|ha(ve|s|d)|may|might|must|need|ought|shall|should|will|would))[\\s\\S]{0,10}((((\\s|\\.|\\?|\\!|\\[|\\]|\\(|\\)|\\:|^|$|\\,|\'|"|/|#|\\$|\\%|&|\\*|\\+|=|`|;|<|>|@|~|{|}|\\|)(better|improv(e|es|ed|ing)|increas(e|es|ed|ing)|reduc(e|es|ed|ing)|worse|make|more|less))((\\s|\\.|\\?|\\!|\\[|\\]|\\(|\\)|\\:|^|$|\\,|\'|"|/|#|\\$|\\%|&|\\*|\\+|=|`|;|<|>|@|~|{|}|\\|)|(\\s|\\.|\\?|\\!|\\[|\\]|\\(|\\)|\\:|^|$|\\,|\'|"|/|#|\\$|\\%|&|\\*|\\+|=|`|;|<|>|@|~|{|}|\\|)[\\s\\S]{0,50}(\\s|\\.|\\?|\\!|\\[|\\]|\\(|\\)|\\:|^|$|\\,|\'|"|/|#|\\$|\\%|&|\\*|\\+|=|`|;|<|>|@|~|{|}|\\|))(abstraction|coherence|cohesion|complexity|correctness|coupling|dependability|duplication|efficiency|extensibility|flexibility|maintainability|naming|performance|portability|quality|readability|reliability|re(-| )?use|re(-| )?usability|security|simplicity|testability|testable|re(-| )?usable|readable|portable|maintainable|flexible|efficient|encapsulation)(\\s|\\.|\\?|\\!|\\[|\\]|\\(|\\)|\\:|^|$|\\,|\'|"|/|#|\\$|\\%|&|\\*|\\+|=|`|;|<|>|@|~|{|}|\\|)))|((\\s|\\.|\\?|\\!|\\[|\\]|\\(|\\)|\\:|^|$|\\,|\'|"|/|#|\\$|\\%|&|\\*|\\+|=|`|;|<|>|@|~|{|}|\\|)(aren\'t|didn\'t|don\'t|doesn\'t|isn\'t|lack|n\'t|never|no|nobody|none|not|nothing|weren\'t|without|won\'t))[\\s\\S]{0,10}((((\\s|\\.|\\?|\\!|\\[|\\]|\\(|\\)|\\:|^|$|\\,|\'|"|/|#|\\$|\\%|&|\\*|\\+|=|`|;|<|>|@|~|{|}|\\|)(better|improv(e|es|ed|ing)|increas(e|es|ed|ing)|reduc(e|es|ed|ing)|worse|make|more|less))((\\s|\\.|\\?|\\!|\\[|\\]|\\(|\\)|\\:|^|$|\\,|\'|"|/|#|\\$|\\%|&|\\*|\\+|=|`|;|<|>|@|~|{|}|\\|)|(\\s|\\.|\\?|\\!|\\[|\\]|\\(|\\)|\\:|^|$|\\,|\'|"|/|#|\\$|\\%|&|\\*|\\+|=|`|;|<|>|@|~|{|}|\\|)[\\s\\S]{0,50}(\\s|\\.|\\?|\\!|\\[|\\]|\\(|\\)|\\:|^|$|\\,|\'|"|/|#|\\$|\\%|&|\\*|\\+|=|`|;|<|>|@|~|{|}|\\|))(abstraction|coherence|cohesion|complexity|correctness|coupling|dependability|duplication|efficiency|extensibility|flexibility|maintainability|naming|performance|portability|quality|readability|reliability|re(-| )?use|re(-| )?usability|security|simplicity|testability|testable|re(-| )?usable|readable|portable|maintainable|flexible|efficient|encapsulation)(\\s|\\.|\\?|\\!|\\[|\\]|\\(|\\)|\\:|^|$|\\,|\'|"|/|#|\\$|\\%|&|\\*|\\+|=|`|;|<|>|@|~|{|}|\\|)))|((\\s|\\.|\\?|\\!|\\[|\\]|\\(|\\)|\\:|^|$|\\,|\'|"|/|#|\\$|\\%|&|\\*|\\+|=|`|;|<|>|@|~|{|}|\\|)(for(get|gets|got|geting)|allow(s|ed|ing)?))[\\s\\S]{0,10}((((\\s|\\.|\\?|\\!|\\[|\\]|\\(|\\)|\\:|^|$|\\,|\'|"|/|#|\\$|\\%|&|\\*|\\+|=|`|;|<|>|@|~|{|}|\\|)(better|improv(e|es|ed|ing)|increas(e|es|ed|ing)|reduc(e|es|ed|ing)|worse|make|more|less))((\\s|\\.|\\?|\\!|\\[|\\]|\\(|\\)|\\:|^|$|\\,|\'|"|/|#|\\$|\\%|&|\\*|\\+|=|`|;|<|>|@|~|{|}|\\|)|(\\s|\\.|\\?|\\!|\\[|\\]|\\(|\\)|\\:|^|$|\\,|\'|"|/|#|\\$|\\%|&|\\*|\\+|=|`|;|<|>|@|~|{|}|\\|)[\\s\\S]{0,50}(\\s|\\.|\\?|\\!|\\[|\\]|\\(|\\)|\\:|^|$|\\,|\'|"|/|#|\\$|\\%|&|\\*|\\+|=|`|;|<|>|@|~|{|}|\\|))(abstraction|coherence|cohesion|complexity|correctness|coupling|dependability|duplication|efficiency|extensibility|flexibility|maintainability|naming|performance|portability|quality|readability|reliability|re(-| )?use|re(-| )?usability|security|simplicity|testability|testable|re(-| )?usable|readable|portable|maintainable|flexible|efficient|encapsulation)(\\s|\\.|\\?|\\!|\\[|\\]|\\(|\\)|\\:|^|$|\\,|\'|"|/|#|\\$|\\%|&|\\*|\\+|=|`|;|<|>|@|~|{|}|\\|)))|((\\s|\\.|\\?|\\!|\\[|\\]|\\(|\\)|\\:|^|$|\\,|\'|"|/|#|\\$|\\%|&|\\*|\\+|=|`|;|<|>|@|~|{|}|\\|)(change( |-)?log|comment(s)?|copy( |-)?right(s)?|doc(s)?|documentation|explanation(s)?|man( |-)?page(s)?|manual|note(s)?|readme(.md)?|translation(s)?|java( |-)?doc(s)?|java( |-)?documentation|example(s)?|diagram(s)?|guide(s)?|icon(s)?|doc( |-)?string(s)?|tutorials(s)?|help|man|doc( |-)?string(s)?|desc(ription)?(s)?|copy( |-)?right(s)?|explanation(s)?|release notes))[\\s\\S]{0,10}((((\\s|\\.|\\?|\\!|\\[|\\]|\\(|\\)|\\:|^|$|\\,|\'|"|/|#|\\$|\\%|&|\\*|\\+|=|`|;|<|>|@|~|{|}|\\|)(better|improv(e|es|ed|ing)|increas(e|es|ed|ing)|reduc(e|es|ed|ing)|worse|make|more|less))((\\s|\\.|\\?|\\!|\\[|\\]|\\(|\\)|\\:|^|$|\\,|\'|"|/|#|\\$|\\%|&|\\*|\\+|=|`|;|<|>|@|~|{|}|\\|)|(\\s|\\.|\\?|\\!|\\[|\\]|\\(|\\)|\\:|^|$|\\,|\'|"|/|#|\\$|\\%|&|\\*|\\+|=|`|;|<|>|@|~|{|}|\\|)[\\s\\S]{0,50}(\\s|\\.|\\?|\\!|\\[|\\]|\\(|\\)|\\:|^|$|\\,|\'|"|/|#|\\$|\\%|&|\\*|\\+|=|`|;|<|>|@|~|{|}|\\|))(abstraction|coherence|cohesion|complexity|correctness|coupling|dependability|duplication|efficiency|extensibility|flexibility|maintainability|naming|performance|portability|quality|readability|reliability|re(-| )?use|re(-| )?usability|security|simplicity|testability|testable|re(-| )?usable|readable|portable|maintainable|flexible|efficient|encapsulation)(\\s|\\.|\\?|\\!|\\[|\\]|\\(|\\)|\\:|^|$|\\,|\'|"|/|#|\\$|\\%|&|\\*|\\+|=|`|;|<|>|@|~|{|}|\\|))))', '@'))-LENGTH(REGEXP_REPLACE(lower(message),'(((\\s|\\.|\\?|\\!|\\[|\\]|\\(|\\)|\\:|^|$|\\,|\'|"|/|#|\\$|\\%|&|\\*|\\+|=|`|;|<|>|@|~|{|}|\\|)(can|could|ha(ve|s|d)|may|might|must|need|ought|shall|should|will|would))[\\s\\S]{0,10}((((\\s|\\.|\\?|\\!|\\[|\\]|\\(|\\)|\\:|^|$|\\,|\'|"|/|#|\\$|\\%|&|\\*|\\+|=|`|;|<|>|@|~|{|}|\\|)(better|improv(e|es|ed|ing)|increas(e|es|ed|ing)|reduc(e|es|ed|ing)|worse|make|more|less))((\\s|\\.|\\?|\\!|\\[|\\]|\\(|\\)|\\:|^|$|\\,|\'|"|/|#|\\$|\\%|&|\\*|\\+|=|`|;|<|>|@|~|{|}|\\|)|(\\s|\\.|\\?|\\!|\\[|\\]|\\(|\\)|\\:|^|$|\\,|\'|"|/|#|\\$|\\%|&|\\*|\\+|=|`|;|<|>|@|~|{|}|\\|)[\\s\\S]{0,50}(\\s|\\.|\\?|\\!|\\[|\\]|\\(|\\)|\\:|^|$|\\,|\'|"|/|#|\\$|\\%|&|\\*|\\+|=|`|;|<|>|@|~|{|}|\\|))(abstraction|coherence|cohesion|complexity|correctness|coupling|dependability|duplication|efficiency|extensibility|flexibility|maintainability|naming|performance|portability|quality|readability|reliability|re(-| )?use|re(-| )?usability|security|simplicity|testability|testable|re(-| )?usable|readable|portable|maintainable|flexible|efficient|encapsulation)(\\s|\\.|\\?|\\!|\\[|\\]|\\(|\\)|\\:|^|$|\\,|\'|"|/|#|\\$|\\%|&|\\*|\\+|=|`|;|<|>|@|~|{|}|\\|)))|((\\s|\\.|\\?|\\!|\\[|\\]|\\(|\\)|\\:|^|$|\\,|\'|"|/|#|\\$|\\%|&|\\*|\\+|=|`|;|<|>|@|~|{|}|\\|)(aren\'t|didn\'t|don\'t|doesn\'t|isn\'t|lack|n\'t|never|no|nobody|none|not|nothing|weren\'t|without|won\'t))[\\s\\S]{0,10}((((\\s|\\.|\\?|\\!|\\[|\\]|\\(|\\)|\\:|^|$|\\,|\'|"|/|#|\\$|\\%|&|\\*|\\+|=|`|;|<|>|@|~|{|}|\\|)(better|improv(e|es|ed|ing)|increas(e|es|ed|ing)|reduc(e|es|ed|ing)|worse|make|more|less))((\\s|\\.|\\?|\\!|\\[|\\]|\\(|\\)|\\:|^|$|\\,|\'|"|/|#|\\$|\\%|&|\\*|\\+|=|`|;|<|>|@|~|{|}|\\|)|(\\s|\\.|\\?|\\!|\\[|\\]|\\(|\\)|\\:|^|$|\\,|\'|"|/|#|\\$|\\%|&|\\*|\\+|=|`|;|<|>|@|~|{|}|\\|)[\\s\\S]{0,50}(\\s|\\.|\\?|\\!|\\[|\\]|\\(|\\)|\\:|^|$|\\,|\'|"|/|#|\\$|\\%|&|\\*|\\+|=|`|;|<|>|@|~|{|}|\\|))(abstraction|coherence|cohesion|complexity|correctness|coupling|dependability|duplication|efficiency|extensibility|flexibility|maintainability|naming|performance|portability|quality|readability|reliability|re(-| )?use|re(-| )?usability|security|simplicity|testability|testable|re(-| )?usable|readable|portable|maintainable|flexible|efficient|encapsulation)(\\s|\\.|\\?|\\!|\\[|\\]|\\(|\\)|\\:|^|$|\\,|\'|"|/|#|\\$|\\%|&|\\*|\\+|=|`|;|<|>|@|~|{|}|\\|)))|((\\s|\\.|\\?|\\!|\\[|\\]|\\(|\\)|\\:|^|$|\\,|\'|"|/|#|\\$|\\%|&|\\*|\\+|=|`|;|<|>|@|~|{|}|\\|)(for(get|gets|got|geting)|allow(s|ed|ing)?))[\\s\\S]{0,10}((((\\s|\\.|\\?|\\!|\\[|\\]|\\(|\\)|\\:|^|$|\\,|\'|"|/|#|\\$|\\%|&|\\*|\\+|=|`|;|<|>|@|~|{|}|\\|)(better|improv(e|es|ed|ing)|increas(e|es|ed|ing)|reduc(e|es|ed|ing)|worse|make|more|less))((\\s|\\.|\\?|\\!|\\[|\\]|\\(|\\)|\\:|^|$|\\,|\'|"|/|#|\\$|\\%|&|\\*|\\+|=|`|;|<|>|@|~|{|}|\\|)|(\\s|\\.|\\?|\\!|\\[|\\]|\\(|\\)|\\:|^|$|\\,|\'|"|/|#|\\$|\\%|&|\\*|\\+|=|`|;|<|>|@|~|{|}|\\|)[\\s\\S]{0,50}(\\s|\\.|\\?|\\!|\\[|\\]|\\(|\\)|\\:|^|$|\\,|\'|"|/|#|\\$|\\%|&|\\*|\\+|=|`|;|<|>|@|~|{|}|\\|))(abstraction|coherence|cohesion|complexity|correctness|coupling|dependability|duplication|efficiency|extensibility|flexibility|maintainability|naming|performance|portability|quality|readability|reliability|re(-| )?use|re(-| )?usability|security|simplicity|testability|testable|re(-| )?usable|readable|portable|maintainable|flexible|efficient|encapsulation)(\\s|\\.|\\?|\\!|\\[|\\]|\\(|\\)|\\:|^|$|\\,|\'|"|/|#|\\$|\\%|&|\\*|\\+|=|`|;|<|>|@|~|{|}|\\|)))|((\\s|\\.|\\?|\\!|\\[|\\]|\\(|\\)|\\:|^|$|\\,|\'|"|/|#|\\$|\\%|&|\\*|\\+|=|`|;|<|>|@|~|{|}|\\|)(change( |-)?log|comment(s)?|copy( |-)?right(s)?|doc(s)?|documentation|explanation(s)?|man( |-)?page(s)?|manual|note(s)?|readme(.md)?|translation(s)?|java( |-)?doc(s)?|java( |-)?documentation|example(s)?|diagram(s)?|guide(s)?|icon(s)?|doc( |-)?string(s)?|tutorials(s)?|help|man|doc( |-)?string(s)?|desc(ription)?(s)?|copy( |-)?right(s)?|explanation(s)?|release notes))[\\s\\S]{0,10}((((\\s|\\.|\\?|\\!|\\[|\\]|\\(|\\)|\\:|^|$|\\,|\'|"|/|#|\\$|\\%|&|\\*|\\+|=|`|;|<|>|@|~|{|}|\\|)(better|improv(e|es|ed|ing)|increas(e|es|ed|ing)|reduc(e|es|ed|ing)|worse|make|more|less))((\\s|\\.|\\?|\\!|\\[|\\]|\\(|\\)|\\:|^|$|\\,|\'|"|/|#|\\$|\\%|&|\\*|\\+|=|`|;|<|>|@|~|{|}|\\|)|(\\s|\\.|\\?|\\!|\\[|\\]|\\(|\\)|\\:|^|$|\\,|\'|"|/|#|\\$|\\%|&|\\*|\\+|=|`|;|<|>|@|~|{|}|\\|)[\\s\\S]{0,50}(\\s|\\.|\\?|\\!|\\[|\\]|\\(|\\)|\\:|^|$|\\,|\'|"|/|#|\\$|\\%|&|\\*|\\+|=|`|;|<|>|@|~|{|}|\\|))(abstraction|coherence|cohesion|complexity|correctness|coupling|dependability|duplication|efficiency|extensibility|flexibility|maintainability|naming|performance|portability|quality|readability|reliability|re(-| )?use|re(-| )?usability|security|simplicity|testability|testable|re(-| )?usable|readable|portable|maintainable|flexible|efficient|encapsulation)(\\s|\\.|\\?|\\!|\\[|\\]|\\(|\\)|\\:|^|$|\\,|\'|"|/|#|\\$|\\%|&|\\*|\\+|=|`|;|<|>|@|~|{|}|\\|))))', '')))
 )
