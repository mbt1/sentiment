import React from 'react';
import createDOMPurify from 'dompurify';
import { Toot } from './Toots';
import { SentimentBar } from './SentimentBar';

export function SingleToot(DOMPurify: createDOMPurify.DOMPurifyI, DOMPurifyConfig: createDOMPurify.Config): (value: Toot, index: number, array: Toot[]) => React.JSX.Element {
  return (toot: Toot, index: number) => {
    const name: string = DOMPurify.sanitize(toot.account.display_name, DOMPurifyConfig) + ' @' + DOMPurify.sanitize(toot.account.username, DOMPurifyConfig);
    const content: { __html: string; } = { __html: "" + DOMPurify.sanitize(toot.content, DOMPurifyConfig) };
    const spoiler: { __html: string; } = { __html: "Spoiler: " + DOMPurify.sanitize(toot.spoiler_text, DOMPurifyConfig) };
    const createdAt: string = "Created at:" + DOMPurify.sanitize(toot.created_at, DOMPurifyConfig);
    // console.log("GH SingleToot:"+index);
    return (
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

            {SentimentBar(toot.sentiment.positive_score,toot.sentiment.neutral_score,toot.sentiment.negative_score)}

          </div>
        )}
      </div>
    );
  };
  
}
