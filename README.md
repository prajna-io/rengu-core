# Rengu Content Management System

The rengu system is a content management system. Rengu puts metadata and content search capabilities first in order to support content data analytics.

The name "rengu" comes from the Japanese word "renku" or "renga", both of which are linked verse poetry forms. Ther idea is that content, like renku/renga should be managed as a set of rich, interlinked pieces of information.

## Structure of Rengu

* [rengu-core](prajna-io/rengu-core) - This package, which includes the basic CLI and local rengu data featureset
* [rengu-dav](prajna-io/rengu-dav) - A WebDAV server implementation of rengu
* [rengu-scrape](prajna-io/rengu-scrape) - Tools for scraping content from external sources, allowing use of rengu as an archive system 


## Entry Points

Rengu plugins are managed through python entry points. The following are the key entry points defining how plug-ins can be added
to rengu.

| Entry Point | Description |
| ----------- | ----------- |
| rengu_cli   | CLI command |
| rengu_store | Storage for Rengu data |
| rengu_map   | Map/Reduce processor for Rengu |
| rengu_input | Input handler for Rengu |
| rengu_output | Output handler for Rengu |

## Rengu Specifier Syntax

Rengu records can be specified through a simple set syntax. Sets can be specified by bare terms and by key/value pairs. [TODO: content terms with order]

### Bare Terms

The following fields are accepted as bare terms:

* ID (a UUID)
* ISBN
* OLID (OpenLibrary ID)
* IAID (Archive.org ID)

In addition, words from the following fields are normalized to a-z lower case and included as bare terms:

* Body
* Title
* Description
* Comment
* SubTitle
* AlternateTitles
* Name
* AlternateNames

The following fields are lemmatized and included as bare terms.

* Body
* Title
* Description
* Comment
* SubTitle
* AlternateTitles

### Key/Value Pairs


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
