.separator ","

CREATE TABLE Papers (
    Id INTEGER PRIMARY KEY,
    Title TEXT,
    EventType TEXT,
    PdfName TEXT,
    Abstract TEXT,
    PaperText TEXT);

CREATE TABLE Authors (
    Id INTEGER PRIMARY KEY,
    Name TEXT);

CREATE TABLE PaperAuthors (
    Id INTEGER PRIMARY KEY,
    PaperId INTEGER,
    AuthorId INTEGER);

.import "working/noHeader/Papers.csv" Papers
.import "working/noHeader/Authors.csv" Authors
.import "working/noHeader/PaperAuthors.csv" PaperAuthors

CREATE INDEX paperauthors_paperid_idx ON PaperAuthors (PaperId);
CREATE INDEX paperauthors_authorid_idx ON PaperAuthors (AuthorId);
