import java.io.BufferedReader;
import java.io.FileInputStream;
import java.io.FileReader;
import java.io.InputStreamReader;
import java.io.IOException;
import java.io.IOException;
import java.io.Reader;
import java.io.StringReader;
import java.nio.file.*;
import java.nio.file.*;
import java.util.HashMap;
import java.util.Iterator;
import java.util.Scanner;
import org.apache.lucene.analysis.CharArraySet;
import org.apache.lucene.analysis.core.StopFilter;
import org.apache.lucene.analysis.en.EnglishAnalyzer;
import org.apache.lucene.analysis.standard.StandardAnalyzer;
import org.apache.lucene.analysis.standard.StandardTokenizer;
import org.apache.lucene.analysis.tokenattributes.*;
import org.apache.lucene.analysis.TokenStream;
import org.apache.lucene.document.Document;
import org.apache.lucene.document.Field;
import org.apache.lucene.document.StringField;
import org.apache.lucene.document.TextField;
import org.apache.lucene.index.DirectoryReader;
import org.apache.lucene.index.IndexReader;
import org.apache.lucene.index.IndexWriter;
import org.apache.lucene.index.IndexWriterConfig;
import org.apache.lucene.index.Term;
import org.apache.lucene.queryparser.classic.ParseException;
import org.apache.lucene.queryparser.classic.QueryParser;
import org.apache.lucene.search.*;
import org.apache.lucene.search.IndexSearcher;
import org.apache.lucene.search.Query;
import org.apache.lucene.search.ScoreDoc;
import org.apache.lucene.search.similarities.*;
import org.apache.lucene.search.TopDocs;
import org.apache.lucene.store.Directory;
import org.apache.lucene.store.FSDirectory;
import org.apache.lucene.store.RAMDirectory;
import org.apache.lucene.util.Version;
import org.json.simple.*;
import org.json.simple.parser.*;
import org.tartarus.snowball.ext.PorterStemmer;

public class QueryString {
	public static String removeStopWordsAndStem(String textFile) {
		CharArraySet stopWords = EnglishAnalyzer.getDefaultStopSet();
		StandardTokenizer tokenStream = new StandardTokenizer();
		Reader targetReader = new StringReader(textFile.trim());
		tokenStream.setReader(targetReader);

		StopFilter filter = new StopFilter(tokenStream, stopWords);

		StringBuilder sb = new StringBuilder();
		CharTermAttribute charTermAttribute = tokenStream.addAttribute(CharTermAttribute.class);
		try{
		  filter.reset();
		}catch(IOException e){
		  e.printStackTrace();
		}
		PorterStemmer stemmer = new PorterStemmer();
		
		boolean tok = false;

		try{
			tok = filter.incrementToken();
		}catch(IOException e){
		  e.printStackTrace();
		}

		while (tok) {
			String term = charTermAttribute.toString();
			
			stemmer.setCurrent(term);
			stemmer.stem();
			String current = stemmer.getCurrent();

			sb.append(current + " ");

			
			try {
				tok = filter.incrementToken();
			} catch(IOException e){
				e.printStackTrace();
			}

		}
		return sb.toString();
	}

	public static void main(String[] args) throws IOException, ParseException {
		int NUM_FILES = args.length > 1 ? Integer.parseInt(args[1]) : 100;

		StandardAnalyzer analyzer = new StandardAnalyzer();
		FSDirectory index = FSDirectory.open(Paths.get("./Index" + NUM_FILES + ".lucene"));

		// 2. query
		String querystr = args.length > 0 ? args[0] : "mexican";

		// the first arg specifies the default field to use
		// when no field is explicitly specified in the query.
		Scanner sc = new Scanner(System.in);
		// System.out.println("\nWhich field would you like to query? (Searches title by default.)");
		// System.out.println("\tEnter 1 for DOC ID");
		// System.out.println("\tEnter 2 for BODY");
		// System.out.println("\tEnter anything else for TITLE");

		// int fieldCode = sc.nextInt();
		int fieldCode = 1;
		// sc.nextLine();
		Query q;
		IndexReader reader = null;

		
		while(!querystr.equals("exit")) {
			System.out.println("Please Enter a query String!");
			querystr = sc.nextLine();

			if(fieldCode==1){
				q = new QueryParser("both", analyzer).parse(querystr);
			}
			else if(fieldCode==2){
				q = new QueryParser("body", analyzer).parse(querystr);
			}
			else{
				q = new QueryParser("title",analyzer).parse(querystr);
			}

					// 3. search
			int hitsPerPage = 10;
			reader = DirectoryReader.open(index);
			IndexSearcher searcher = new IndexSearcher(reader);
			TopDocs docs = searcher.search(q, hitsPerPage);
			ScoreDoc[] hits = docs.scoreDocs;

			// 4. display results
			System.out.println("Found " + hits.length + " hits.");
			for(int i=0;i<hits.length;++i) {
				int docId = hits[i].doc;
				Document d = searcher.doc(docId);
				System.out.println((i + 1) + ". " + "\t" + d.get("title") + "\n" + d.get("body") + "\n");
			}
		}

		// reader can only be closed when there
		// is no need to access the documents any more.
		reader.close();
	}
}
