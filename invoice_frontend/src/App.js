import 'devextreme/dist/css/dx.common.css';
import 'devextreme/dist/css/dx.light.css';
import React from 'react';
import { BrowserRouter, Switch, Route } from 'react-router-dom';

import GridPage from './components/GridPage';
import Report from './components/Report';

// import CSRFToken from './components/CSRFToken' // For Django CSRFToken

function App() {
  return (
    <>
      <BrowserRouter>
        <Switch>
          <Route exact path="/app/" component={GridPage} />
          <Route path={`/app/report/:id`} component={Report} />
        </Switch>
      </BrowserRouter>
    </>
  );
}

export default App;
