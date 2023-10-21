import React from 'react';
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
  sentiment: {
    positive_score: number;
    neutral_score: number;
    negative_score: number;
    overall_sentiment: string;
  }
}
  
interface AppProps {
  searchTerm: string;
}

const App: React.FC<AppProps> = ({searchTerm}) => {
  const [toots, setToots] = React.useState<Toot[]>([]);
  const [isLoading, setIsLoading] = React.useState(false);

  React.useEffect(() => {
    if(searchTerm!=""){
      console.log('Processing toots for SearchTerm:',searchTerm)
      const encodedSearchTerm = encodeURIComponent(searchTerm);
      setIsLoading(true)
      fetch(`${targetAPIBaseURL}/api/toots/?search_term=${encodedSearchTerm}`)
        .then((response) => response.json())
        .then((data: Toot[]) => {
          // Rate Limiter
          return new Promise(resolve => setTimeout(() => resolve(data), 3000));
        })
        .then((data: Toot[]) => {
          setToots(data)
          setIsLoading(false)
        })
        .catch(() => setIsLoading(false))

    }
  }, [searchTerm]);

  const DOMPurify = createDOMPurify(window);
  DOMPurify.addHook('uponSanitizeElement', function(node, data) {
    if (data.tagName === 'a') {
      const span = document.createElement('span');
      while (node.firstChild) {span.appendChild(node.firstChild);}
      node.parentNode.replaceChild(span, node);
    }
  });
  const DOMPurifyConfig: DOMPurify.Config = {ALLOWED_TAGS: ['p', 'b', 'i', 'span', '#text'], ALLOWED_ATTR: [], KEEP_CONTENT: false};

  if(searchTerm == ""){
    return(
      <>
      <div className='warning'>Please provide a search term!</div>
      </>
    )
  }
  if(isLoading){
    return <div className='Loading'><span>Loading...</span></div>
  }
  return (
    <div>
    {toots.map((toot: Toot, index: number) => {
      const name:string  = DOMPurify.sanitize(toot.account.display_name,DOMPurifyConfig) +' @'+ DOMPurify.sanitize(toot.account.username,DOMPurifyConfig)
      const content:{ __html: string }  = {__html: ""+DOMPurify.sanitize(toot.content,DOMPurifyConfig)}
      const spoiler:{ __html: string }  = {__html: "Spoiler: "+DOMPurify.sanitize(toot.spoiler_text,DOMPurifyConfig)}
      const createdAt:string = "Created at:" +DOMPurify.sanitize(toot.created_at,DOMPurifyConfig)
      return(
        <div key={toot.id} className={`toot-wrapper ${toot.sentiment ? toot.sentiment.overall_sentiment : ''}`}>
          <div className="toot">
            <h3>{name}</h3>
            <p dangerouslySetInnerHTML={content} />
            {toot.spoiler_text && <span dangerouslySetInnerHTML={spoiler} />}
            <small>{createdAt}</small>
          </div>
          {toot.sentiment && (
            <div className="sentiment">
              <h2>{toot.sentiment.overall_sentiment}</h2>
              <p>Positive: {toot.sentiment.positive_score}</p>
              <p>Neutral: {toot.sentiment.neutral_score}</p>
              <p>Negative: {toot.sentiment.negative_score}</p>
            </div>
          )}
        </div>
      )}
    )}
    </div>
  );
};

export default App;
