JFLAGS = -g
JC = javac

all: Indexer.class QueryString.class

Indexer:
	javac -cp .:json-simple-1.1.jar:lucene-6.4.0/core/lucene-core-6.4.0.jar:lucene-6.4.0/queryparser/lucene-queryparser-6.4.0.jar:lucene-6.4.0/analysis/common/lucene-analyzers-common-6.4.0.jar Indexer.java
	java -cp .:json-simple-1.1.jar:lucene-6.4.0/core/lucene-core-6.4.0.jar:lucene-6.4.0/queryparser/lucene-queryparser-6.4.0.jar:lucene-6.4.0/analysis/common/lucene-analyzers-common-6.4.0.jar Indexer $(a)

QueryString:
	@javac -cp .:json-simple-1.1.jar:lucene-6.4.0/core/lucene-core-6.4.0.jar:lucene-6.4.0/queryparser/lucene-queryparser-6.4.0.jar:lucene-6.4.0/analysis/common/lucene-analyzers-common-6.4.0.jar QueryString.java
	@java -cp .:json-simple-1.1.jar:lucene-6.4.0/core/lucene-core-6.4.0.jar:lucene-6.4.0/queryparser/lucene-queryparser-6.4.0.jar:lucene-6.4.0/analysis/common/lucene-analyzers-common-6.4.0.jar QueryString $(a)

Indexer.class: Indexer.java
	javac -cp .:json-simple-1.1.jar:lucene-6.4.0/core/lucene-core-6.4.0.jar:lucene-6.4.0/queryparser/lucene-queryparser-6.4.0.jar:lucene-6.4.0/analysis/common/lucene-analyzers-common-6.4.0.jar Indexer.java

QueryString.class: QueryString.java
	javac -cp .:json-simple-1.1.jar:lucene-6.4.0/core/lucene-core-6.4.0.jar:lucene-6.4.0/queryparser/lucene-queryparser-6.4.0.jar:lucene-6.4.0/analysis/common/lucene-analyzers-common-6.4.0.jar QueryString.java

clean:
	rm -rf *.class