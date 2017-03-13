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

public class Indexer {
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

        IndexWriter w = new IndexWriter(index, config);
        BufferedReader br = new BufferedReader(new FileReader("lines-trec45.txt"));
        String line;
        String[] stuff;
        while((line = br.readLine()) != null){
            stuff = line.split("\t");
            if(stuff.length == 1){
                addDoc(w,stuff[0],"","");
            }
            else if(stuff.length == 2){
                addDoc(w,stuff[0],stuff[1],"");
            }else{
                addDoc(w,stuff[0],stuff[1],stuff[2]); 
            }
        }

        br.close();
        w.close();
    }

    private static void addDoc(IndexWriter w, String docID, String title, String body) throws IOException {
        // 488473549 Jan 18 17:50 lines-trec45.txt.gz
        // This file has the same content as trec-disk4-5.xml except that
        // the XML data is  stripped to plaintext.
        // Each line is a document and the format is:
        // Up to the first tab  --> the docid,
        // between the first and second tab -->  the title,
        // after the second tab --> the body of the document
        Document doc = new Document();
        doc.add(new StringField("docID", docID, Field.Store.YES));
        doc.add(new TextField("title", title, Field.Store.YES));
        doc.add(new TextField("body", body, Field.Store.YES));
        w.addDocument(doc);
    }
}