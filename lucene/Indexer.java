import java.io.IOException;
import org.apache.lucene.analysis.standard.StandardAnalyzer;
import org.apache.lucene.document.Document;
import org.apache.lucene.document.Field;
import org.apache.lucene.document.StringField;
import org.apache.lucene.document.TextField;
import org.apache.lucene.store.Directory;
import org.apache.lucene.index.IndexWriter;
import org.apache.lucene.store.FSDirectory;
import java.nio.file.*;
import org.apache.lucene.store.RAMDirectory;
import org.apache.lucene.index.IndexWriterConfig;
import java.io.BufferedReader;
import java.io.FileReader;
import org.json.simple.*;
import org.json.simple.parser.*;
import java.util.Iterator;

public class Indexer {
    public static void print(String s){
        System.out.println(s);
    }
    public static void main(String[] args) throws IOException {
        int NUM_FILES = args.length > 0 ? Integer.parseInt(args[0]) : 100;

        // 0. Specify the analyzer for tokenizing text.
        //    The same analyzer should be used for indexing and searching
        StandardAnalyzer analyzer = new StandardAnalyzer();

        // 1. create the index

        String fileName = "./Index" + NUM_FILES + ".lucene";
        FSDirectory index = FSDirectory.open(Paths.get(fileName));

        IndexWriterConfig config = new IndexWriterConfig(analyzer);
        config.setOpenMode(IndexWriterConfig.OpenMode.CREATE);
        JSONParser parser = new JSONParser();

        IndexWriter w = new IndexWriter(index, config);
        JSONObject o;
        try{
            o = (JSONObject)parser.parse(new FileReader("consol_strains.json"));
        } catch(Exception e) {
            e.printStackTrace();
            return;
        }
        String line;
        String[] stuff;
        Iterator<?> keys = o.keySet().iterator();
        String desc;

        while( keys.hasNext() ) {
            String strain_name = (String)keys.next();
            desc = strain_name;
            JSONArray strain_array = (JSONArray) o.get(strain_name);
            int i = 0;
            for(Object obj : strain_array) {
                i++;
                JSONObject jsobj = (JSONObject)obj;
                desc = desc + "\n" + "Description " + i + "." + jsobj.get("description").toString();
            }

            addDoc(w, strain_name, desc);
        }

        w.close();
    }

    private static void addDoc(IndexWriter w, String title, String body) throws IOException {
        // 488473549 Jan 18 17:50 lines-trec45.txt.gz
        // This file has the same content as trec-disk4-5.xml except that
        // the XML data is  stripped to plaintext.
        // Each line is a document and the format is:
        // Up to the first tab  --> the docid,
        // between the first and second tab -->  the title,
        // after the second tab --> the body of the document
        Document doc = new Document();
        doc.add(new TextField("title", title, Field.Store.YES));
        doc.add(new TextField("body", body, Field.Store.YES));
        doc.add(new TextField("both", title + " " + body, Field.Store.YES));
        w.addDocument(doc);
    }
}