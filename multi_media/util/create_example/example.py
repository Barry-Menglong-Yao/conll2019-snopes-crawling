class Example():
    """
    claim
    truthfulness
    relevant_doc_list
        img_list
        text
        evidence_list
            img_list
            text_list
    claim_id
    snope_url
    ruling_article
    """
    def __init__(self,claim_id,snopes_url,evidence,claim ,truthfulness,ruling_article ) :
        self.claim=claim 
        self.truthfulness=truthfulness
        self.relevant_doc_list=[]
        self.evidence_img_list=[]
        self.evidence_text_list=[]
        self.evidence_text_list.append(evidence)
        self.claim_id=claim_id
        self.snopes_url=snopes_url
        self.ruling_article=ruling_article
        


    def add_evidence(self,evidence):
        self.evidence_text_list.append(evidence)

    def add_relevant_doc(self,relevant_doc):
        self.relevant_doc_list.append(relevant_doc)