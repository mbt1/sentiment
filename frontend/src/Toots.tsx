import React, { useEffect, useState } from 'react';
import createDOMPurify from 'dompurify';
import DOMPurify from 'dompurify';

const targetAPIBaseURL = process.env.REACT_APP_TARGET_API_BASE_URL;

interface Toot {
    id: string;
    created_at: string;
    content: string;
    spoiler_text: string;
    account: {
      id: string;
      username: string;
      display_name: string;
    };
  }
  
const App: React.FC = () => {
  const [toots, setToots] = useState<Toot[]>([]);

  useEffect(() => {
    fetch(targetAPIBaseURL+'/api/toots/?search_term=SQLServer')
      .then((response) => response.json())
      .then((data: Toot[]) => setToots(data));
  }, []);

  const DOMPurify = createDOMPurify(window);
  DOMPurify.addHook('uponSanitizeElement', function(node, data) {
    if (data.tagName === 'a') {
      const span = document.createElement('span');
      while (node.firstChild) {span.appendChild(node.firstChild);}
      node.parentNode.replaceChild(span, node);
    }
  });
  const DOMPurifyConfig: DOMPurify.Config = {ALLOWED_TAGS: ['p', 'b', 'i', 'span', '#text'], ALLOWED_ATTR: [], KEEP_CONTENT: false};

  return (
    <div>
    {toots.map((toot: Toot, index: number) => {
      const name:string  = DOMPurify.sanitize(toot.account.display_name,DOMPurifyConfig) +' @'+ DOMPurify.sanitize(toot.account.username,DOMPurifyConfig)
      const content:{ __html: string }  = {__html: ""+DOMPurify.sanitize(toot.content,DOMPurifyConfig)}
      const spoiler:{ __html: string }  = {__html: "Spoiler: "+DOMPurify.sanitize(toot.spoiler_text,DOMPurifyConfig)}
      const createdAt:string = "Created at:" +DOMPurify.sanitize(toot.created_at,DOMPurifyConfig)
      return(
        <div key={toot.id} className="toot">
        <h3>{name}</h3>
        <p dangerouslySetInnerHTML={content} />
        {toot.spoiler_text && <span dangerouslySetInnerHTML={spoiler} />}
        <small>{createdAt}</small>
        </div>
      )}
    )}
    </div>
  );
};

export default App;
