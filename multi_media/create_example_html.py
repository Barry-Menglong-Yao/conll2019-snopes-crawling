from util.create_example.read_example import read_example
import dominate
from dominate.tags import *
import webbrowser



def main():
    data_path="out/example/"
    example_dict=read_example(data_path)
    

    doc = dominate.document(title='examples')
    with doc.head:
        link(rel='stylesheet', href='style.css')
        script(type='text/javascript', src='script.js')

    with doc:
        with div() as body:
            attr(cls='body')
            for _,example in example_dict.items():
                body.add(h1(f"claim id:{example.claim_id}"))
        
                body.add(h2(a("snopes_url",href=example.snopes_url)))
                body.add(h2("claim"))
                body.add(p(example.claim))
                body.add(h2("truthfulness"))
                body.add(p(example.truthfulness))
                body.add(h2("evidence"))
                with body.add(ol()):
                    for evidence_text in example.evidence_text_list:
                        li(p(evidence_text))

                
                
                body.add(h2("text in relevant docs"))
                with body.add(ol()):
                    for relevant_doc in example.relevant_doc_list:
                        li(p(relevant_doc))
                body.add(h2("image in relevant docs"))
                with body.add(ol()):
                    for img_name in example.evidence_img_list:
                        li(img(src=img_name,alt=""))

                body.add(h2("ruling_article"))
                body.add(p(example.ruling_article))

                        
                body.add(hr())


    print(doc)
    html_name=data_path+'img.html'
    with open(html_name, 'w') as f:
        print(doc,file=f)
    webbrowser.open(html_name) 

def test():
    doc = dominate.document(title='examples')

    with doc.head:
        link(rel='stylesheet', href='style.css')
        script(type='text/javascript', src='script.js')

    with doc:
        with div(id='header').add(ol()):
            for i in ['home', 'about', 'contact']:
                li(a(i.title(), href='/%s.html' % i))

        with div():
            attr(cls='body')
            p('Lorem ipsum..')

    print(doc)


if __name__ == '__main__':
    main() 
    
