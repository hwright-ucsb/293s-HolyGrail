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
import java.util.Arrays;
import java.util.Set;
import java.util.Scanner;
import java.util.ArrayList;
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
import org.apache.lucene.search.PhraseQuery;
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

	public static boolean entireWord(String tmp, int index, String strain) {
		// System.out.println("strain is " + strain);
		// System.out.println("tmp is |" + tmp + "| and index is " + Integer.toString(index));
		if(index != 0)
			if(!(tmp.charAt(index - 1) == ' ')) return false;
		if(index + strain.length() - 1 < tmp.length() - 1) {
			if(!(tmp.charAt(index + strain.length()) == ' ')) return false;
		}
		else return false;
		// System.out.println("returning true");
		return true;
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
		MultiFieldQueryParser conjunctiveParser;
		QueryParser queryParser;
		IndexReader reader = null;
		JSONObject o;
		JSONParser parser = new JSONParser();
		try{
            o = (JSONObject)parser.parse(new FileReader("../data_consol/consol_strains-5.json"));
        } catch(Exception e) {
            e.printStackTrace();
            return;
        }
        String line;
        String[] stuff;

        String oldQuery;
        String oldQueryStopRemoved;

        ArrayList<String> strains = new ArrayList<String>(o.keySet());
        // ArrayList.sort(strains, java.util.Comparator);
        // System.out.println(strains);
		while(!querystr.equals("exit")) {
			System.out.println("Please Enter a query String!\n\n\n\n");
			oldQuery = sc.nextLine();
			querystr = removeStopWordsAndStem(oldQuery, false);
			oldQueryStopRemoved = removeStopWordsAndStem(oldQuery, false);

			oldQueryStopRemoved.replaceAll("( )+", " ");

			System.out.println("\n");
			System.out.println("Your Query: " + oldQuery);
			System.out.println("Stop Word Removal Query: " + oldQueryStopRemoved);

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
			BooleanQuery.Builder totalQuery = new BooleanQuery.Builder();
			ArrayList<String> totalQueryStrings = new ArrayList<String>();

			String tmp = oldQueryStopRemoved;
			for(String strain : strains) {
				int ind = tmp.indexOf(strain);
				if((ind >= 0) && entireWord(tmp, ind, strain)) {
					System.out.println("strain is " + strain);
					System.out.println("here");
					tmp = tmp.replace(strain, "");
					// conjunctiveParser = new MultiFieldQueryParser(fields, analyzer, boosts);
					// conjunctiveParser.setDefaultOperator(QueryParser.Operator.AND);
		   //  		q = conjunctiveParser.parse(strain);
		    		totalQueryStrings.add(strain);

		    		PhraseQuery.Builder quer = new PhraseQuery.Builder();

					String[] words = strain.split(" ");
					int asd = 0;
					System.out.println("words is " + words);
					for (String word : words) {
						System.out.println("adding " + word);
					    quer.add(new Term("title", word), asd++);
					}

					BoostQuery boost = new BoostQuery(quer.build(), 0.8f);
					totalQuery.add(boost, Occur.MUST);
					System.out.println("Query " + Integer.toString(j) + ": " + strain);
					j++;
				}
			}
    		// System.out.println("Query " + Integer.toString(j) + ": " + tmp);
    		//if no strain, just do it normally
    		if(!tmp.trim().equals("")) {
    			System.out.println("here");
    			conjunctiveParser = new MultiFieldQueryParser(fields, analyzer);
    			conjunctiveParser.setDefaultOperator(QueryParser.Operator.OR);
    			q = conjunctiveParser.parse(tmp);
    			BoostQuery boost = new BoostQuery(q, 0.1f);
    			totalQuery.add(boost, Occur.SHOULD);
    			totalQueryStrings.add(tmp);
    		} else {
    			if (oldQuery.trim() == "") {
    				System.out.println("enter something valid plz \n");
    				continue;
    			}
    		}

    		System.out.println("Query Terms Split:");
    		int it = 0;
    		for (String ter: totalQueryStrings) {
    			System.out.println("\t\033[1;31mQuery" + it + ": " + ter + "\033[0m");
    			it++;
    		}
    		System.out.println("\n");

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

				for(String s : totalQueryStrings) {	
					ArrayList<String> k = new ArrayList();

					if(!strains.contains(s.trim()) && s.contains(" ")) {
						k = new ArrayList(Arrays.asList(s.split(" ")));
					} else {
						k.add(s);
					}
					for(String a : k) {
						a = a.trim();
						if(!a.equals("")){
							// System.out.println("a is " + a);
							formattedTitle = formattedTitle.replaceAll("((?i)" + a + ")", "\033[1;32m" + "$1" + "\033[0m");
							formattedBody = formattedBody.replaceAll("((?i)" + a + ")", "\033[1;32m" + "$1" + "\033[0m");
						}
					}
					
					
				}


				System.out.println((i + 1) + ". " + "\t" + formattedTitle + "\n" + formattedBody + "\n");
			}
		}

		// reader can only be closed when there
		// is no need to access the documents any more.
		reader.close();
	}
}
