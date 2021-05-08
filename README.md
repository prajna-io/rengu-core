# Rengu Content Management System

The rengu system is used to manage content sets. The intent is prove a rich content environment that puts metadata and content search capabilities first in order to support content data analytics.

The name "rengu" comes from the Japanese word "renku" or "renga", both of which are linked verse poetry forms. Ther idea is that content, like renku/renga should be managed as a set of rich, interlinked pieces of information.

## Structure of Rengu

* [rengu-core](//prajna-io/rengu-core) - This package, which includes the basic CLI and local rengu data featureset
* [rengu-dav](//prajna-io/rengu-dav) - A WebDAV server implementation of rengu
* [rengu-scrape](//prajna-io/rengu-scrape) - Tools for scraping content from external sources, allowing use of rengu as an archive system 

## Rengu Specifier Syntax

The goal of the specifier syntax is to provide something that is compatible with both web-based URLs and with normal Unix shell scripting.

* `+` or `" "`(space) default operator
* `/` AND
* `^` OR
* `-` NOT
* `{}` (scope delimiter)
