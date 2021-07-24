import 'devextreme/dist/css/dx.common.css';
import 'devextreme/dist/css/dx.light.css';
import React from 'react';
import { BrowserRouter, Switch, Route } from 'react-router-dom';

import InvoiceList from './pages/InvoiceList';
import InvoiceMgmt from './pages/InvoiceMgmt';
import Report from './components/Report';

function App() {
  return (
    <>
      <BrowserRouter>
        <Switch>
          <Route exact path="/app/" component={InvoiceList} />
          <Route path="/app/management" component={InvoiceMgmt} />
          <Route path={`/app/report/:id`} component={Report} />
        </Switch>
      </BrowserRouter>
    </>
  );
}

export default App;
