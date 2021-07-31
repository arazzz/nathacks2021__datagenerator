import React, { Suspense } from 'react';
import { BrowserRouter as Router, Switch, Route } from 'react-router-dom';
import { ThemeProvider as MuiThemeProvider } from '@material-ui/core/styles';
import theme from 'config/theme.js';
import { StylesProvider } from '@material-ui/styles';
import { ThemeProvider } from 'styled-components';

// Contexts
import AppContextProvider from 'contexts/AppContext';

import './App.css';
import MainLayout from 'components/layouts/MainLayout';

import IndexPage from 'pages/IndexPage';

const App = () => {
  return (
    <Router>
      <StylesProvider injectFirst>
        <AppContextProvider>
          <MuiThemeProvider theme={theme}>
            <ThemeProvider theme={theme}>
              <Suspense fallback="loading">
                <MainLayout>
                  <Switch>
                    <Route exact path="/">
                      <IndexPage />
                    </Route>
                  </Switch>
                </MainLayout>
              </Suspense>
            </ThemeProvider>
          </MuiThemeProvider>
        </AppContextProvider>
      </StylesProvider>
    </Router>
  );
};

export default App;
