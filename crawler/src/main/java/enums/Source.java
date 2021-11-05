package enums;

public enum Source {
    Snopes  ( "https://www.snopes.com/fact-check/",".+(fact-check)/.*"),   
    Politifact( "https://www.snopes.com/fact-check/",".+(fact-check)/.*")   
    
    ;  


 
    public String seed_url;
    public String fact_check_pattern;
    private Source( String seed_url,String fact_check_pattern) {
        this.seed_url=seed_url;
        this.fact_check_pattern=fact_check_pattern;
        
    }
}
