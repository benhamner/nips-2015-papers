
input/papers.csv:
	mkdir -p input
	mkdir -p input/pdfs
	python src/download_papers.py
download-papers: input/papers.csv

output/database.sqlite:
	mkdir -p output
	python src/papers_to_database.py
db: output/database.sqlite
