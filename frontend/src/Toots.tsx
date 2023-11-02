import React from 'react';
import createDOMPurify from 'dompurify';
import DOMPurify from 'dompurify';
import { SingleToot } from './SingleToot';
import { SentimentBarHooks } from './SentimentBar';

const targetAPIBaseURL = process.env.REACT_APP_TARGET_API_BASE_URL;

export interface Toot {
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

  SentimentBarHooks();

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
      <div className='warning'><span>Please provide a search term!</span></div>
      </>
    )
  }
  if(isLoading){
    return <div className='Loading'><span>Loading...</span></div>
  }
  return (
    <div>
    {toots.map(SingleToot(DOMPurify, DOMPurifyConfig))}
    </div>
  );
};

export default App;

