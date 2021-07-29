import React, { useState } from 'react';
import InvoiceMgmtMain from '../components/InvoiceMgmtMain';
import InvoiceMgmtDetail from '../components/InvoiceMgmtDetail';
import GridToolbar from '../components/GridToolbar';
import * as utils from '../utils';

const initialSearchMonth = 3
const girdToolbarSize = 280

function InvoiceMgmt() {
    const [start, end] = utils.getDateSet(initialSearchMonth)
    const [invoiceId, setInvoiceId] = useState("")
    const [startDate, setStartDate] = useState(start);
    const [endDate, setEndDate] = useState(end);
    const [mainParam, setMainParam] = useState("")

    return (
        <div>
            <div style={{position: 'absolute', zIndex: 5}}>
                <GridToolbar
                    startDate={startDate}
                    setStartDate={setStartDate}
                    endDate={endDate}
                    setEndDate={setEndDate}
                    girdToolbarSize={girdToolbarSize}
                    setMainParam={setMainParam}
                    enableIdSearch
                />
            </div>
            <InvoiceMgmtMain setInvoiceId={setInvoiceId} param={mainParam} />
            <InvoiceMgmtDetail invoiceId={invoiceId} />
        </div>
    )
}

export default InvoiceMgmt;
