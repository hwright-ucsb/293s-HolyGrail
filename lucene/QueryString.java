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
import java.util.Set;
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
import org.apache.lucene.queryparser.classic.*;
import org.apache.lucene.search.*;
import org.apache.lucene.search.IndexSearcher;
import org.apache.lucene.search.Query;
import org.apache.lucene.search.BoostQuery;
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
import org.apache.lucene.search.BooleanClause.Occur;

public class QueryString {
	public static String removeStopWordsAndStem(String textFile, boolean stem) {
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
			String current;
			if(stem) {
				stemmer.setCurrent(term);
				stemmer.stem();
				current = stemmer.getCurrent();
			} else {
				current = term;
			}

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
		BooleanQuery.Builder totalQuery = new BooleanQuery.Builder();
		MultiFieldQueryParser conjunctiveParser;
		QueryParser queryParser;
		IndexReader reader = null;
		JSONObject o;
		JSONParser parser = new JSONParser();
		try{
            o = (JSONObject)parser.parse(new FileReader("consol_strains.json"));
        } catch(Exception e) {
            e.printStackTrace();
            return;
        }
        String line;
        String[] stuff;

        String oldQuery;
        String oldQueryStopRemoved;

        Set<String> strains = o.keySet();
        // System.out.println(strains);
		while(!querystr.equals("exit")) {
			System.out.println("Please Enter a query String!\n\n\n\n");
			oldQuery = sc.nextLine();
			querystr = removeStopWordsAndStem(oldQuery, false);
			oldQueryStopRemoved = removeStopWordsAndStem(oldQuery, false);

			System.out.println("\n");
			System.out.println("Your Query: " + oldQuery);

			// if(fieldCode==1){
			// 	queryParser = new QueryParser("both", analyzer).parse(querystr);
			// 	// conjunctiveParser = new MultiFieldQueryParser("both", analyzer);
   //  //     		conjunctiveParser.setDefaultOperator(QueryParser.Operator.AND);
			// }
			// else if(fieldCode==2){
			// 	queryParser = new QueryParser("body", analyzer).parse(querystr);
			// 	// conjunctiveParser = new MultiFieldQueryParser("body", analyzer);
   //  //    			conjunctiveParser.setDefaultOperator(QueryParser.Operator.AND);
			// }
			// else{
			// 	queryParser = new QueryParser("title",analyzer).parse(querystr);
			// 	// conjunctiveParser = new MultiFieldQueryParser("title", analyzer);
   //  //     		conjunctiveParser.setDefaultOperator(QueryParser.Operator.AND);
			// }

			String[] fields = new String[2];
			fields[0] = "title_stem";
			fields[1] = "body_stem";
			HashMap<String,Float> boosts = new HashMap<String,Float>();
			boosts.put("title_stem", 2f);
			boosts.put("body_stem", 1f);

			int j= 0;

			String tmp = oldQueryStopRemoved;
			for(String strain : strains) {
				if(tmp.contains(strain)) {
					tmp = tmp.replace(strain, "");
					conjunctiveParser = new MultiFieldQueryParser(fields, analyzer, boosts);
					conjunctiveParser.setDefaultOperator(QueryParser.Operator.AND);
		    		q = conjunctiveParser.parse(strain);
					BoostQuery boost = new BoostQuery(q, 0.8f);
					totalQuery.add(boost, Occur.MUST);
					// System.out.println("Query " + Integer.toString(j) + ": " + strain);
					j++;
				}
			}
    		// System.out.println("Query " + Integer.toString(j) + ": " + tmp);
    		//if no strain, just do it normally
    		if(!tmp.trim().equals("")) {
    			conjunctiveParser = new MultiFieldQueryParser(fields, analyzer);
    			conjunctiveParser.setDefaultOperator(QueryParser.Operator.OR);
    			q = conjunctiveParser.parse(tmp);
    			BoostQuery boost = new BoostQuery(q, 0.1f);
    			totalQuery.add(boost, Occur.SHOULD);
    		}

			int hitsPerPage = 10;
			reader = DirectoryReader.open(index);
			IndexSearcher searcher = new IndexSearcher(reader);
			
			


			TopDocs docs = searcher.search(totalQuery.build(), hitsPerPage);
			ScoreDoc[] hits = docs.scoreDocs;

			// 4. display results
			if(hits.length == 0)
				System.out.println("Sorry, " + hits.length + " hits found for " + oldQuery + ".");
			for(int i=0;i<hits.length;++i) {
				int docId = hits[i].doc;
				Document d = searcher.doc(docId);
				String formattedTitle = d.get("title");
				String formattedBody = d.get("body");

				String[] l;
				if(oldQueryStopRemoved.contains(" "))
					l = oldQueryStopRemoved.split(" ");
				else {
					l = new String[1];
					l[0] = oldQueryStopRemoved;
				}
				for(String s : l) {
					formattedTitle = formattedTitle.replaceAll("((?i)" + s + ")", "\033[1;31m" + "$1" + "\033[0m");
					formattedBody = formattedBody.replaceAll("((?i)" + s + ")", "\033[1;31m" + "$1" + "\033[0m");
				}


				System.out.println((i + 1) + ". " + "\t" + formattedTitle + "\n" + formattedBody + "\n");
			}
		}

		// reader can only be closed when there
		// is no need to access the documents any more.
		reader.close();
	}
}
