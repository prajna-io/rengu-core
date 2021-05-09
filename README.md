# Rengu Content Management System

The rengu system is used to manage content sets. The intent is prove a rich content environment that puts metadata and content search capabilities first in order to support content data analytics.

The name "rengu" comes from the Japanese word "renku" or "renga", both of which are linked verse poetry forms. Ther idea is that content, like renku/renga should be managed as a set of rich, interlinked pieces of information.

## Structure of Rengu

* [rengu-core](prajna-io/rengu-core) - This package, which includes the basic CLI and local rengu data featureset
* [rengu-dav](prajna-io/rengu-dav) - A WebDAV server implementation of rengu
* [rengu-scrape](prajna-io/rengu-scrape) - Tools for scraping content from external sources, allowing use of rengu as an archive system 

## Rengu Specifier Syntax

The goal of the specifier syntax is to provide something that is compatible with both web-based URLs and with normal Unix shell scripting.

* `+` or `" "`(space) default operator
* `/` AND
* `^` OR
* `-` NOT
* `{}` (scope delimiter)
* `=` Equals operator
* `:` Equals (with order and lemmatization)
* `~` Graph operator
* `*` Glob operator

The following fields are accepted as bare terms:

* ID
* ISBN
* OLID
* words from Body, Title, Description, Comment, SubTitle, AlternateTitles, Name, AlternateNames (normalized to a-z and lower case)

The following fields are lemmatized with order:

* Body
* Title
* Description
* Comment
* SubTitle
* AlternateTitles

The following fields can be used for graph vectors:

* By
* Editor
* Translator
* Contributor
* Creator (any of By, Editor, Translator, Contributor)
* Source
* References
* SeeAlso
* Related (any of the above)

## Data Format

The primary index and data are stored in a LMDB database. The `index` sub-database stores all the terms as keys and all the matching IDs as values. The `data` subdatabase stores all the IDs as values with msgpack values for the data. The `graph` sub-databaase stores all the IDs from->to as keys->values. The `rgraph` sub-database stores ID to<-from as keys<-values.

The `index`, `graph`, and `rgraph` can all be re-built from `data`.

Additional BLOB data is stored in a directory called 
