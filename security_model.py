"""
Sources:
https://arxiv.org/pdf/2001.09148.pdf

"""


import re
from os.path import join
import pandas as pd


from configuration import DATA_PATH
from language_utils import  regex_to_big_query, generate_bq_function, match, SCHEMA_NAME, print_logic_to_bq\
    , build_sepereted_term, build_non_positive_linguistic, REGULAR_SUFFIX
from model_evaluation import classifiy_commits_df, evaluate_performance, evaluate_concept_classifier

# Not sure list
"""
"""

positive_terms = [
 'advisory',
 'anti(?: |-)virus(?:es)?',
 'attack(?:s)?',
 'auth',
 'authenticat(e|ion)',
 #'brute force', # consider
 'bug bount(y|ies)',
 #'bypass(?:es|ed|ing)?', # mostly tests related
 'certificate(?:s)?',
 #'constant time', # too general
 'crack(?:s)?',
 'credential(s)?',
 'cross(?: |-)origin',
 'cross(?: |-)site',
 '(?:cryptographic|cryptography)',
 'cve(-d+)?(-d+)?',
 'clickjack',
 'cyber',
 'decript' + REGULAR_SUFFIX,
 'decription',
 'denial of service',
 '(de)?serializ', # consider
 'directory traversal',
 'dos', # consider
 'encript' + REGULAR_SUFFIX,
 'encription',
 'exploit(?:s)?',
 'fire(?: |-)wall(?:s)?',
 #'expos(e|ing)',
 # 'hack', # A bit general, consider
 'hijack',
 'harden(?:s|ed|ing)?',
 #'infinite loop', # consider
 'injection',
 '(in)?secur(e|ity)',
 'lockout',
 'malicious',
 'malware(?:s)?', #plural of malware is malware yet not all are aware
 'nvd' # NVD
 'open redirect',
 'osvdb', # OSVDB
 #'overflow', # usually general
 'password(?:s)?',
 'permission(?:s)?',
 'poison(?:s|es|ed|ing)?',
 'port scan(?:s|ed|ing)?',
 'privilege(?:s)?',
 # 'proof of concept', # consider
 'rce', # remote code execution
 'redos' # ReDoS
 'remote code execution',
 'return oriented programming',
 #'(?:safe|safety|unsafe|safer)',
 #'(?:safety|unsafe|safer)', # safe alone seems too general
 'secret(?:s)?',
 'security',
 'session fixation',
 'spoof(?:s|es|ed|ing)?',
 'threat(?:s|ed|ing)?',
 #'tls', # transport layer security, sometime too general
 #'timing', # consider
 #'token(?:s)?',
 #'traversal',
 'unauthori[z|s]ed',
 'vulnerabilit(?:y|ies)',
 'x(?: |-)frame(?: |-)option(?:s)?',
 'xss',
 'xsrf', # XSRF
 'xxe' # XXE
    ]


excluded_terms = ['https://secure', # A too common link in commits
                  'error(?:s)? injection', # in tests
                  ]

def build_positive_regex():

    return build_sepereted_term(positive_terms)



def build_excluded_regex():

    return build_sepereted_term(excluded_terms)

def build_not_positive_regex():

    return build_non_positive_linguistic(build_positive_regex())


def is_security(commit_text):

    return (len(re.findall(build_positive_regex(), commit_text))
            - len(re.findall(build_excluded_regex(), commit_text))
            - len(re.findall(build_not_positive_regex(), commit_text)))  > 0



def security_to_bq():
    concept = 'security'
    print("# " + concept)
    print( "# " + concept +  ": Core")
    #print( ",")
    print("{schema}.bq_core_{concept}(message)".format(schema=SCHEMA_NAME
                                                       , concept=concept))
    print(" - ")
    print("# " + concept +  ": Excluded")
    print("{schema}.bq_excluded_{concept}(message)".format(schema=SCHEMA_NAME
                                                           , concept=concept))

    print(" - ")
    print("# " + concept +  ": not positive")
    print("{schema}.bq_not_positive_{concept}(message)".format(schema=SCHEMA_NAME
                                                               , concept=concept))
    print("# end - " + concept)

def print_concepts_functions_for_bq(commit: str = 'XXX'):

    concept = 'security'

    concepts = {'core_' + concept : build_positive_regex
        , 'excluded_' + concept : build_excluded_regex
        , 'not_positive_' + concept : build_not_positive_regex
        #, 'swearing': swearing_to_bq

                }

    for i in concepts.keys():
        print()
        print_func = lambda : print_logic_to_bq(regex_func=concepts[i]
                                                , concept=i)
        generate_bq_function('{schema}.bq_{concept}'.format(schema=SCHEMA_NAME
                                                            , concept=i)
                             , print_func
                             , commit=commit)
        print()

    generate_bq_function('{schema}.bq_{concept}'.format(schema=SCHEMA_NAME
                                                        , concept=concept)
                         , security_to_bq
                         , commit=commit)
    print()
def evaluate_security_classifier():

    evaluate_concept_classifier(concept='Swearing'
                                , text_name='message'
                                , classification_function=is_security
                                , samples_file=join(DATA_PATH, 'commit_security_samples.csv'))


if __name__ == '__main__':
    print_concepts_functions_for_bq(commit='df6d53facd9475ed54ecbb3f1d2cb8076b227f77')
    #evaluate_security_classifier()

    text = """""Regenerate AnalyticsData client (#6761)

This PR was generated using Autosynth. :rainbow:


<details><summary>Log from Synthtool</summary>

```
2020-11-18 05:10:43,230 synthtool [DEBUG] > Executing /home/kbuilder/.cache/synthtool/elixir-google-api/synth.py.
On branch autosynth-analyticsdata
nothing to commit, working tree clean
2020-11-18 05:10:44,906 synthtool [DEBUG] > Running: docker run --rm -v/tmpfs/tmp/tmpjjiec57b/repo:/workspace -v/var/run/docker.sock:/var/run/docker.sock -e USER_GROUP=1000:1000 -w /workspace gcr.io/cloud-devrel-public-resources/elixir19 scripts/generate_client.sh AnalyticsData
DEBUG:synthtool:Running: docker run --rm -v/tmpfs/tmp/tmpjjiec57b/repo:/workspace -v/var/run/docker.sock:/var/run/docker.sock -e USER_GROUP=1000:1000 -w /workspace gcr.io/cloud-devrel-public-resources/elixir19 scripts/generate_client.sh AnalyticsData
/workspace /workspace
[33mThe mix.lock file was generated with a newer version of Hex. Update your client by running `mix local.hex` to avoid losing data.[0m
Resolving Hex dependencies...
Dependency resolution completed:
Unchanged:
  certifi 2.5.1
  google_api_discovery 0.7.0
  google_gax 0.3.2
  hackney 1.15.2
  idna 6.0.0
  jason 1.2.1
  metrics 1.0.1
  mime 1.3.1
  mimerl 1.2.0
  oauth2 0.9.4
  parse_trans 3.3.0
  poison 3.1.0
  ssl_verify_fun 1.1.5
  temp 0.4.7
  tesla 1.3.3
  unicode_util_compat 0.4.1
* Getting google_api_discovery (Hex package)
* Getting tesla (Hex package)
* Getting oauth2 (Hex package)
* Getting temp (Hex package)
* Getting jason (Hex package)
* Getting poison (Hex package)
* Getting hackney (Hex package)
* Getting certifi (Hex package)
* Getting idna (Hex package)
* Getting metrics (Hex package)
* Getting mimerl (Hex package)
* Getting ssl_verify_fun (Hex package)
* Getting unicode_util_compat (Hex package)
* Getting parse_trans (Hex package)
* Getting mime (Hex package)
* Getting google_gax (Hex package)
[33mThe mix.lock file was generated with a newer version of Hex. Update your client by running `mix local.hex` to avoid losing data.[0m
==> temp
Compiling 3 files (.ex)
Generated temp app
===> Compiling parse_trans
===> Compiling mimerl
===> Compiling metrics
===> Compiling unicode_util_compat
===> Compiling idna
==> jason
Compiling 8 files (.ex)
Generated jason app
warning: String.strip/1 is deprecated. Use String.trim/1 instead
  /workspace/deps/poison/mix.exs:4

==> poison
Compiling 4 files (.ex)
warning: Integer.to_char_list/2 is deprecated. Use Integer.to_charlist/2 instead
  lib/poison/encoder.ex:173

Generated poison app
==> ssl_verify_fun
Compiling 7 files (.erl)
Generated ssl_verify_fun app
===> Compiling certifi
===> Compiling hackney
==> oauth2
Compiling 13 files (.ex)
Generated oauth2 app
==> mime
Compiling 2 files (.ex)
Generated mime app
==> tesla
Compiling 26 files (.ex)
Generated tesla app
==> google_gax
Compiling 5 files (.ex)
Generated google_gax app
==> google_api_discovery
Compiling 21 files (.ex)
Generated google_api_discovery app
==> google_apis
Compiling 28 files (.ex)
Generated google_apis app

13:11:15.373 [info]  FETCHING: https://analyticsdata.googleapis.com/$discovery/GOOGLE_REST_SIMPLE_URI?version=v1alpha

13:11:15.698 [info]  FETCHING: https://analyticsdata.googleapis.com/$discovery/rest?version=v1alpha

13:11:15.936 [info]  FOUND: https://analyticsdata.googleapis.com/$discovery/rest?version=v1alpha
Revision check: old=20201112, new=20201116, generating=true
Creating leading directories
Writing BatchRunPivotReportsRequest to clients/analytics_data/lib/google_api/analytics_data/v1alpha/model/batch_run_pivot_reports_request.ex.
Writing BatchRunPivotReportsResponse to clients/analytics_data/lib/google_api/analytics_data/v1alpha/model/batch_run_pivot_reports_response.ex.
Writing BatchRunReportsRequest to clients/analytics_data/lib/google_api/analytics_data/v1alpha/model/batch_run_reports_request.ex.
Writing BatchRunReportsResponse to clients/analytics_data/lib/google_api/analytics_data/v1alpha/model/batch_run_reports_response.ex.
Writing BetweenFilter to clients/analytics_data/lib/google_api/analytics_data/v1alpha/model/between_filter.ex.
Writing CaseExpression to clients/analytics_data/lib/google_api/analytics_data/v1alpha/model/case_expression.ex.
Writing Cohort to clients/analytics_data/lib/google_api/analytics_data/v1alpha/model/cohort.ex.
Writing CohortReportSettings to clients/analytics_data/lib/google_api/analytics_data/v1alpha/model/cohort_report_settings.ex.
Writing CohortSpec to clients/analytics_data/lib/google_api/analytics_data/v1alpha/model/cohort_spec.ex.
Writing CohortsRange to clients/analytics_data/lib/google_api/analytics_data/v1alpha/model/cohorts_range.ex.
Writing ConcatenateExpression to clients/analytics_data/lib/google_api/analytics_data/v1alpha/model/concatenate_expression.ex.
Writing DateRange to clients/analytics_data/lib/google_api/analytics_data/v1alpha/model/date_range.ex.
Writing Dimension to clients/analytics_data/lib/google_api/analytics_data/v1alpha/model/dimension.ex.
Writing DimensionExpression to clients/analytics_data/lib/google_api/analytics_data/v1alpha/model/dimension_expression.ex.
Writing DimensionHeader to clients/analytics_data/lib/google_api/analytics_data/v1alpha/model/dimension_header.ex.
Writing DimensionMetadata to clients/analytics_data/lib/google_api/analytics_data/v1alpha/model/dimension_metadata.ex.
Writing DimensionOrderBy to clients/analytics_data/lib/google_api/analytics_data/v1alpha/model/dimension_order_by.ex.
Writing DimensionValue to clients/analytics_data/lib/google_api/analytics_data/v1alpha/model/dimension_value.ex.
Writing Entity to clients/analytics_data/lib/google_api/analytics_data/v1alpha/model/entity.ex.
Writing Filter to clients/analytics_data/lib/google_api/analytics_data/v1alpha/model/filter.ex.
Writing FilterExpression to clients/analytics_data/lib/google_api/analytics_data/v1alpha/model/filter_expression.ex.
Writing FilterExpressionList to clients/analytics_data/lib/google_api/analytics_data/v1alpha/model/filter_expression_list.ex.
Writing InListFilter to clients/analytics_data/lib/google_api/analytics_data/v1alpha/model/in_list_filter.ex.
Writing Metadata to clients/analytics_data/lib/google_api/analytics_data/v1alpha/model/metadata.ex.
Writing Metric to clients/analytics_data/lib/google_api/analytics_data/v1alpha/model/metric.ex.
Writing MetricHeader to clients/analytics_data/lib/google_api/analytics_data/v1alpha/model/metric_header.ex.
Writing MetricMetadata to clients/analytics_data/lib/google_api/analytics_data/v1alpha/model/metric_metadata.ex.
Writing MetricOrderBy to clients/analytics_data/lib/google_api/analytics_data/v1alpha/model/metric_order_by.ex.
Writing MetricValue to clients/analytics_data/lib/google_api/analytics_data/v1alpha/model/metric_value.ex.
Writing NumericFilter to clients/analytics_data/lib/google_api/analytics_data/v1alpha/model/numeric_filter.ex.
Writing NumericValue to clients/analytics_data/lib/google_api/analytics_data/v1alpha/model/numeric_value.ex.
Writing OrderBy to clients/analytics_data/lib/google_api/analytics_data/v1alpha/model/order_by.ex.
Writing Pivot to clients/analytics_data/lib/google_api/analytics_data/v1alpha/model/pivot.ex.
Writing PivotDimensionHeader to clients/analytics_data/lib/google_api/analytics_data/v1alpha/model/pivot_dimension_header.ex.
Writing PivotHeader to clients/analytics_data/lib/google_api/analytics_data/v1alpha/model/pivot_header.ex.
Writing PivotOrderBy to clients/analytics_data/lib/google_api/analytics_data/v1alpha/model/pivot_order_by.ex.
Writing PivotSelection to clients/analytics_data/lib/google_api/analytics_data/v1alpha/model/pivot_selection.ex.
Writing PropertyQuota to clients/analytics_data/lib/google_api/analytics_data/v1alpha/model/property_quota.ex.
Writing QuotaStatus to clients/analytics_data/lib/google_api/analytics_data/v1alpha/model/quota_status.ex.
Writing ResponseMetaData to clients/analytics_data/lib/google_api/analytics_data/v1alpha/model/response_meta_data.ex.
Writing Row to clients/analytics_data/lib/google_api/analytics_data/v1alpha/model/row.ex.
Writing RunPivotReportRequest to clients/analytics_data/lib/google_api/analytics_data/v1alpha/model/run_pivot_report_request.ex.
Writing RunPivotReportResponse to clients/analytics_data/lib/google_api/analytics_data/v1alpha/model/run_pivot_report_response.ex.
Writing RunRealtimeReportRequest to clients/analytics_data/lib/google_api/analytics_data/v1alpha/model/run_realtime_report_request.ex.
Writing RunRealtimeReportResponse to clients/analytics_data/lib/google_api/analytics_data/v1alpha/model/run_realtime_report_response.ex.
Writing RunReportRequest to clients/analytics_data/lib/google_api/analytics_data/v1alpha/model/run_report_request.ex.
Writing RunReportResponse to clients/analytics_data/lib/google_api/analytics_data/v1alpha/model/run_report_response.ex.
Writing StringFilter to clients/analytics_data/lib/google_api/analytics_data/v1alpha/model/string_filter.ex.
Writing Properties to clients/analytics_data/lib/google_api/analytics_data/v1alpha/api/properties.ex.
Writing V1alpha to clients/analytics_data/lib/google_api/analytics_data/v1alpha/api/v1alpha.ex.
Writing connection.ex.
Writing metadata.ex.
Writing mix.exs
Writing README.md
Writing LICENSE
Writing .gitignore
Writing config/config.exs
Writing test/test_helper.exs
[33mThe mix.lock file was generated with a newer version of Hex. Update your client by running `mix local.hex` to avoid losing data.[0m

13:11:17.515 [info]  Bumping patch
fixing file permissions
2020-11-18 05:11:20,187 synthtool [DEBUG] > Wrote metadata to clients/analytics_data/synth.metadata.
DEBUG:synthtool:Wrote metadata to clients/analytics_data/synth.metadata.

```
</details>

Full log will be available here:
https://source.cloud.google.com/results/invocations/725a4817-73e8-42f2-8ba6-a36810184277/targets

- [ ] To automatically regenerate this PR, check this box."
""".lower()
    print("is fix", is_security(text))
    print("security in text", re.findall(build_positive_regex(), text))


