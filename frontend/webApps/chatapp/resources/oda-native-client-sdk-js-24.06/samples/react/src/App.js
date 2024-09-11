import logo from './logo.svg';
import './App.css';
import WebSDK from './web-sdk';
import { createRoot } from 'react-dom/client';
import Card from './Card';
import { useEffect } from 'react';

function App() {
  // Initialize the WebSDK only once using useEffect hook
  useEffect(() => {
    const chatSettings = {
      URI: '<URI>',                               // ODA URI, only the hostname part should be passed, without the https://
      clientAuthEnabled: false,                   // Enables client auth enabled mode of connection if set true, no need to pass if set false
      channelId: '<channelId>',                   // Channel ID, available in channel settings in ODA UI, optional if client auth enabled
      userId: '<userID>',                         // User ID, optional field to personalize user experience
      enableAutocomplete: true,                   // Enables autocomplete suggestions on user input
      enableBotAudioResponse: true,               // Enables audio utterance of skill responses
      enableClearMessage: true,                   // Enables display of button to clear conversation
      enableSpeech: true,                         // Enables voice recognition
      showConnectionStatus: true,                 // Displays current connection status on the header
      i18n: {                                     // Provide translations for the strings used in the widget
        en: {                                     // en locale, can be configured for any locale
          chatTitle: 'Oracle Assistant'           // Set title at chat header
        }
      },
      timestampMode: 'relative',                  // Sets the timestamp mode, relative to current time or default (absolute)           // Redwood dark theme. The default is THEME.DEFAULT, while older theme is available as THEME.CLASSIC
      icons: {
        logo: null,
        avatarAgent: '<svg xmlns="http://www.w3.org/2000/svg" height="32" width="32"><path fill="black" d="M12 2c5.523 0 10 4.477 10 10a9.982 9.982 0 01-3.804 7.85L18 20a9.952 9.952 0 01-6 2C6.477 22 2 17.523 2 12S6.477 2 12 2zm2 16h-4a2 2 0 00-1.766 1.06c1.123.6 2.405.94 3.766.94s2.643-.34 3.765-.94a1.997 1.997 0 00-1.616-1.055zM12 4a8 8 0 00-5.404 13.9A3.996 3.996 0 019.8 16.004L10 16h4c1.438 0 2.7.76 3.404 1.899A8 8 0 0012 4zm0 2c2.206 0 4 1.794 4 4s-1.794 4-4 4-4-1.794-4-4 1.794-4 4-4zm0 2c-1.103 0-2 .897-2 2s.897 2 2 2 2-.897 2-2-.897-2-2-2z" fill="#100f0e" fill-rule="evenodd"/></svg>',
        avatarUser: '<svg xmlns="http://www.w3.org/2000/svg" height="32" width="32"><path fill="black" d="M12 2c5.523 0 10 4.477 10 10a9.982 9.982 0 01-3.804 7.85L18 20a9.952 9.952 0 01-6 2C6.477 22 2 17.523 2 12S6.477 2 12 2zm2 16h-4a2 2 0 00-1.766 1.06c1.123.6 2.405.94 3.766.94s2.643-.34 3.765-.94a1.997 1.997 0 00-1.616-1.055zM12 4a8 8 0 00-5.404 13.9A3.996 3.996 0 019.8 16.004L10 16h4c1.438 0 2.7.76 3.404 1.899A8 8 0 0012 4zm0 2c2.206 0 4 1.794 4 4s-1.794 4-4 4-4-1.794-4-4 1.794-4 4-4zm0 2c-1.103 0-2 .897-2 2s.897 2 2 2 2-.897 2-2-.897-2-2-2z" fill="#100f0e" fill-rule="evenodd"/></svg>',
        avatarBot: '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 36 36" fill="none"><path d="M0 0h36v36H0V0z" fill="#C74634"/><path fill-rule="evenodd" clip-rule="evenodd" d="M7.875 8.625a2.25 2.25 0 00-2.25 2.25v16c0 .621.504 1.125 1.125 1.125h.284c.298 0 .585-.119.796-.33l2.761-2.76a2.25 2.25 0 011.59-.66h15.944a2.25 2.25 0 002.25-2.25V10.875a2.25 2.25 0 00-2.25-2.25H7.875zM24.75 18a2.25 2.25 0 100-4.5 2.25 2.25 0 000 4.5zm-4.5-2.25a2.25 2.25 0 11-4.5 0 2.25 2.25 0 014.5 0zm-9 2.25a2.25 2.25 0 100-4.5 2.25 2.25 0 000 4.5z" fill="#fff"/></svg>'
      },
      delegate: {
        render: (message) => {
          // Customize the rendering for card payloads
          if (message.messagePayload.type === 'card') {
            // Get the msg rendering placeholder created by Web SDK by the msgId Ref
            const container = document.getElementById(message.msgId);
            const msgRoot = createRoot(container);
            // Render the custom react component in the message rendering placeholder
            msgRoot.render(
              <>
                <Card cards={message.messagePayload.cards} onAction={action => handleAction(action)}></Card>
                {message.messagePayload.actions && message.messagePayload.actions.length &&
                  <div className='actions-wrapper'>
                    {message.messagePayload.actions.map((action, index) =>
                      <button key={index} onClick={e => handleAction(action, e)}>{action.label}</button>
                    )}
                  </div>
                }
              </>);
            // Return `true` for customizing rendering for cards
            return true;
          }
          // Return `false` for all other payloads to continue with WebSDK rendering
          return false;
        }
      }
    };

    const chatWidget = new WebSDK(chatSettings);

    chatWidget.connect();

    function handleAction(action) {
      chatWidget.sendMessage(action);
    }
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header>
    </div>
  );
}

export default App;
