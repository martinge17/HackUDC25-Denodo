import React from 'react';
import ReactDOM from 'react-dom/client';
import {BrowserRouter} from 'react-router-dom';
import {Provider} from 'react-redux';
import {IntlProvider} from 'react-intl';
import './Global.css';
import App from './modules/app/components/App';
import reportWebVitals from './reportWebVitals';
import {initReactIntl} from "./i18n";
import store from "./store";


/* Configure i18n. */
const {locale, messages} = initReactIntl();

/* Render application. */
const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
    <React.StrictMode>
        <Provider store={store}>
            <IntlProvider locale={locale} messages={messages}>
                <BrowserRouter>
                    <App/>
                </BrowserRouter>
            </IntlProvider>
        </Provider>
    </React.StrictMode>
);

reportWebVitals();
