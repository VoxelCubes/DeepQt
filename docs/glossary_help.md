# Glossary Format

These glossaries do not take advantage of DeepL's integrated glossaries, however, they are more powerful in other ways.  
A glossary is a collection of terms, each of which consists of a pattern to look for in the left cell, and the pattern to substitute it with in the right cell. The substitution patterns require a prefix symbol which dictates what type of term it is. DeepQt glossaries support 6 different types of terms, processed in the following order:

#### Exact match

| pattern | #substitution |
|:-------:| ------------- |
| painter | #Maler        |

The simplest form of substitution. It simply replaces the pattern with the substitution regardless of context.  

**Note:** This pattern type inserts a trailing space. This can be useful when a word was replaced in the middle of another word and in conjunction with title suffix and prefix options. See [No Suffix](#NoSuffix) terms to avoid this behavior.

#### Regex

| pattern | :subsitution |
| ------- | ------------ |
| / +/    | /: /         |

When you need full control over context, [Regular Expressions](https://en.wikipedia.org/wiki/Regular_expression) are the way to go. Here to condense multiple spaces into only one. The use of capture groups can also allow you to change the order of words.

**Note:** To use capture groups, you need to use Python-style syntax. That means group 1 is \1, instead of $1, as you may see in other styles. Further, if your patterns include whitespace in the front or back, your editor is likely to strip it out. To prevent this, you can wrap your patterns in slashes, as seen in the example (This works for all pattern types).

#### Title suffixes (honorifics)

| pattern  | $substitution |
| -------- | ------------- |
| of Power | $de force     |

These substitutions only engage when preceded by the pattern `[a-z] ` (any lower-case letter, followed by a space). This way they aren't accidentally inserted in improper locations. Particularly useful when dealing with languages that have suffix honorific systems.

#### Title prefixes

| pattern | !substitution |
| ------- | ------------- |
| Master  | !Herr         |

Similar to title suffixes. These substitutions only engage when followed by the pattern `&nbsp;[A-Z]` (a space,  followed by any upper-case letter).

#### <a name="NoSuffix"></a>No Suffix

| pattern  | &#124;substitution |
| -------- | ----------- |
| Künstler | &#124;artist      |

Like exact patterns, but do not insert a trailing space.

#### Post term

| pattern | ~substitution |
| ------- | ------------- |
| paper   | ~Arbeit       |

Like exact matches, but are simply performed last. This can be useful to avoid potential collisions with other terms that should be processed first.

## Supported File Formats

DeepQt uses [pyexcel](http://docs.pyexcel.org/en/latest/) to read glossaries. It supports a plethora of formats, including:  
.ods, .xlsx, .html, .csv, .csvz, .tsv, .tsvz, .rst, .json ... and many more.  
You can see the full list [here](https://github.com/pyexcel/pyexcel#feature-highlights).