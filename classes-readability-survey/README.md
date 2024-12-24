# ReadabilitySurveyClasses

### Projects Repository

- commons-cli: https://github.com/apache/commons-cli.git
- commons-csv: https://github.com/apache/commons-csv.git
- commons-lang: https://github.com/apache/commons-lang.git
- gson (tag: gson-parent-2.8.5): https://github.com/google/gson.git
- jfreechart (tag: v1.5.4): https://github.com/jfree/jfreechart.git

### Filters used to extract classes
We exclude trivial classes and those having extremely long method lengths from these filters.

- **Total number of lines of code**: [50,inf)
- **Average length of methods**: [3,20]

The collected data was extracted using cloc(https://github.com/AlDanial/cloc.git) and custom functions.

### Ranking selection

From the classes resulting from the filters, these are sorted to form a ranking, the records are sorted according to the following factors: Internal Import, Lines of Code.

The first **six classes** (fewer in number if the project has a few) considered **core** will be selected for the study.
