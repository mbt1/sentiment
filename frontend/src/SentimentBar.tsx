import React, { useEffect } from 'react';

export function SentimentBar(positive_score:number,neutral_score:number,negative_score:number) {
    const [scaled_positive, scaled_neutral, scaled_negative] = scaleValues(positive_score,neutral_score,negative_score); 
    return <div className="sentiment-bar">
        {SentimentBarSection("positive", scaled_positive)}
        {SentimentBarSection("neutral", scaled_neutral)}
        {SentimentBarSection("negative", scaled_negative)}
    </div>;
}

export function SentimentBarHooks() {
    const handleResize = () => {
        const sections = document.querySelectorAll('.sentiment-section');
        // console.log("GH HandleResize:"+sections.length)
        sections.forEach(section => {
            const width = (section as HTMLElement).offsetWidth;
            if (width < 30) {
                section.classList.add('hide-label');
            } else {
                section.classList.remove('hide-label');
            }
        });
    };

    useEffect(() => {
        window.addEventListener('resize', handleResize);

        // Initial check
        handleResize();

        // Cleanup
        return () => {
            window.removeEventListener('resize', handleResize);
        };
    });
}

function scaleValues(v1: number, v2: number, v3: number): [number, number, number] {
let [scaledV1, scaledV2, scaledV3] = [v1, v2, v3].map(v => Number((v / (v1 + v2 + v3)).toFixed(2)));
// If they don't add up to 1 after rounding, add 0.01 to v2
if (scaledV1 + scaledV2 + scaledV3 !== 1) {
    scaledV2 += 0.01;
}
return [scaledV1, scaledV2, scaledV3];
}

function SentimentBarSection(sentimentName:string , score:number): React.ReactNode {
var barSections:number = Math.trunc(score*100);
if(barSections<1){
    return <></>
}
return (
    <div
    className={`sentiment-section ${sentimentName}`}
    style={{ gridColumnEnd: `span ${barSections}` }}
    data-value={score}
    ></div>
);
}
