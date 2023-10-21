import React from 'react';
import Toots from './Toots';
import './App.scss';

const App: React.FC = () => {
  const [searchTerm, setSearchTerm] = React.useState('');
  const [submittedSearchTerm, setSubmittedSearchTerm] = React.useState(searchTerm);
  
  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setSearchTerm(e.target.value);
  };
  
  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setSubmittedSearchTerm(searchTerm)
  };
  
  return (
    <>
      <div className="search-form-wrapper">
        <h1>Mastodon Toot Sentiment Analyzer</h1>
        <form onSubmit={handleSubmit}>
          <label htmlFor="searchTerm">Search Term:</label>
          <input type="text" id="searchTerm" name="searchTerm" onChange={handleInputChange} />
          <button type="submit">Search</button>
        </form>
      </div>
      <div className="toot-list">
        <Toots searchTerm={submittedSearchTerm}/>
      </div>
    </>
  );
};

export default App;