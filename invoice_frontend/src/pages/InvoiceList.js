import React, { useState } from 'react';
import InvoiceListMain from '../components/InvoiceListMain';
import InvoiceListDetail from '../components/InvoiceListDetail';
import GridToolbar from '../components/GridToolbar';
import * as utils from '../utils';

const initialSearchMonth = 3
const girdToolbarSize = 155
const urlInvoice = "/api/v1/invoice/"

function InvoiceList() {
    const [start, end] = utils.getDateSet(initialSearchMonth)
    const [invoiceId, setInvoiceId] = useState(0)
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
                />
            </div>
            <InvoiceListMain setInvoiceId={setInvoiceId} url={urlInvoice} param={mainParam} />
            <InvoiceListDetail invoiceId={invoiceId} />
        </div>
    )
}

export default InvoiceList;
