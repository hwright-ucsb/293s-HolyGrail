JFLAGS = -g
JC = javac

all: Indexer.class QueryString.class

Indexer:
	java -cp .:json-simple-1.1.jar:lucene-6.4.0/core/lucene-core-6.4.0.jar:lucene-6.4.0/queryparser/lucene-queryparser-6.4.0.jar Indexer $(a)

QueryString:
	java -cp .:json-simple-1.1.jar:lucene-6.4.0/core/lucene-core-6.4.0.jar:lucene-6.4.0/queryparser/lucene-queryparser-6.4.0.jar QueryString $(a) $(b)

Indexer.class: Indexer.java
	javac -cp .:json-simple-1.1.jar:lucene-6.4.0/core/lucene-core-6.4.0.jar:lucene-6.4.0/queryparser/lucene-queryparser-6.4.0.jar Indexer.java

QueryString.class: QueryString.java
	javac -cp .:json-simple-1.1.jar:lucene-6.4.0/core/lucene-core-6.4.0.jar:lucene-6.4.0/queryparser/lucene-queryparser-6.4.0.jar QueryString.java

clean:
	rm -rf *.class
