# Mastodon Toot Sentiment Analyzer

This is a portfolio project, using several modern technologies, including:

* React frontend hosted in Gihub Pages
  * Typescript
  * SCSS  
* Python backend hosted in Azure Functions
* Azure ML
* Fully automated deployment using Github Actions
* Development Environment in a DevContainer that includes
  * Backend Server to emulate that Azure Function environment
  * Frontend Server to host the React app. This includes an on the fly auto-updating server (npm start) as well as a separate run a full compile local server (npm buildserve)
 
The app is accessible at [https://mbt1.github.io/sentiment](https://mbt1.github.io/sentiment).

(c)2023, mbt1, all rights reserved.
Source code published under the [Apache 2.0 license](https://github.com/mbt1/sentiment/blob/main/LICENSE).

## Current Architecture: 

### Python Backend on Azure Functions

1. **API Endpoints**: Set up HTTP-triggered Azure Functions for your endpoints.

2. **Calling the ML Model**: The function makes HTTP requests to Mastodon and to the Azure ML model to get sentiment analysis results.

3. **Response**: The response is in JSON that includes the original toot and the sentiment analysis.

4. **Security**: API keys are stored in Azure KeyVault.

5. **Environment Variables**: Other settings live in the Azure Function Settings

6. **Deployment**: The function is deployed automatically on checkin using a GitHub Action

### React Frontend on GitHub Pages

1. **API Consumption**: Your React makes HTTP requests to the Azure Function API and display the results.

2. **State Management**: The App is using React patterns like React.useEffect() for state management.

3. **Deployment**: The app is build and deployed automatically to GitHub Pages using two separate GitHub Actions. The first on builds the app and "publishes" to a special branch in this repository. The second deploys that branch's content to GitHub Pages if it detects a change. 

4. **Environment Variables**: The API URL is set on deploy, so no env variables are needed.

### Integration

1. **Backend to Mastodon and to the Model**: This is handled using libraries.
  
2. **Frontend to Backend**: HTTP requests are used to fetch and send data to and from the Azure Function.

3. **CORS**: CORS settings are set in the Azure Function to accept requests from the GitHub Pages domain.

Everything above lives in this (mono)repo.

## Future Features

### Rate Limiting

* currently there is very rudimentary rate limiting deployed in the app. This should be more robust.

### Captcha 

When using a CAPTCHA service like Google's reCAPTCHA, we'll need two keys: a "site key" that is publicly visible and used within the client-side JavaScript, and a "secret key" that should be kept secure on the server-side. The "site key" is used to display the CAPTCHA challenge in the browser, and the "secret key" is used to verify the user's answer on the server-side.

Here's a simplified workflow:

1. **Client-Side**: When the user navigates to the page requiring a CAPTCHA, your React app uses the "site key" to request and display the CAPTCHA challenge from Google's servers.
  
2. **User Action**: The user completes the CAPTCHA challenge.

3. **Client-Side**: Once the CAPTCHA is completed, Google's servers provide a "response" token, which the React app then sends to the backend server along with any other data (like the API request you want to make).

4. **Server-Side**: The backend receives this "response" token and uses the "secret key" to call Google's server for verification.

5. **Verification**: Google's server will respond to your server, confirming whether or not the CAPTCHA was successfully completed.

6. **Server Response**: Depending on the verification result, the function will then either process the user's original API request or return an error.

So, while the React app does "provide a token to the CAPTCHA provider," this token is not the same as the "secret key," which remains secure on the server. The token provided by Google is specifically meant to be passed back to your server for verification. This is adding an additional layer of verification that is intended to ensure that the request comes from a human.

That said, like any other API, CAPTCHAs aren't foolproof. They add an additional layer of security but shouldn't be the only measure we take. Combining them with other security best practices can make the API more resilient to misuse.

### Model Training with OpenAI-Generated Data

right now the app is relying on pretrained models provided by Azure. This should be changed to use our own models.

1. **Data Collection**: Use Python or other tools to collect and preprocess text data. We could potentially use OpenAI's GPT models to generate synthetic training data.

2. **Training the Model**: Use a machine learning library like TensorFlow or PyTorch to train the model. We can host the training process on Azure ML.

3. **Continuous Training with GitHub Actions**: Automate the training using GitHub Actions whenever new data is pushed to the repository. This pipeline can push the trained model to Azure Blob Storage or directly to the Azure Function app.

4. **Hosting the Model**: Azure ML or Azure Functions with a custom container can serve the trained model.

