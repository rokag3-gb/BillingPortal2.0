import React, { useState } from 'react';
import InvoiceMgmtMain from '../components/InvoiceMgmtMain';
import InvoiceMgmtDetail from '../components/InvoiceMgmtDetail';

function GridPage() {
    const [invoiceId, setInvoiceId] = useState(0)

    return (
        <>
            <InvoiceMgmtMain setInvoiceId={setInvoiceId} />
            <InvoiceMgmtDetail invoiceId={invoiceId} />
        </>
    )
}

export default GridPage;
