import React, { useEffect, useState } from 'react';

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

  return (
    <div>
    {toots.map((toot: Toot, index: number) => (
      <div key={toot.id}>
      <h3>{toot.account.display_name} (@{toot.account.username})</h3>
      <p>{toot.content}</p>
      {toot.spoiler_text && <span>Spoiler: {toot.spoiler_text}</span>}
      <small>Created at: {toot.created_at}</small>
      </div>
    ))}
    </div>
  );
};

export default App;
