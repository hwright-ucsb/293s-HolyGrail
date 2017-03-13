import org.apache.lucene.index.DirectoryReader;
import org.apache.lucene.index.IndexReader;
import org.apache.lucene.queryparser.classic.ParseException;
import org.apache.lucene.queryparser.classic.QueryParser;
import org.apache.lucene.search.Query;
import org.apache.lucene.store.FSDirectory;
import org.apache.lucene.search.IndexSearcher;
import org.apache.lucene.search.TopDocs;
import org.apache.lucene.search.ScoreDoc;
import org.apache.lucene.document.Document;
import org.apache.lucene.analysis.standard.StandardAnalyzer;
import java.io.IOException;
import java.nio.file.*;
import java.util.Scanner;

public class QueryString {
    public static void main(String[] args) throws IOException, ParseException {
        int NUM_FILES = args.length > 1 ? Integer.parseInt(args[1]) : 100;

        StandardAnalyzer analyzer = new StandardAnalyzer();
        FSDirectory index = FSDirectory.open(Paths.get("./Index" + NUM_FILES + ".lucene"));

        // 2. query
        String querystr = args.length > 0 ? args[0] : "mexican";

        // the first arg specifies the default field to use
        // when no field is explicitly specified in the query.
        Scanner sc = new Scanner(System.in);
        System.out.println("\nWhich field would you like to query? (Searches title by default.)");
        System.out.println("\tEnter 1 for DOC ID");
        System.out.println("\tEnter 2 for BODY");
        System.out.println("\tEnter anything else for TITLE");

        int fieldCode = sc.nextInt();
        sc.nextLine();
        Query q;
        if(fieldCode==1){
            q = new QueryParser("docID", analyzer).parse(querystr);
        }
        else if(fieldCode==2){
            q = new QueryParser("body", analyzer).parse(querystr);
        }
        else{
            q = new QueryParser("title",analyzer).parse(querystr);
        }

        // 3. search
        int hitsPerPage = 10;
        IndexReader reader = DirectoryReader.open(index);
        IndexSearcher searcher = new IndexSearcher(reader);
        TopDocs docs = searcher.search(q, hitsPerPage);
        ScoreDoc[] hits = docs.scoreDocs;

        // 4. display results
        System.out.println("Found " + hits.length + " hits.");
        for(int i=0;i<hits.length;++i) {
            int docId = hits[i].doc;
            Document d = searcher.doc(docId);
            System.out.println((i + 1) + ". " + d.get("docID") + "\t" + d.get("title"));
        }

        // reader can only be closed when there
        // is no need to access the documents any more.
        reader.close();
    }
}
