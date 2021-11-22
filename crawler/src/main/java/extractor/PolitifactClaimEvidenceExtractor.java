package extractor;

import java.util.HashSet;

import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;
/**  
 * This class is implemented the parsing rules for retrieve useful information on the Politifact  fact-check pages.
 * Each function retrieve one kind of information.
 * The results can retrieve with all the get fucntions.
 */

public class PolitifactClaimEvidenceExtractor extends ClaimEvidenceExtractor {

    public PolitifactClaimEvidenceExtractor(String htmlContent,String url,String serverURL,long offset,int length,String running_dir){
        super(htmlContent, url, serverURL, offset, length, running_dir);
    }
     
    protected String claimExtractor(Document doc){
        // Elements articleBody = getArticleBody( doc);
        Element claimElement = doc.select(".m-statement__quote").first();//or use ".o-stage .m-statement__quote"
        claim = claimElement.text();

        //clean
        int index = claim.lastIndexOf(".");
        if (index>30){
            claim = claim.substring(0,claim.lastIndexOf(".")+1);
        }
        claim = stringNormalize(claim,true,true);
        return claim;
    }
    protected HashSet<String> originalLinksExtractor(Document doc){
        Elements relevantDocumentUrlElements=doc.select("#sources a");
        HashSet<String> relevantDocumentLinks = new HashSet<String>();
        for (Element relevantDocumentUrlElement:relevantDocumentUrlElements){
            relevantDocumentLinks.add(relevantDocumentUrlElement.attr("href"));
        }
        return relevantDocumentLinks;
    }
    protected HashSet<String> evidencesExtractor(Document doc){
        HashSet<String> evidenceStrSet=new HashSet<String>();
        Elements evidenceElements=doc.select(".short-on-time > p");
        for (Element evidenceElement:evidenceElements){
            String evidence = stringNormalize(evidenceElement.text(),true,false);
            evidenceStrSet.add(evidence);
        }
       
        return evidenceStrSet;
    }
    protected String truthfulnessExtractor(Document doc){
        Element truthfulnessElement = doc.select(".c-image__original[alt]").first();
        String truthfulness=truthfulnessElement.attr("alt");

        truthfulness = stringNormalize(truthfulness,true,true);
        return truthfulness;
    }

    private Elements getRulingArticleElements(Document doc){
        Elements rulingArticleElements=doc.select(".m-textblock").first().children();
        return rulingArticleElements;
    }

    //ruling article
    protected String originExtactor(Document doc){
        Elements rulingArticleElements=getRulingArticleElements(doc);
        String rulingArticle="";
        for (Element rulingArticleElement:rulingArticleElements){
            if ( rulingArticleElement.select(".o-pick").size()>0){
                continue;//ad
            }else if (rulingArticleElement.text().contains("Our ruling")){
                break; //begin the ruling outline
            }else{
                rulingArticle += rulingArticleElement.text();
                rulingArticle +=" ";
            }
            
        }
        rulingArticle = stringNormalize(rulingArticle,true,true);
        return rulingArticle;
    }
    //ruling outline
    protected String rulingOutlineExtactor(Document doc){
        Elements rulingArticleElements=getRulingArticleElements(doc);
        String rulingOutline="";
        boolean is_start=false;
        for (Element rulingArticleElement:rulingArticleElements){
            if (rulingArticleElement.text().contains("Our ruling")){
                is_start=true; //begin the ruling outline
                continue;
            } 
            
            if (is_start){
                rulingOutline += rulingArticleElement.text();
                rulingOutline +=" ";
            }
             
            
        }
        rulingOutline = stringNormalize(rulingOutline,true,true);
        return rulingOutline;
    }


    //no use
    protected String headlineExtractor(Document doc){
        return "" ;
    }
    protected String descriptionExtractor(Document doc){
        return "" ;
    }
    protected String subCategoryExtractor(Document doc){
        return "" ;
    }
    protected String categoryExtractor(Document doc){
        return "" ;
    }
    protected String sourceExtractor(Document doc){
        return "" ;
    }
}
